#!/usr/bin/env node
/**
 * 通过 LinkedIn 企业号查询企业详情、联系方式、社媒和职员信息。
 *
 * 用法:
 *   node ./scripts/search_by_linkedin.js "microsoft"
 *   node ./scripts/search_by_linkedin.js "https://www.linkedin.com/company/microsoft/"
 */

const fs = require("fs");
const path = require("path");

const BASE_URL = "https://api.topeasychina.com:6443/TPAiAgentSkill";
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

function extractUniversalName(value) {
  const text = value.trim();
  const match = text.match(/linkedin\.com\/company\/([^/?#]+)/i);
  if (match) return decodeURIComponent(match[1]).trim();
  return text.replace(/^@+/, "").replace(/^\/+|\/+$/g, "").trim();
}

function saveResult(universalName, json) {
  const ts = new Date().toISOString().slice(0, 19).replace(/[:-]/g, "");
  const safeName = universalName.replace(/[^a-zA-Z0-9._-]/g, "_").slice(0, 60) || "linkedin";
  const fileName = `easy_search_linkedin_${safeName}_${ts}.json`;
  const filePath = path.join(process.cwd(), fileName);
  fs.writeFileSync(filePath, JSON.stringify(json, null, 2), "utf-8");
  return { fileName, filePath };
}

function isEmptyData(body) {
  const data = body && Object.prototype.hasOwnProperty.call(body, "data") ? body.data : body;
  return data == null || (typeof data === "object" && !Array.isArray(data) && Object.keys(data).length === 0);
}

async function main() {
  const universalName = extractUniversalName(process.argv[2] || "");
  if (!universalName) {
    console.error('用法: node ./scripts/search_by_linkedin.js "<LinkedIn企业号或公司链接>"');
    process.exit(1);
  }

  const url = new URL(`${BASE_URL}/EasySearch/GetCompanyDetailByUniversalName`);
  url.searchParams.set("universalName", universalName);

  const headers = {};
  const apiKey = readApiKey();
  if (apiKey) headers.Authorization = `Bearer ${apiKey}`;

  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS);

  try {
    const response = await fetch(url, { method: "GET", headers, signal: controller.signal });
    const text = await response.text();
    let body;
    try {
      body = text ? JSON.parse(text) : null;
    } catch {
      body = { raw: text };
    }

    if (!response.ok) {
      console.log(`STATUS:${response.status}`);
      if (response.status === 402) console.log("RECHARGE_URL:https://www.oraskl.com/platform");
      console.log(`BODY:${JSON.stringify(body)}`);
      process.exit(1);
    }

    const saved = saveResult(universalName, body);
    console.log("查询完成");
    console.log("搜索类型: LinkedIn企业号");
    console.log(`搜索内容: ${universalName}`);
    console.log(`结果为空: ${isEmptyData(body) ? "是" : "否"}`);
    console.log(`原始数据文件: ${saved.filePath.replace(/\\/g, "/")}`);
    console.log(`数据文件标识: ${saved.fileName}`);
  } catch (error) {
    console.error(error.name === "AbortError" ? `超时: 超过 ${REQUEST_TIMEOUT_MS / 1000} 秒` : `错误: ${error.message}`);
    process.exit(1);
  } finally {
    clearTimeout(timer);
  }
}

main();
