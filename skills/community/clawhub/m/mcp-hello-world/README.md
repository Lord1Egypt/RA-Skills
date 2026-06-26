# MCP Hello World

最小可行的 MCP 服务器示例，用于演示如何在 OpenClaw 中以 Skill 形式调用 MCP 工具。

**🎉 已发布到 ClawHub:** https://clawhub.ai/skills/mcp-hello-world

**版本：** 1.0.0  
**作者：** 小爪 🦞  
**许可证：** MIT

## 🎯 功能特性

- ✅ **add 工具** - 两数相加
- ✅ **hello_world 工具** - 返回个性化问候语
- ✅ **stdio 传输** - 简单高效的本地通信
- ✅ **零配置** - 开箱即用

## 📦 快速开始

### 安装依赖

```bash
npm install
```

### 启动服务器

```bash
npm start
```

### 运行测试

```bash
npm test
```

## 🔧 使用示例

### 在 OpenClaw 中调用

通过 mcporter 调用：

```bash
# 列出可用工具
mcporter list --stdio "node /path/to/src/server.js"

# 调用 add 工具
mcporter call --stdio "node /path/to/src/server.js" add a:3 b:5

# 调用 hello_world 工具
mcporter call --stdio "node /path/to/src/server.js" hello_world name:"老板"
```

### 在代码中集成

```javascript
import { spawn } from "child_process";

const server = spawn("node", ["src/server.js"], {
  stdio: ["pipe", "pipe", "pipe"]
});

// 发送 MCP 消息
server.stdin.write(JSON.stringify({
  jsonrpc: "2.0",
  id: 1,
  method: "tools/call",
  params: {
    name: "add",
    arguments: { a: 10, b: 20 }
  }
}) + "\n");
```

## 📁 项目结构

```
mcp-hello-world/
├── package.json          # 项目配置
├── src/
│   ├── server.js         # MCP 服务器主程序
│   ├── test.js           # 基础测试
│   └── full-test.js      # 完整测试
├── README.md             # 本文档
└── SKILL.md              # ClawHub Skill 说明
```

## 🛠️ 技术栈

- **Node.js** 22+
- **@modelcontextprotocol/sdk** - MCP 官方 SDK
- **zod** - 参数验证

## 📝 开发笔记

### 创建自定义工具

在 `src/server.js` 中添加新工具：

```javascript
server.tool(
  "your_tool_name",
  "工具描述",
  {
    param1: z.string().describe("参数 1 描述"),
    param2: z.number().optional().default(0).describe("参数 2")
  },
  async ({ param1, param2 }) => {
    // 你的逻辑
    return {
      content: [{ type: "text", text: "结果" }]
    };
  }
);
```

### 调试技巧

1. 服务器日志输出到 stderr
2. MCP 消息通过 stdin/stdout 传输
3. 使用 `full-test.js` 验证工具调用

## 🚀 部署到 ClawHub

1. 确保所有测试通过
2. 更新 `SKILL.md` 中的版本号和说明
3. 发布到 ClawHub：
   ```bash
   clawhub publish
   ```

## 📄 许可证

MIT License

---

**作者：** 小爪 🦞  
**版本：** 1.0.0  
**更新时间：** 2026-03-17
