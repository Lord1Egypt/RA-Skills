import { readFileSync, writeFileSync, existsSync, mkdirSync } from "fs";
import { join, dirname } from "path";
import { homedir } from "os";

const CONFIG_DIR = join(homedir(), ".config", "maoyan-ticket-booking");
export const UUID_FILE = join(CONFIG_DIR, ".device-uuid.json");
export const AUTHKEY_FILE = join(CONFIG_DIR, ".authkey.json");

export const DEFAULT_TIMEOUT_MS = 10000;

export const CHANNEL_ID = "1000545";
export const CHANNEL_NAME = "龙虾购票";
export const UTM_SOURCE = "openclaw";

/**
 * 生成反扒 headers
 * @returns {Object} 包含反扒参数的 headers 对象
 */
export function generateAntiSpiderHeaders() {
  return {
    clawbot: generateNonce(),
  };
}

/**
 * 生成猫眼接口通用 headers（包含反扒参数、UUID、token 等）
 * @param {Object} options
 * @param {string} [options.token] - 认证 token
 * @param {string} [options.uuid] - 设备 UUID（可选，会自动调用 getOrCreateUuid）
 * @param {string} [options.channelId] - 渠道 ID（可选，默认使用 CHANNEL_ID 常量）
 * @param {Object} [options.extraHeaders] - 额外的 headers（可选）
 * @returns {Object} 完整的 headers 对象
 */
export function generateMaoyanHeaders(options = {}) {
  const { token, uuid: inputUuid, channelId = CHANNEL_ID, extraHeaders = {} } = options;

  // 统一获取或创建 UUID，确保同一用户的连续行为使用相同的 UUID
  const uuid = getOrCreateUuid(inputUuid);

  return {
    Accept: "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7",
    Referer: "https://m.maoyan.com/",
    "User-Agent":
      "Mozilla/5.0 (iPhone; CPU iPhone OS 18_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.5 Mobile/15E148 Safari/604.1",
    "X-Requested-With": "ajax",
    "x-ta": "1",
    ...generateAntiSpiderHeaders(), // 反扒参数
    ...(token ? { token } : {}),
    ...(uuid ? { uuid } : {}), // 统一添加 UUID
    "X-Channel-ID": channelId,
    channelId,
    ...extraHeaders, // 允许各脚本添加特定的 headers
  };
}

/**
 * 生成 32 位随机字符串（字母数字混合）
 * @returns {string}
 */
function generateNonce() {
  const chars = "abcdefghijklmnopqrstuvwxyz0123456789";
  let nonce = "";
  for (let i = 0; i < 32; i++) {
    nonce += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  return nonce;
}

/**
 *  UUID，格式：oc-xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxx
 * 总长度 36 位，与标准 UUID v4 保持一致（末组缩短为 9 位）
 * @returns {string}
 */
function generateUuid() {
  return "oc-xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxx".replace(/[xy]/g, (c) => {
    const r = (Math.random() * 16) | 0;
    const v = c === "x" ? r : (r & 0x3) | 0x8;
    return v.toString(16);
  });
}

/**
 * 加载或生成持久化的设备 UUID
 * 优先级：输入参数 > 本地文件 > 新生成
 * @param {string|undefined} inputUuid - 从输入参数传入的 UUID
 * @returns {string} UUID 字符串
 */
export function getOrCreateUuid(inputUuid) {
  // 1. 优先使用输入参数
  if (inputUuid) {
    return inputUuid;
  }

  // 2. 从本地文件加载
  try {
    if (existsSync(UUID_FILE)) {
      const content = readFileSync(UUID_FILE, "utf-8");
      const data = JSON.parse(content);
      if (data.uuid) {
        return data.uuid;
      }
    }
  } catch (error) {
    // 文件读取失败，继续生成新的
  }

  // 3. 生成新 UUID 并保存
  const newUuid = generateUuid();
  try {
    mkdirSync(dirname(UUID_FILE), { recursive: true });
    writeFileSync(
      UUID_FILE,
      JSON.stringify(
        {
          uuid: newUuid,
          createdAt: new Date().toISOString(),
        },
        null,
        2
      ),
      { encoding: "utf-8", mode: 0o600 }
    );
  } catch (error) {
    // 保存失败也不影响使用，只是下次会重新生成
  }

  return newUuid;
}

/**
 * 将数据写入 .authkey.json（仅当前用户可读写）
 * @param {object} data - 调用方负责构造完整数据结构
 */
export function saveAuthKey(data) {
  mkdirSync(dirname(AUTHKEY_FILE), { recursive: true });
  writeFileSync(AUTHKEY_FILE, JSON.stringify(data, null, 2), { encoding: "utf-8", mode: 0o600 });
}

/**
 * 加载已保存的 token
 * 优先级：输入参数 > 本地文件
 * token 不对外暴露，由脚本内部直接读取使用
 * @param {string|undefined} inputToken - 从输入参数传入的 token
 * @returns {string} token 字符串，未找到时返回空字符串
 */
export function loadSavedToken(inputToken) {
  if (inputToken) return inputToken;

  try {
    if (existsSync(AUTHKEY_FILE)) {
      const data = JSON.parse(readFileSync(AUTHKEY_FILE, "utf-8"));
      if (data.token) return data.token;
    }
  } catch {
    // 读取失败返回空字符串
  }

  return "";
}

export const ERROR_CODES = {
  INVALID_INPUT: 1001,
  TOKEN_INVALID: 1002,
  CONFIG_MISSING: 1003,
  HTTP_ERROR: 1004,
  TIMEOUT: 1005,
  UNEXPECTED_ERROR: 1000,
};

export async function readJsonInput() {
  const arg = process.argv[2];
  if (arg) {
    return JSON.parse(arg);
  }

  const chunks = [];
  for await (const chunk of process.stdin) {
    chunks.push(chunk);
  }

  const raw = Buffer.concat(chunks).toString("utf8").trim();
  if (!raw) {
    return {};
  }

  return JSON.parse(raw);
}

/**
 * 将外部 authKey 映射为内部 token
 * @param {Object} input - 输入参数对象
 * @returns {Object} 映射后的参数对象
 */
export function mapAuthKey(input) {
  if (input.authKey) {
    input.token = input.authKey;
    delete input.authKey;
  }
  return input;
}

export function requireFields(input, fields) {
  const missing = fields.filter((field) => {
    const value = input[field];
    return value === undefined || value === null || value === "";
  });

  if (missing.length > 0) {
    throw new ScriptError(
      ERROR_CODES.INVALID_INPUT,
      `缺少必要字段：${missing.join(", ")}`
    );
  }
}

export function normalizeLimit(limit, fallback = 5) {
  const value = Number(limit || fallback);
  if (Number.isNaN(value) || value <= 0) {
    return fallback;
  }
  return value;
}

export function outputSuccess(data) {
  const normalized = normalizeSuccessPayload(data);

  process.stdout.write(
    JSON.stringify(
      {
        success: true,
        error: null,
        data: normalized.data,
        paging: normalized.paging,
      },
      null,
      2
    )
  );
}

export function outputError(error) {
  const normalized =
    error instanceof ScriptError
      ? error
      : new ScriptError(
          ERROR_CODES.UNEXPECTED_ERROR,
          error.message || "未知错误",
          error.stack || null
        );

  process.stdout.write(
    JSON.stringify(
      {
        success: false,
        error: {
          code: normalized.code,
          message: normalized.message,
          traceInfo: normalized.traceInfo ?? null,
        },
        data: null,
        paging: null,
      },
      null,
      2
    )
  );
}

export class ScriptError extends Error {
  constructor(code, message, traceInfo = null) {
    super(message);
    this.code = normalizeErrorCode(code, ERROR_CODES.UNEXPECTED_ERROR);
    this.traceInfo = traceInfo;
  }
}

export function normalizeErrorCode(code, fallback = ERROR_CODES.UNEXPECTED_ERROR) {
  if (typeof code === "number" && Number.isFinite(code)) {
    return code;
  }

  if (typeof code === "string") {
    const asNumber = Number(code);
    if (!Number.isNaN(asNumber) && Number.isFinite(asNumber)) {
      return asNumber;
    }

    if (code in ERROR_CODES) {
      return ERROR_CODES[code];
    }
  }

  return fallback;
}

export function normalizeSuccessPayload(result) {
  if (
    result &&
    typeof result === "object" &&
    !Array.isArray(result) &&
    ("data" in result || "paging" in result)
  ) {
    return {
      data: result.data ?? null,
      paging: result.paging ?? null,
    };
  }

  return {
    data: result ?? null,
    paging: null,
  };
}

export async function run(main) {
  try {
    const data = await main();
    outputSuccess(data);
  } catch (error) {
    outputError(error);
    if (!(error instanceof ScriptError)) {
      process.exitCode = 1;
    }
  }
}
