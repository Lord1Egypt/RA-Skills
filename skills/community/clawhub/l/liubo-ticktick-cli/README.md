# ticktick-cli

> 通过命令行管理 TickTick / 滴答清单任务和项目，支持 OAuth2 认证、批量操作和限流自动重试。

```bash
# 安装
pip install ticktick-cli

# 认证
ticktick auth --client-id YOUR_ID --client-secret YOUR_SECRET

# 创建任务
ticktick task "买咖啡" --list "个人" --priority high --due tomorrow

# 列出任务
ticktick tasks --list "工作" --status pending

# 完成任务
ticktick complete "买咖啡"
```

## 功能特性

| 功能 | 说明 |
|------|------|
| **OAuth2 认证** | 支持浏览器自动认证和手动模式（Linux 服务器） |
| **任务管理** | 创建、更新、完成任务，支持优先级/标签/到期时间/时间块 |
| **批量操作** | 批量放弃任务，单次 API 调用完成 |
| **文件附件** | 上传文件附件到任务 |
| **自动重试** | 限流时自动等待并重试（最多 4 次） |
| **Token 自动刷新** | OAuth Token 过期自动刷新 |

## 安装

```bash
# 从 PyPI 安装
pip install ticktick-cli

# 从源码安装（开发模式）
pip install -e .

# 仅安装依赖（无需包管理）
pip install requests
```

## 快速开始

### 1. 注册开发者应用

1. 访问 [TickTick Developer Center](https://developer.ticktick.com/manage)
2. 创建新应用，设置重定向 URI 为 `http://localhost:8080`
3. 记录 `Client ID` 和 `Client Secret`

### 2. 认证

```bash
# 交互式认证（自动打开浏览器）
ticktick auth --client-id YOUR_CLIENT_ID --client-secret YOUR_CLIENT_SECRET

# 检查认证状态
ticktick auth --status

# 手动认证（无浏览器 / Linux 服务器）
ticktick auth --client-id YOUR_CLIENT_ID --client-secret YOUR_CLIENT_SECRET --manual

# 退出登录（清除 Token，保留凭证）
ticktick auth --logout
```

### 3. 创建任务

```bash
# 基础任务
ticktick task "买咖啡" --list "个人"

# 带描述和优先级
ticktick task "Review PR" --list "工作" --content "检查新的认证改动" --priority high

# 带到期日期
ticktick task "提交报告" --list "工作" --due tomorrow
ticktick task "项目启动" --list "工作" --due "2026-04-20"

# 带开始和到期时间（时间块）
ticktick task "周会" --list "工作" \
  --start "2026-04-26T14:00:00" --due "2026-04-26T15:00:00"

# 带标签
ticktick task "研究 AI 工具" --list "工作" --tag AI --tag research
```

### 4. 更新任务

```bash
# 修改优先级
ticktick task "买咖啡" --update --priority high

# 更新到期日期
ticktick task "提交报告" --update --due "2026-04-25"

# 重命名任务
ticktick task "旧标题" --update --new-title "新标题"
```

### 5. 查看任务

```bash
# 列出所有任务
ticktick tasks

# 按项目过滤
ticktick tasks --list "工作"

# 按状态过滤
ticktick tasks --status pending
ticktick tasks --status completed

# JSON 输出（脚本使用）
ticktick tasks --list "工作" --json
```

### 6. 完成任务 / 放弃任务

```bash
# 完成任务
ticktick complete "买咖啡"

# 放弃任务
ticktick abandon "旧任务"

# 批量放弃（需要任务 ID）
ticktick batch-abandon abc123def456... xyz789...
```

### 7. 项目管理

```bash
# 列出所有项目
ticktick lists --json

# 新建项目
ticktick list "新项目"
ticktick list "重要工作" --color "#FF5733"

# 更新项目
ticktick list "旧名称" --update --new-name "新名称"
```

### 8. 上传附件

```bash
ticktick attach "买咖啡" /path/to/file.pdf --list "个人"
```

**注意**：附件上传需要 `sessionCookie`（从浏览器 ticktick.com 获取），Cookie 过期后需要重新获取。

## 日期格式

| 输入 | 说明 |
|------|------|
| `today` | 今天 23:59 |
| `tomorrow` | 明天 23:59 |
| `in 3 days` | 3 天后 23:59 |
| `next monday` | 下周一 23:59 |
| `YYYY-MM-DD` | 指定日期 23:59 |
| `YYYY-MM-DDTHH:MM:SS+08:00` | 精确时间（推荐使用时区） |

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

CLI 包含自动限流重试机制，最多重试 4 次。

## 故障排除

### "Not authenticated"
运行 `ticktick auth` 重新认证。

### "Project not found"
用 `ticktick lists` 确认项目名称。

### "Task not found"
- 检查任务名称（大小写不敏感）
- 尝试使用任务 ID（24 位十六进制字符串）
- 加 `--list` 缩小搜索范围

### 附件上传失败（401/403）
Session Cookie 已过期。在浏览器中打开 ticktick.com → F12 → Application → Cookies → 复制 `t` Cookie 值，更新到 `~/.clawdbot/credentials/ticktick-cli/config.json` 的 `sessionCookie` 字段。

## 项目结构

```
ticktick-cli/
├── SKILL.md              # WorkBuddy Skill 说明
├── README.md             # 本文件
├── LICENSE               # MIT License
├── pyproject.toml        # Python 包配置
└── ticktick/
    ├── __init__.py
    ├── api.py            # TickTick API 封装
    ├── auth.py           # OAuth2 认证
    ├── cli.py            # CLI 入口
    ├── util.py           # 日期解析工具
    └── commands/
        ├── task.py           # task create / update
        ├── tasks.py          # tasks list
        ├── complete.py       # 完成任务
        ├── abandon.py        # 放弃任务
        ├── batch_abandon.py  # 批量放弃
        ├── list.py           # project create / update
        ├── lists.py          # project list
        └── attach.py         # 文件附件
```

## 许可证

MIT License - 详见 [LICENSE](LICENSE)

## 相关链接

- [TickTick Developer Center](https://developer.ticktick.com/manage)
- [TickTick Open API v1](https://developer.ticktick.com/api)
- [dida365.com](https://dida365.com)
