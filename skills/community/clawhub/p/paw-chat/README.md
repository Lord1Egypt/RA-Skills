# 🐾 Paw - OpenClaw Web Chat

<p align="center">
  <img src="https://img.shields.io/badge/OpenClaw-Paw-blue?style=for-the-badge" alt="OpenClaw Paw">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/Zero-Dependencies-orange?style=flat-square" alt="Zero Dependencies">
</p>

> 🌍 English documentation available at [README_EN.md](./README_EN.md)

Paw 是专为 [OpenClaw](https://github.com/openclaw/openclaw) 打造的 Web Chat 前端。一个网址就能打开的优雅聊天界面。

![Paw Screenshot](./screenshot.png)

## ✨ 特性

- 🌐 **Web 端聊天** - 浏览器直接打开，无需安装任何软件
- 📱 **响应式设计** - 电脑手机都能用
- 🔌 **WebSocket 直连** - 实时消息推送，支持流式输出
- 💾 **会话管理** - 支持多会话切换，会话历史自动保存
- 🎨 **代码高亮** - 内置 Markdown 和代码语法高亮
- 🔒 **本地存储** - 认证信息保存在浏览器，安全可靠
- ⚡ **零依赖** - 纯静态文件，无需构建工具，无需后端服务

## 🚀 快速开始

### 安装

```bash
# 全局安装 (推荐)
npm install -g @openclaw/paw

# 或使用 npx 免安装运行
npx @openclaw/paw start
```

### 一键启动

```bash
# 安装后直接使用 paw 命令
paw start

# 或者手动启动
cd paw
python3 -m http.server 8080
```

然后浏览器打开 http://localhost:8080

### 首次配置

1. 点击右上角 ⚙️ **Settings** 设置
2. 填写以下信息：
   - **Gateway URL**: `ws://localhost:18789` (本机) 或 `wss://你的IP:18789` (远程)
   - **Token**: 你的 OpenClaw Gateway 令牌
3. 点击 **Connect** 连接

### 查找 Gateway 信息

```bash
# 查看 Gateway 状态和地址
openclaw status

# 查看认证令牌
openclaw config get gateway.auth.token
```

> ⚠️ 首次从新设备连接可能需要审批：`openclaw devices approve <设备ID>`

## 📖 使用方法

### 基本操作

| 操作 | 说明 |
|------|------|
| 发送消息 | 在输入框输入，回车或点击发送按钮 |
| 停止生成 | 点击停止按钮中断 AI 回复 |
| 新建会话 | 点击会话列表，选择"新建会话" |
| 切换会话 | 点击顶部会话名称切换 |
| 上传文件 | 点击附件按钮上传文件 |

### 快捷键

- `Ctrl + Enter` - 发送消息
- `Ctrl + Shift + R` - 重新连接

## 🛠️ 高级用法

### 部署到 Gateway

一键部署到你的 OpenClaw Gateway：

```bash
paw install
```

或者手动部署：

```bash
# 复制文件到 Gateway UI 目录
UIROOT="$(openclaw config get gateway.controlUi.root 2>/dev/null || echo ~/.openclaw/control-ui-static)"
cp index.html "$UIROOT/paw.html"
cp paw-app.js marked.min.js highlight.min.js github-dark.min.css "$UIROOT/"
```

然后访问 `https://<gateway-host>:<port>/paw.html`

### Docker 运行

```bash
docker run -d -p 8080:80 \
  -v $(pwd):/usr/share/nginx/html:ro \
  nginx:alpine
```

## 📁 项目结构

```
paw/
├── index.html          # 主页面
├── paw-app.js          # 核心逻辑
├── marked.min.js       # Markdown 解析器
├── highlight.min.js    # 代码高亮
├── github-dark.min.css # 深色主题
├── start.sh            # macOS/Linux 启动脚本
├── start.bat           # Windows 启动脚本
├── paw-cli.js          # CLI 工具 (可选)
└── README.md           # 本文档
```

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 本项目
2. 创建分支 (`git checkout -b feature/xxx`)
3. 提交更改 (`git commit -m 'Add xxx'`)
4. 推送到分支 (`git push origin feature/xxx`)
5. 创建 Pull Request

## 📜 许可证

MIT License - 查看 [LICENSE](./LICENSE) 文件

## 🔗 相关链接

- [OpenClaw 官网](https://openclaw.ai)
- [OpenClaw 文档](https://docs.openclaw.ai)
- [OpenClaw GitHub](https://github.com/openclaw/openclaw)
- [社区 Discord](https://discord.com/invite/clawd)

---

<p align="center">Made with ❤️ for OpenClaw users</p>