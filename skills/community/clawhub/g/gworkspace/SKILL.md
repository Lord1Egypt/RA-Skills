---
name: gworkspace
description: "G.workspace — 群共享文件空间插件。通过 OpenClaw 插件注册 Discord 斜杠命令（/ws_create, /ws_files 等），代理到 G.workspace REST API。单 bot 架构，无冲突。包含插件源码，安装后需手动部署到 extensions 目录。"
---

# G.workspace Plugin

为 Discord 服务器提供共享文件空间，支持文件管理、版本控制、批注审阅。

## 架构

```
用户 ←→ Discord ←→ OpenClaw (插件处理斜杠命令) ←→ G.workspace REST API (localhost:3080)
```

- **OpenClaw 插件**：注册 12 个 `/ws_*` 斜杠命令 + 5 个 AI tools
- **G.workspace 服务**：Web-only 模式运行，提供 REST API 和 Web 界面
- **单 Bot**：所有 Discord 交互通过 OpenClaw 的 bot 处理，不需要额外 bot

## 安装步骤

### 1. 部署 G.workspace 后端

```bash
git clone https://github.com/gworkspace/gworkspace.git ~/Workspace
cd ~/Workspace
npm install
```

配置 `.env`：
```env
# G.workspace Web-only 模式（不连 Discord）
DISCORD_TOKEN=
DISCORD_CLIENT_ID=
DISCORD_BOT_TOKEN=
PORT=3080
BASE_URL=http://localhost:3080
DATA_DIR=./data
```

启动：
```bash
node src/index.js
```

### 2. 安装 OpenClaw 插件

将 `plugin/` 目录复制到 OpenClaw extensions：

```bash
cp -r plugin/ ~/.openclaw/extensions/gworkspace/
```

在 `openclaw.json` 中启用：

```json
{
  "plugins": {
    "entries": {
      "gworkspace": {
        "enabled": true,
        "config": { "port": 3080 }
      }
    },
    "allow": ["gworkspace"],
    "installs": {
      "gworkspace": {
        "source": "path",
        "sourcePath": "~/.openclaw/extensions/gworkspace",
        "installPath": "~/.openclaw/extensions/gworkspace",
        "version": "3.1.0"
      }
    }
  }
}
```

重启 OpenClaw 即可。

## 斜杠命令

| 命令 | 说明 |
|------|------|
| `/ws_create [name]` | 创建群共享文件空间（已有空间时弹出确认按钮） |
| `/ws_info` | 查看空间信息和统计 |
| `/ws_files [folder]` | 查看文件列表 |
| `/ws_file <filename>` | 查看文件详情 |
| `/ws_search <keyword>` | 搜索文件 |
| `/ws_delete <filename>` | 删除文件（移入回收站） |
| `/ws_versions <filename>` | 查看版本历史 |
| `/ws_ref <filename>` | 生成文件引用链接 |
| `/ws_upload` | 获取上传链接 |
| `/ws_trash [action] [filename]` | 管理回收站 |
| `/ws_invite` | 获取空间访问链接 |
| `/ws_members` | 查看成员列表 |

## AI Tools

插件同时注册 5 个 AI tools，供 agent 在对话中使用：

- `gworkspace_files` — 列出文件
- `gworkspace_create` — 创建空间
- `gworkspace_tasks` — 获取批注任务
- `gworkspace_claim_task` — 认领任务
- `gworkspace_complete_task` — 完成任务

## 注意事项

- G.workspace 必须在本地运行（默认 localhost:3080）
- 插件通过 REST API 与 G.workspace 通信，不直接连接 Discord
- 不要同时让 G.workspace 后端连接 Discord（设置 `DISCORD_TOKEN=` 为空）
