import {
  assertBucketAction,
  buildBucketRequest,
  isMain,
  parseCommonArgs,
  runCli
} from "../core/cli.mjs";
import { getBucketList } from "../products/bucket_list.mjs";
import { getBucketInstruments } from "../products/bucket_instruments.mjs";
import { addBucketInstruments } from "../products/bucket_add_instruments.mjs";
import { getInstrumentProfile } from "../products/instrument_profile.mjs";

function createFlowError(code, message) {
  const error = new Error(message);
  error.code = code;
  return error;
}

function buildNeedsInputResponse({
  prompt,
  missing,
  reason,
  bucket,
  options,
  attempted,
  skipped_invalid,
  skipped_duplicate
}) {
  return {
    action: "add",
    status: "needs_input",
    prompt,
    missing,
    reason,
    ...(bucket ? { bucket } : {}),
    ...(options ? { options } : {}),
    ...(attempted ? { attempted } : {}),
    ...(skipped_invalid ? { skipped_invalid } : {}),
    ...(skipped_duplicate ? { skipped_duplicate } : {})
  };
}

function buildBlockedResponse({ reason, message, buckets }) {
  return {
    action: "add",
    status: "blocked",
    reason,
    message,
    ...(buckets ? { options: { buckets } } : {})
  };
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

  return {
    instrument_name: value
  };
}

function isFatalResolutionError(error) {
  return ["AUTH_INVALID", "PERMISSION_DENIED", "RATE_LIMITED", "UPSTREAM_ERROR"].includes(
    error?.code
  );
}

async function resolveBucketInstrument(rawInput) {
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

function normalizeBucket(bucket) {
  return {
    bucket_id: bucket.bucket_id,
    name: bucket.name
  };
}

function resolveBucketBySelector(buckets, request) {
  const hasBucketId = Boolean(request.bucket_id);
  const hasBucketName = Boolean(request.bucket_name);

  if (hasBucketId && hasBucketName) {
    return {
      response: buildNeedsInputResponse({
        missing: ["bucket"],
        reason: "ambiguous_bucket_selector",
        prompt: "请只提供一个目标票池。你可以使用 bucket_id 或票池名称其一重新选择。",
        options: { buckets: buckets.map(normalizeBucket) },
        attempted: {
          bucket_id: request.bucket_id,
          bucket_name: request.bucket_name
        }
      })
    };
  }

  if (!hasBucketId && !hasBucketName) {
    return {
      response: buildNeedsInputResponse({
        missing: ["bucket"],
        reason: "missing_bucket",
        prompt: "你要把这些标的加到哪个票池？请先选择一个目标票池。",
        options: { buckets: buckets.map(normalizeBucket) }
      })
    };
  }

  if (request.bucket_id) {
    const bucket = buckets.find((item) => item.bucket_id === request.bucket_id);
    if (!bucket) {
      return {
        response: buildNeedsInputResponse({
          missing: ["bucket"],
          reason: "bucket_not_found",
          prompt: "未找到指定票池，请从当前票池列表中重新选择。",
          options: { buckets: buckets.map(normalizeBucket) },
          attempted: {
            bucket_id: request.bucket_id
          }
        })
      };
    }
    return { bucket };
  }

  const targetName = request.bucket_name.trim();
  const matched = buckets.filter((item) => item.name === targetName);

  if (matched.length === 0) {
    return {
      response: buildNeedsInputResponse({
        missing: ["bucket"],
        reason: "bucket_not_found",
        prompt: "未找到这个票池名称，请从当前票池列表中重新选择。",
        options: { buckets: buckets.map(normalizeBucket) },
        attempted: {
          bucket_name: targetName
        }
      })
    };
  }

  if (matched.length > 1) {
    return {
      response: buildNeedsInputResponse({
        missing: ["bucket"],
        reason: "bucket_ambiguous",
        prompt: "存在同名票池，请改用 bucket_id 在下面的候选票池中重新选择。",
        options: { buckets: matched.map(normalizeBucket) },
        attempted: {
          bucket_name: targetName
        }
      })
    };
  }

  return { bucket: matched[0] };
}

async function resolveAddPlan(bucket, request) {
  const existing = await getBucketInstruments({ bucket_id: bucket.bucket_id });
  const existingKeys = new Set(
    existing.map((item) => `${item.exchange_id}#${item.instrument_id}`)
  );
  const seenKeys = new Set();

  const added = [];
  const skipped_invalid = [];
  const skipped_duplicate = [];

  for (const rawInput of request.bucket_instruments) {
    const normalizedInput = String(rawInput).trim();
    if (!normalizedInput) {
      continue;
    }

    const resolved = await resolveBucketInstrument(normalizedInput);
    if (!resolved.ok) {
      skipped_invalid.push({
        input: normalizedInput,
        reason: resolved.reason
      });
      continue;
    }

    const key = `${resolved.instrument.exchange_id}#${resolved.instrument.instrument_id}`;
    if (seenKeys.has(key)) {
      skipped_duplicate.push({
        input: normalizedInput,
        reason: "请求中存在重复标的",
        instrument: resolved.instrument
      });
      continue;
    }

    seenKeys.add(key);

    if (existingKeys.has(key)) {
      skipped_duplicate.push({
        input: normalizedInput,
        reason: "该标的已在目标票池中",
        instrument: resolved.instrument
      });
      continue;
    }

    added.push(resolved.instrument);
  }

  return {
    added,
    skipped_invalid,
    skipped_duplicate
  };
}

async function listBucketsFlow() {
  const buckets = await getBucketList();
  return {
    action: "list",
    status: "completed",
    buckets,
    total: buckets.length,
    ...(buckets.length === 0
      ? { message: "当前账号下还没有票池。" }
      : {})
  };
}

async function addToBucketFlow(request) {
  const buckets = await getBucketList();
  if (buckets.length === 0) {
    return buildBlockedResponse({
      reason: "empty_bucket_list",
      message: "当前账号下还没有票池，请先准备票池后再试。"
    });
  }

  const selection = resolveBucketBySelector(buckets, request);
  if (selection.response) {
    return selection.response;
  }

  const bucket = selection.bucket;
  const normalizedBucket = normalizeBucket(bucket);

  if (!Array.isArray(request.bucket_instruments) || request.bucket_instruments.length === 0) {
    return buildNeedsInputResponse({
      missing: ["instruments"],
      reason: "missing_instruments",
      prompt: "请提供要加入票池的标的列表。",
      bucket: normalizedBucket
    });
  }

  const resolution = await resolveAddPlan(bucket, request);

  if (resolution.added.length === 0 && resolution.skipped_invalid.length > 0 && resolution.skipped_duplicate.length === 0) {
    return buildNeedsInputResponse({
      missing: ["instruments"],
      reason: "all_instruments_invalid",
      prompt: "输入的标的都无法识别，请检查后重新输入。",
      bucket: normalizedBucket,
      skipped_invalid: resolution.skipped_invalid
    });
  }

  let upstream = {
    success: true,
    message: "没有新的标的需要加入票池。"
  };

  if (resolution.added.length > 0) {
    upstream = await addBucketInstruments({
      bucket_id: bucket.bucket_id,
      instruments: resolution.added
    });
  }

  return {
    action: "add",
    status: "completed",
    bucket: normalizedBucket,
    added: resolution.added,
    skipped_invalid: resolution.skipped_invalid,
    skipped_duplicate: resolution.skipped_duplicate,
    upstream,
    summary: {
      requested: request.bucket_instruments.length,
      added: resolution.added.length,
      skipped_invalid: resolution.skipped_invalid.length,
      skipped_duplicate: resolution.skipped_duplicate.length
    }
  };
}

export async function runBucketFlow(values) {
  const request = buildBucketRequest(values);
  assertBucketAction(request);

  if (request.bucket_action === "list") {
    return listBucketsFlow();
  }

  if (request.bucket_action === "add") {
    return addToBucketFlow(request);
  }

  throw createFlowError("UNSUPPORTED_BUCKET_ACTION", "不支持的票池动作。");
}

if (isMain(import.meta)) {
  await runCli(async () => {
    const { values } = parseCommonArgs();
    return runBucketFlow(values);
  });
}
