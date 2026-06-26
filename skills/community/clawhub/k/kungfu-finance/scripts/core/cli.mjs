import { parseArgs } from "node:util";
import { pathToFileURL } from "node:url";
import { cleanObject, toInteger } from "./runtime.mjs";

export const commonOptions = {
  product: { type: "string" },
  "instrument-id": { type: "string" },
  "exchange-id": { type: "string" },
  "instrument-name": { type: "string" },
  "bayesian-action": { type: "string" },
  "bayesian-task-id": { type: "string" },
  "bayesian-topic": { type: "string" },
  "bayesian-record-limit": { type: "string" },
  "strategy-action": { type: "string" },
  "strategy-scope": { type: "string" },
  "strategy-id": { type: "string" },
  "strategy-name": { type: "string" },
  "strategy-market-mode": { type: "string" },
  "strategy-start-date": { type: "string" },
  "strategy-end-date": { type: "string" },
  "strategy-instrument": { type: "string", multiple: true },
  "strategy-instruments": { type: "string" },
  "researcher-action": { type: "string" },
  "researcher-rank-by": { type: "string" },
  "researcher-limit": { type: "string" },
  "researcher-min-reports": { type: "string" },
  "researcher-author-id": { type: "string" },
  "researcher-name": { type: "string" },
  "researcher-org-name": { type: "string" },
  "bucket-action": { type: "string" },
  "bucket-id": { type: "string" },
  "bucket-name": { type: "string" },
  "bucket-instrument": { type: "string", multiple: true },
  "bucket-instruments": { type: "string" },
  "sector-id": { type: "string" },
  "sector-name": { type: "string" },
  query: { type: "string" },
  "target-date": { type: "string" },
  "target-time": { type: "string" },
  "visual-days-len": { type: "string" },
  "chart-type": { type: "string" },
  "with-chip-peak": { type: "string" },
  "with-price-levels": { type: "string" },
  annotations: { type: "string" },
  "subscription-action": { type: "string" },
  "subscription-instrument": { type: "string", multiple: true },
  "subscription-instruments": { type: "string" },
  openkey: { type: "string" }
};

export function parseCommonArgs({ allowPositionals = false, options = {} } = {}) {
  return parseArgs({
    allowPositionals,
    options: {
      ...commonOptions,
      ...options
    },
    strict: true
  });
}

// Public model-facing stock identifier modes:
// 1. instrument-name
// 2. instrument-id + exchange-id
export function buildInstrumentQuery(values) {
  return cleanObject({
    instrument_id: values["instrument-id"],
    exchange_id: values["exchange-id"],
    instrument_name: values["instrument-name"]
  });
}

// Public model-facing sector inputs:
// 1. sector-name / sector-id for detail products
// 2. query for resolver products
export function buildSectorQuery(values) {
  return cleanObject({
    sector_id: values["sector-id"],
    sector_name: values["sector-name"],
    query: values.query
  });
}

// Keep the public date surface narrow.
// We always expose target_date (+ optional visual_days_len) and hide
// start_date/end_date/is_realtime from the model side.
export function buildWindowQuery(values) {
  const targetDate = values["target-date"];
  const visualDaysLen = toInteger(values["visual-days-len"]);
  return cleanObject({
    target_date: targetDate,
    visual_days_len: visualDaysLen,
    is_realtime: true
  });
}

export function buildCommonRequest(values) {
  return {
    ...buildInstrumentQuery(values),
    ...buildSectorQuery(values),
    ...buildWindowQuery(values),
    target_time: values["target-time"]
  };
}

function splitInputList(value) {
  if (!hasValue(value)) {
    return [];
  }

  return String(value)
    .split(/[\n,，;；、]+/u)
    .map((item) => item.trim())
    .filter(Boolean);
}

export function buildBucketRequest(values) {
  const repeated = Array.isArray(values["bucket-instrument"])
    ? values["bucket-instrument"]
    : hasValue(values["bucket-instrument"])
      ? [values["bucket-instrument"]]
      : [];

  return cleanObject({
    bucket_action: values["bucket-action"],
    bucket_id: values["bucket-id"],
    bucket_name: values["bucket-name"],
    bucket_instruments: [
      ...repeated.flatMap((item) => splitInputList(item)),
      ...splitInputList(values["bucket-instruments"])
    ]
  });
}

export function buildStrategyRequest(values) {
  const repeated = Array.isArray(values["strategy-instrument"])
    ? values["strategy-instrument"]
    : hasValue(values["strategy-instrument"])
      ? [values["strategy-instrument"]]
      : [];

  return cleanObject({
    strategy_action: values["strategy-action"],
    strategy_scope: values["strategy-scope"],
    strategy_id: values["strategy-id"],
    strategy_name: values["strategy-name"],
    strategy_market_mode: values["strategy-market-mode"],
    strategy_start_date: values["strategy-start-date"],
    strategy_end_date: values["strategy-end-date"],
    ...buildCommonRequest(values),
    strategy_instruments: [
      ...repeated.flatMap((item) => splitInputList(item)),
      ...splitInputList(values["strategy-instruments"])
    ]
  });
}

export function buildResearcherRequest(values) {
  return cleanObject({
    researcher_action: values["researcher-action"],
    researcher_rank_by: values["researcher-rank-by"],
    researcher_limit: toInteger(values["researcher-limit"]),
    researcher_min_reports: toInteger(values["researcher-min-reports"]),
    researcher_author_id: values["researcher-author-id"],
    researcher_name: values["researcher-name"],
    researcher_org_name: values["researcher-org-name"],
    ...buildInstrumentQuery(values)
  });
}

export function buildBayesianMonitorRequest(values) {
  return cleanObject({
    bayesian_action: values["bayesian-action"],
    bayesian_task_id: values["bayesian-task-id"],
    bayesian_topic: values["bayesian-topic"],
    bayesian_record_limit: toInteger(values["bayesian-record-limit"])
  });
}

function hasValue(value) {
  return value !== undefined && value !== null && value !== "";
}

function hasAny(query, keys) {
  return keys.some((key) => hasValue(query[key]));
}

export function assertNoFields(query, keys, message) {
  if (hasAny(query, keys)) {
    throw new Error(message);
  }
}

export function assertTargetDate(query, product) {
  if (!query.target_date) {
    throw new Error(`${product} requires --target-date.`);
  }
}

export function assertSingleInstrumentInput(query) {
  const hasName = Boolean(query.instrument_name);
  const hasPair = Boolean(query.instrument_id && query.exchange_id);
  const hasPartialPair = Boolean(query.instrument_id || query.exchange_id);

  if (hasName && hasPair) {
    throw new Error("Use either --instrument-name, or both --instrument-id and --exchange-id. Do not mix both input modes. If the code is unknown, prefer --instrument-name.");
  }

  if (hasPartialPair && !hasPair) {
    throw new Error("When using instrument code mode, provide both --instrument-id and --exchange-id. If the code is unknown, prefer --instrument-name.");
  }

  if (!hasName && !hasPair) {
    throw new Error("Provide either --instrument-name, or both --instrument-id and --exchange-id. If the code is unknown, prefer --instrument-name.");
  }

  if (query.exchange_id && !["SSE", "SZE"].includes(query.exchange_id)) {
    throw new Error("When using instrument code mode, --exchange-id must be SSE or SZE.");
  }
}

export function assertSingleSectorInput(query) {
  const hasName = Boolean(query.sector_name);
  const hasId = Boolean(query.sector_id);

  if (hasName && hasId) {
    throw new Error("Use either --sector-name or --sector-id. Do not mix both input modes. Prefer --sector-name unless a resolved --sector-id was already returned by the backend.");
  }

  if (!hasName && !hasId) {
    throw new Error("Provide either --sector-name or --sector-id. Prefer --sector-name unless a resolved --sector-id was already returned by the backend.");
  }
}

export function assertBucketAction(request) {
  const action = request.bucket_action;
  if (!action) {
    throw new Error("Provide --bucket-action with one of: list, add.");
  }

  if (!["list", "add"].includes(action)) {
    throw new Error("Unsupported --bucket-action. Use one of: list, add.");
  }
}

export function assertStrategyAction(request) {
  const action = request.strategy_action;
  if (!action) {
    throw new Error("Provide --strategy-action with one of: list, signal, count, batch-scan, market-select.");
  }

  if (!["list", "signal", "count", "batch-scan", "market-select"].includes(action)) {
    throw new Error("Unsupported --strategy-action. Use one of: list, signal, count, batch-scan, market-select.");
  }
}

export function assertResearcherAction(request) {
  const action = request.researcher_action;
  if (!action) {
    throw new Error("Provide --researcher-action with one of: rank, stock-reports, author-reports.");
  }

  if (!["rank", "stock-reports", "author-reports"].includes(action)) {
    throw new Error("Unsupported --researcher-action. Use one of: rank, stock-reports, author-reports.");
  }
}

export function assertBayesianMonitorAction(request) {
  const action = request.bayesian_action;
  if (!action) {
    throw new Error("Provide --bayesian-action with one of: list, reports.");
  }

  if (!["list", "reports"].includes(action)) {
    throw new Error("Unsupported --bayesian-action. Use one of: list, reports.");
  }
}

export function assertSingleBucketInput(request) {
  const hasId = Boolean(request.bucket_id);
  const hasName = Boolean(request.bucket_name);

  if (hasId && hasName) {
    throw new Error("Use either --bucket-id or --bucket-name. Do not pass both.");
  }

  if (!hasId && !hasName) {
    throw new Error("Provide either --bucket-id or --bucket-name.");
  }
}

export function printJson(data) {
  process.stdout.write(`${JSON.stringify(data, null, 2)}\n`);
}

function buildStructuredError(error) {
  const code = error?.code || "RUNTIME_ERROR";
  const message = error?.message || "运行失败";
  const status = error?.status;
  const retryable = !["AUTH_INVALID", "PERMISSION_DENIED"].includes(code);

  return {
    success: false,
    error: {
      code,
      message,
      status,
      retryable
    }
  };
}

export async function runCli(main) {
  try {
    const result = await main();
    printJson(result);
  } catch (error) {
    const structured = buildStructuredError(error);
    printJson(structured);

    if (structured.error.retryable) {
      process.exitCode = 1;
    }
  }
}

export function isMain(importMeta) {
  if (!process.argv[1]) {
    return false;
  }
  return importMeta.url === pathToFileURL(process.argv[1]).href;
}
