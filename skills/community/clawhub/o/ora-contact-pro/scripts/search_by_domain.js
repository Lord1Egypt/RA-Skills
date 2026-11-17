#!/usr/bin/env node
/**
 * 通过一个或多个企业域名流式查询企业详情、联系方式、社媒和职员信息。
 *
 * 用法:
 *   node ./scripts/search_by_domain.js baidu.com xiaomi.com huawei.com
 *   node ./scripts/search_by_domain.js '["baidu.com","xiaomi.com"]'
 */

const fs = require("fs");
const os = require("os");
const path = require("path");

const API_URL = "https://api.topeasychina.com:6443/TPAiAgentSkill/EasySearch/GetCompanyDetailByDomains";
const REQUEST_TIMEOUT_MS = 600_000;

let KEY_FILE = path.join(__dirname, "..", "OraAgent.key");
if (!fs.existsSync(KEY_FILE)) {
  KEY_FILE = path.join(__dirname, "..", "..", "OraAgent.key");
}

function readApiKey() {
  try {
    return fs.readFileSync(KEY_FILE, "utf-8").trim();
  } catch {
    return null;
  }
}

function normalizeDomain(value) {
  return String(value)
    .trim()
    .replace(/^https?:\/\//i, "")
    .split(/[/?#]/)[0]
    .replace(/\.$/, "")
    .toLowerCase();
}

function parseDomains(args) {
  let values = args;
  if (args.length === 1 && args[0].trim().startsWith("[")) {
    let parsed;
    try {
      parsed = JSON.parse(args[0]);
    } catch (error) {
      throw new Error(`域名 JSON 数组格式不正确: ${error.message}`);
    }
    if (!Array.isArray(parsed)) throw new Error("域名参数必须是 JSON 数组");
    values = parsed;
  } else {
    values = args.flatMap((value) => value.split(/[\s,]+/));
  }

  return [...new Set(values.map(normalizeDomain).filter(Boolean))];
}

function saveResult(domains, json) {
  const ts = new Date().toISOString().slice(0, 19).replace(/[:-]/g, "");
  const label = domains.length === 1
    ? domains[0].replace(/[^a-zA-Z0-9._-]/g, "_").slice(0, 60)
    : `${domains.length}_domains`;
  const fileName = `easy_search_domains_${label || "domains"}_${ts}.json`;
  const outputDir = path.join(os.tmpdir(), "ora-contact-pro");
  fs.mkdirSync(outputDir, { recursive: true });
  const filePath = path.join(outputDir, fileName);
  fs.writeFileSync(filePath, JSON.stringify(json, null, 2), "utf-8");
  return { fileName, filePath };
}

function isEmptyData(body) {
  const data = body && Object.prototype.hasOwnProperty.call(body, "data") ? body.data : body;
  return data == null
    || (Array.isArray(data) && data.length === 0)
    || (typeof data === "object" && !Array.isArray(data) && Object.keys(data).length === 0);
}

function parseStreamLine(line) {
  let value = line.trim();
  if (!value || value.startsWith(":")) return undefined;
  if (/^(event|id|retry):/i.test(value)) return undefined;
  if (/^data:/i.test(value)) value = value.slice(5).trim();
  if (!value || value === "[DONE]") return undefined;
  try {
    return JSON.parse(value);
  } catch {
    return undefined;
  }
}

async function consumeStreamingResponse(response, onMessage = () => {}) {
  if (!response.body || typeof response.body.getReader !== "function") {
    const text = await response.text();
    try {
      return text ? JSON.parse(text) : null;
    } catch {
      return { raw: text };
    }
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  const messages = [];
  let raw = "";
  let buffer = "";

  const consumeLine = (line) => {
    const message = parseStreamLine(line);
    if (message !== undefined) {
      messages.push(message);
      onMessage(message, messages.length);
    }
  };

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    const chunk = decoder.decode(value, { stream: true });
    raw += chunk;
    buffer += chunk;
    const lines = buffer.split(/\r?\n/);
    buffer = lines.pop() || "";
    lines.forEach(consumeLine);
  }

  const tail = decoder.decode();
  raw += tail;
  buffer += tail;
  if (buffer.trim()) consumeLine(buffer);

  // 普通 JSON 响应也可能被 HTTP 分块；优先保留它原本的整体结构。
  try {
    return raw.trim() ? JSON.parse(raw) : null;
  } catch {
    return messages.length > 0 ? messages : { raw };
  }
}

async function main() {
  let domains;
  try {
    domains = parseDomains(process.argv.slice(2));
  } catch (error) {
    console.error(`错误: ${error.message}`);
    process.exitCode = 1;
    return;
  }

  if (domains.length === 0) {
    console.error('用法: node ./scripts/search_by_domain.js <域名1> [域名2 ...]');
    console.error('或: node ./scripts/search_by_domain.js \'["baidu.com","xiaomi.com"]\'');
    process.exitCode = 1;
    return;
  }

  const headers = {
    "Content-Type": "application/json",
    Accept: "application/x-ndjson, text/event-stream, application/json",
  };
  const apiKey = readApiKey();
  if (apiKey) headers.Authorization = `Bearer ${apiKey}`;

  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS);

  try {
    console.log("注意: 这将读取本地 OraAgent.key 并向外部服务发送查询，请确保你已获得授权并适用于合规场景。");
    console.log(`正在查询 ${domains.length} 个域名: ${domains.join(", ")}`);
    const response = await fetch(API_URL, {
      method: "POST",
      headers,
      body: JSON.stringify(domains),
      signal: controller.signal,
    });

    if (!response.ok) {
      const text = await response.text();
      let body;
      try {
        body = text ? JSON.parse(text) : null;
      } catch {
        body = { raw: text };
      }
      console.log(`STATUS:${response.status}`);
      if (response.status === 402) console.log("RECHARGE_URL:https://www.oraskl.com/platform");
      console.log(`BODY:${JSON.stringify(body)}`);
      process.exitCode = 1;
      return;
    }

    const body = await consumeStreamingResponse(response, (message, count) => {
      const domain = message?.domain || message?.Domain || message?.data?.domain || message?.data?.Domain;
      console.error(`[流] 已接收第 ${count} 条${domain ? `: ${domain}` : ""}`);
    });
    const saved = saveResult(domains, body);
    console.log("查询完成");
    console.log("搜索类型: 企业域名（批量）");
    console.log(`搜索数量: ${domains.length}`);
    console.log(`搜索内容: ${domains.join(", ")}`);
    console.log(`结果为空: ${isEmptyData(body) ? "是" : "否"}`);
    console.log(`原始数据文件: ${saved.filePath.replace(/\\/g, "/")}`);
    console.log(`数据文件标识: ${saved.fileName}`);
  } catch (error) {
    console.error(error.name === "AbortError" ? `超时: 超过 ${REQUEST_TIMEOUT_MS / 1000} 秒` : `错误: ${error.message}`);
    process.exitCode = 1;
  } finally {
    clearTimeout(timer);
  }
}

if (require.main === module) main();

module.exports = {
  consumeStreamingResponse,
  isEmptyData,
  normalizeDomain,
  parseDomains,
  parseStreamLine,
};
