#!/usr/bin/env node
/**
 * 步骤 1：从流式 API 获取原始数据
 *
 * 用法: node fetch_stream.js <英文关键字> <纬度> <经度>
 * 示例: node fetch_stream.js toys 40.74959 -74.002533
 *
 * 输出: 保存 raw_<关键字>.json 文件，stdout 输出文件路径
 *
 * 注意: API 地址在下方 MAP_SEARCH_API 中配置，部署时修改即可
 */

const MAP_SEARCH_API = "https://api.topeasychina.com:6443/TPAiAgentSkill/MapsSearchTask/stream";
const STREAM_TIMEOUT_MS = 600_000;
const fs = require("fs");
const path = require("path");

let KEY_FILE = path.join(__dirname, "..", "OraAgent.key");
if (!fs.existsSync(KEY_FILE)) {
    KEY_FILE = path.join(__dirname, "..", "..", "OraAgent.key");
}

function log(msg) {
  process.stderr.write(msg + "\n");
}

/** 从 OraAgent.key 读取 MapSearchKey */
function readApiKey() {
  try {
    return fs.readFileSync(KEY_FILE, "utf-8").trim();
  } catch { /* 文件不存在则不用 key */ }
  return null;
}

async function main() {
  const args = process.argv.slice(2);
  if (args.length < 3) {
    console.error("用法: node fetch_stream.js <英文关键字> <纬度> <经度>");
    process.exit(1);
  }

  const keyword = args[0].trim();
  const lat = parseFloat(args[1]);
  const lng = parseFloat(args[2]);

  if (isNaN(lat) || isNaN(lng)) {
    console.error("错误: 纬度或经度格式不正确");
    process.exit(1);
  }

  const apiKey = readApiKey();
  if (apiKey) log(`[认证] 已加载 API Key`);
  else log(`[认证] 未找到 API Key，使用无认证请求`);

  log(`[获取数据] API: ${MAP_SEARCH_API}`);
  log(`[获取数据] 关键字: ${keyword}, 坐标: ${lat},${lng}`);

  const payload = {
    KeywordList: [{ Keyword: keyword }],
    GeographyList: [{ Lat: lat, Lng: lng, Radius: 50000 }],
  };

const headers = { "Content-Type": "application/json" };
if (apiKey) headers["Authorization"] = `Bearer ${apiKey}`;

  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), STREAM_TIMEOUT_MS);

  try {
    const resp = await fetch(MAP_SEARCH_API, {
      method: "POST",
      headers,
      body: JSON.stringify(payload),
      signal: controller.signal,
    });

    if (!resp.ok) {
      const body = await resp.text();
      if (resp.status === 402) {
        // 免费额度用尽，输出结构化信息让 Claude 识别
        console.log(`STATUS:402`);
        console.log(`MESSAGE:免费额度已用尽，请付费后继续使用`);
        console.log(`RECHARGE_URL:https://www.oraskl.com/platform`);
      } else {
        console.error(`API 错误: ${resp.status} ${body}`);
      }
      process.exit(1);
    }

    log(`[获取数据] 连接成功，等待流数据...`);
    const results = [];
    let count = 0;

    const reader = resp.body.getReader();
    const decoder = new TextDecoder();
    let buffer = "";

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split("\n");
      buffer = lines.pop() || "";

      for (const line of lines) {
        const trimmed = line.trim();
        if (!trimmed) continue;
        try {
          const msg = JSON.parse(trimmed);
          if (msg.type === "result" && msg.data) {
            count++;
            results.push(msg.data);
            log(`[流] >>> 第 ${count} 条: ${msg.data.Name || "未知"}`);
          } else if (msg.type === "done") {
            log(`[流] <<< 全部完成，共 ${count} 条结果`);
          }
        } catch { /* 不完整行跳过 */ }
      }
    }

    // 保存到文件
    const ts = new Date().toISOString().slice(0, 19).replace(/[:-]/g, "");
    const safeKeyword = keyword.replace(/[^a-zA-Z0-9_-]/g, "_");
    const fileName = `raw_${safeKeyword}_${ts}.json`;
    fs.writeFileSync(fileName, JSON.stringify(results, null, 2), "utf-8");

    const fullPath = process.cwd().replace(/\\/g, "/") + "/";

    console.log(`获取完成，共 ${count} 条数据`);
    console.log(`原始数据文件: ${fullPath}${fileName}`);
    console.log(`数据文件标识: ${fileName}`);

  } catch (e) {
    if (e.name === "AbortError") {
      console.error(`超时: 超过 ${STREAM_TIMEOUT_MS / 1000} 秒`);
    } else {
      console.error(`错误: ${e.message}`);
    }
    process.exit(1);
  } finally {
    clearTimeout(timer);
  }
}

main();
