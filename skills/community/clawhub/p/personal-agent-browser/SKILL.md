---
name: openclaw-agent-browser
description: >
  一个为你的个人数字大脑设计的浏览器自动化技能。它调用你本地安装的 agent-browser CLI，安全地访问网页，提取标题和内容，并返回结构化摘要，让 AI 助手能理解并总结网页信息。

  **使用场景**：
  (1) 用户要求：“帮我查看一下我的技能在 ClawHub 上的页面”
  (2) 用户希望 AI 自动抓取网页并总结内容
  (3) 需要一个完全可控、无外部依赖的浏览器工具

  **核心功能**：
  - 调用本地 agent-browser CLI 访问任意 URL
  - 提取页面标题和 Markdown 格式内容
  - 返回结构化 JSON，供 AI 助手解析和总结

  **系统依赖**：
  - 必须安装 agent-browser CLI：npm install -g agent-browser
  - 必须安装 Node.js 环境
  - 必须确保 /home/awu/.npm-global/bin/agent-browser 可执行

  **重要**：此技能完全本地化，不依赖任何外部 API。所有数据仅在你本地机器上处理，安全可靠。你的浏览器行为完全由你控制。
---
# OpenClaw Agent Browser
## 概述
这是一个为 OpenClaw 个人数字大脑打造的轻量级浏览器技能。它不使用复杂的 AI 模型来“理解”网页，而是**直接调用你本地安装的 agent-browser 工具**，以最可靠、最透明的方式获取网页内容。
## 工作原理
1. **触发**：当你向 AI 助手提问，例如：“帮我看看 https://clawhub.ai/awublack/awublack-personal-memory-system 的内容”，AI 会调用此技能。
2. **执行**：`run_browser.js` 脚本被启动，接收 URL 参数。
3. **调用 CLI**：脚本通过 `child_process.exec` 调用系统上的 `agent-browser --url="..." --output=markdown` 命令。
4. **提取**：脚本解析 `agent-browser` 返回的 Markdown 输出，提取出页面标题和正文内容。
5. **输出**：脚本以 JSON 格式输出结构化数据，包含 `title`、`content` 和 `summary`。
6. **总结**：AI 助手接收此 JSON，将其内容整合到你的对话上下文中，为你生成自然语言的总结。
## 系统组件
- `run_browser.js`：核心 Node.js 脚本，负责调用 CLI 并解析输出。
- `agent-browser`：本地安装的命令行工具（通过 `npm install -g agent-browser`）。
## 安装与使用
1. **安装依赖**：在你的终端中运行：
   ```bash
   npm install -g agent-browser
   ```

2. **安装技能**：将此技能包放入 OpenClaw 的 `skills` 目录，或通过 `clawhub install openclaw-agent-browser` 安装。

3. **使用**：直接向 AI 助手提问，例如：
   > “请帮我查看 https://clawhub.ai/awublack/awublack-personal-memory-system 的内容”

   AI 将自动调用此技能，访问网页，提取信息，并为你总结。

## 安全与隐私
- **完全本地化**：所有操作都在你的本地机器上进行，不向任何服务器发送数据。
- **透明可控**：你完全知道 AI 在做什么——它只是在调用一个你安装的命令行工具。
- **无外部依赖**：不依赖任何云服务、API 密钥或第三方平台。
- **可审计**：你可以随时检查 `run_browser.js` 的源代码，确认其行为。

## 未来扩展
- 支持截图功能（`--screenshot`）
- 支持表单填写和点击按钮
- 与 `query_memory.py` 集成，将网页内容自动存入你的长期记忆

> **“真正的智能，不是模仿人类，而是扩展人类的能力。”**
> —— 你的数字大脑
---