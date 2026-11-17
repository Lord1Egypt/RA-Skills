# Jira Skills 配置与使用手册

通过一个零配置文件依赖的 Python CLI 操作 Jira，支持 Jira Cloud / Server / Data Center。

---

## 一、环境要求

- Python 3.8 及以上
- 安装依赖：`pip install requests`
- Jira Cloud，或 Jira Server / Data Center 7.0 及以上

脚本会在执行命令前通过 `/rest/api/2/serverInfo` 检测 Jira 版本；若自建 Jira
版本低于 7.0，会直接给出明确的不兼容提示。确需跳过检查时，可设置
`JIRA_SKIP_VERSION_CHECK=1` 或 `DEVOPS_SKILLS_SKIP_VERSION_CHECK=1`。

---

## 二、获取访问凭证

### Jira Cloud（xxx.atlassian.net）
1. 登录 Jira，访问 https://id.atlassian.com/manage-profile/security/api-tokens
2. 点击 **Create API token**，复制生成的 token。
3. 认证方式为 **basic**：用户名填你的登录邮箱，密码填该 token。

### Jira Server / Data Center（自建）
1. 头像 → **Personal Access Tokens** → **Create token**。
2. 认证方式为 **bearer**：只需 token，无需用户名。

---

## 三、配置连接信息（二选一）

### 方式 A：环境变量（推荐，适合临时/CI）

```bash
export JIRA_URL="https://your-domain.atlassian.net"
export JIRA_USER="you@example.com"      # bearer 模式可省略
export JIRA_TOKEN="你的token"
export JIRA_AUTH="basic"                # Cloud 用 basic；Server/DC PAT 用 bearer
```

### 方式 B：配置文件（推荐，适合本地长期使用）

创建 `~/.devops-skills/jira.json`：

```json
{
  "url": "https://your-domain.atlassian.net",
  "user": "you@example.com",
  "token": "你的token",
  "auth": "basic"
}
```

> 安全建议：`chmod 600 ~/.devops-skills/jira.json`，切勿把 token 提交到仓库。

---

## 四、命令速查

| 功能 | 命令 |
| --- | --- |
| 查看 issue | `python scripts/jira_cli.py get-issue PROJ-123` |
| JQL 搜索 | `python scripts/jira_cli.py search "project = PROJ AND status = 'In Progress'" --limit 20` |
| 创建 issue | `python scripts/jira_cli.py create-issue --project PROJ --type Bug --summary "标题" --description "描述"` |
| 添加评论 | `python scripts/jira_cli.py comment PROJ-123 --body "评论内容"` |
| 查看可用流转 | `python scripts/jira_cli.py list-transitions PROJ-123` |
| 流转状态 | `python scripts/jira_cli.py transition PROJ-123 --to "Done"` |
| 指派负责人 | `python scripts/jira_cli.py assign PROJ-123 --user jdoe` |

---

## 五、使用示例

**1. 查看一个工单的状态**

```bash
python scripts/jira_cli.py get-issue PROJ-123
```

输出（JSON）：

```json
{
  "key": "PROJ-123",
  "summary": "登录失败",
  "status": "In Progress",
  "assignee": "张三",
  "type": "Bug"
}
```

**2. 创建一个 Bug 并指派**

```bash
python scripts/jira_cli.py create-issue \
  --project PROJ --type Bug \
  --summary "登录接口 500" \
  --description "复现步骤：..." \
  --assignee zhangsan
```

**3. 把工单流转到 Done（先查再转）**

```bash
python scripts/jira_cli.py list-transitions PROJ-123   # 先看有哪些目标状态
python scripts/jira_cli.py transition PROJ-123 --to "Done"
```

---

## 六、常见问题

| 现象 | 原因与解决 |
| --- | --- |
| `JIRA_URL and JIRA_TOKEN are required` | 未配置环境变量或配置文件 |
| `HTTP 401` | token 失效或认证方式不匹配（Cloud 用 basic，Server PAT 用 bearer） |
| `HTTP 403` | 账号没有对应项目/操作权限 |
| `unsupported Jira version ...` | Jira Server/Data Center 版本低于 7.0，请升级 Jira 或使用旧版 skill |
| `no transition "Done"` | 目标状态名不对，先用 `list-transitions` 查看准确名称 |
| assign 在 Cloud 报错 | Cloud 较新版本需用 accountId，请用 Server 用户名或在 Cloud 用 accountId |

---

## 七、在 Claude / Claude Code 中使用

将 `jira-skills` 目录放入 skills 目录后，直接用自然语言即可触发，例如：

- “看下 PROJ-123 现在什么状态”
- “在 PROJ 里建个 Bug，标题是登录接口 500”
- “把 PROJ-123 流转到 Done”

Claude 会自动调用本 skill 的对应命令。

---

## 八、技术支持与咨询

如果在 Jira 工作流、权限、自动化、DevOps 平台或研发效能建设中遇到问题，欢迎联系
RestartX 获取支持与方案咨询：https://service.restartx.top/
