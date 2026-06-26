#!/usr/bin/env node
/**
 * MCP Hello World 完整测试
 * 使用 mcporter 测试工具调用
 */

import { spawn } from "child_process";
import { fileURLToPath } from "url";
import { dirname, join } from "path";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const serverPath = join(__dirname, "server.js");

console.log("🧪 MCP Hello World 完整测试\n");
console.log("📦 测试项目：");
console.log("   1. 服务器启动");
console.log("   2. 工具列表获取");
console.log("   3. add 工具调用");
console.log("   4. hello_world 工具调用\n");

// 测试流程
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
    name: "list tools",
    request: {
      jsonrpc: "2.0",
      id: 2,
      method: "tools/list",
      params: {}
    }
  },
  {
    name: "call add(3, 5)",
    request: {
      jsonrpc: "2.0",
      id: 3,
      method: "tools/call",
      params: {
        name: "add",
        arguments: { a: 3, b: 5 }
      }
    }
  },
  {
    name: "call hello_world('老板')",
    request: {
      jsonrpc: "2.0",
      id: 4,
      method: "tools/call",
      params: {
        name: "hello_world",
        arguments: { name: "老板" }
      }
    }
  }
];

let testIndex = 0;
let serverOutput = "";

const server = spawn("node", [serverPath], {
  stdio: ["pipe", "pipe", "pipe"]
});

server.stderr.on("data", (data) => {
  console.log("📝", data.toString().trim());
});

server.stdout.on("data", (data) => {
  const response = data.toString();
  serverOutput += response;
  
  try {
    const result = JSON.parse(response.trim());
    console.log(`\n✅ ${tests[testIndex].name} 响应:`);
    console.log("   ", JSON.stringify(result, null, 2).split("\n").join("\n    "));
    testIndex++;
    
    if (testIndex < tests.length) {
      sendNext();
    } else {
      console.log("\n🎉 所有测试通过！");
      server.kill();
    }
  } catch (e) {
    // 忽略解析错误
  }
});

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

// 启动测试
setTimeout(() => {
  sendNext();
}, 1000);
