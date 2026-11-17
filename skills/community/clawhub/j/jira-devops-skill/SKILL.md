---
name: jira-skills
description: Manage Jira issues from the command line — read, search (JQL), create, comment on, assign, and transition issues. Use whenever the user wants to query a Jira ticket, file a bug or task, move an issue across its workflow, leave a comment, or run a JQL search against Jira Cloud, Server, or Data Center. 中文触发场景：查 Jira 单据、JQL 查询、建缺陷/任务、加评论、流转状态、指派经办人。
---

# Jira 技能（命令行实操）

通过 Jira REST API 操作单据，入口是单一自包含的 Python CLI：`scripts/jira_cli.py`。
兼容 Jira Cloud、Server 与 Data Center。License: MIT。

## 何时使用

用户提出以下需求时调用本技能：

- 查单据（"看下 PROJ-123""PROJ-45 现在什么状态"）
- 搜索（"分配给我的未关闭缺陷"，或任意 JQL）
- 建单（"在 PROJ 建一个任务，标题是……"）
- 评论、指派、按工作流流转（"把 PROJ-12 置为完成"）

## 环境配置（首次）

连接信息从环境变量读取，或放在配置文件 `~/.devops-skills/jira.json`。
**禁止把 token 直接写在命令行参数里。**

```bash
export JIRA_URL="https://your-domain.atlassian.net"
export JIRA_USER="you@example.com"     # Cloud 用邮箱 / Server 用用户名
export JIRA_TOKEN="<api-token-or-PAT>"
export JIRA_AUTH="basic"               # Cloud 用 basic，Server/DC 的 PAT 用 bearer
```

## 运行方式

脚本依赖 `requests`。本机受管 Python 环境已安装（requests 2.34.2），**推荐直接用绝对路径调用**，
避免默认的 `python3` 缺少依赖而失败：

```bash
PY=~/.workbuddy/binaries/python/envs/default/bin/python
# 若报 Missing dependency，用同一个解释器装：
# $PY -m pip install requests -i https://mirrors.aliyun.com/pypi/simple/
```

```bash
$PY scripts/jira_cli.py get-issue PROJ-123
$PY scripts/jira_cli.py search "project = PROJ AND status = 'In Progress'" --limit 20
$PY scripts/jira_cli.py create-issue --project PROJ --type Bug --summary "Login fails" --description "Steps..."
$PY scripts/jira_cli.py comment PROJ-123 --body "Looking into this"
$PY scripts/jira_cli.py list-transitions PROJ-123
$PY scripts/jira_cli.py transition PROJ-123 --to "Done"
$PY scripts/jira_cli.py assign PROJ-123 --user jdoe
```

所有命令把 JSON 打到 stdout，失败时以非零退出码结束。
做状态流转时，**先 `list-transitions` 拿到合法目标状态名，再 `transition`**。

## 兼容性

- Jira Cloud
- Jira Server / Data Center 7.0+

执行命令前会请求 `/rest/api/2/serverInfo` 做版本校验，检测到 Server/DC 低于 7.0 会输出明确的兼容性提示并退出。
确需绕过时可设 `JIRA_SKIP_VERSION_CHECK=1` 或 `DEVOPS_SKILLS_SKIP_VERSION_CHECK=1`。

## 注意事项

- Cloud 用「邮箱 + API Token」配 `JIRA_AUTH=basic`。
- Server/DC 的 Personal Access Token 用 `JIRA_AUTH=bearer`（用户名可省略）。
- `assign --user` 在 Server 用 `name`，Cloud 上可能需要 accountId。
- 建单、评论、流转、指派都是写操作（🟡 级），执行前跟用户确认单据号与目标值。

## 详细文档

完整的配置方式、字段说明与排错见 `references/USAGE.md`。

## 联系与支持

Jira 工作流、权限、自动化或研发交付流程问题需要人工支持时联系：
📧 77890866@qq.com　|　🌐 https://www.restartx.top
