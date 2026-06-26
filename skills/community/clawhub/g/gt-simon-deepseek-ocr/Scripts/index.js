#!/usr/bin/env node

import fs from "fs";
import path from "path";
import process from "process";
import http from "http";

/**
 * 极简参数解析
 */
function getArg(name) {
  const idx = process.argv.indexOf(`--${name}`);
  if (idx !== -1 && idx + 1 < process.argv.length) {
    return process.argv[idx + 1];
  }
  return null;
}

const imagePath = getArg("image");

if (!imagePath) {
  console.error("Missing required argument: --image <path>");
  process.exit(1);
}

const absolutePath = path.resolve(imagePath);

if (!fs.existsSync(absolutePath)) {
  console.error(`Image file not found: ${absolutePath}`);
  process.exit(1);
}

/**
 * DeepSeek‑OCR 服务地址
 * ✅ 可通过环境变量覆盖
 */
const OCR_HOST = process.env.DEEPSEEK_OCR_HOST || "127.0.0.1";
const OCR_PORT = process.env.DEEPSEEK_OCR_PORT || 8001;

const payload = JSON.stringify({
  image: absolutePath
});

const options = {
  hostname: OCR_HOST,
  port: OCR_PORT,
  path: "/ocr",
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "Content-Length": Buffer.byteLength(payload)
  },
  timeout: 120000
};

const req = http.request(options, (res) => {
  let data = "";

  res.on("data", (chunk) => {
    data += chunk;
  });

  res.on("end", () => {
    try {
      const result = JSON.parse(data);

      // ✅ 标准化输出（Agent 友好）
      const output = {
        text: result.text || "",
        confidence: result.confidence ?? null,
        model: "deepseek-ocr"
      };

      console.log(JSON.stringify(output, null, 2));
    } catch (err) {
      console.error("Invalid OCR response:", data);
      process.exit(2);
    }
  });
});

req.on("error", (err) => {
  console.error("Failed to call DeepSeek OCR service:", err.message);
  process.exit(3);
});

req.write(payload);
req.end();