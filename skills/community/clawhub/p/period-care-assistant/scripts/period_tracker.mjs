#!/usr/bin/env node

import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const BASE_DIR = path.resolve(__dirname, "..");
const DEFAULT_STORE_PATH = process.env.PERIOD_TRACKER_STORE
  ? expandHome(process.env.PERIOD_TRACKER_STORE)
  : path.join(BASE_DIR, ".state", "period-tracker.enc");
const DEFAULTS = Object.freeze({
  reminderDaysBefore: 4,
  periodLengthDays: 5,
  timezone: "Asia/Shanghai",
  reminderTime: "09:00",
  deliveryMode: "none",
  deliveryChannel: null,
  deliveryTo: null,
  deliveryWebhook: null,
});

function expandHome(inputPath) {
  if (!inputPath || !inputPath.startsWith("~")) {
    return inputPath;
  }

  const home = process.env.HOME || process.env.USERPROFILE;
  if (!home) {
    return inputPath;
  }
  return path.join(home, inputPath.slice(1));
}

function parseArgs(argv) {
  const args = { _: [] };
  for (let index = 0; index < argv.length; index += 1) {
    const token = argv[index];
    if (!token.startsWith("--")) {
      args._.push(token);
      continue;
    }
    const key = token.slice(2);
    const next = argv[index + 1];
    if (!next || next.startsWith("--")) {
      args[key] = true;
      continue;
    }
    args[key] = next;
    index += 1;
  }
  return args;
}

function requiredSecret() {
  const secret = process.env.PERIOD_TRACKER_KEY;
  if (!secret) {
    throw new Error("PERIOD_TRACKER_KEY is required.");
  }
  return secret;
}

function emptyStore() {
  return { version: 1, users: {} };
}

function loadStore(storePath = DEFAULT_STORE_PATH, secret = requiredSecret()) {
  if (!fs.existsSync(storePath)) {
    return emptyStore();
  }

  const envelope = JSON.parse(fs.readFileSync(storePath, "utf8"));
  if (envelope.version !== 1) {
    throw new Error(`Unsupported store version: ${String(envelope.version)}`);
  }

  const salt = Buffer.from(envelope.salt, "base64");
  const iv = Buffer.from(envelope.iv, "base64");
  const tag = Buffer.from(envelope.tag, "base64");
  const ciphertext = Buffer.from(envelope.data, "base64");
  const key = crypto.scryptSync(secret, salt, 32);
  const decipher = crypto.createDecipheriv("aes-256-gcm", key, iv);
  decipher.setAuthTag(tag);
  const plaintext = Buffer.concat([decipher.update(ciphertext), decipher.final()]);
  return JSON.parse(plaintext.toString("utf8"));
}

function saveStore(store, storePath = DEFAULT_STORE_PATH, secret = requiredSecret()) {
  fs.mkdirSync(path.dirname(storePath), { recursive: true });
  const salt = crypto.randomBytes(16);
  const iv = crypto.randomBytes(12);
  const key = crypto.scryptSync(secret, salt, 32);
  const cipher = crypto.createCipheriv("aes-256-gcm", key, iv);
  const plaintext = Buffer.from(JSON.stringify(store, null, 2), "utf8");
  const ciphertext = Buffer.concat([cipher.update(plaintext), cipher.final()]);
  const tag = cipher.getAuthTag();
  const envelope = {
    version: 1,
    algorithm: "aes-256-gcm",
    kdf: "scrypt",
    salt: salt.toString("base64"),
    iv: iv.toString("base64"),
    tag: tag.toString("base64"),
    data: ciphertext.toString("base64"),
  };
  fs.writeFileSync(storePath, `${JSON.stringify(envelope, null, 2)}\n`, "utf8");
}

function ensureUser(store, userKey) {
  if (!store.users[userKey]) {
    store.users[userKey] = {
      settings: { ...DEFAULTS },
      records: [],
      reminder: null,
    };
  }

  const user = store.users[userKey];
  user.settings = { ...DEFAULTS, ...user.settings };
  user.records = Array.isArray(user.records) ? user.records : [];
  return user;
}

function parseDateString(input) {
  if (!/^\d{4}-\d{2}-\d{2}$/.test(input)) {
    throw new Error(`Invalid date '${input}'. Expected YYYY-MM-DD.`);
  }

  const [year, month, day] = input.split("-").map(Number);
  const date = new Date(Date.UTC(year, month - 1, day));
  if (
    Number.isNaN(date.getTime()) ||
    date.getUTCFullYear() !== year ||
    date.getUTCMonth() !== month - 1 ||
    date.getUTCDate() !== day
  ) {
    throw new Error(`Invalid calendar date '${input}'.`);
  }
  return date;
}

function formatDate(date) {
  const year = date.getUTCFullYear();
  const month = String(date.getUTCMonth() + 1).padStart(2, "0");
  const day = String(date.getUTCDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
}

function addDays(input, days) {
  const date = typeof input === "string" ? parseDateString(input) : new Date(input.getTime());
  date.setUTCDate(date.getUTCDate() + days);
  return formatDate(date);
}

function diffDays(left, right) {
  const leftDate = typeof left === "string" ? parseDateString(left) : left;
  const rightDate = typeof right === "string" ? parseDateString(right) : right;
  return Math.round((leftDate.getTime() - rightDate.getTime()) / 86400000);
}

function currentDateInTimeZone(timezone) {
  const parts = new Intl.DateTimeFormat("en-CA", {
    timeZone: timezone,
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
  }).formatToParts(new Date());
  const values = Object.fromEntries(
    parts
      .filter((part) => part.type !== "literal")
      .map((part) => [part.type, part.value]),
  );
  return `${values.year}-${values.month}-${values.day}`;
}

function clamp(value, min, max) {
  return Math.min(Math.max(value, min), max);
}

function average(values) {
  if (!values.length) {
    return null;
  }
  return values.reduce((sum, value) => sum + value, 0) / values.length;
}

function median(values) {
  if (!values.length) {
    return null;
  }
  const sorted = [...values].sort((left, right) => left - right);
  const middle = Math.floor(sorted.length / 2);
  if (sorted.length % 2 === 1) {
    return sorted[middle];
  }
  return (sorted[middle - 1] + sorted[middle]) / 2;
}

function weightedAverage(values) {
  if (!values.length) {
    return null;
  }
  let weightedSum = 0;
  let weightTotal = 0;
  values.forEach((value, index) => {
    const weight = index + 1;
    weightedSum += value * weight;
    weightTotal += weight;
  });
  return weightedSum / weightTotal;
}

function stddev(values) {
  if (values.length < 2) {
    return 0;
  }
  const mean = average(values);
  const variance = average(values.map((value) => (value - mean) ** 2));
  return Math.sqrt(variance);
}

function round(value) {
  if (value == null || Number.isNaN(value)) {
    return null;
  }
  return Math.round(value * 10) / 10;
}

function sanitizeRecords(records) {
  const seen = new Set();
  return records
    .map((record) => ({
      startDate: String(record.startDate),
      source: record.source || "user",
      recordedAt: record.recordedAt || new Date().toISOString(),
    }))
    .filter((record) => {
      if (!/^\d{4}-\d{2}-\d{2}$/.test(record.startDate)) {
        return false;
      }
      if (seen.has(record.startDate)) {
        return false;
      }
      seen.add(record.startDate);
      return true;
    })
    .sort((left, right) => left.startDate.localeCompare(right.startDate));
}

function summarizeIntervals(intervals) {
  const recent = intervals.slice(-6);
  if (!recent.length) {
    return {
      recent,
      medianCycle: 28,
      averageCycle: 28,
      weightedCycle: 28,
      variability: 0,
      predictedCycleLength: 28,
    };
  }

  const medianCycle = median(recent);
  const averageCycle = average(recent);
  const weightedCycle = weightedAverage(recent);
  const variability = stddev(recent);
  const predictedCycleLength = clamp(
    Math.round(medianCycle * 0.5 + weightedCycle * 0.35 + averageCycle * 0.15),
    18,
    45,
  );

  return {
    recent,
    medianCycle,
    averageCycle,
    weightedCycle,
    variability,
    predictedCycleLength,
  };
}

function rollingMae(startDates) {
  if (startDates.length < 4) {
    return null;
  }

  const errors = [];
  for (let index = 2; index < startDates.length; index += 1) {
    const history = startDates.slice(0, index);
    const intervals = [];
    for (let offset = 1; offset < history.length; offset += 1) {
      intervals.push(diffDays(history[offset], history[offset - 1]));
    }
    const summary = summarizeIntervals(intervals);
    const predictedDate = addDays(history[history.length - 1], summary.predictedCycleLength);
    errors.push(Math.abs(diffDays(startDates[index], predictedDate)));
  }
  return average(errors);
}

function evaluateConfidence(sampleSize, variability, mae) {
  if (sampleSize >= 5 && variability <= 2.5 && mae != null && mae <= 2) {
    return "high";
  }
  if (sampleSize >= 2 && variability <= 4.5 && (mae == null || mae <= 4)) {
    return "medium";
  }
  return "low";
}

function makeReminderJobName(userKey) {
  return `period-reminder-${crypto.createHash("sha256").update(userKey).digest("hex").slice(0, 12)}`;
}

function localMinuteIndex(dateString, timeString) {
  const [hours, minutes] = timeString.split(":").map(Number);
  return Math.round(parseDateString(dateString).getTime() / 60000) + hours * 60 + minutes;
}

function zoneParts(date, timezone) {
  const parts = new Intl.DateTimeFormat("en-CA", {
    timeZone: timezone,
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    hourCycle: "h23",
  }).formatToParts(date);
  const values = Object.fromEntries(
    parts
      .filter((part) => part.type !== "literal")
      .map((part) => [part.type, part.value]),
  );
  return {
    date: `${values.year}-${values.month}-${values.day}`,
    time: `${values.hour}:${values.minute}`,
  };
}

function localDateTimeToUtcIso(dateString, timeString, timezone) {
  let guess = Date.parse(`${dateString}T${timeString}:00Z`);
  const target = localMinuteIndex(dateString, timeString);
  for (let attempts = 0; attempts < 5; attempts += 1) {
    const current = zoneParts(new Date(guess), timezone);
    const delta = target - localMinuteIndex(current.date, current.time);
    if (delta === 0) {
      return new Date(guess).toISOString();
    }
    guess += delta * 60000;
  }
  return new Date(guess).toISOString();
}

function composeReminderText(predictedNextStart) {
  return `温馨提醒：按你最近的记录，预计下次月经会在 ${predictedNextStart} 左右开始，可以提前准备卫生用品并安排好休息。如果这次明显提前或推迟，直接告诉我，我会重新更新预测。`;
}

function buildReminder(userKey, settings, predictedNextStart) {
  if (!predictedNextStart) {
    return null;
  }
  const reminderDate = addDays(predictedNextStart, -settings.reminderDaysBefore);
  const reminderTime = settings.reminderTime || DEFAULTS.reminderTime;
  return {
    jobName: makeReminderJobName(userKey),
    predictedNextStart,
    reminderDate,
    reminderTime,
    timezone: settings.timezone,
    scheduleAt: localDateTimeToUtcIso(reminderDate, reminderTime, settings.timezone),
    delivery: {
      mode: settings.deliveryMode,
      channel: settings.deliveryChannel,
      to: settings.deliveryTo,
      webhook: settings.deliveryWebhook,
    },
    reminderText: composeReminderText(predictedNextStart),
  };
}

function computeUserStats(userKey, user) {
  const records = sanitizeRecords(user.records);
  user.records = records;

  if (!records.length) {
    user.reminder = null;
    return {
      sampleSize: 0,
      lastStartDate: null,
      predictedCycleLength: 28,
      predictedNextStart: null,
      averageCycleLength: null,
      medianCycleLength: null,
      weightedCycleLength: null,
      variability: null,
      historicalMae: null,
      confidence: "low",
      reminder: null,
    };
  }

  const starts = records.map((record) => record.startDate);
  const intervals = [];
  for (let index = 1; index < starts.length; index += 1) {
    intervals.push(diffDays(starts[index], starts[index - 1]));
  }
  const summary = summarizeIntervals(intervals);
  const historicalMae = rollingMae(starts);
  const confidence = evaluateConfidence(summary.recent.length, summary.variability, historicalMae);
  const predictedNextStart = addDays(starts[starts.length - 1], summary.predictedCycleLength);
  const reminder = buildReminder(userKey, user.settings, predictedNextStart);
  user.reminder = reminder;

  return {
    sampleSize: summary.recent.length,
    lastStartDate: starts[starts.length - 1],
    predictedCycleLength: summary.predictedCycleLength,
    predictedNextStart,
    averageCycleLength: round(summary.averageCycle),
    medianCycleLength: round(summary.medianCycle),
    weightedCycleLength: round(summary.weightedCycle),
    variability: round(summary.variability),
    historicalMae: round(historicalMae),
    confidence,
    reminder,
  };
}

function resolvePhase(daysSinceLast, daysUntilNext, predictedCycleLength, periodLengthDays, reminderDaysBefore) {
  if (daysSinceLast < 0) {
    return { code: "unknown", label: "日期异常", description: "当前日期早于最近一次记录。" };
  }
  if (daysSinceLast < periodLengthDays) {
    return { code: "menstrual", label: "经期中", description: "仍处于本次经期的估计窗口内。" };
  }
  const ovulationDay = Math.max(0, predictedCycleLength - 14);
  if (Math.abs(daysSinceLast - ovulationDay) <= 1) {
    return { code: "ovulation", label: "排卵窗口", description: "接近基于历史数据估计的排卵窗口。" };
  }
  if (daysSinceLast < ovulationDay - 1) {
    return { code: "follicular", label: "卵泡期", description: "处于经期后到排卵前的估计阶段。" };
  }
  if (daysUntilNext >= 0 && daysUntilNext <= reminderDaysBefore) {
    return { code: "premenstrual", label: "经前提醒期", description: "已进入下次月经前的提醒窗口。" };
  }
  if (daysUntilNext < 0) {
    return { code: "late", label: "可能推迟", description: "已经超过预测开始日，建议用新记录尽快修正模型。" };
  }
  return { code: "luteal", label: "黄体期", description: "处于排卵后到下次月经前的估计阶段。" };
}

function buildStatus(userKey, user, today) {
  const stats = computeUserStats(userKey, user);
  if (!stats.lastStartDate) {
    return {
      userKey,
      hasData: false,
      today,
      message: "还没有可用的月经起始记录。至少记录一次“月经来了”后才能开始预测。",
      settings: user.settings,
      stats,
    };
  }

  const daysSinceLast = diffDays(today, stats.lastStartDate);
  const daysUntilNext = diffDays(stats.predictedNextStart, today);
  const phase = resolvePhase(
    daysSinceLast,
    daysUntilNext,
    stats.predictedCycleLength,
    user.settings.periodLengthDays,
    user.settings.reminderDaysBefore,
  );

  return {
    userKey,
    hasData: true,
    today,
    settings: user.settings,
    currentPhase: phase,
    daysSinceLastStart: daysSinceLast,
    daysUntilNextStart: daysUntilNext,
    predictedNextStart: stats.predictedNextStart,
    cycleLengthDays: stats.predictedCycleLength,
    periodLengthDays: user.settings.periodLengthDays,
    confidence: stats.confidence,
    historicalMaeDays: stats.historicalMae,
    variabilityDays: stats.variability,
    lastStartDate: stats.lastStartDate,
    reminder: stats.reminder,
  };
}

function maybeNumber(value, flagName) {
  if (value == null) {
    return null;
  }
  const number = Number(value);
  if (!Number.isFinite(number)) {
    throw new Error(`Invalid number for --${flagName}: ${String(value)}`);
  }
  return number;
}

function applySettingOverrides(user, args) {
  if (args.timezone) {
    currentDateInTimeZone(args.timezone);
    user.settings.timezone = args.timezone;
  }
  if (args["reminder-days"]) {
    user.settings.reminderDaysBefore = clamp(
      Math.round(maybeNumber(args["reminder-days"], "reminder-days")),
      1,
      10,
    );
  }
  if (args["period-length"]) {
    user.settings.periodLengthDays = clamp(
      Math.round(maybeNumber(args["period-length"], "period-length")),
      1,
      10,
    );
  }
  if (args["reminder-time"]) {
    if (!/^\d{2}:\d{2}$/.test(args["reminder-time"])) {
      throw new Error("Invalid --reminder-time. Expected HH:MM.");
    }
    user.settings.reminderTime = args["reminder-time"];
  }
  if (args["delivery-mode"]) {
    const mode = String(args["delivery-mode"]);
    if (!["none", "announce", "webhook"].includes(mode)) {
      throw new Error("Invalid --delivery-mode. Use none, announce, or webhook.");
    }
    user.settings.deliveryMode = mode;
  }
  if (args["delivery-channel"]) {
    user.settings.deliveryChannel = String(args["delivery-channel"]);
  }
  if (args["delivery-to"]) {
    user.settings.deliveryTo = String(args["delivery-to"]);
  }
  if (args["delivery-webhook"]) {
    user.settings.deliveryWebhook = String(args["delivery-webhook"]);
  }
}

function requireUserKey(args) {
  const userKey = args.user;
  if (!userKey) {
    throw new Error("--user is required.");
  }
  return String(userKey);
}

function emit(output, asJson) {
  if (asJson) {
    process.stdout.write(`${JSON.stringify(output, null, 2)}\n`);
    return;
  }
  process.stdout.write(renderText(output));
}

function renderText(output) {
  if (output.command === "status") {
    if (!output.result.hasData) {
      return `${output.result.message}\n`;
    }
    return [
      `用户: ${output.result.userKey}`,
      `当前阶段: ${output.result.currentPhase.label}`,
      `最近一次开始: ${output.result.lastStartDate}`,
      `预计下次开始: ${output.result.predictedNextStart}`,
      `距上次开始: ${output.result.daysSinceLastStart} 天`,
      `距下次开始: ${output.result.daysUntilNextStart} 天`,
      `提醒日期: ${output.result.reminder ? output.result.reminder.reminderDate : "未生成"}`,
      `置信度: ${output.result.confidence}`,
    ].join("\n") + "\n";
  }

  if (output.command === "record") {
    return [
      `已记录: ${output.recordedDate}`,
      `是否重复: ${output.duplicate ? "是" : "否"}`,
      `预计下次开始: ${output.predictedNextStart || "暂无"}`,
      `提醒日期: ${output.reminder?.reminderDate || "暂无"}`,
    ].join("\n") + "\n";
  }

  if (output.command === "configure") {
    return `已更新设置，当前提醒方式为 ${output.settings.deliveryMode}。\n`;
  }

  if (output.command === "reminder-plan") {
    if (!output.plan) {
      return `${output.message}\n`;
    }
    return [
      `提醒作业: ${output.plan.jobName}`,
      `提醒日期: ${output.plan.reminderDate} ${output.plan.reminderTime}`,
      `UTC 时间: ${output.plan.scheduleAt}`,
      `提醒内容: ${output.plan.reminderText}`,
    ].join("\n") + "\n";
  }

  if (output.command === "history") {
    return `${output.records.map((record) => record.startDate).join("\n")}\n`;
  }

  return `${JSON.stringify(output, null, 2)}\n`;
}

function commandRecord(store, args) {
  const userKey = requireUserKey(args);
  const user = ensureUser(store, userKey);
  applySettingOverrides(user, args);
  const recordDate = args.date
    ? formatDate(parseDateString(args.date))
    : currentDateInTimeZone(user.settings.timezone);
  const duplicate = user.records.some((record) => record.startDate === recordDate);
  if (!duplicate) {
    user.records.push({
      startDate: recordDate,
      source: args.source ? String(args.source) : "user",
      recordedAt: new Date().toISOString(),
    });
  }
  const stats = computeUserStats(userKey, user);
  return {
    command: "record",
    userKey,
    duplicate,
    recordedDate: recordDate,
    predictedNextStart: stats.predictedNextStart,
    cycleLengthDays: stats.predictedCycleLength,
    confidence: stats.confidence,
    reminder: stats.reminder,
    historyCount: user.records.length,
  };
}

function commandStatus(store, args) {
  const userKey = requireUserKey(args);
  const user = ensureUser(store, userKey);
  const today = args.today
    ? formatDate(parseDateString(args.today))
    : currentDateInTimeZone(user.settings.timezone);
  return {
    command: "status",
    result: buildStatus(userKey, user, today),
  };
}

function commandPredict(store, args) {
  const userKey = requireUserKey(args);
  const user = ensureUser(store, userKey);
  const stats = computeUserStats(userKey, user);
  return {
    command: "predict",
    userKey,
    stats,
  };
}

function commandHistory(store, args) {
  const userKey = requireUserKey(args);
  const user = ensureUser(store, userKey);
  user.records = sanitizeRecords(user.records);
  return {
    command: "history",
    userKey,
    records: user.records,
  };
}

function commandConfigure(store, args) {
  const userKey = requireUserKey(args);
  const user = ensureUser(store, userKey);
  applySettingOverrides(user, args);
  const stats = computeUserStats(userKey, user);
  return {
    command: "configure",
    userKey,
    settings: user.settings,
    reminder: stats.reminder,
    confidence: stats.confidence,
  };
}

function commandReminderPlan(store, args) {
  const userKey = requireUserKey(args);
  const user = ensureUser(store, userKey);
  const stats = computeUserStats(userKey, user);
  if (!stats.reminder) {
    return {
      command: "reminder-plan",
      userKey,
      plan: null,
      message: "当前没有足够的数据生成提醒计划。",
    };
  }

  const deliveryReady = Boolean(
    stats.reminder.delivery.mode !== "none" &&
      ((stats.reminder.delivery.mode === "announce" &&
        stats.reminder.delivery.channel &&
        stats.reminder.delivery.to) ||
        (stats.reminder.delivery.mode === "webhook" && stats.reminder.delivery.webhook)),
  );

  return {
    command: "reminder-plan",
    userKey,
    plan: {
      ...stats.reminder,
      deliveryReady,
      agentTurnMessage: `Use $period-care-assistant to send a short caring reminder to user ${userKey}. Predicted next period start date: ${stats.reminder.predictedNextStart}. Reminder text: ${stats.reminder.reminderText}`,
    },
  };
}

export function execute(argv = process.argv.slice(2), options = {}) {
  const args = parseArgs(argv);
  const command = args._[0];
  if (!command || ["help", "--help", "-h"].includes(command)) {
    return {
      exitCode: 0,
      output: {
        command: "help",
        usage:
          "record|status|predict|history|configure|reminder-plan with --user <userKey> and optional --json",
      },
    };
  }

  const storePath = options.storePath || DEFAULT_STORE_PATH;
  const secret = options.secret || requiredSecret();
  const store = loadStore(storePath, secret);
  let output;

  switch (command) {
    case "record":
      output = commandRecord(store, args);
      saveStore(store, storePath, secret);
      break;
    case "status":
      output = commandStatus(store, args);
      break;
    case "predict":
      output = commandPredict(store, args);
      break;
    case "history":
      output = commandHistory(store, args);
      break;
    case "configure":
      output = commandConfigure(store, args);
      saveStore(store, storePath, secret);
      break;
    case "reminder-plan":
      output = commandReminderPlan(store, args);
      break;
    default:
      throw new Error(`Unknown command '${command}'.`);
  }

  return { exitCode: 0, output, asJson: Boolean(args.json) };
}

export function main(argv = process.argv.slice(2)) {
  try {
    const { output, asJson } = execute(argv);
    emit(output, asJson);
  } catch (error) {
    process.stderr.write(`${error.message}\n`);
    process.exitCode = 1;
  }
}

if (process.argv[1] === __filename) {
  main();
}
