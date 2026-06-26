#!/usr/bin/env node
/**
 * Nano Banana 2 Pro 图片生成脚本
 * 支持文本生成图片、图片编辑、多模态对话
 * 
 * 用法:
 *   node nanobanana.js "生成一张红色的苹果"
 *   node nanobanana.js "编辑图片" --image input.jpg
 *   node nanobanana.js "回答问题" --text "What's in this image?" --image input.jpg
 */

import OpenAI from "openai";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// ============ 配置区 ============
const CONFIG = {
  baseURL: "https://claw.cjcook.site/v1",
  apiKey: "YOUR_API_KEY",
  model: "nanobanana-2pro",
  maxTokens: 4096,
  outputDir: path.join(__dirname, "output"),
};

// ============ 工具函数 ============
function ensureOutputDir() {
  if (!fs.existsSync(CONFIG.outputDir)) {
    fs.mkdirSync(CONFIG.outputDir, { recursive: true });
  }
}

function generateFilename(ext = "jpg") {
  const timestamp = Date.now();
  return path.join(CONFIG.outputDir, `nanobanana_${timestamp}.${ext}`);
}

function base64ToFile(base64String, filepath) {
  // 移除 data URI 前缀（如有）
  const data = base64String.replace(/^data:image\/\w+;base64,/, "");
  const buffer = Buffer.from(data, "base64");
  fs.writeFileSync(filepath, buffer);
  return filepath;
}

function fileToBase64(filepath) {
  const buffer = fs.readFileSync(filepath);
  const ext = path.extname(filepath).toLowerCase().slice(1);
  const mimeType = ext === "png" ? "image/png" : ext === "jpg" || ext === "jpeg" ? "image/jpeg" : "image/webp";
  return `data:${mimeType};base64,${buffer.toString("base64")}`;
}

// ============ 核心功能 ============
const client = new OpenAI({
  baseURL: CONFIG.baseURL,
  apiKey: CONFIG.apiKey,
});

/**
 * 生成图片
 * @param {string} prompt 文本提示
 * @param {string|null} inputImage 本地图片路径（可选，用于图片编辑）
 * @param {object} options 可选参数
 * @returns {Promise<{text: string|null, images: string[]}>}
 */
async function generateImage(prompt, inputImage = null, options = {}) {
  const contents = [];

  // 如果有输入图片，放在前面
  if (inputImage) {
    if (!fs.existsSync(inputImage)) {
      throw new Error(`输入图片不存在: ${inputImage}`);
    }
    contents.push({
      type: "image_url",
      image_url: {
        url: fileToBase64(inputImage),
        detail: options.imageDetail || "auto",
      },
    });
  }

  // 添加文本提示
  contents.push({
    type: "text",
    text: prompt,
  });

  const messages = [
    {
      role: "user",
      content: contents,
    },
  ];

  console.log("📤 发送请求...");
  console.log(`   提示词: ${prompt}`);
  if (inputImage) {
    console.log(`   输入图片: ${inputImage}`);
  }

  const response = await client.chat.completions.create({
    model: CONFIG.model,
    messages: messages,
    max_tokens: options.maxTokens || CONFIG.maxTokens,
    ...options,
  });

  const message = response.choices[0].message;
  const result = {
    text: message.content || null,
    images: [],
  };

  // 提取图片
  if (message.images && message.images.length > 0) {
    ensureOutputDir();
    for (const img of message.images) {
      const filename = generateFilename("jpg");
      base64ToFile(img.image_url.url, filename);
      result.images.push(filename);
      console.log(`🖼️  图片已保存: ${filename}`);
    }
  }

  // 打印文本回复
  if (result.text) {
    console.log(`📝 回复: ${result.text}`);
  }

  return result;
}

/**
 * 简单的纯文本对话（不带图片）
 */
async function chat(text) {
  console.log("📤 发送请求...");

  const response = await client.chat.completions.create({
    model: CONFIG.model,
    messages: [{ role: "user", content: text }],
    max_tokens: CONFIG.maxTokens,
  });

  const reply = response.choices[0].message.content;
  console.log(`📝 回复: ${reply}`);
  return reply;
}

// ============ CLI 入口 ============
async function main() {
  const args = process.argv.slice(2);

  if (args.length === 0) {
    console.log(`
Nano Banana 2 Pro 图片生成工具
================================

用法:
  node nanobanana.js "提示词"                    # 文本生成图片
  node nanobanana.js "提示词" --image xxx.jpg    # 图片编辑
  node nanobanana.js "提示词" --text "问题"       # 纯文本对话
  node nanobanana.js --help                      # 显示帮助

示例:
  node nanobanana.js "一只可爱的猫咪在草地上玩耍"
  node nanobanana.js "把这只猫变成机器人" --image cat.jpg
`);
    return;
  }

  // 解析参数
  let prompt = null;
  let inputImage = null;
  let textOnly = false;

  for (let i = 0; i < args.length; i++) {
    if (args[i] === "--image" && args[i + 1]) {
      inputImage = args[++i];
    } else if (args[i] === "--text" && args[i + 1]) {
      textOnly = true;
      prompt = args[++i];
    } else if (!args[i].startsWith("--")) {
      prompt = args[i];
    }
  }

  if (!prompt) {
    console.error("❌ 请提供提示词");
    process.exit(1);
  }

  try {
    if (textOnly || (!inputImage && !prompt.includes("图"))) {
      // 纯文本对话
      await chat(prompt);
    } else {
      // 图片生成/编辑
      await generateImage(prompt, inputImage);
    }
    console.log("✅ 完成!");
  } catch (error) {
    console.error("❌ 错误:", error.message);
    if (error.message.includes("401")) {
      console.error("   API Key 无效或已过期");
    } else if (error.message.includes("429")) {
      console.error("   请求频率超限，请稍后重试");
    }
    process.exit(1);
  }
}

main();
