import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { CallToolRequestSchema, ListToolsRequestSchema } from "@modelcontextprotocol/sdk/types.js";
import { execSync } from "child_process";

const server = new Server({ name: "playwright-scraper", version: "1.0.0" }, { capabilities: { tools: {} } });

// 1. 告诉 AI 这个工具有什么功能
server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [{
    name: "stealth_scrape",
    description: "使用 Playwright 隐身模式抓取受保护或动态网页内容",
    inputSchema: {
      type: "object",
      properties: {
        url: { type: "string", description: "目标网页 URL" }
      },
      required: ["url"]
    }
  }]
}));

// 2. 定义执行逻辑：调用你的 scripts/playwright-stealth.js
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (request.params.name === "stealth_scrape") {
    const url = request.params.arguments.url;
    try {
      // 执行你的脚本并获取输出
      const stdout = execSync(`node scripts/playwright-stealth.js "${url}"`, { encoding: 'utf8' });
      return { content: [{ type: "text", text: stdout }] };
    } catch (error) {
      return { content: [{ type: "text", text: `抓取失败: ${error.message}` }], isError: true };
    }
  }
});

const transport = new StdioServerTransport();
await server.connect(transport);