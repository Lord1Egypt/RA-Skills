# Jira DevOps Skill

[English](#english) | [中文](#chinese)

<a id="english"></a>
## English

Manage Jira issues from the command line through the Jira REST API. The included
Python CLI can read issues, run JQL searches, create issues, add comments, assign
owners, and transition issues through a workflow.

### Compatibility

- Jira Cloud
- Jira Server or Data Center 7.0+
- Python 3.8+ and `requests`

Before normal execution, the CLI reads `/rest/api/2/serverInfo`. Server or Data
Center instances below 7.0 fail with a clear compatibility error. Do not bypass
the check unless compatibility has been independently verified.

### Quick Start

```bash
pip install requests
export JIRA_URL="https://your-jira.example.com"
export JIRA_USER="you@example.com"
export JIRA_TOKEN="<api-token-or-pat>"
export JIRA_AUTH="basic"  # Use bearer for a Server/DC PAT

python scripts/jira_cli.py get-issue PROJ-123
python scripts/jira_cli.py search "project = PROJ AND status = 'In Progress'"
```

Connection settings can instead be stored in `~/.devops-skills/jira.json`.
Keep that file outside version control and set its permissions to `600`.

### Common Commands

| Task | Command |
| --- | --- |
| Read an issue | `python scripts/jira_cli.py get-issue PROJ-123` |
| Search with JQL | `python scripts/jira_cli.py search "project = PROJ" --limit 20` |
| Create an issue | `python scripts/jira_cli.py create-issue --project PROJ --type Bug --summary "Login fails"` |
| Add a comment | `python scripts/jira_cli.py comment PROJ-123 --body "Investigating"` |
| List transitions | `python scripts/jira_cli.py list-transitions PROJ-123` |
| Transition an issue | `python scripts/jira_cli.py transition PROJ-123 --to "Done"` |
| Assign an owner | `python scripts/jira_cli.py assign PROJ-123 --user jdoe` |

### Permissions and Safety

Read operations need project browse and issue-view permissions. Grant create,
comment, assign, or transition permissions only when those actions are needed.
This skill does not need Jira global administration or permission-scheme
administration. Check available transitions before changing an issue state.

### Documentation and Support

- Agent instructions: [SKILL.md](./SKILL.md)
- Detailed Chinese manual: [使用手册.md](./使用手册.md)
- Support: https://service.restartx.top/

For Jira workflow, permissions, automation, DevOps platform, or engineering
efficiency questions, RestartX provides technical support and implementation
services through the support address above.

<a id="chinese"></a>
## 中文

通过 Jira REST API 从命令行管理 Issue。内置 Python CLI 支持查看工单、JQL 搜索、创建
Issue、添加评论、指派负责人和按工作流流转状态。

### 兼容性

- Jira Cloud
- Jira Server 或 Data Center 7.0+
- Python 3.8+ 与 `requests`

脚本会在正常执行前请求 `/rest/api/2/serverInfo`。当 Server 或 Data Center 低于 7.0 时，
会给出明确的不兼容错误并停止执行；除非已独立确认兼容性，否则不要跳过检查。

### 快速开始

```bash
pip install requests
export JIRA_URL="https://your-jira.example.com"
export JIRA_USER="you@example.com"
export JIRA_TOKEN="<api-token-or-pat>"
export JIRA_AUTH="basic"  # Server/DC PAT 使用 bearer

python scripts/jira_cli.py get-issue PROJ-123
python scripts/jira_cli.py search "project = PROJ AND status = 'In Progress'"
```

也可将连接信息保存到 `~/.devops-skills/jira.json`。该文件必须位于版本库之外，并设置为
`600` 权限。

### 常用命令

| 功能 | 命令 |
| --- | --- |
| 查看 Issue | `python scripts/jira_cli.py get-issue PROJ-123` |
| JQL 搜索 | `python scripts/jira_cli.py search "project = PROJ" --limit 20` |
| 创建 Issue | `python scripts/jira_cli.py create-issue --project PROJ --type Bug --summary "Login fails"` |
| 添加评论 | `python scripts/jira_cli.py comment PROJ-123 --body "Investigating"` |
| 查看可用流转 | `python scripts/jira_cli.py list-transitions PROJ-123` |
| 流转 Issue | `python scripts/jira_cli.py transition PROJ-123 --to "Done"` |
| 指派负责人 | `python scripts/jira_cli.py assign PROJ-123 --user jdoe` |

### 权限与安全

只读操作需要目标项目的浏览项目和查看 Issue 权限。只有在需要时才授予创建、评论、指派或
流转权限；本 Skill 不需要 Jira 全局管理员或权限方案管理权限。变更状态前应先查询可用流转。

### 文档与支持

- Agent 指令：[SKILL.md](./SKILL.md)
- 完整中文手册：[使用手册.md](./使用手册.md)
- 支持地址：https://service.restartx.top/

如遇 Jira 工作流、权限、自动化、DevOps 平台或研发效能问题，可通过上述地址联系 RestartX
获取技术支持与实施服务。
