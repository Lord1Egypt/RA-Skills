#!/usr/bin/env node
/**
 * 通过企业名称查询企业详情、联系方式、社媒和职员信息。
 *
 * 用法:
 *   node ./scripts/search_by_company_name.js "Microsoft"
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

function saveResult(companyName, json) {
  const ts = new Date().toISOString().slice(0, 19).replace(/[:-]/g, "");
  const safeName = companyName.replace(/[^a-zA-Z0-9\u4e00-\u9fa5_-]/g, "_").slice(0, 60) || "company";
  const fileName = `easy_search_company_name_${safeName}_${ts}.json`;
  const filePath = path.join(process.cwd(), fileName);
  fs.writeFileSync(filePath, JSON.stringify(json, null, 2), "utf-8");
  return { fileName, filePath };
}

function isEmptyData(body) {
  const data = body && Object.prototype.hasOwnProperty.call(body, "data") ? body.data : body;
  return data == null || (typeof data === "object" && !Array.isArray(data) && Object.keys(data).length === 0);
}

async function main() {
  const companyName = (process.argv[2] || "").trim();
  if (!companyName) {
    console.error('用法: node ./scripts/search_by_company_name.js "<企业名称>"');
    process.exit(1);
  }

  const url = new URL(`${BASE_URL}/EasySearch/GetCompanyDetailByCompanyName`);
  url.searchParams.set("companyName", companyName);

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

    const saved = saveResult(companyName, body);
    console.log("查询完成");
    console.log("搜索类型: 企业名称");
    console.log(`搜索内容: ${companyName}`);
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
