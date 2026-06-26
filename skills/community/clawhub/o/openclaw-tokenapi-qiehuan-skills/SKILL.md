# OpenClaw Model Switcher（模型切换工具）

一个基于 WebUI 的 OpenClaw 模型切换工具，支持快速切换 AI 模型提供商。

## 功能特性

- **模型通讯录**：保存常用模型配置，方便重复使用
- **一键切换**：点击卡片快速切换当前使用模型
- **批量导入**：支持在线输入或 TXT 文件批量导入模型
- **API Key 记忆**：自动记住每个提供商的 API Key（本地浏览器 localStorage）
- **提供商筛选**：卡片太多时可按提供商筛选
- **内置预设**：阿里云、火山引擎、Kimi、DeepSeek、OpenAI、MiniMax 等

## 触发词

当用户提到以下内容时激活此技能：
- 「打开模型切换」「模型切换工具」「切换模型」
- 「切换到 xxx 模型」「换个模型」
- 「打开模型管理」「模型配置」
- 「切换 AI 模型」「换一个大模型」

## 使用方式

### 启动 WebUI（主要方式）

用户说「打开模型切换」后：
1. 启动后端服务（端口 9131）
2. 自动打开浏览器访问 http://127.0.0.1:9131

### 快速切换模型（对话式）

用户说「切换到 deepseek 模型」后，直接调用 OpenClaw 配置接口修改 `openclaw.json`。

## 技术架构

```
后端：Python FastAPI (端口 9131)
前端：Vue 3 + Element Plus (已构建为静态文件)
配置：~/.openclaw/openclaw.json
```

## API 接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `GET /api/config` | GET | 获取当前配置和模型列表 |
| `POST /api/save` | POST | 保存模型到通讯录（不重启） |
| `POST /api/switch` | POST | 切换模型并重启服务 |
| `POST /api/gateway/control` | POST | 控制 Gateway（stop/start/restart） |
| `POST /api/delete` | POST | 删除模型或提供商 |
| `GET /api/providers` | GET | 获取所有提供商 |

## 安全设计

- API Key 仅保存在浏览器 localStorage（本地），不上传到任何服务器
- 后端只读写 openclaw.json（不含 API Key 的部分）
- API Key 同时写入 `~/.openclaw/agents/main/agent/auth-profiles.json` 供 OpenClaw 使用

## 依赖

- Python 3.10+
- fastapi, uvicorn, pydantic, psutil, pywin32
- Node.js（仅构建前端时需要，开发版已内置 dist）

## 文件结构

```
openclaw-model-switcher/
├── SKILL.md
├── scripts/
│   ├── start.ps1          # Windows 启动脚本
│   └── switch_model.py    # 命令行快速切换
└── assets/
    └── frontend/           # 已构建的前端静态文件
        ├── index.html
        └── assets/
```

## 快速切换命令

无需启动 WebUI，直接用 Python 脚本切换模型：

```bash
# 切换模型
python switch_model.py --provider deepseek --model deepseek-chat

# 查看当前模型
python switch_model.py --status

# 重启 Gateway
python switch_model.py --restart
```
