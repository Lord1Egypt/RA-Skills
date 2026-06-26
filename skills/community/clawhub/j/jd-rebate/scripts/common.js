"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.PENDING_WITHDRAW_TTL_MS = exports.PENDING_AUTH_SCENES = exports.INSECURE_REBATE_V1_HOSTS = exports.DEFAULT_REBATE_V1_BASE_URL = exports.OPENCLAW_CONFIG_PATH = exports.PENDING_WITHDRAW_REQUEST_PATH = exports.PENDING_AUTH_REQUEST_PATH = exports.OPENID_STORE_PATH = exports.AUTH_STATE_PATH = exports.MACHINE_CODE_PATH = exports.SKILL_DATA_DIR = exports.IDENTITY_PATH = exports.WORKSPACE_DATA_DIR = exports.SKILL_DIR = void 0;
exports.ensureSkillDataDir = ensureSkillDataDir;
exports.loadJsonFile = loadJsonFile;
exports.saveJsonFile = saveJsonFile;
exports.loadOpenclawId = loadOpenclawId;
exports.loadMachineCode = loadMachineCode;
exports.saveLocalMachineCode = saveLocalMachineCode;
exports.fetchRemoteMachineCode = fetchRemoteMachineCode;
exports.getOrCreateMachineCode = getOrCreateMachineCode;
exports.candidateRebateV1BaseUrls = candidateRebateV1BaseUrls;
exports.requestRebateV1Json = requestRebateV1Json;
exports.fetchUrlText = fetchUrlText;
exports.isTaobaoShortLink = isTaobaoShortLink;
exports.extractTaobaoTargetUrlFromHtml = extractTaobaoTargetUrlFromHtml;
exports.resolveTaobaoShortLink = resolveTaobaoShortLink;
exports.updateLocalAuthState = updateLocalAuthState;
exports.loadLocalAuthState = loadLocalAuthState;
exports.saveLocalOpenidBinding = saveLocalOpenidBinding;
exports.loadLocalOpenidBinding = loadLocalOpenidBinding;
exports.loadPendingAuthState = loadPendingAuthState;
exports.savePendingAuthRequest = savePendingAuthRequest;
exports.loadPendingAuthRequest = loadPendingAuthRequest;
exports.clearPendingAuthRequest = clearPendingAuthRequest;
exports.loadPendingWithdrawState = loadPendingWithdrawState;
exports.savePendingWithdrawRequest = savePendingWithdrawRequest;
exports.loadPendingWithdrawRequest = loadPendingWithdrawRequest;
exports.clearPendingWithdrawRequest = clearPendingWithdrawRequest;
exports.printJson = printJson;
exports.formatUserMessageMarkdown = formatUserMessageMarkdown;
exports.printUserMessage = printUserMessage;
exports.loadOpenclawConfig = loadOpenclawConfig;
exports.loadPrimaryModelConfig = loadPrimaryModelConfig;
exports.extractJsonObject = extractJsonObject;
exports.requestModelJson = requestModelJson;
const fs_1 = __importDefault(require("fs"));
const path_1 = __importDefault(require("path"));
const child_process_1 = require("child_process");
const url_1 = require("url");
const http_1 = require("./lib/http");
const CURRENT_DIR = __dirname;
exports.SKILL_DIR = path_1.default.resolve(CURRENT_DIR, "..");
exports.WORKSPACE_DATA_DIR = path_1.default.resolve(exports.SKILL_DIR, "..", "..");
exports.IDENTITY_PATH = path_1.default.join(exports.WORKSPACE_DATA_DIR, "identity", "device.json");
exports.SKILL_DATA_DIR = path_1.default.join(exports.SKILL_DIR, "data");
exports.MACHINE_CODE_PATH = path_1.default.join(exports.SKILL_DATA_DIR, "machine-code.json");
exports.AUTH_STATE_PATH = path_1.default.join(exports.SKILL_DATA_DIR, "wechat-auth-state.json");
exports.OPENID_STORE_PATH = path_1.default.join(exports.SKILL_DATA_DIR, "wechat-openid-store.json");
exports.PENDING_AUTH_REQUEST_PATH = path_1.default.join(exports.SKILL_DATA_DIR, "pending-auth-request.json");
exports.PENDING_WITHDRAW_REQUEST_PATH = path_1.default.join(exports.SKILL_DATA_DIR, "pending-withdraw-request.json");
exports.OPENCLAW_CONFIG_PATH = path_1.default.join(exports.WORKSPACE_DATA_DIR, "openclaw.json");
exports.DEFAULT_REBATE_V1_BASE_URL = "https://rebate-skill.io.mlj130.com";
exports.INSECURE_REBATE_V1_HOSTS = new Set();
exports.PENDING_AUTH_SCENES = new Set(["link_rebate", "search_rebate"]);
exports.PENDING_WITHDRAW_TTL_MS = 5 * 60 * 1000;
const MARKDOWN_TITLE_PREFIXES = ["💰 ", "🎉 ", "💡 "];
const MARKDOWN_NUMBER_EMOJI = {
    "1️⃣": "1.",
    "2️⃣": "2.",
    "3️⃣": "3.",
    "4️⃣": "4.",
    "5️⃣": "5.",
};
const MARKDOWN_URL_STOP_CHAR_RE = /[\s<>"'`，。！？；：、（）【】「」《》]/;
const MARKDOWN_URL_TRAILING_CHARS = new Set([
    ".",
    ",",
    "!",
    "?",
    ";",
    ":",
    ">",
    "\"",
    "'",
    "，",
    "。",
    "！",
    "？",
    "；",
    "：",
    "、",
    "】",
    "》",
    "」",
    "』",
    "）",
]);
function countChar(text, target) {
    let count = 0;
    for (const char of text) {
        if (char === target) {
            count += 1;
        }
    }
    return count;
}
function shouldTrimMarkdownUrlTrailingChar(url, char) {
    if (char === ")") {
        return countChar(url, ")") > countChar(url, "(");
    }
    if (char === "]") {
        return countChar(url, "]") > countChar(url, "[");
    }
    if (char === "}") {
        return countChar(url, "}") > countChar(url, "{");
    }
    return MARKDOWN_URL_TRAILING_CHARS.has(char);
}
function splitMarkdownUrlToken(token) {
    let end = token.length;
    while (end > 0 && shouldTrimMarkdownUrlTrailingChar(token.slice(0, end), token[end - 1])) {
        end -= 1;
    }
    return {
        url: token.slice(0, end),
        trailing: token.slice(end),
    };
}
function isValidMarkdownHttpUrl(value) {
    try {
        const parsed = new url_1.URL(value);
        return parsed.protocol === "http:" || parsed.protocol === "https:";
    }
    catch {
        return false;
    }
}
function formatInlineMarkdownLinks(text) {
    let output = "";
    let index = 0;
    while (index < text.length) {
        if (text[index] === "`") {
            const codeEnd = text.indexOf("`", index + 1);
            if (codeEnd === -1) {
                output += text.slice(index);
                break;
            }
            output += text.slice(index, codeEnd + 1);
            index = codeEnd + 1;
            continue;
        }
        const startsWithUrl = text.startsWith("https://", index) || text.startsWith("http://", index);
        if (!startsWithUrl) {
            output += text[index];
            index += 1;
            continue;
        }
        let end = index;
        while (end < text.length && !MARKDOWN_URL_STOP_CHAR_RE.test(text[end])) {
            end += 1;
        }
        const token = text.slice(index, end);
        const { url, trailing } = splitMarkdownUrlToken(token);
        const isMarkdownLinkTarget = index >= 2 && text[index - 1] === "(" && text[index - 2] === "]";
        const isAutolink = index >= 1 && text[index - 1] === "<";
        if (!url || !isValidMarkdownHttpUrl(url) || isMarkdownLinkTarget || isAutolink) {
            output += token;
        }
        else {
            output += `${url}${trailing}`;
        }
        index = end;
    }
    return output;
}
function ensureSkillDataDir() {
    fs_1.default.mkdirSync(exports.SKILL_DATA_DIR, { recursive: true });
}
function loadJsonFile(filePath, defaultValue) {
    if (!fs_1.default.existsSync(filePath)) {
        return defaultValue;
    }
    try {
        return JSON.parse(fs_1.default.readFileSync(filePath, "utf-8"));
    }
    catch {
        return defaultValue;
    }
}
function saveJsonFile(filePath, payload) {
    fs_1.default.mkdirSync(path_1.default.dirname(filePath), { recursive: true });
    fs_1.default.writeFileSync(filePath, `${JSON.stringify(payload, null, 2)}\n`, "utf-8");
}
function loadOpenclawId() {
    const payload = loadJsonFile(exports.IDENTITY_PATH, {});
    const openclawId = String(payload.deviceId || "").trim();
    if (!openclawId) {
        throw new Error(`未在 ${exports.IDENTITY_PATH} 中找到 deviceId`);
    }
    return openclawId;
}
function loadMachineCode() {
    const payload = loadJsonFile(exports.MACHINE_CODE_PATH, {});
    return String(payload.machine_code || "").trim();
}
function saveLocalMachineCode(machineCode, generatedAt, formatHint) {
    const normalized = String(machineCode || "").trim();
    if (!normalized) {
        throw new Error("machine_code 不能为空");
    }
    const payload = {
        version: 1,
        machine_code: normalized,
    };
    if (generatedAt) {
        payload.generated_at = generatedAt;
    }
    if (formatHint) {
        payload.format = formatHint;
    }
    saveJsonFile(exports.MACHINE_CODE_PATH, payload);
}
async function fetchRemoteMachineCode() {
    const response = await requestRebateV1Json("GET", "/v1/common/machine-code");
    const data = response.data || {};
    const machineCode = String(data.machine_code || data.machineCode || response.machine_code || response.machineCode || "").trim();
    if (!machineCode) {
        throw new Error("machine-code 接口未返回有效 machine_code");
    }
    saveLocalMachineCode(machineCode, data.generated_at || data.generatedAt || undefined, data.format || undefined);
    return {
        machine_code: machineCode,
        generated_at: data.generated_at || data.generatedAt || null,
        format: data.format || null,
    };
}
async function getOrCreateMachineCode() {
    const machineCode = loadMachineCode();
    if (machineCode) {
        return machineCode;
    }
    const created = await fetchRemoteMachineCode();
    return String(created.machine_code || "").trim();
}
function candidateRebateV1BaseUrls() {
    const seen = [];
    const configured = String(process.env.REBATE_V1_BASE_URL || "").trim();
    const legacyConfigured = String(process.env.REBATE_MIDPLATFORM_V1_BASE_URL || "").trim();
    for (const url of [configured, legacyConfigured, exports.DEFAULT_REBATE_V1_BASE_URL]) {
        if (!url) {
            continue;
        }
        const normalized = url.replace(/\/+$/, "");
        if (!seen.includes(normalized)) {
            seen.push(normalized);
        }
    }
    return seen;
}
function stringifyErrorPayload(payload) {
    return JSON.stringify(payload, undefined, 0);
}
class RebateV1ResponseError extends Error {
}
function createRebateV1ResponseError(payload) {
    return new RebateV1ResponseError(stringifyErrorPayload(payload));
}
function isRebateV1ResponseError(error) {
    return error instanceof RebateV1ResponseError;
}
function parseJson(text, defaultValue = {}) {
    try {
        return JSON.parse(text);
    }
    catch {
        return defaultValue;
    }
}
async function requestRebateV1Json(method, apiPath, payload) {
    const headers = {
        Accept: "application/json",
    };
    let encoded;
    if (payload !== undefined) {
        encoded = JSON.stringify(payload);
        headers["Content-Type"] = "application/json";
    }
    let lastError = null;
    for (const baseUrl of candidateRebateV1BaseUrls()) {
        const insecure = Array.from(exports.INSECURE_REBATE_V1_HOSTS).some((host) => baseUrl.includes(host));
        try {
            return requestRebateV1JsonViaCurl(baseUrl, apiPath, method, payload, insecure);
        }
        catch (error) {
            if (isRebateV1ResponseError(error)) {
                throw error;
            }
            lastError = error instanceof Error ? error : new Error(String(error));
        }
        try {
            const response = await (0, http_1.requestText)(`${baseUrl}${apiPath}`, {
                method: method.toUpperCase(),
                headers,
                body: encoded,
                timeoutMs: 15000,
                insecure,
            });
            if (response.statusCode >= 400) {
                throw createRebateV1ResponseError({
                    message: `返利接口返回错误 HTTP ${response.statusCode}`,
                    base_url: baseUrl,
                    detail: response.body ? parseJson(response.body, { raw: response.body }) : {},
                });
            }
            let parsed;
            try {
                parsed = JSON.parse(response.body || "{}");
            }
            catch (error) {
                throw new Error(`返利接口响应不是合法 JSON: ${(response.body || "").slice(0, 300)}`);
            }
            if (parsed.result === "error") {
                throw createRebateV1ResponseError({
                    message: parsed.message || "返利接口返回错误",
                    base_url: baseUrl,
                    detail: parsed,
                });
            }
            return parsed;
        }
        catch (error) {
            if (isRebateV1ResponseError(error)) {
                throw error;
            }
            lastError = error instanceof Error ? error : new Error(String(error));
        }
    }
    throw new Error(`无法连接返利接口: ${lastError ? lastError.message : "unknown error"}`);
}
function requestRebateV1JsonViaCurl(baseUrl, apiPath, method, payload, insecure = false) {
    const command = [
        "-sS",
        "--connect-timeout",
        "8",
        "--max-time",
        "15",
        "-X",
        method.toUpperCase(),
        `${baseUrl}${apiPath}`,
        "-H",
        "Accept: application/json",
        "-w",
        "\n%{http_code}",
    ];
    if (insecure) {
        command.push("-k");
    }
    if (payload !== undefined) {
        command.push("-H", "Content-Type: application/json", "-d", JSON.stringify(payload));
    }
    const result = (0, child_process_1.spawnSync)("curl", command, {
        encoding: "utf-8",
    });
    if (result.error) {
        throw result.error;
    }
    if (result.status !== 0) {
        throw new Error(stringifyErrorPayload({
            message: "返利接口 curl 调用失败",
            base_url: baseUrl,
            detail: {
                stderr: String(result.stderr || "").trim(),
                returncode: result.status,
            },
        }));
    }
    const output = String(result.stdout || "");
    const lastNewline = output.lastIndexOf("\n");
    const body = lastNewline >= 0 ? output.slice(0, lastNewline) : "";
    const statusText = lastNewline >= 0 ? output.slice(lastNewline + 1) : output;
    const statusCode = Number(String(statusText || "0").trim() || "0");
    if (statusCode >= 400) {
        throw createRebateV1ResponseError({
            message: `返利接口返回错误 HTTP ${statusCode}`,
            base_url: baseUrl,
            detail: body ? parseJson(body, { raw: body }) : {},
        });
    }
    let parsed;
    try {
        parsed = JSON.parse(body);
    }
    catch {
        throw new Error(`返利接口响应不是合法 JSON: ${body.slice(0, 300)}`);
    }
    if (parsed.result === "error") {
        throw createRebateV1ResponseError({
            message: parsed.message || "返利接口返回错误",
            base_url: baseUrl,
            detail: parsed,
        });
    }
    return parsed;
}
async function fetchUrlText(rawUrl, insecure = false, timeoutSeconds = 10) {
    try {
        return fetchUrlTextViaCurl(rawUrl, insecure, timeoutSeconds);
    }
    catch {
        // Fall back to Node HTTP client below.
    }
    const response = await (0, http_1.requestText)(rawUrl, {
        method: "GET",
        timeoutMs: (timeoutSeconds + 7) * 1000,
        insecure,
        maxRedirects: 8,
    });
    if (response.statusCode >= 400) {
        throw new Error(`URL 不可达: HTTP ${response.statusCode}`);
    }
    return response.body;
}
function fetchUrlTextViaCurl(rawUrl, insecure = false, timeoutSeconds = 10) {
    const command = [
        "-sS",
        "-L",
        "--connect-timeout",
        String(timeoutSeconds),
        "--max-time",
        String(timeoutSeconds + 7),
        rawUrl,
    ];
    if (insecure) {
        command.push("-k");
    }
    const result = (0, child_process_1.spawnSync)("curl", command, {
        encoding: "utf-8",
    });
    if (result.error) {
        throw result.error;
    }
    if (result.status !== 0) {
        throw new Error(`URL 不可达: ${String(result.stderr || "").trim() || `curl exit ${result.status}`}`);
    }
    return String(result.stdout || "");
}
function isTaobaoShortLink(link) {
    try {
        const host = new url_1.URL(String(link || "").trim()).hostname.trim().toLowerCase();
        return host === "e.tb.cn";
    }
    catch {
        return false;
    }
}
function extractTaobaoTargetUrlFromHtml(html) {
    const text = String(html || "");
    const marker = "var url = '";
    const start = text.indexOf(marker);
    if (start < 0) {
        return null;
    }
    const from = start + marker.length;
    const end = text.indexOf("';", from);
    if (end < 0) {
        return null;
    }
    const candidate = text.slice(from, end).trim();
    return candidate || null;
}
async function resolveTaobaoShortLink(link) {
    if (!isTaobaoShortLink(link)) {
        return null;
    }
    const html = await fetchUrlText(link);
    const resolved = extractTaobaoTargetUrlFromHtml(html);
    if (!resolved) {
        throw new Error("淘宝短链页面里没有解析到最终商品链接");
    }
    return resolved;
}
function updateLocalAuthState(machineCode, session) {
    const state = loadJsonFile(exports.AUTH_STATE_PATH, { version: 1, sessions: {} });
    if (!state.sessions || typeof state.sessions !== "object") {
        state.sessions = {};
    }
    state.sessions[machineCode] = session;
    saveJsonFile(exports.AUTH_STATE_PATH, state);
}
function loadLocalAuthState(machineCode) {
    const state = loadJsonFile(exports.AUTH_STATE_PATH, { version: 1, sessions: {} });
    return state.sessions?.[machineCode] || null;
}
function saveLocalOpenidBinding(binding) {
    const store = loadJsonFile(exports.OPENID_STORE_PATH, { version: 1, bindings: {} });
    if (!store.bindings || typeof store.bindings !== "object") {
        store.bindings = {};
    }
    store.bindings[binding.machine_code] = binding;
    saveJsonFile(exports.OPENID_STORE_PATH, store);
}
function loadLocalOpenidBinding(machineCode) {
    const store = loadJsonFile(exports.OPENID_STORE_PATH, { version: 1, bindings: {} });
    return store.bindings?.[machineCode] || null;
}
function loadPendingAuthState() {
    const state = loadJsonFile(exports.PENDING_AUTH_REQUEST_PATH, { version: 1, requests: {} });
    const requests = state && typeof state.requests === "object" && state.requests ? state.requests : {};
    return { version: 1, requests };
}
function savePendingAuthRequest(machineCode, options) {
    const { scene, handler, rawMessage, reason = "" } = options;
    if (!machineCode || !exports.PENDING_AUTH_SCENES.has(scene)) {
        return null;
    }
    const message = String(rawMessage || "").trim();
    if (!message) {
        return null;
    }
    const pendingRequest = {
        scene,
        handler,
        reason,
        raw_message: message,
        created_at: new Date().toISOString(),
    };
    const state = loadPendingAuthState();
    state.requests[machineCode] = pendingRequest;
    saveJsonFile(exports.PENDING_AUTH_REQUEST_PATH, state);
    return pendingRequest;
}
function loadPendingAuthRequest(machineCode) {
    if (!machineCode) {
        return null;
    }
    const request = loadPendingAuthState().requests?.[machineCode];
    if (!request || typeof request !== "object") {
        return null;
    }
    if (!exports.PENDING_AUTH_SCENES.has(String(request.scene || ""))) {
        return null;
    }
    if (!String(request.raw_message || "").trim()) {
        return null;
    }
    return request;
}
function clearPendingAuthRequest(machineCode) {
    if (!machineCode) {
        return;
    }
    const state = loadPendingAuthState();
    if (!state.requests || !state.requests[machineCode]) {
        return;
    }
    delete state.requests[machineCode];
    saveJsonFile(exports.PENDING_AUTH_REQUEST_PATH, state);
}
function loadPendingWithdrawState() {
    const state = loadJsonFile(exports.PENDING_WITHDRAW_REQUEST_PATH, { version: 1, requests: {} });
    const requests = state && typeof state.requests === "object" && state.requests ? state.requests : {};
    return { version: 1, requests };
}
function savePendingWithdrawRequest(machineCode, options) {
    const openid = String(options.openid || "").trim();
    const amount = Number(options.amount);
    if (!machineCode || !openid || !Number.isFinite(amount) || amount <= 0) {
        return null;
    }
    const now = Date.now();
    const ttlMs = Number.isFinite(Number(options.ttlMs)) ? Number(options.ttlMs) : exports.PENDING_WITHDRAW_TTL_MS;
    const pendingRequest = {
        openid,
        amount,
        available_amount: options.availableAmount ?? null,
        withdrawing_amount: options.withdrawingAmount ?? null,
        created_at: new Date(now).toISOString(),
        expires_at: new Date(now + Math.max(1, ttlMs)).toISOString(),
    };
    const state = loadPendingWithdrawState();
    state.requests[machineCode] = pendingRequest;
    saveJsonFile(exports.PENDING_WITHDRAW_REQUEST_PATH, state);
    return pendingRequest;
}
function loadPendingWithdrawRequest(machineCode) {
    if (!machineCode) {
        return null;
    }
    const state = loadPendingWithdrawState();
    const request = state.requests?.[machineCode];
    if (!request || typeof request !== "object") {
        return null;
    }
    const amount = Number(request.amount);
    const openid = String(request.openid || "").trim();
    if (!openid || !Number.isFinite(amount) || amount <= 0) {
        return null;
    }
    const expiresAt = Date.parse(String(request.expires_at || ""));
    const createdAt = Date.parse(String(request.created_at || ""));
    const expired = Number.isFinite(expiresAt)
        ? Date.now() > expiresAt
        : Number.isFinite(createdAt) && Date.now() - createdAt > exports.PENDING_WITHDRAW_TTL_MS;
    if (expired) {
        delete state.requests[machineCode];
        saveJsonFile(exports.PENDING_WITHDRAW_REQUEST_PATH, state);
        return null;
    }
    return request;
}
function clearPendingWithdrawRequest(machineCode) {
    if (!machineCode) {
        return;
    }
    const state = loadPendingWithdrawState();
    if (!state.requests || !state.requests[machineCode]) {
        return;
    }
    delete state.requests[machineCode];
    saveJsonFile(exports.PENDING_WITHDRAW_REQUEST_PATH, state);
}
function printJson(payload) {
    process.stdout.write(`${JSON.stringify(payload, null, 2)}\n`);
}
function formatUserMessageMarkdown(message) {
    const text = String(message || "").replace(/\r\n/g, "\n").replace(/\r/g, "\n").trim();
    if (!text) {
        return "";
    }
    const lines = [];
    for (const rawLine of text.split("\n")) {
        let stripped = rawLine.trim();
        if (!stripped) {
            lines.push("");
            continue;
        }
        if (/^[━\-—]{3,}$/.test(stripped)) {
            lines.push("---");
            continue;
        }
        for (const prefix of MARKDOWN_TITLE_PREFIXES) {
            if (stripped.startsWith(prefix)) {
                stripped = `## ${stripped.slice(prefix.length).trim()}`;
                break;
            }
        }
        for (const [prefix, replacement] of Object.entries(MARKDOWN_NUMBER_EMOJI)) {
            if (stripped.startsWith(prefix)) {
                stripped = `${replacement} ${stripped.slice(prefix.length).trim()}`;
                break;
            }
        }
        if (stripped.startsWith("• ")) {
            stripped = `- ${stripped.slice(2).trim()}`;
        }
        else if (/^【[^】]{1,30}】$/.test(stripped)) {
            stripped = `### ${stripped.slice(1, -1).trim()}`;
        }
        stripped = formatInlineMarkdownLinks(stripped);
        lines.push(stripped);
    }
    const normalized = [];
    let blankCount = 0;
    for (const line of lines) {
        if (!line) {
            blankCount += 1;
            if (blankCount <= 1) {
                normalized.push("");
            }
            continue;
        }
        blankCount = 0;
        normalized.push(line);
    }
    return normalized.join("\n").trim();
}
function printUserMessage(message, options = {}) {
    const output = options.markdown ? formatUserMessageMarkdown(message) : String(message || "").trim();
    process.stdout.write(`${output}\n`);
}
function loadOpenclawConfig() {
    return loadJsonFile(exports.OPENCLAW_CONFIG_PATH, {});
}
function loadPrimaryModelConfig() {
    const config = loadOpenclawConfig();
    const providers = config.models?.providers || {};
    if (!providers || typeof providers !== "object" || !Object.keys(providers).length) {
        throw new Error(`未在 ${exports.OPENCLAW_CONFIG_PATH} 中找到 models.providers 配置`);
    }
    const primary = String(config.agents?.defaults?.model?.primary || "").trim();
    let providerName = "";
    let modelId = "";
    if (primary.includes("/")) {
        [providerName, modelId] = primary.split("/", 2);
    }
    else if (primary) {
        modelId = primary;
    }
    if (!providerName) {
        providerName = Object.keys(providers)[0];
    }
    const provider = providers[providerName];
    if (!provider) {
        throw new Error(`未找到模型提供方配置: ${providerName}`);
    }
    const models = Array.isArray(provider.models) ? provider.models : [];
    if (!modelId) {
        if (!models.length) {
            throw new Error(`模型提供方 ${providerName} 未配置 models`);
        }
        modelId = String(models[0]?.id || "").trim();
    }
    if (!modelId) {
        throw new Error(`模型提供方 ${providerName} 缺少默认模型 id`);
    }
    const baseUrl = String(provider.baseUrl || "").trim().replace(/\/+$/, "");
    const apiKey = String(provider.apiKey || "").trim();
    const apiStyle = String(provider.api || "openai-completions").trim();
    if (!baseUrl || !apiKey) {
        throw new Error(`模型配置不完整: provider=${providerName}`);
    }
    return {
        provider: providerName,
        model: modelId,
        base_url: baseUrl,
        api_key: apiKey,
        api: apiStyle,
    };
}
function extractJsonObject(rawText) {
    const text = String(rawText || "").trim();
    if (!text) {
        throw new Error("模型返回为空");
    }
    try {
        return JSON.parse(text);
    }
    catch {
        // Ignore and try to extract outer object.
    }
    const start = text.indexOf("{");
    const end = text.lastIndexOf("}");
    if (start === -1 || end === -1 || end <= start) {
        throw new Error(`模型返回中未找到 JSON 对象: ${text.slice(0, 200)}`);
    }
    const candidate = text.slice(start, end + 1);
    try {
        return JSON.parse(candidate);
    }
    catch (error) {
        throw new Error(`模型返回 JSON 解析失败: ${error?.message || error}`);
    }
}
async function requestModelJson(systemPrompt, userPrompt, temperature = 0.1, maxTokens = 1200) {
    const modelConf = loadPrimaryModelConfig();
    if (modelConf.api !== "openai-completions") {
        throw new Error(`当前仅支持 openai-completions 风格接口: ${modelConf.api}`);
    }
    const payload = {
        model: modelConf.model,
        messages: [
            { role: "system", content: systemPrompt },
            { role: "user", content: userPrompt },
        ],
        temperature,
        max_tokens: maxTokens,
        response_format: { type: "json_object" },
    };
    const response = await (0, http_1.requestText)(`${modelConf.base_url}/chat/completions`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${modelConf.api_key}`,
        },
        body: JSON.stringify(payload),
        timeoutMs: 20000,
    });
    if (response.statusCode >= 400) {
        throw new Error(`模型接口 HTTP ${response.statusCode}: ${response.body}`);
    }
    let result;
    try {
        result = JSON.parse(response.body);
    }
    catch {
        throw new Error(`模型响应不是合法 JSON: ${response.body.slice(0, 300)}`);
    }
    const choices = Array.isArray(result.choices) ? result.choices : [];
    if (!choices.length) {
        throw new Error(`模型响应缺少 choices: ${response.body.slice(0, 300)}`);
    }
    const message = choices[0]?.message || {};
    let content = message.content || "";
    if (Array.isArray(content)) {
        content = content
            .map((part) => (part && typeof part === "object" ? String(part.text || "") : String(part)))
            .join("");
    }
    const parsed = extractJsonObject(String(content));
    return {
        provider: modelConf.provider,
        model: modelConf.model,
        raw: result,
        content: String(content),
        json: parsed,
    };
}
