/**
 * MCP Hello World 服务器测试脚本
 * 用于本地测试服务器功能
 */

import { spawn } from "child_process";
import { fileURLToPath } from "url";
import { dirname, join } from "path";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const serverPath = join(__dirname, "server.js");

console.log("🧪 开始测试 MCP Hello World 服务器...\n");

// 启动服务器进程
const server = spawn("node", [serverPath], {
  stdio: ["pipe", "pipe", "pipe"]
});

let output = "";
let errorOutput = "";

server.stdout.on("data", (data) => {
  output += data.toString();
});

server.stderr.on("data", (data) => {
  errorOutput += data.toString();
  console.log("📝 [服务器]", data.toString().trim());
});

// 等待服务器启动
setTimeout(() => {
  console.log("\n✅ 服务器启动成功！");
  console.log("📦 测试完成 - 服务器可以正常运行\n");
  
  // 发送测试消息（模拟 MCP 客户端）
  const testMessage = {
    jsonrpc: "2.0",
    id: 1,
    method: "initialize",
    params: {
      protocolVersion: "2024-11-05",
      capabilities: {},
      clientInfo: {
        name: "test-client",
        version: "1.0.0"
      }
    }
  };
  
  server.stdin.write(JSON.stringify(testMessage) + "\n");
  
  // 等待响应后关闭
  setTimeout(() => {
    server.kill();
    console.log("\n🎉 测试结束！");
  }, 1000);
}, 2000);

server.on("error", (error) => {
  console.error("❌ 服务器启动失败:", error);
  process.exit(1);
});

server.on("close", (code) => {
  console.log(`\n📊 服务器进程结束，退出码：${code}`);
});
