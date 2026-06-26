#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const DATA_PATH = path.resolve(__dirname, "../references/cn-holidays-2026.json");
const YEAR = 2026;

function readHolidayData() {
  return JSON.parse(fs.readFileSync(DATA_PATH, "utf8"));
}

function assertIsoDate(isoDate) {
  const match = /^(\d{4})-(\d{2})-(\d{2})$/.exec(isoDate);
  if (!match) {
    throw new Error(`无效日期: ${isoDate}`);
  }
  const year = Number(match[1]);
  const month = Number(match[2]);
  const day = Number(match[3]);
  const date = new Date(Date.UTC(year, month - 1, day));
  if (
    Number.isNaN(date.getTime()) ||
    date.getUTCFullYear() !== year ||
    date.getUTCMonth() !== month - 1 ||
    date.getUTCDate() !== day
  ) {
    throw new Error(`无效日期: ${isoDate}`);
  }
  return { year, month, day };
}

function getWeekdayName(isoDate) {
  const { year, month, day } = assertIsoDate(isoDate);
  return new Intl.DateTimeFormat("zh-Hans-CN", {
    timeZone: "UTC",
    weekday: "long",
  }).format(new Date(Date.UTC(year, month - 1, day)));
}

function normalizeFestivalName(name) {
  return String(name ?? "")
    .trim()
    .replace(/\s+/g, "");
}

function isDateInRange(isoDate, startDate, endDate) {
  return isoDate >= startDate && isoDate <= endDate;
}

export function buildDateStatus(isoDate, entries = readHolidayData()) {
  const { year } = assertIsoDate(isoDate);
  if (year !== YEAR) {
    throw new Error(`当前只内置 ${YEAR} 年数据: ${isoDate}`);
  }

  const weekday = getWeekdayName(isoDate);
  for (const entry of entries) {
    if (isDateInRange(isoDate, entry.start_date, entry.end_date)) {
      return {
        isoDate,
        weekday,
        year,
        type: "holiday",
        label: "节假日",
        festival: entry.festival,
        startDate: entry.start_date,
        endDate: entry.end_date,
        holidayDays: entry.holiday_days,
        workDays: entry.work_days,
      };
    }
    if (entry.work_days.includes(isoDate)) {
      return {
        isoDate,
        weekday,
        year,
        type: "makeup_workday",
        label: "调休上班",
        festival: entry.festival,
        startDate: entry.start_date,
        endDate: entry.end_date,
        holidayDays: entry.holiday_days,
        workDays: entry.work_days,
      };
    }
  }

  const isWeekend = weekday === "星期六" || weekday === "星期日";
  return {
    isoDate,
    weekday,
    year,
    type: isWeekend ? "weekend" : "workday",
    label: isWeekend ? "普通周末" : "普通工作日",
  };
}

export function findFestival(name, entries = readHolidayData()) {
  const normalized = normalizeFestivalName(name);
  const entry = entries.find((item) => normalizeFestivalName(item.festival) === normalized);
  if (!entry) {
    throw new Error(`未找到节日安排: ${name}`);
  }
  return entry;
}

export function listSchedules(entries = readHolidayData()) {
  return entries.map((entry) => ({
    festival: entry.festival,
    startDate: entry.start_date,
    endDate: entry.end_date,
    holidayDays: entry.holiday_days,
    workDays: entry.work_days,
  }));
}

function formatDateStatusText(status) {
  const lines = [`${status.isoDate} ${status.weekday}: ${status.label}`];
  if (status.festival) {
    lines.push(`节日: ${status.festival}`);
    lines.push(`放假: ${status.startDate} 至 ${status.endDate} (${status.holidayDays} 天)`);
    lines.push(
      `调休: ${status.workDays.length > 0 ? status.workDays.join("、") : "无"}`,
    );
  }
  return lines.join("\n");
}

function formatFestivalText(entry) {
  return [
    `${entry.festival}: ${entry.start_date} 至 ${entry.end_date} (${entry.holiday_days} 天)`,
    `调休: ${entry.work_days.length > 0 ? entry.work_days.join("、") : "无"}`,
  ].join("\n");
}

function formatScheduleListText(entries) {
  return entries
    .map(
      (entry) =>
        `${entry.festival}: ${entry.startDate} 至 ${entry.endDate} (${entry.holidayDays} 天); 调休: ${entry.workDays.length > 0 ? entry.workDays.join("、") : "无"}`,
    )
    .join("\n");
}

export function usageText() {
  return [
    "用法:",
    "  jiejiari.js date <YYYY-MM-DD> [--json]",
    "  jiejiari.js festival <名称> [--json]",
    "  jiejiari.js list [--json]",
  ].join("\n");
}

export async function main(argv = process.argv.slice(2)) {
  const args = [...argv];
  const json = args.includes("--json");
  const filteredArgs = args.filter((arg) => arg !== "--json");
  const [command, ...rest] = filteredArgs;

  if (!command || command === "--help" || command === "-h") {
    console.log(usageText());
    return;
  }

  if (command === "date") {
    const isoDate = rest[0];
    if (!isoDate) {
      throw new Error("date 需要 <YYYY-MM-DD>");
    }
    const result = buildDateStatus(isoDate);
    console.log(json ? JSON.stringify(result, null, 2) : formatDateStatusText(result));
    return;
  }

  if (command === "festival") {
    const festivalName = rest.join("");
    if (!festivalName) {
      throw new Error("festival 需要节日名称");
    }
    const entry = findFestival(festivalName);
    console.log(json ? JSON.stringify(entry, null, 2) : formatFestivalText(entry));
    return;
  }

  if (command === "list") {
    const entries = listSchedules();
    console.log(json ? JSON.stringify(entries, null, 2) : formatScheduleListText(entries));
    return;
  }

  throw new Error(`不支持的命令: ${command}`);
}

if (process.argv[1] && path.resolve(process.argv[1]) === __filename) {
  main().catch((error) => {
    console.error(error instanceof Error ? error.message : String(error));
    process.exitCode = 1;
  });
}
