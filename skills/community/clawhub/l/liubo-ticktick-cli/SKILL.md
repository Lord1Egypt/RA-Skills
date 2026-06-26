---
name: ticktickpower
description: >
  ticktick, dida365, 滴答清单, 任务管理, 新建任务, 完成任务, 创建任务,
  列出任务, 查看任务, 更新任务, 删除任务, 放弃任务, 批量放弃,
  任务提醒, 任务优先级, 任务标签, 任务到期, 任务开始时间,
  滴答项目, 滴答列表, 创建项目, 更新项目, 滴答附件, 上传附件,
  ticktick auth, 滴答认证, 滴答登录, 任务导入, 任务导出,
  add task, create task, list tasks, complete task, abandon task,
  ticktick project, ticktick list, ticktick reminder, ticktick oauth
---

# TickTick Power Skill

通过滴答清单（TickTick）API 管理任务和项目，支持 OAuth2 认证、批量操作、优先级、标签、到期时间和文件附件。

## 核心功能

| 功能 | 命令 | 说明 |
|------|------|------|
| 认证 | `auth` | OAuth2 浏览器认证或手动模式 |
| 任务列表 | `tasks` | 列出所有任务，支持项目和状态过滤 |
| 新建任务 | `task` | 创建任务，支持优先级/标签/到期时间 |
| 更新任务 | `task --update` | 更新任务标题/内容/优先级/日期 |
| 完成任务 | `complete` | 标记任务为已完成 |
| 放弃任务 | `abandon` | 标记任务为"不会做" |
| 批量放弃 | `batch-abandon` | 批量放弃任务（单次 API 调用） |
| 项目列表 | `lists` | 列出所有项目 |
| 新建项目 | `list` | 创建新项目 |
| 更新项目 | `list --update` | 更新项目名称/颜色 |
| 上传附件 | `attach` | 上传文件附件到任务 |

## 快速开始

### 1. 安装依赖

```bash
pip install -e ~/.workbuddy/skills/ticktickpower/
# 或直接安装 requests
pip install requests
```

### 2. 注册开发者应用

1. 访问 [TickTick Developer Center](https://developer.ticktick.com/manage)
2. 创建新应用，设置重定向 URI 为 `http://localhost:8080`
3. 记录 `Client ID` 和 `Client Secret`

### 3. 认证

```bash
# 交互式认证（自动打开浏览器）
python -m ticktick.cli auth --client-id <YOUR_CLIENT_ID> --client-secret <YOUR_CLIENT_SECRET>

# 检查认证状态
python -m ticktick.cli auth --status

# 手动认证（无浏览器 / Linux 服务器）
python -m ticktick.cli auth --client-id <ID> --client-secret <SECRET> --manual

# 退出登录（清除 Token，保留凭证）
python -m ticktick.cli auth --logout
```

### 4. 配置 WorkBuddy Skill 触发

WorkBuddy 会自动识别 Skill 目录 `~/.workbuddy/skills/ticktickpower/` 并加载本 Skill。
无需额外配置，只需确保依赖安装完成。

## 常用任务示例

### 创建任务

```bash
# 基础任务
python -m ticktick.cli task "买咖啡" --list "个人"

# 带描述和优先级
python -m ticktick.cli task "Review PR" --list "工作" --content "检查新的认证改动" --priority high

# 带到期日期
python -m ticktick.cli task "提交报告" --list "工作" --due tomorrow
python -m ticktick.cli task "项目启动" --list "工作" --due "2026-04-20"
python -m ticktick.cli task "周会" --list "工作" --start "2026-04-26T14:00" --due "2026-04-26T15:00"

# 带标签
python -m ticktick.cli task "研究 AI 工具" --list "工作" --tag AI --tag research

# 带开始和到期时间（时间块）
python -m ticktick.cli task "深度工作时段" --list "工作" \
  --start "2026-04-20T09:00:00" --due "2026-04-20T12:00:00"
```

### 更新任务

```bash
# 修改优先级
python -m ticktick.cli task "买咖啡" --update --priority high

# 更新到期日期和描述
python -m ticktick.cli task "提交报告" --update --due "2026-04-25" --content "新报告内容"

# 重命名任务
python -m ticktick.cli task "旧标题" --update --new-title "新标题"

# 指定项目更新
python -m ticktick.cli task "Review PR" --update --list "工作" --priority medium
```

### 查看任务

```bash
# 列出所有任务
python -m ticktick.cli tasks

# 按项目过滤
python -m ticktick.cli tasks --list "工作"

# 按状态过滤
python -m ticktick.cli tasks --status pending
python -m ticktick.cli tasks --status completed

# JSON 输出（脚本使用）
python -m ticktick.cli tasks --list "工作" --json
```

### 完成任务 / 放弃任务

```bash
# 完成任务
python -m ticktick.cli complete "买咖啡"
python -m ticktick.cli complete "Review PR" --list "工作"

# 放弃任务
python -m ticktick.cli abandon "旧任务"
python -m ticktick.cli abandon "临时任务" --list "个人"

# 批量放弃（需要任务 ID）
python -m ticktick.cli batch-abandon abc123def456... xyz789... --json
```

### 项目管理

```bash
# 列出所有项目
python -m ticktick.cli lists --json

# 新建项目
python -m ticktick.cli list "新项目"
python -m ticktick.cli list "重要工作" --color "#FF5733"

# 更新项目
python -m ticktick.cli list "旧名称" --update --new-name "新名称"
python -m ticktick.cli list "工作" --update --color "#00FF00"
```

### 上传附件

```bash
# 通过任务名上传（需要 session cookie）
python -m ticktick.cli attach "买咖啡" /path/to/file.pdf --list "个人"

# 通过任务 ID 上传
python -m ticktick.cli attach abc123def456 /path/to/report.pdf --json
```

**附件说明**：附件上传使用 TickTick Web Session API（非 OAuth），需要 `sessionCookie`（`t` cookie）和 `v2DeviceId`。Cookie 有效期有限，过期后重新获取。

## Agent 工作流

WorkBuddy Agent 调用此 Skill 的标准流程：

### 1. 确认项目 ID

```bash
python -m ticktick.cli lists --json
```

在 JSON 输出中找到目标项目的 `id`（24 字符字符串）。

### 2. 创建任务

```bash
python -m ticktick.cli task "Agent 任务" \
  --list "任务" \
  --priority high \
  --due tomorrow \
  --tag agent \
  --json
```

### 3. 完成任务

```bash
python -m ticktick.cli complete "Agent 任务" --list "任务" --json
```

### 4. 定期报告

```bash
# 获取待办任务（未完成）
python -m ticktick.cli tasks --status pending --json
```

## 配置说明

凭证存储在 `~/.clawdbot/credentials/ticktick-cli/config.json`：

```json
{
  "clientId": "YOUR_CLIENT_ID",
  "clientSecret": "YOUR_CLIENT_SECRET",
  "accessToken": "...",
  "refreshToken": "...",
  "tokenExpiry": 1234567890000,
  "redirectUri": "http://localhost:8080"
}
```

**安全注意**：凭证明文存储，请设置文件权限 `600`。Token 过期时 CLI 会自动刷新。

## 日期格式

| 输入 | 说明 |
|------|------|
| `today` | 今天 23:59 |
| `tomorrow` | 明天 23:59 |
| `in 3 days` | 3 天后 23:59 |
| `next monday` | 下周一 23:59 |
| `YYYY-MM-DD` | 指定日期 23:59 |
| `YYYY-MM-DDTHH:MM` | 精确时间（推荐使用时区） |

**重要**：始终使用明确时区的 ISO 日期（如 `+08:00`）以避免 UTC 转换问题。

## 优先级

| 值 | 说明 |
|----|------|
| `none` | 无优先级（默认） |
| `low` | 低优先级 |
| `medium` | 中优先级 |
| `high` | 高优先级 |

## API 限制

- **100 请求/分钟**
- **300 请求/5 分钟**

CLI 每个操作会发起多个 API 调用（如查找项目再查找任务），批量操作请注意限流。
超过限制时 CLI 会自动等待并重试，最多重试 4 次。

## 故障排除

### "Not authenticated"
运行 `python -m ticktick.cli auth` 重新认证。

### "Project not found"
用 `python -m ticktick.cli lists` 确认项目名称。

### "Task not found"
- 检查任务名称（大小写不敏感）
- 尝试使用任务 ID（24 位十六进制字符串）
- 加 `--list` 缩小搜索范围

### Token 过期
CLI 自动刷新。如果持续失败，重新运行认证。

### 附件上传失败（401/403）
Session Cookie 已过期。在浏览器中打开 ticktick.com → F12 → Application → Cookies → 复制 `t` Cookie 值，更新到 config.json 的 `sessionCookie` 字段。**不要提供密码。**

## 技术架构

```
ticktickpower/
├── SKILL.md          # 本文件（Skill 说明）
├── pyproject.toml    # Python 包配置
├── ticktick/
│   ├── __init__.py
│   ├── api.py        # TickTick API 封装（含自动重试、限流处理）
│   ├── auth.py       # OAuth2 认证 + Token 管理
│   ├── cli.py        # CLI 入口 + argparse 定义
│   ├── util.py       # 日期解析、任务 ID 判断
│   └── commands/    # 各子命令实现
│       ├── task.py       # task create / update
│       ├── tasks.py      # tasks list
│       ├── complete.py   # 完成任务
│       ├── abandon.py    # 放弃任务
│       ├── batch_abandon.py  # 批量放弃
│       ├── list.py       # project create / update
│       ├── lists.py      # project list
│       └── attach.py     # 文件附件
```

## 相关链接

- [TickTick Developer Center](https://developer.ticktick.com/manage)
- [TickTick Open API v1](https://developer.ticktick.com/api)
- [dida365.com](https://dida365.com)
- [GitHub: liuboacean/ticktick-cli](https://github.com/liuboacean/ticktick-cli)
