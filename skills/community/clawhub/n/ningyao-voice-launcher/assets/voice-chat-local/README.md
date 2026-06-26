# voice-chat-local

本地浏览器语音对话小工具。

## 功能

- 浏览器麦克风语音输入
- 调用 OpenAI 文本模型生成回复
- 浏览器直接朗读回复
- 说话时支持更自然的停顿结束
- 朗读中可以直接按住说话打断
- 本地运行，不走电话线路

## 准备

1. 进入目录：`cd voice-chat-local`
2. 安装依赖：`cmd /c npm install`
3. 复制配置：`copy .env.example .env`
4. 编辑 `.env`，填入 `OPENAI_API_KEY`
5. 启动：`node --env-file=.env server.js`
6. 打开：`http://localhost:3030`

也可以直接双击：
- `voice-chat-local/start-voice-chat.cmd`：前台启动，窗口会保留
- `voice-chat-local/start-voice-chat-bg.cmd`：后台最小化启动，并自动打开页面

## 说明

- 语音识别和语音朗读依赖浏览器，推荐 Chrome 或 Edge。
- 如果想换模型，改 `.env` 里的 `OPENAI_MODEL`。
- 如果想改说话风格，改 `.env` 里的 `SYSTEM_PROMPT`。
