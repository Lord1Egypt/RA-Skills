---
name: paw-chat
description: Install and manage Paw - a standalone web chat frontend for OpenClaw Gateway. Use when the user wants to install Paw, update Paw, or set up a web chat interface for OpenClaw. Triggers on phrases like "install paw", "setup paw chat", "web chat for openclaw", "paw frontend".
---

# Paw Chat

🐾 Paw 是 OpenClaw 的独立 Web 聊天前端，零构建工具，零后端 —— 只需静态文件即可通过 WebSocket 连接到任何 OpenClaw Gateway。

## 功能特性

- **独立运行**：纯静态文件，无需构建，无需后端
- **WebSocket 连接**：直接连接到 OpenClaw Gateway
- **多会话管理**：支持切换和管理多个聊天会话
- **Agent 管理**：内置 Agent 配置界面（身份、性格、用户信息、定时任务）
- **图片支持**：支持粘贴、拖拽、上传图片
- **Markdown 渲染**：完整的 Markdown 支持，包括代码高亮
- **工具调用展示**：实时显示工具调用过程和结果
- **主题切换**：支持深色/浅色模式

## 安装方式

### 方式一：安装到 OpenClaw Gateway（推荐）

将 Paw 安装到 Gateway 的 control-ui-static 目录，直接通过 Gateway 访问：

```bash
# 运行安装脚本
./scripts/install.sh
```

安装后访问：`https://<gateway-host>:<port>/<basePath>/chat.html`

### 方式二：本地启动

```bash
# 进入 assets 目录
cd assets

# macOS / Linux
./start.sh

# Windows
start.bat
```

默认端口：18790

访问：`http://localhost:18790`

### 方式三：手动部署

```bash
# 复制文件到任意 Web 服务器
cp assets/index.html /var/www/html/chat.html
cp assets/paw-app.js assets/marked.min.js assets/highlight.min.js assets/github-dark.min.css assets/logo.jpg /var/www/html/
```

## 首次使用

1. 打开 Paw 页面
2. 点击右上角 ⚙ **设置**
3. 填写：
   - **Gateway URL**: `wss://<your-gateway-host>:<port>`
   - **Token**: 从 `~/.openclaw/config.yaml` 获取 `gateway.auth.token`
4. 点击 **连接**

## 文件结构

```
assets/
├── index.html          # 主页面
├── paw-app.js          # 核心逻辑
├── marked.min.js       # Markdown 解析器
├── highlight.min.js    # 代码高亮
├── github-dark.min.css # 代码主题
├── logo.jpg            # Paw Logo
├── start.sh            # macOS/Linux 启动脚本
└── start.bat           # Windows 启动脚本
```

## 更新 Paw

重新运行安装脚本即可更新：

```bash
./scripts/install.sh
```

## 卸载

删除 Gateway 目录中的文件：

```bash
rm -f ~/.openclaw/control-ui-static/chat.html
rm -f ~/.openclaw/control-ui-static/paw-app.js
rm -f ~/.openclaw/control-ui-static/marked.min.js
rm -f ~/.openclaw/control-ui-static/highlight.min.js
rm -f ~/.openclaw/control-ui-static/github-dark.min.css
rm -f ~/.openclaw/control-ui-static/logo.jpg
```
