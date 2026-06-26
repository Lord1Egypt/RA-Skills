import {
  isMain,
  parseCommonArgs,
  runCli,
  buildInstrumentQuery
} from "../core/cli.mjs";
import { getSubscriptionList } from "../products/subscription_list.mjs";
import { addSubscription } from "../products/subscription_add.mjs";
import { deleteSubscription } from "../products/subscription_delete.mjs";
import { getSubscriptionReport } from "../products/subscription_report.mjs";
import { getSubscriptionSummary } from "../products/subscription_summary.mjs";
import { getInstrumentProfile } from "../products/instrument_profile.mjs";

function createFlowError(code, message) {
  const error = new Error(message);
  error.code = code;
  return error;
}

function parseInstrumentToken(input) {
  const value = String(input).trim();
  const dotMode = value.match(/^(\d{6})\.(SSE|SZE)$/i);
  if (dotMode) {
    return {
      instrument_id: dotMode[1],
      exchange_id: dotMode[2].toUpperCase()
    };
  }

  const prefixMode = value.match(/^(SSE|SZE)[:：](\d{6})$/i);
  if (prefixMode) {
    return {
      instrument_id: prefixMode[2],
      exchange_id: prefixMode[1].toUpperCase()
    };
  }

  return { instrument_name: value };
}

function isFatalResolutionError(error) {
  return ["AUTH_INVALID", "PERMISSION_DENIED", "RATE_LIMITED", "UPSTREAM_ERROR"].includes(
    error?.code
  );
}

async function resolveInstrument(rawInput) {
  try {
    const resolved = await getInstrumentProfile(parseInstrumentToken(rawInput));
    return {
      ok: true,
      input: rawInput,
      instrument: {
        instrument_id: resolved.instrument_id,
        exchange_id: resolved.exchange_id,
        instrument_name: resolved.instrument_name || String(rawInput).trim()
      }
    };
  } catch (error) {
    if (isFatalResolutionError(error)) {
      throw error;
    }
    return {
      ok: false,
      input: rawInput,
      reason: "无法识别该标的，请检查名称或代码后重新输入"
    };
  }
}

function extractInstrumentKey(sub) {
  const inst = sub.instrument ?? {};
  return `${inst.exchange_id ?? ""}#${inst.instrument_id ?? ""}`;
}

function summarizeSubscription(sub) {
  const inst = sub.instrument ?? {};
  return {
    subscription_id: sub.subscription_id,
    instrument_id: inst.instrument_id,
    exchange_id: inst.exchange_id,
    instrument_name: inst.instrument_name,
    question_tag: sub.question_tag,
    auto_update: sub.auto_update ?? false,
    created_at: sub.created_at
  };
}

function groupByInstrument(subscriptions) {
  const groups = new Map();
  for (const sub of subscriptions) {
    const key = extractInstrumentKey(sub);
    if (!groups.has(key)) {
      const inst = sub.instrument ?? {};
      groups.set(key, {
        instrument_id: inst.instrument_id,
        exchange_id: inst.exchange_id,
        instrument_name: inst.instrument_name,
        subscriptions: []
      });
    }
    groups.get(key).subscriptions.push(summarizeSubscription(sub));
  }
  return [...groups.values()];
}

async function listSubscriptionsFlow() {
  const subscriptions = await getSubscriptionList();
  const grouped = groupByInstrument(subscriptions);

  return {
    action: "list",
    status: "completed",
    instruments: grouped,
    total_instruments: grouped.length,
    total_subscriptions: subscriptions.length,
    ...(grouped.length === 0
      ? { message: "当前账号下还没有自选标的。" }
      : {})
  };
}

async function addSubscriptionFlow(request) {
  const inputs = request.subscription_instruments;
  if (!Array.isArray(inputs) || inputs.length === 0) {
    return {
      action: "add",
      status: "needs_input",
      missing: ["instruments"],
      reason: "missing_instruments",
      prompt: "请提供要加入自选的标的名称或代码。"
    };
  }

  const existing = await getSubscriptionList();
  const existingKeys = new Set(existing.map(extractInstrumentKey));

  const added = [];
  const skippedInvalid = [];
  const skippedDuplicate = [];

  for (const rawInput of inputs) {
    const normalizedInput = String(rawInput).trim();
    if (!normalizedInput) continue;

    const resolved = await resolveInstrument(normalizedInput);
    if (!resolved.ok) {
      skippedInvalid.push({ input: normalizedInput, reason: resolved.reason });
      continue;
    }

    const key = `${resolved.instrument.exchange_id}#${resolved.instrument.instrument_id}`;
    if (existingKeys.has(key)) {
      skippedDuplicate.push({
        input: normalizedInput,
        reason: "该标的已在自选中",
        instrument: resolved.instrument
      });
      continue;
    }

    existingKeys.add(key);

    const result = await addSubscription({
      instrument_id: resolved.instrument.instrument_id,
      exchange_id: resolved.instrument.exchange_id,
      instrument_name: resolved.instrument.instrument_name,
      source_name: "openclaw",
      bypass_realtime: false
    });

    added.push({
      input: normalizedInput,
      instrument: resolved.instrument,
      upstream: result
    });
  }

  if (added.length === 0 && skippedInvalid.length > 0 && skippedDuplicate.length === 0) {
    return {
      action: "add",
      status: "needs_input",
      missing: ["instruments"],
      reason: "all_instruments_invalid",
      prompt: "输入的标的都无法识别，请检查后重新输入。",
      skipped_invalid: skippedInvalid
    };
  }

  return {
    action: "add",
    status: "completed",
    added: added.map((a) => a.instrument),
    skipped_invalid: skippedInvalid,
    skipped_duplicate: skippedDuplicate,
    summary: {
      requested: inputs.length,
      added: added.length,
      skipped_invalid: skippedInvalid.length,
      skipped_duplicate: skippedDuplicate.length
    }
  };
}

async function deleteSubscriptionFlow(request) {
  const inputs = request.subscription_instruments;
  if (!Array.isArray(inputs) || inputs.length === 0) {
    return {
      action: "delete",
      status: "needs_input",
      missing: ["instruments"],
      reason: "missing_instruments",
      prompt: "请提供要从自选中移除的标的名称或代码。"
    };
  }

  const deleted = [];
  const skippedInvalid = [];

  for (const rawInput of inputs) {
    const normalizedInput = String(rawInput).trim();
    if (!normalizedInput) continue;

    const resolved = await resolveInstrument(normalizedInput);
    if (!resolved.ok) {
      skippedInvalid.push({ input: normalizedInput, reason: resolved.reason });
      continue;
    }

    const result = await deleteSubscription({
      instrument_id: resolved.instrument.instrument_id,
      exchange_id: resolved.instrument.exchange_id
    });

    deleted.push({
      input: normalizedInput,
      instrument: resolved.instrument,
      upstream: result
    });
  }

  return {
    action: "delete",
    status: "completed",
    deleted: deleted.map((d) => d.instrument),
    skipped_invalid: skippedInvalid,
    summary: {
      requested: inputs.length,
      deleted: deleted.length,
      skipped_invalid: skippedInvalid.length
    }
  };
}

function extractUnusualMovements(report) {
  const content = report?.report?.content;
  if (!content) return { movements: [], signals_count: 0 };

  const result = content.result ?? {};
  const movements = (result.all_unusual_movements ?? [])
    .sort((a, b) => Number(b.trading_day) - Number(a.trading_day));

  return {
    movements,
    signals_count: content.latest_date_signals_count ?? 0,
    signals_count_map: content.latest_date_signals_count_map ?? {},
    finance_analysis: content.finance_analysis ?? "",
    overall_analysis: result.overall_analysis ?? [],
    opportunities: result.opportunities ?? [],
    risks: result.risks ?? []
  };
}

async function anomalyReportFlow(request) {
  if (!request.instrument_id && !request.instrument_name) {
    return {
      action: "anomaly",
      status: "needs_input",
      missing: ["instrument"],
      reason: "missing_instrument",
      prompt: "请提供要查看异动的标的名称或代码。"
    };
  }

  let instrumentId = request.instrument_id;
  let exchangeId = request.exchange_id;
  let instrumentName = request.instrument_name;

  if (!instrumentId || !exchangeId) {
    const token = instrumentName
      ? { instrument_name: instrumentName }
      : { instrument_id: instrumentId, exchange_id: exchangeId };
    const resolved = await getInstrumentProfile(token);
    instrumentId = resolved.instrument_id;
    exchangeId = resolved.exchange_id;
    instrumentName = instrumentName || resolved.instrument_name;
  }

  const report = await getSubscriptionReport({
    instrument_id: instrumentId,
    exchange_id: exchangeId,
    target_date: request.target_date
  });

  const extracted = extractUnusualMovements(report);

  return {
    action: "anomaly",
    status: "completed",
    instrument: {
      instrument_id: instrumentId,
      exchange_id: exchangeId,
      instrument_name: instrumentName
    },
    target_date: report?.report?.target_datetime ?? request.target_date,
    unusual_movements: extracted.movements,
    signals_count: extracted.signals_count,
    signals_count_map: extracted.signals_count_map,
    finance_analysis: extracted.finance_analysis,
    overall_analysis: extracted.overall_analysis,
    opportunities: extracted.opportunities,
    risks: extracted.risks,
    ...(extracted.movements.length === 0
      ? { message: "当前无异动。" }
      : {})
  };
}

async function summaryFlow() {
  const summary = await getSubscriptionSummary();
  return {
    action: "summary",
    status: "completed",
    summary
  };
}

function splitInputList(value) {
  if (value === undefined || value === null || value === "") return [];
  return String(value)
    .split(/[\n,，;；、]+/u)
    .map((item) => item.trim())
    .filter(Boolean);
}

function buildSubscriptionRequest(values) {
  const repeated = Array.isArray(values["subscription-instrument"])
    ? values["subscription-instrument"]
    : values["subscription-instrument"]
      ? [values["subscription-instrument"]]
      : [];

  return {
    subscription_action: values["subscription-action"],
    subscription_instruments: [
      ...repeated.flatMap((item) => splitInputList(item)),
      ...splitInputList(values["subscription-instruments"])
    ],
    ...buildInstrumentQuery(values),
    target_date: values["target-date"]
  };
}

function assertSubscriptionAction(request) {
  const action = request.subscription_action;
  if (!action) {
    throw createFlowError(
      "MISSING_ACTION",
      "Provide --subscription-action with one of: list, add, delete, anomaly, summary."
    );
  }
  if (!["list", "add", "delete", "anomaly", "summary"].includes(action)) {
    throw createFlowError(
      "UNSUPPORTED_ACTION",
      "Unsupported --subscription-action. Use one of: list, add, delete, anomaly, summary."
    );
  }
}

export async function runSubscriptionFlow(values) {
  const request = buildSubscriptionRequest(values);
  assertSubscriptionAction(request);

  if (request.subscription_action === "list") {
    return listSubscriptionsFlow();
  }

  if (request.subscription_action === "add") {
    return addSubscriptionFlow(request);
  }

  if (request.subscription_action === "delete") {
    return deleteSubscriptionFlow(request);
  }

  if (request.subscription_action === "anomaly") {
    return anomalyReportFlow(request);
  }

  if (request.subscription_action === "summary") {
    return summaryFlow();
  }

  throw createFlowError("UNSUPPORTED_ACTION", "不支持的自选动作。");
}

if (isMain(import.meta)) {
  await runCli(async () => {
    const { values } = parseCommonArgs({ allowPositionals: true });
    return runSubscriptionFlow(values);
  });
}
