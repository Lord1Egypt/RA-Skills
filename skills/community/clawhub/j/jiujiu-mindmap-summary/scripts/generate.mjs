#!/usr/bin/env node

function usage() {
  console.error(`Usage: generate.mjs "query" [--input "your text here"]`);
  process.exit(2);
}

const args = process.argv.slice(2);
if (args.length === 0 || args[0] === "-h" || args[0] === "--help") usage();

// 1. 解析参数
let textInput = args[0]; // 默认取第一个参数作为内容

for (let i = 0; i < args.length; i++) {
  const a = args[i];
  if (a === "--input") {
    textInput = args[i + 1] ?? "";
    i++;
    continue;
  }
}

if (!textInput) {
  console.error("请输入需要总结的文本！");
  usage();
}

// 2. 获取本机的 API KEY 环境变量
const apiKey = (process.env.JIUJIUMINDMAP_API_KEY ?? "").trim();
if (!apiKey) {
  console.error("Missing JIUJIUMINDMAP_API_KEY. 请配置环境变量。");
  process.exit(1);
}

// 3. 准备向你的服务器发起请求
// 【注意】把这里的 URL 替换成你第二步部署后得到的真实域名
const API_URL = "http://127.0.0.1:8000/generate"; 

const body = {
  text: textInput
};

// 4. 发起网络请求
const resp = await fetch(API_URL, {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "x-api-key": apiKey // 将 API KEY 放在请求头中传递给你的服务器鉴权
  },
  body: JSON.stringify(body),
});

// 5. 处理结果
if (!resp.ok) {
  const errText = await resp.text().catch(() => "");
  throw new Error(`思维导图生成失败 (${resp.status}): ${errText}`);
}

const data = await resp.json();

// 6. 打印输出给 AI 或用户
console.log("## 生成的思维导图 JSON\n");
// 假设你的服务器返回的数据在 data.data 里
console.log(JSON.stringify(data.data, null, 2));
console.log("\n---\n");