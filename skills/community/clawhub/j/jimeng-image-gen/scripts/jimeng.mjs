#!/usr/bin/env node
/**
 * 即梦 AI 图片生成脚本 v2.0
 * 基于火山引擎即梦 AI 图片生成 4.0 API（异步接口）
 *
 * 用法:
 *   node jimeng.mjs generate --prompt "赛博朋克城市夜景" --ratio 16:9
 *   node jimeng.mjs generate --prompt "可爱的猫咪" --width 2048 --height 2048 --save ./cat.png
 *   node jimeng.mjs generate --prompt "一组表情包" --size 2097152
 *   node jimeng.mjs generate --text "新年快乐" --color 红色 --illustration "烟花,灯笼" --ratio 4:3
 *   node jimeng.mjs generate --prompt "把背景换成海边" --image-url "https://..." --scale 0.7
 *   node jimeng.mjs models
 *   node jimeng.mjs ratios
 */

import crypto from "crypto";
import fs from "fs";
import path from "path";
import https from "https";
import { URL } from "url";

// ─── 配置 ────────────────────────────────────────────────────────────────────

const ENDPOINT  = "https://visual.volcengineapi.com";
const HOST      = "visual.volcengineapi.com";
const REGION    = "cn-north-1";
const SERVICE   = "cv";
const REQ_KEY   = "jimeng_t2i_v40";
const VERSION   = "2022-08-31";

const ACCESS_KEY = process.env.JIMENG_ACCESS_KEY;
const SECRET_KEY = process.env.JIMENG_SECRET_KEY;

// 推荐宽高预设（来自官方文档）
const RATIO_PRESETS = {
  // 1K
  "1:1-1k":   { width: 1024,  height: 1024, label: "1K 1:1" },
  // 2K（推荐）
  "1:1":      { width: 2048,  height: 2048, label: "2K 1:1（推荐）" },
  "4:3":      { width: 2304,  height: 1728, label: "2K 4:3" },
  "3:2":      { width: 2496,  height: 1664, label: "2K 3:2" },
  "16:9":     { width: 2560,  height: 1440, label: "2K 16:9" },
  "21:9":     { width: 3024,  height: 1296, label: "2K 21:9" },
  "3:4":      { width: 1728,  height: 2304, label: "2K 3:4" },
  "2:3":      { width: 1664,  height: 2496, label: "2K 2:3" },
  "9:16":     { width: 1440,  height: 2560, label: "2K 9:16" },
  // 4K
  "1:1-4k":   { width: 4096,  height: 4096, label: "4K 1:1" },
  "16:9-4k":  { width: 5404,  height: 3040, label: "4K 16:9" },
  "4:3-4k":   { width: 4694,  height: 3520, label: "4K 4:3" },
};

// 任务状态轮询配置
const POLL_INTERVAL_MS = 3000;   // 每 3 秒查询一次
const POLL_TIMEOUT_MS  = 120000; // 最多等 120 秒

// ─── 签名算法（火山引擎 V4 HMAC-SHA256）────────────────────────────────────

function hmac(key, data, encoding = undefined) {
  return crypto.createHmac("sha256", key).update(data).digest(encoding);
}

function sha256hex(data) {
  return crypto.createHash("sha256").update(data).digest("hex");
}

function buildSignedRequest(action, bodyObj) {
  const body    = JSON.stringify(bodyObj);
  const now     = new Date();
  const xDate   = now.toISOString().replace(/[:\-]|\.\d{3}/g, "");
  const datestamp = xDate.slice(0, 8);

  const queryStr = `Action=${action}&Version=${VERSION}`;
  const payloadHash  = sha256hex(body);
  const contentType  = "application/json";

  const canonicalHeaders =
    `content-type:${contentType}\n` +
    `host:${HOST}\n` +
    `x-content-sha256:${payloadHash}\n` +
    `x-date:${xDate}\n`;

  const signedHeaders = "content-type;host;x-content-sha256;x-date";

  const canonicalRequest = [
    "POST", "/", queryStr,
    canonicalHeaders, signedHeaders, payloadHash,
  ].join("\n");

  const credentialScope = `${datestamp}/${REGION}/${SERVICE}/request`;
  const stringToSign = [
    "HMAC-SHA256", xDate, credentialScope, sha256hex(canonicalRequest),
  ].join("\n");

  const kDate    = hmac(SECRET_KEY, datestamp);
  const kRegion  = hmac(kDate, REGION);
  const kService = hmac(kRegion, SERVICE);
  const kSigning = hmac(kService, "request");
  const signature = hmac(kSigning, stringToSign, "hex");

  return {
    url: `${ENDPOINT}?${queryStr}`,
    headers: {
      "Content-Type":    contentType,
      "X-Date":          xDate,
      "X-Content-Sha256": payloadHash,
      "Authorization":   `HMAC-SHA256 Credential=${ACCESS_KEY}/${credentialScope}, SignedHeaders=${signedHeaders}, Signature=${signature}`,
    },
    body,
  };
}

// ─── HTTP POST ────────────────────────────────────────────────────────────────

function httpPost(url, headers, body) {
  return new Promise((resolve, reject) => {
    const u = new URL(url);
    const req = https.request(
      {
        hostname: u.hostname,
        path: u.pathname + u.search,
        method: "POST",
        headers: { ...headers, "Content-Length": Buffer.byteLength(body) },
      },
      (res) => {
        let data = "";
        res.on("data", (c) => (data += c));
        res.on("end", () => resolve({ status: res.statusCode, body: data }));
      }
    );
    req.on("error", reject);
    req.write(body);
    req.end();
  });
}

// ─── 下载图片 ─────────────────────────────────────────────────────────────────

function downloadImage(url, savePath) {
  return new Promise((resolve, reject) => {
    const file = fs.createWriteStream(savePath);
    https.get(url, (res) => {
      if (res.statusCode === 301 || res.statusCode === 302) {
        file.close();
        return downloadImage(res.headers.location, savePath).then(resolve).catch(reject);
      }
      res.pipe(file);
      file.on("finish", () => { file.close(); resolve(); });
    }).on("error", (err) => { fs.unlink(savePath, () => {}); reject(err); });
  });
}

// ─── API：提交任务 ────────────────────────────────────────────────────────────

async function submitTask(params) {
  const { url, headers, body } = buildSignedRequest("CVSync2AsyncSubmitTask", params);
  const res = await httpPost(url, headers, body);

  if (res.status !== 200) {
    throw new Error(`HTTP ${res.status}: ${res.body}`);
  }

  const json = JSON.parse(res.body);
  if (json.code !== 10000) {
    throw new Error(`提交失败 [${json.code}]: ${json.message}  (request_id: ${json.request_id})`);
  }

  return json.data.task_id;
}

// ─── API：查询任务结果 ────────────────────────────────────────────────────────

async function queryTask(taskId) {
  const reqJson = JSON.stringify({ return_url: true, logo_info: { add_logo: false } });
  const { url, headers, body } = buildSignedRequest("CVSync2AsyncGetResult", {
    req_key: REQ_KEY,
    task_id: taskId,
    req_json: reqJson,
  });

  const res = await httpPost(url, headers, body);
  if (res.status !== 200) {
    throw new Error(`HTTP ${res.status}: ${res.body}`);
  }

  const json = JSON.parse(res.body);
  if (json.code !== 10000) {
    throw new Error(`查询失败 [${json.code}]: ${json.message}  (request_id: ${json.request_id})`);
  }

  return json.data; // { status, image_urls, binary_data_base64 }
}

// ─── 轮询等待完成 ─────────────────────────────────────────────────────────────

async function waitForResult(taskId) {
  const deadline = Date.now() + POLL_TIMEOUT_MS;
  let dots = 0;

  while (Date.now() < deadline) {
    const data = await queryTask(taskId);

    if (data.status === "done") {
      process.stdout.write("\n");
      if (!data.image_urls || data.image_urls.length === 0) {
        throw new Error("任务完成但未返回图片 URL，可能被内容审核拦截");
      }
      return data.image_urls;
    }

    if (data.status === "not_found") {
      throw new Error("任务未找到，可能已过期（12小时）");
    }
    if (data.status === "expired") {
      throw new Error("任务已过期，请重新提交");
    }

    // in_queue / generating → 继续等待
    dots = (dots + 1) % 4;
    process.stdout.write(`\r   等待生成中${".".repeat(dots + 1)}   `);
    await new Promise((r) => setTimeout(r, POLL_INTERVAL_MS));
  }

  throw new Error(`超时（${POLL_TIMEOUT_MS / 1000}s），任务 ID: ${taskId}`);
}

// ─── 字体设计模式提示词 ───────────────────────────────────────────────────────

function buildFontDesignPrompt(text, color, illustration) {
  return `字体设计："${text}"，黑色字体，斜体，带阴影。干净的背景，白色到${color}渐变。点缀浅灰色、半透明${illustration}等元素插图做配饰插画。`;
}

// ─── 主生成流程 ───────────────────────────────────────────────────────────────

async function generate(opts) {
  if (!ACCESS_KEY || !SECRET_KEY) {
    throw new Error(
      "未设置环境变量 JIMENG_ACCESS_KEY 或 JIMENG_SECRET_KEY\n" +
      "请先配置：setx JIMENG_ACCESS_KEY 你的Key  &&  setx JIMENG_SECRET_KEY 你的Key"
    );
  }

  // 构建提示词
  let prompt = opts.prompt;
  if (opts.text) {
    const color = opts.color || "蓝色";
    const illustration = opts.illustration || "几何图形, 线条";
    prompt = buildFontDesignPrompt(opts.text, color, illustration);
    console.log(`📝 字体设计模式，提示词:\n   ${prompt}\n`);
  }
  if (!prompt) throw new Error("请提供 --prompt 或 --text 参数");

  // 构建请求体
  const reqBody = { req_key: REQ_KEY, prompt };

  // 分辨率：优先 width/height，其次 ratio 预设，其次 size，默认 2K
  if (opts.width && opts.height) {
    reqBody.width  = parseInt(opts.width);
    reqBody.height = parseInt(opts.height);
  } else if (opts.ratio) {
    const preset = RATIO_PRESETS[opts.ratio];
    if (!preset) throw new Error(`不支持的比例: ${opts.ratio}，运行 ratios 查看可用选项`);
    reqBody.width  = preset.width;
    reqBody.height = preset.height;
  } else if (opts.size) {
    reqBody.size = parseInt(opts.size);
  }
  // 不传则默认 2K 自动比例

  // 图生图：输入图片
  if (opts["image-url"]) {
    reqBody.image_urls = opts["image-url"].split(",").map((s) => s.trim());
  }

  // 文本影响强度（图生图时有效）
  if (opts.scale !== undefined) {
    reqBody.scale = parseFloat(opts.scale);
  }

  // 强制单图（省钱省时）
  if (opts["force-single"]) {
    reqBody.force_single = true;
  }

  // 打印参数摘要
  const sizeDesc = reqBody.width
    ? `${reqBody.width}×${reqBody.height}`
    : reqBody.size
    ? `面积 ${reqBody.size}（AI 自动比例）`
    : "2K 自动比例";

  console.log(`🎨 即梦 AI 图片生成 4.0`);
  console.log(`   提示词: ${prompt.slice(0, 80)}${prompt.length > 80 ? "..." : ""}`);
  console.log(`   分辨率: ${sizeDesc}`);
  if (reqBody.image_urls) console.log(`   参考图: ${reqBody.image_urls.length} 张`);
  console.log();

  // 提交任务
  console.log("📤 提交任务...");
  const taskId = await submitTask(reqBody);
  console.log(`   task_id: ${taskId}`);

  // 轮询结果
  const imageUrls = await waitForResult(taskId);

  console.log(`\n✅ 生成成功！共 ${imageUrls.length} 张图片\n`);
  imageUrls.forEach((u, i) => console.log(`   图片 ${i + 1}: ${u}`));

  // 保存到本地
  if (opts.save) {
    const ext  = path.extname(opts.save) || ".png";
    const base = opts.save.replace(/\.[^.]+$/, "");
    console.log();
    for (let i = 0; i < imageUrls.length; i++) {
      const savePath = imageUrls.length === 1
        ? path.resolve(opts.save)
        : path.resolve(`${base}_${i + 1}${ext}`);
      process.stdout.write(`⬇️  下载图片 ${i + 1} → ${savePath} ...`);
      await downloadImage(imageUrls[i], savePath);
      process.stdout.write(" ✅\n");
    }
  }

  return imageUrls;
}

// ─── CLI 解析 ─────────────────────────────────────────────────────────────────

function parseArgs(argv) {
  const args = argv.slice(2);
  const cmd  = args[0];
  const opts = {};
  for (let i = 1; i < args.length; i++) {
    if (args[i].startsWith("--")) {
      const key = args[i].slice(2);
      const next = args[i + 1];
      opts[key] = next && !next.startsWith("--") ? args[++i] : true;
    }
  }
  return { cmd, opts };
}

// ─── 主程序 ───────────────────────────────────────────────────────────────────

async function main() {
  const { cmd, opts } = parseArgs(process.argv);

  if (!cmd || cmd === "help") {
    console.log(`
即梦 AI 图片生成工具 v2.0（基于图片生成 4.0 异步接口）

用法:
  node jimeng.mjs generate [选项]     生成图片
  node jimeng.mjs models              列出支持的模型
  node jimeng.mjs ratios              列出支持的比例预设

generate 选项:
  提示词（二选一）:
    --prompt <文字>          图片描述提示词（通用模式）
    --text <文字>            字体设计模式：图片上显示的文字
      --color <颜色>         字体设计模式：背景主色调（默认: 蓝色）
      --illustration <元素>  字体设计模式：配饰元素，逗号分隔（默认: 几何图形, 线条）

  分辨率（三选一，不传则默认 2K 自动比例）:
    --ratio <比例>           比例预设，如 16:9 / 4:3 / 1:1（见 ratios 命令）
    --width <宽> --height <高>  精确宽高（官方推荐值见 ratios 命令）
    --size <面积>            像素面积，如 4194304（2K）、16777216（4K）

  图生图:
    --image-url <URL>        参考图片 URL（多张用逗号分隔，最多 10 张）
    --scale <0~1>            文本影响强度（0=完全参考图，1=完全按提示词，默认 0.5）

  其他:
    --force-single           强制只生成 1 张（省钱省时）
    --save <路径>            保存图片到本地（多图自动加序号）

示例:
  # 文生图
  node jimeng.mjs generate --prompt "赛博朋克城市夜景，霓虹灯，雨天" --ratio 16:9

  # 4K 高清
  node jimeng.mjs generate --prompt "山水画，中国风" --ratio 16:9-4k --save ./output.png

  # 字体设计
  node jimeng.mjs generate --text "618大促" --color 橙色 --illustration "购物车,礼盒,星星" --ratio 4:3

  # 图生图（换背景）
  node jimeng.mjs generate --prompt "把背景换成星空" --image-url "https://..." --scale 0.7

  # 强制单图（快速/省钱）
  node jimeng.mjs generate --prompt "一只猫" --force-single --save ./cat.png
`);
    return;
  }

  if (cmd === "models") {
    console.log("\n当前使用模型: 即梦 AI 图片生成 4.0");
    console.log(`req_key: ${REQ_KEY}`);
    console.log("\n特性:");
    console.log("  • 文生图 + 图生图 + 多图组合编辑，统一接口");
    console.log("  • 最高 4K 分辨率输出");
    console.log("  • 最多输入 10 张参考图，最多输出 15 张图");
    console.log("  • 中文文字生成准确率显著提升");
    console.log("  • AI 自动推理最优比例和数量");
    return;
  }

  if (cmd === "ratios") {
    console.log("\n比例预设（--ratio 参数可用值）:\n");
    console.log("  预设名称      宽×高          说明");
    console.log("  ─────────────────────────────────────────");
    for (const [key, val] of Object.entries(RATIO_PRESETS)) {
      console.log(`  ${key.padEnd(12)}  ${String(val.width + "×" + val.height).padEnd(12)} ${val.label}`);
    }
    console.log("\n也可用 --width <宽> --height <高> 精确指定");
    console.log("或用 --size <面积> 让 AI 自动判断比例");
    console.log("  常用面积: 1048576(1K) / 4194304(2K) / 16777216(4K)");
    return;
  }

  if (cmd === "generate") {
    try {
      await generate(opts);
    } catch (err) {
      console.error(`\n❌ 错误: ${err.message}`);
      process.exit(1);
    }
    return;
  }

  console.error(`未知命令: ${cmd}，运行 node jimeng.mjs help 查看帮助`);
  process.exit(1);
}

main();
