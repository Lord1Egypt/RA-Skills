import { API_URL, API_KEY, getWalletAddress } from "./config.js";
import {
  coreAbi,
  getPublicRuntime,
  optionalNumber,
  optionalString,
  requireCoreAddress,
  requiredBigInt,
  requiredString,
  stringifyJson,
  toRecord,
  tupleField,
  type ToolHandler,
} from "./shared.js";
import {
  type JsonValue,
  type RequirementJson,
  normalizeRequirementJson,
  verifyRequirementHash,
} from "./requirement.js";
import { getStoredJwt } from "./siwe.js";

type ApiSyncResult = {
  attempted: boolean;
  success: boolean;
  endpoint?: string;
  error?: string;
  skippedReason?: string;
};

type ApiConfig = {
  url: string;
  apiKey?: string;
  jwt?: string;
};

type SyncTaskPayload = {
  taskId: string;
  requirementJson: RequirementJson;
};

type SyncDisputePayload = {
  taskId: string;
  takerAddress: string;
  makerAddress: string;
  evidenceIpfsHash: string;
  commitDeadline: string;
  revealDeadline: string;
  raisedAt: string;
  evidenceDescription?: string;
  evidenceFiles?: JsonValue;
};

function readApiConfig(): ApiConfig {
  // JWT priority: env var (CI / manual override) > ~/.moltx/auth.json (from siwe_login)
  const jwt = process.env.MOLTX_API_JWT?.trim() || getStoredJwt();

  return {
    url: API_URL.replace(/\/+$/, ""),
    apiKey: API_KEY,
    jwt,
  };
}

function hasApiBaseConfig(): boolean {
  return readApiConfig().url.trim() !== "";
}

function requireApiConfig(): ApiConfig {
  const config = readApiConfig();
  if (!config.jwt) {
    throw new Error("Not authenticated. Run: node runtime/dist/cli.js call siwe_login --json '{}'");
  }
  return config;
}

function buildApiHeaders(config: ApiConfig, hasBody = false): HeadersInit {
  const headers: Record<string, string> = {};
  if (hasBody) {
    headers["Content-Type"] = "application/json";
  }
  if (config.apiKey) {
    headers.apikey = config.apiKey;
  }
  if (config.jwt) {
    headers.Authorization = `Bearer ${config.jwt}`;
  } else if (config.apiKey) {
    headers.Authorization = `Bearer ${config.apiKey}`;
  }

  return headers;
}

async function apiGet(viewName: string, query: URLSearchParams) {
  const config = requireApiConfig();
  const response = await fetch(`${config.url}/rest/v1/${viewName}?${query.toString()}`, {
    headers: buildApiHeaders(config),
  });

  if (!response.ok) {
    throw new Error(`api read failed: ${response.status} ${await response.text()}`);
  }

  return response.json();
}

async function apiRpc(functionName: string, payload: Record<string, unknown>) {
  const config = requireApiConfig();
  const response = await fetch(`${config.url}/rest/v1/rpc/${functionName}`, {
    method: "POST",
    headers: buildApiHeaders(config, true),
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    throw new Error(`api rpc failed: ${response.status} ${await response.text()}`);
  }

  if (response.status === 204) {
    return null;
  }

  const text = await response.text();
  return text === "" ? null : JSON.parse(text);
}

function parseJsonLike(value: unknown, key: string): JsonValue | undefined {
  if (value === undefined) {
    return undefined;
  }
  if (typeof value === "string") {
    const trimmed = value.trim();
    if (trimmed === "") {
      return undefined;
    }
    return JSON.parse(trimmed) as JsonValue;
  }
  if (value === null || typeof value === "number" || typeof value === "boolean") {
    return value as JsonValue;
  }
  if (Array.isArray(value) || typeof value === "object") {
    return value as JsonValue;
  }

  throw new Error(`${key} must be valid JSON`);
}

async function fetchOnchainRequirementHash(taskId: string): Promise<string> {
  const { config, publicClient } = getPublicRuntime();
  const task = await publicClient.readContract({
    address: requireCoreAddress(config),
    abi: coreAbi,
    functionName: "getTask",
    args: [BigInt(taskId)],
  });

  return requiredString(
    { requirementHash: tupleField(task, 16, "requirementHash") },
    "requirementHash",
  );
}

export async function maybeSyncTaskToApi(payload: SyncTaskPayload): Promise<ApiSyncResult> {
  if (!hasApiBaseConfig()) {
    return {
      attempted: false,
      success: false,
      skippedReason: "API base URL not configured",
    };
  }

  try {
    // 调用 submit-task-details Edge Function，由它做链上验证 + 写入数据库
    const config = requireApiConfig();
    const response = await fetch(`${config.url}/functions/v1/submit-task-details`, {
      method: "POST",
      headers: buildApiHeaders(config, true),
      body: JSON.stringify({
        taskId: payload.taskId,
        requirementJson: payload.requirementJson,
      }),
    });

    if (!response.ok) {
      const body = await response.text();
      throw new Error(`submit-task-details failed (${response.status}): ${body}`);
    }

    return { attempted: true, success: true, endpoint: "submit-task-details" };
  } catch (error) {
    return {
      attempted: true,
      success: false,
      endpoint: "submit-task-details",
      error: error instanceof Error ? error.message : "unknown api sync error",
    };
  }
}

export async function maybeSyncDisputeToApi(payload: SyncDisputePayload): Promise<ApiSyncResult> {
  if (!hasApiBaseConfig()) {
    return {
      attempted: false,
      success: false,
      skippedReason: "API base URL not configured",
    };
  }

  try {
    await apiRpc("rpc_raise_dispute", {
      p_task_id: Number(payload.taskId),
      p_taker_address: payload.takerAddress.toLowerCase(),
      p_maker_address: payload.makerAddress.toLowerCase(),
      p_evidence_ipfs_hash: payload.evidenceIpfsHash,
      p_commit_deadline: payload.commitDeadline,
      p_reveal_deadline: payload.revealDeadline,
      p_raised_at: payload.raisedAt,
      p_evidence_description: payload.evidenceDescription,
      p_evidence_files: payload.evidenceFiles,
    });
    return { attempted: true, success: true, endpoint: "rpc_raise_dispute" };
  } catch (error) {
    return {
      attempted: true,
      success: false,
      endpoint: "rpc_raise_dispute",
      error: error instanceof Error ? error.message : "unknown api sync error",
    };
  }
}

const list_active_tasks: ToolHandler = async (args) => {
  const record = toRecord(args ?? {});
  const query = new URLSearchParams();
  query.set("select", "*");
  query.set("order", "created_at.desc");
  if (record.status !== undefined) {
    query.set("status", `eq.${requiredString(record, "status")}`);
  }
  if (record.maker !== undefined) {
    query.set("maker_address", `eq.${requiredString(record, "maker").toLowerCase()}`);
  }
  if (record.categoryId !== undefined) {
    const catId = record.categoryId;
    if (typeof catId !== "number" && typeof catId !== "string") {
      throw new Error("categoryId must be a number or string");
    }
    query.set("category_id", `eq.${catId}`);
  }
  if (record.limit !== undefined) {
    query.set("limit", String(optionalNumber(record, "limit")));
  }
  if (record.offset !== undefined) {
    query.set("offset", String(optionalNumber(record, "offset")));
  }

  return stringifyJson(await apiGet("active_tasks", query));
};

const get_task_details: ToolHandler = async (args) => {
  const record = toRecord(args);
  const taskId = requiredBigInt(record, "taskId");
  const query = new URLSearchParams();
  query.set("select", "*");
  query.set("task_id", `eq.${taskId.toString()}`);

  const rows = await apiGet("task_details", query);
  return stringifyJson(Array.isArray(rows) ? rows[0] ?? null : rows);
};

const list_disputes: ToolHandler = async (args) => {
  const record = toRecord(args ?? {});
  const query = new URLSearchParams();
  query.set("select", "*");
  query.set("order", "raised_at.desc");
  if (record.taskId !== undefined) {
    query.set("task_id", `eq.${requiredBigInt(record, "taskId").toString()}`);
  }
  if (record.taker !== undefined) {
    query.set("taker_address", `eq.${requiredString(record, "taker").toLowerCase()}`);
  }
  if (record.maker !== undefined) {
    query.set("maker_address", `eq.${requiredString(record, "maker").toLowerCase()}`);
  }
  if (record.resolved !== undefined) {
    query.set("resolved_at", Boolean(record.resolved) ? "not.is.null" : "is.null");
  }
  if (record.limit !== undefined) {
    query.set("limit", String(optionalNumber(record, "limit")));
  }
  if (record.offset !== undefined) {
    query.set("offset", String(optionalNumber(record, "offset")));
  }

  return stringifyJson(await apiGet("dispute_overview", query));
};

const sync_task_to_api: ToolHandler = async (args) => {
  const record = toRecord(args);
  const taskId = requiredBigInt(record, "taskId").toString();
  if (record.requirementJson === undefined) {
    throw new Error("requirementJson must be provided");
  }

  // 只需要 taskId + requirementJson，其他字段由 submit-task-details Edge Function 从链上读取
  return stringifyJson(await maybeSyncTaskToApi({
    taskId,
    requirementJson: normalizeRequirementJson(record.requirementJson),
  }));
};

const verify_task_requirement: ToolHandler = async (args) => {
  const record = toRecord(args);
  const taskId = requiredBigInt(record, "taskId");
  const { config, publicClient } = getPublicRuntime();
  const onchainTask = await publicClient.readContract({
    address: requireCoreAddress(config),
    abi: coreAbi,
    functionName: "getTask",
    args: [taskId],
  });

  const onchainRequirementHash = requiredString(
    { requirementHash: tupleField(onchainTask, 16, "requirementHash") },
    "requirementHash",
  );

  const query = new URLSearchParams();
  query.set("select", "*");
  query.set("task_id", `eq.${taskId.toString()}`);
  const rows = await apiGet("task_details", query);
  const taskDetails =
    Array.isArray(rows) ? (rows[0] as Record<string, unknown> | undefined) : undefined;

  if (!taskDetails) {
    return stringifyJson({
      match: false,
      onchainRequirementHash,
      reason: "task details not found in api",
    });
  }

  if (taskDetails.requirement_json === undefined || taskDetails.requirement_json === null) {
    return stringifyJson({
      match: false,
      onchainRequirementHash,
      reason: "task details missing requirement_json",
    });
  }

  return stringifyJson(
    verifyRequirementHash(onchainRequirementHash, taskDetails.requirement_json),
  );
};

const sync_dispute_to_api: ToolHandler = async (args) => {
  const record = toRecord(args);
  return stringifyJson(await maybeSyncDisputeToApi({
    taskId: requiredBigInt(record, "taskId").toString(),
    takerAddress: optionalString(record, "takerAddress") ?? await getWalletAddress(),
    makerAddress: requiredString(record, "makerAddress"),
    evidenceIpfsHash: requiredString(record, "evidenceIpfsHash"),
    commitDeadline: requiredString(record, "commitDeadline"),
    revealDeadline: requiredString(record, "revealDeadline"),
    raisedAt: requiredString(record, "raisedAt"),
    evidenceDescription: optionalString(record, "evidenceDescription"),
    evidenceFiles: parseJsonLike(record.evidenceFiles, "evidenceFiles"),
  }));
};

/**
 * Taker: store the encrypted symmetric key for private-evidence disputes.
 * Must be called after raise_dispute succeeds.
 * The key is idempotent — a second write for the same (taskId, takerAddress) is silently ignored.
 */
const store_evidence_key: ToolHandler = async (args) => {
  const record = toRecord(args);
  const taskId = Number(requiredBigInt(record, "taskId"));
  const takerAddress = optionalString(record, "takerAddress") ?? await getWalletAddress();
  const encryptedKey = requiredString(record, "encryptedKey");

  await apiRpc("rpc_store_evidence_key", {
    p_task_id: taskId,
    p_taker_address: takerAddress.toLowerCase(),
    p_encrypted_key: encryptedKey,
  });

  return stringifyJson({ success: true, taskId, takerAddress: takerAddress.toLowerCase() });
};

/**
 * Taker or committed Arbitrator: read the encrypted symmetric key for a dispute.
 * RLS enforces access: Taker sees their own key; Arbitrators see it only after committing.
 */
const get_evidence_key: ToolHandler = async (args) => {
  const record = toRecord(args);
  const taskId = requiredBigInt(record, "taskId");
  const takerAddress = optionalString(record, "takerAddress");

  const query = new URLSearchParams();
  query.set("select", "task_id,taker_address,encrypted_key,created_at");
  query.set("task_id", `eq.${taskId.toString()}`);
  if (takerAddress) {
    query.set("taker_address", `eq.${takerAddress.toLowerCase()}`);
  }

  const rows = await apiGet("evidence_keys", query);
  const result = Array.isArray(rows) ? (rows[0] ?? null) : rows ?? null;
  return stringifyJson(result);
};

export const apiTools: Record<string, ToolHandler> = {
  get_evidence_key,
  get_task_details,
  list_active_tasks,
  list_disputes,
  store_evidence_key,
  sync_dispute_to_api,
  sync_task_to_api,
  verify_task_requirement,
};
