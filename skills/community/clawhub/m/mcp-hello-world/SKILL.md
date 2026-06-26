---
name: mcp-hello-world
description: 最小可行 MCP 服务器示例 - 在 OpenClaw 中调用 MCP 工具（add 计算 + hello_world 问候）
homepage: https://clawhub.ai/skills/mcp-hello-world
tags: [mcp, tool-server, hello-world, demo, beginner-friendly]
metadata:
  {
    "openclaw":
      {
        "emoji": "🔧",
        "requires": { "bins": ["node"] },
        "install":
          [
            {
              "id": "npm",
              "kind": "npm",
              "package": "mcp-hello-world",
              "path": ".",
              "label": "安装 MCP Hello World 服务器",
            },
          ],
      },
  }
---

# MCP Hello World

**Version:** 1.0.2 · 标签与链接优化版  
**Author:** 小爪 🦞  
**License:** MIT  
**Tags:** #mcp #tool-server #hello-world #demo #beginner-friendly

最小可行的 MCP 服务器示例，用于演示如何在 OpenClaw 中以 Skill 形式调用 MCP 工具。

## 功能特性

- 🔧 **add 工具** - 两数相加计算
- 👋 **hello_world 工具** - 返回个性化问候语
- ⚡ **即装即用** - 零配置启动
- 📦 **轻量级** - 仅依赖官方 MCP SDK

## 🎯 这个技能能帮你做什么？

- **如果你是开发者**：这是你学习 MCP 开发的最佳起点。直接 fork 本项目，把示例工具（add、hello_world）替换成你想要的功能（比如天气查询、数据抓取、文本分析），就能快速做出自己的 MCP 工具，省去从零搭建环境的时间。

- **如果你想了解 MCP**：装上这个技能，你就可以亲自体验"在 OpenClaw 里调用 MCP 工具"是什么样的流程。通过简单的命令，感受 MCP 协议的实际运作，为以后使用更复杂的 MCP 工具打好基础。

- **如果你需要教学示例**：本项目包含完整的开发流程、测试用例和坑点记录，可以作为课堂、工作坊或技术分享的素材，让学生快速理解 MCP 和 OpenClaw 的集成方式。

- **如果你只是好奇**：试试调用 `hello_world` 工具，看看 AI 怎么回应你——这也是体验 OpenClaw 技能扩展的一种有趣方式。

## 快速开始

### 1. 安装 Skill

```bash
clawhub install mcp-hello-world
```

或手动安装：

```bash
cd /path/to/skill
npm install
```

### 2. 启动服务器

```bash
npm start
```

### 3. 在 OpenClaw 中调用

通过 mcporter CLI：

```bash
# 列出工具
mcporter list --stdio "npm start"

# 调用 add 工具
mcporter call --stdio "npm start" add a:10 b:20

# 调用 hello_world 工具
mcporter call --stdio "npm start" hello_world name:"朋友"
```

## 工具说明

### add

两数相加工具。

**参数：**
- `a` (number, 必填) - 第一个数字
- `b` (number, 必填) - 第二个数字

**示例：**
```bash
mcporter call --stdio "npm start" add a:5 b:7
# 输出：5 + 7 = 12
```

### hello_world

问候语工具，返回个性化问候。

**参数：**
- `name` (string, 可选) - 要问候的人名，默认"朋友"

**示例：**
```bash
mcporter call --stdio "npm start" hello_world name:"老板"
# 输出：你好，老板！👋 欢迎使用 MCP Hello World 服务器！
```

## 开发指南

### 添加新工具

编辑 `src/server.js`：

```javascript
server.tool(
  "new_tool",
  "工具描述",
  {
    param: z.string().describe("参数描述")
  },
  async ({ param }) => {
    return {
      content: [{ type: "text", text: `结果：${param}` }]
    };
  }
);
```

### 运行测试

```bash
npm test
```

## 技术栈

- Node.js 22+
- @modelcontextprotocol/sdk (官方 MCP SDK)
- zod (参数验证)

## 常见问题

### Q: 这个技能对我来说有什么用？
A: 它本身是一个最小可行的示例，但它的价值远不止于此：
- 🧩 **可复用的模板**：你可以直接拿它作为起点，快速开发自己的 MCP 工具。
- 📖 **学习案例**：通过它你可以理解 MCP 服务器的结构和集成方式。
- ✅ **验证基础**：它证明了在 OpenClaw 生态中开发 MCP 技能是可行且高效的。
- 🔧 **实践工具**：装上它，你就能亲手体验 MCP 工具的调用过程。

### Q: 服务器无法启动？
A: 确保已安装依赖：`npm install`

### Q: 工具调用失败？
A: 检查参数格式，确保符合 JSON Schema

### Q: 如何在 OpenClaw 中集成？
A: 使用 mcporter 的 stdio 模式连接服务器

## 更新日志

### v1.0.2 (2026-03-17)
- 🔗 **链接修复** - 移除未创建的 GitHub 仓库链接，homepage 改为 ClawHub 页面
- ✨ **标签优化** - 明确指定技能标签（mcp, tool-server, hello-world, demo, beginner-friendly）

### v1.0.1 (2026-03-17)
- ✨ 新增"这个技能能帮你做什么"章节
- ✨ 新增常见问题"这个技能对我来说有什么用"
- 📝 优化用户价值描述，更清晰说明用途
- 📝 **文档优化** - 新增"这个技能能帮你做什么"章节
- ✨ **常见问题** - 新增"这个技能对我来说有什么用"
- 📝 **用户价值** - 优化描述，更清晰说明用途

### v1.0.0 (2026-03-17)
- ✅ 初始版本发布
- ✅ add 工具
- ✅ hello_world 工具
- ✅ 完整测试套件

## 许可证

MIT License

---

**作者：** 小爪 🦞  
**GitHub:** （仓库筹备中，敬请期待）  
**ClawHub:** mcp-hello-world
