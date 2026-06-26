/**
 * MCP Hello World Server
 * 最小可行 MCP 服务器 - 提供两个简单工具
 * 
 * 功能：
 * - add: 两数相加
 * - hello_world: 返回个性化问候语
 */

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

// 创建 MCP 服务器
const server = new McpServer({
  name: "hello-world",
  version: "1.0.0",
  description: "最小可行 MCP 服务器 - 用于 ClawHub Skill 演示"
});

// 工具 1: add - 两数相加
server.tool(
  "add",
  "两数相加工具 - 返回两个数字的和",
  {
    a: z.number().describe("第一个数字"),
    b: z.number().describe("第二个数字")
  },
  async ({ a, b }) => {
    const result = a + b;
    return {
      content: [
        {
          type: "text",
          text: `${a} + ${b} = ${result}`
        }
      ]
    };
  }
);

// 工具 2: hello_world - 返回个性化问候语
server.tool(
  "hello_world",
  "问候语工具 - 返回个性化的问候消息",
  {
    name: z.string().optional().default("朋友").describe("要问候的人名")
  },
  async ({ name }) => {
    const greetings = [
      `你好，${name}！👋 欢迎使用 MCP Hello World 服务器！`,
      `哈喽，${name}！🦞 今天过得怎么样？`,
      `嗨，${name}！✨ 很高兴见到你！`
    ];
    const greeting = greetings[Math.floor(Math.random() * greetings.length)];
    
    return {
      content: [
        {
          type: "text",
          text: greeting
        }
      ]
    };
  }
);

// 启动服务器
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("✅ MCP Hello World 服务器已启动");
  console.error("📦 可用工具：add, hello_world");
  console.error("🔌 传输方式：stdio");
}

main().catch((error) => {
  console.error("❌ 服务器启动失败:", error);
  process.exit(1);
});
