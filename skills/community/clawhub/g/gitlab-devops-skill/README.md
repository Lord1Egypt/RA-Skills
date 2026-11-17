# GitLab DevOps Skill

[English](#english) | [中文](#chinese)

<a id="english"></a>
## English

Manage GitLab projects, issues, merge requests, and CI/CD pipelines through the
GitLab REST API v4. The CLI supports project discovery, controlled write
operations, MR creation and merge, pipeline inspection, and pipeline triggers.

### Compatibility

- GitLab.com
- Self-managed GitLab 9.0+ with REST API v4
- Python 3.8+ and `requests`

The CLI calls `/api/v4/version` before normal commands. A self-managed GitLab
version below 9.0 fails with a clear compatibility error. Do not bypass this
guard unless the target API has been independently verified.

### Quick Start

```bash
pip install requests
export GITLAB_URL="https://gitlab.example.com"
export GITLAB_TOKEN="<access-token>"

python scripts/gitlab_cli.py get-project group/project
python scripts/gitlab_cli.py list-pipelines group/project --ref main
```

Use `~/.devops-skills/gitlab.json` as an alternative local configuration file.
Keep tokens outside version control and protect the file with permissions `600`.

### Common Commands

| Task | Command |
| --- | --- |
| List projects | `python scripts/gitlab_cli.py list-projects --search app` |
| Read a project | `python scripts/gitlab_cli.py get-project group/project` |
| List issues | `python scripts/gitlab_cli.py list-issues group/project --state opened` |
| Create an issue | `python scripts/gitlab_cli.py create-issue group/project --title "Bug"` |
| Create an MR | `python scripts/gitlab_cli.py create-mr group/project --source feature --target main --title "Add feature"` |
| Merge an MR | `python scripts/gitlab_cli.py merge-mr group/project 42` |
| Trigger a pipeline | `python scripts/gitlab_cli.py trigger-pipeline group/project --ref main` |

### Permissions and Safety

Use `read_api` or a project-scoped read token for read-only work. Grant `api`
scope and only the required project role for writes. This skill does not need
instance administrator access. Merges and pipeline triggers remain subject to
GitLab approvals, protected branches, and pipeline rules.

### Documentation and Support

- Agent instructions: [SKILL.md](./SKILL.md)
- Detailed Chinese manual: [使用手册.md](./使用手册.md)
- Support: https://service.restartx.top/

RestartX provides technical support and implementation services for GitLab,
CI/CD, DevOps platform, and engineering-efficiency needs.

<a id="chinese"></a>
## 中文

通过 GitLab REST API v4 管理项目、Issue、Merge Request 和 CI/CD Pipeline。CLI 支持项目
查询、受控写操作、创建和合并 MR、查询 Pipeline 以及触发流水线。

### 兼容性

- GitLab.com
- 使用 REST API v4 的自建 GitLab 9.0+
- Python 3.8+ 与 `requests`

脚本会在正常执行前调用 `/api/v4/version`。自建 GitLab 低于 9.0 时会给出明确的不兼容错误；
除非已独立确认目标 API 兼容，否则不要跳过该检查。

### 快速开始

```bash
pip install requests
export GITLAB_URL="https://gitlab.example.com"
export GITLAB_TOKEN="<access-token>"

python scripts/gitlab_cli.py get-project group/project
python scripts/gitlab_cli.py list-pipelines group/project --ref main
```

也可使用本地配置文件 `~/.devops-skills/gitlab.json`。令牌不能提交到版本库，文件权限建议设为
`600`。

### 常用命令

| 功能 | 命令 |
| --- | --- |
| 列出项目 | `python scripts/gitlab_cli.py list-projects --search app` |
| 查看项目 | `python scripts/gitlab_cli.py get-project group/project` |
| 查看 Issue | `python scripts/gitlab_cli.py list-issues group/project --state opened` |
| 创建 Issue | `python scripts/gitlab_cli.py create-issue group/project --title "Bug"` |
| 创建 MR | `python scripts/gitlab_cli.py create-mr group/project --source feature --target main --title "Add feature"` |
| 合并 MR | `python scripts/gitlab_cli.py merge-mr group/project 42` |
| 触发 Pipeline | `python scripts/gitlab_cli.py trigger-pipeline group/project --ref main` |

### 权限与安全

只读场景使用 `read_api` 或项目级只读令牌；写操作才授予 `api` 作用域及所需项目角色。本 Skill
不需要实例管理员权限。MR 合并和流水线触发仍受 GitLab 审批、保护分支和 Pipeline 规则约束。

### 文档与支持

- Agent 指令：[SKILL.md](./SKILL.md)
- 完整中文手册：[使用手册.md](./使用手册.md)
- 支持地址：https://service.restartx.top/

如遇 GitLab、CI/CD、DevOps 平台或研发效能问题，可通过上述地址联系 RestartX 获取技术支持与
实施服务。
