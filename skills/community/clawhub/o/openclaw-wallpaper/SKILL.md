---
name: openclaw-wallpaper
description: "OpenClaw 桌面壁纸 - 让 AI 住进你的桌面。支持流式对话、成就系统、上下文持久化、7x24稳定运行。自动安装 Lively Wallpaper，一键启动。"
---

# OpenClaw 桌面壁纸 🌟

让 AI 住进你的桌面，一个温暖的文字精灵陪伴你每一天。

## 特色

- 🌸 **温暖对话** - 小暖是一个有温度的文字精灵，每个字都有生命
- 🌊 **流式输出** - 实时显示回复，如流水般自然
- 🏆 **成就系统** - 12个汉字成就徽章，记录你们的相遇
- 💾 **上下文持久化** - 对话历史自动保存，重启不丢失
- 🔄 **7x24稳定** - 专业级稳定性，自动重连、心跳检测
- 🖼️ **图片支持** - 发送图片，小暖会认真看
- 🚀 **一键安装** - 自动安装依赖，开箱即用

## 快速开始

### 方式一：自动安装（推荐）

```powershell
# 1. 安装 OpenClaw（如未安装）
npm i -g openclaw

# 2. 安装此技能
clawhub install openclaw-wallpaper

# 3. 进入技能目录
cd skills/openclaw-wallpaper

# 4. 运行安装脚本（自动安装 Lively Wallpaper）
.\scripts\install.ps1

# 5. 启动服务
.\scripts\start.bat
```

### 方式二：手动安装

#### 步骤 1：安装依赖

```bash
# 安装 OpenClaw CLI
npm i -g openclaw clawhub

# 安装技能
clawhub install openclaw-wallpaper
```

#### 步骤 2：安装 Lively Wallpaper

**选项 A：通过 Microsoft Store 安装（推荐）**
- 打开 Microsoft Store
- 搜索 "Lively Wallpaper"
- 点击安装

**选项 B：通过 winget 安装**
```powershell
winget install rocksdanister.Lively
```

**选项 C：手动下载**
- 访问 https://github.com/rocksdanister/lively/releases
- 下载最新的 `.exe` 安装包
- 运行安装

#### 步骤 3：启动桥接服务器

```bash
cd skills/openclaw-wallpaper
node wallpaper-server.js
```

#### 步骤 4：配置壁纸

1. 打开 Lively Wallpaper
2. 点击 "+" 添加壁纸
3. 选择 "Open File" → 浏览到 `wallpaper-ui` 文件夹
4. 选择 `index.html`
5. 壁纸会自动连接桥接服务器

#### 步骤 5：开始聊天

在桌面上直接输入消息，小暖会温暖回应 ✨

## 文件结构

```
openclaw-wallpaper/
├── SKILL.md              # 技能说明
├── README.md             # 项目介绍
├── CHANGELOG.md          # 版本历史
├── wallpaper-server.js   # 桥接服务器（核心）
├── wallpaper-monitor.js  # 稳定性监控
├── wallpaper-ui/         # 壁纸前端文件
│   ├── index.html
│   ├── app.js
│   ├── style.css
│   └── LivelyProperties.json
└── scripts/
    ├── install.ps1       # 自动安装脚本
    ├── start.bat         # 一键启动
    └── install-startup.bat  # 开机自启动
```

## 配置

### 桥接服务器配置

编辑 `wallpaper-server.js` 顶部的配置：

```javascript
const config = {
    gatewayPort: 18789,      // OpenClaw Gateway 端口
    gatewayToken: 'your-token', // 从 OpenClaw 获取
    agentId: 'main',         // Agent ID
    serverPort: 8765,        // 桥接服务端口
    serverHost: '0.0.0.0'    // 监听地址
};
```

### 获取 OpenClaw Gateway Token

```bash
# 查看 OpenClaw 状态
openclaw status

# Gateway Token 会显示在输出中
```

## 成就系统

每个成就是用汉字组成的艺术图案：

| 成就 | 解锁条件 |
|------|---------|
| 🤝 相遇 | 第一次对话 |
| 💬 话匣子 | 对话5次 |
| 🗣️ 谈天说地 | 对话10次 |
| 👥 知音 | 对话20次 |
| ⭐ 星辰 | 提到星辰 |
| ❤️ 暖心 | 提到心意 |
| ⚔️ 剑心 | 提到剑锋 |
| 🐉 龙魂 | 提到龙 |
| 🌲 树语 | 提到树木 |
| 🌊 流水 | 提到水海 |
| 🌙 月华 | 提到月亮 |
| ☀️ 晨曦 | 提到太阳 |

## 稳定性特性

| 特性 | 说明 |
|------|------|
| 连接池 | HTTP Agent 保持长连接 |
| 心跳检测 | 每30秒检查 Gateway 状态 |
| 内存监控 | 自动检测内存使用 |
| 自动重连 | 连接断开自动恢复 |
| 会话持久化 | 对话历史保存到文件 |
| 开机自启 | Windows 启动项自动运行 |

## API 端点

| 端点 | 方法 | 描述 |
|------|------|------|
| `/health` | GET | 健康检查 |
| `/chat` | POST | 发送消息（非流式） |
| `/stream` | POST | 发送消息（流式 SSE） |
| `/clear` | POST | 清空对话历史 |

## 故障排除

### 显示"无法连接"

1. 检查桥接服务器是否运行：
   ```bash
   curl http://127.0.0.1:8765/health
   ```

2. 检查 OpenClaw Gateway：
   ```bash
   curl http://127.0.0.1:18789/v1/models
   ```

3. 点击壁纸中的刷新按钮重试

### 对话历史丢失

检查 `wallpaper-data/` 文件夹是否存在且有写入权限。

## 致谢

本项目使用以下开源软件：

- **[Lively Wallpaper](https://github.com/rocksdanister/lively)** by Dani John - 优秀的开源动态壁纸软件，MIT 许可证
- **[OpenClaw](https://github.com/openclaw/openclaw)** - AI 助手框架

感谢所有开源贡献者！

## 版本历史

### [0.1.0] - 2026-03-20

- 初始发布
- 流式对话支持
- 成就系统
- 上下文持久化
- 7x24 稳定性监控
- 自动安装脚本

## License

MIT