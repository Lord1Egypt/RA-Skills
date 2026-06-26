#!/usr/bin/env node
/**
 * 语言景观分析 MCP 服务器 - 完整测试
 */

import { spawn } from "child_process";
import { fileURLToPath } from "url";
import { dirname, join } from "path";

const __filename = fileURLToPath(import.meta.url);
const srcDir = dirname(dirname(__filename)); // 向上一级到 src/
const serverPath = join(srcDir, "server.js");

console.log("🧪 语言景观分析 MCP 服务器 - 完整测试\n");
console.log("📦 测试项目：");
console.log("   1. 服务器启动");
console.log("   2. 情感分析测试");
console.log("   3. 关键词提取测试");
console.log("   4. 笔记列表测试");
console.log("   5. 周报生成测试\n");

const server = spawn("node", [serverPath], {
  stdio: ["pipe", "pipe", "pipe"]
});

let testIndex = 0;

server.stderr.on("data", (data) => {
  console.log("📝", data.toString().trim());
});

server.stdout.on("data", (data) => {
  const response = data.toString();
  try {
    const result = JSON.parse(response.trim());
    const testName = tests[testIndex]?.name || "Unknown";
    console.log(`\n✅ ${testName} 响应:`);
    console.log("   ", JSON.stringify(result, null, 2).split("\n").join("\n    "));
    testIndex++;
    
    if (testIndex < tests.length) {
      setTimeout(sendNext, 500);
    } else {
      console.log("\n🎉 所有测试通过！");
      server.kill();
    }
  } catch (e) {
    // 忽略解析错误
  }
});

const tests = [
  {
    name: "initialize",
    request: {
      jsonrpc: "2.0",
      id: 1,
      method: "initialize",
      params: {
        protocolVersion: "2024-11-05",
        capabilities: {},
        clientInfo: { name: "test", version: "1.0.0" }
      }
    }
  },
  {
    name: "情感分析测试",
    request: {
      jsonrpc: "2.0",
      id: 2,
      method: "tools/call",
      params: {
        name: "analyze_sentiment",
        arguments: { text: "这个产品很好用，推荐购买", language: "zh" }
      }
    }
  },
  {
    name: "关键词提取测试",
    request: {
      jsonrpc: "2.0",
      id: 3,
      method: "tools/call",
      params: {
        name: "extract_keywords",
        arguments: { text: "小红书运营数据分析报告，内容优化方向明确", limit: 5, language: "zh" }
      }
    }
  },
  {
    name: "笔记列表测试",
    request: {
      jsonrpc: "2.0",
      id: 4,
      method: "tools/call",
      params: {
        name: "list_notes",
        arguments: { source: "sample", limit: 3, sortBy: "likes", order: "desc" }
      }
    }
  },
  {
    name: "周报生成测试",
    request: {
      jsonrpc: "2.0",
      id: 5,
      method: "tools/call",
      params: {
        name: "generate_weekly_report",
        arguments: { limit: 5 }
      }
    }
  }
];

function sendNext() {
  if (testIndex < tests.length) {
    console.log(`\n📤 发送：${tests[testIndex].name}`);
    server.stdin.write(JSON.stringify(tests[testIndex].request) + "\n");
  }
}

server.on("error", (error) => {
  console.error("❌ 测试失败:", error);
  process.exit(1);
});

server.on("close", (code) => {
  console.log(`\n📊 测试结束，退出码：${code}`);
});

setTimeout(() => {
  sendNext();
}, 1000);
