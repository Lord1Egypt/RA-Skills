# Ningyao Voice Launcher

一个可本地运行的宁姚语音启动器包：浏览器语音对话、宁姚人格预设、屏幕感知、安全终端，以及适合 Windows 的一键启动脚本。

## 这是什么

这个仓库同时包含两部分：

- `SKILL.md`：可发布到 ClawHub 的技能描述，方便代理识别和安装
- `assets/voice-chat-local/`：真正的本地启动器模板

目标很直接：把“宁姚”的说话方式和一个能马上跑起来的本地语音界面打包在一起，别人拉下来后，不必自己从零拼装。

## 功能

- 浏览器麦克风语音输入
- 浏览器直接朗读回复
- 宁姚风格中文系统提示词
- 屏幕共享后自动做简短画面摘要
- 受限白名单终端
- Windows 一键启动脚本

## 目录

- `SKILL.md`：ClawHub 技能入口
- `scripts/install-launcher.ps1`：把启动器复制到目标目录的安装脚本
- `assets/voice-chat-local/`：启动器模板源码

## 快速开始

### 方式一：直接使用仓库里的启动器模板

```powershell
cd assets/voice-chat-local
npm install
Copy-Item .env.example .env
notepad .env
node --env-file=.env server.js
```

然后打开 `http://localhost:3030`。

### 方式二：用安装脚本复制到你自己的目录

```powershell
powershell -ExecutionPolicy Bypass -File scripts/install-launcher.ps1 -Destination "$env:USERPROFILE\Desktop\ningyao-voice-chat" -InstallDeps
```

复制完成后：

```powershell
cd "$env:USERPROFILE\Desktop\ningyao-voice-chat"
Copy-Item .env.example .env
notepad .env
.\start-voice-chat.cmd
```

## 环境变量

在 `.env` 中配置：

- `OPENAI_API_KEY`：必填
- `OPENAI_BASE_URL`：可选，兼容 OpenAI API 的网关地址
- `OPENAI_MODEL`：默认模型；如果要用屏幕感知，建议填支持图像输入的模型
- `OPENAI_TIMEOUT_MS`：请求超时
- `PORT`：本地端口，默认 `3030`
- `SYSTEM_PROMPT`：宁姚的人格提示词

## 适用场景

- 想要一个本地运行、低门槛的中文语音聊天界面
- 想把“宁姚”这个人格预设连同启动器一起分发
- 想给 OpenClaw / 其他代理生态做一个可安装的语音前端模板

## 发布

### 发布到 GitHub

这是一个普通仓库，直接推送即可。

### 发布到 ClawHub

在仓库根目录执行：

```powershell
cmd /c clawhub publish . --slug ningyao-voice-launcher --name "Ningyao Voice Launcher" --version 0.1.0 --changelog "Initial public release"
```

发布前需要先登录：

```powershell
cmd /c clawhub login
cmd /c clawhub whoami
```

## 注意

- 推荐使用 Chrome 或 Edge
- `assets/voice-chat-local/.env` 不应提交
- 终端功能是刻意收紧的，不是通用 shell
- 如果网络到模型服务不通，聊天与屏幕识别都会失败

## License

MIT
