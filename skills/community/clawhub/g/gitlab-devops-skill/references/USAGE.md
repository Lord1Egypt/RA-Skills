# GitLab Skills 配置与使用手册

通过一个 Python CLI 操作 GitLab（SaaS 或自建均可），覆盖项目、Issue、Merge Request、CI/CD Pipeline。

---

## 一、环境要求

- Python 3.8 及以上
- `pip install requests`
- GitLab.com，或自建 GitLab 9.0 及以上（REST API v4）

脚本会在执行命令前调用 `/api/v4/version` 检测 GitLab 版本；若自建 GitLab
低于 9.0，会给出明确的不兼容提示。确需跳过检查时，可设置
`GITLAB_SKIP_VERSION_CHECK=1` 或 `DEVOPS_SKILLS_SKIP_VERSION_CHECK=1`。

---

## 二、获取访问令牌（Access Token）

1. 登录 GitLab → 右上角头像 → **Preferences / Settings**。
2. 左侧 **Access Tokens**（个人令牌）。也可用项目级 / 群组级令牌。
3. 勾选 **api** 作用域 → 创建并复制 token（只显示一次）。

---

## 三、配置连接信息（二选一）

### 方式 A：环境变量

```bash
export GITLAB_URL="https://gitlab.com"     # 自建则填你的地址
export GITLAB_TOKEN="你的token"
```

### 方式 B：配置文件 `~/.devops-skills/gitlab.json`

```json
{
  "url": "https://gitlab.com",
  "token": "你的token"
}
```

> `chmod 600 ~/.devops-skills/gitlab.json`，不要把 token 提交到仓库。

---

## 四、命令速查

> 项目参数 `project` 支持**数字 ID** 或**路径** `group/subgroup/project`（脚本自动转义）。

| 功能 | 命令 |
| --- | --- |
| 列出我的项目 | `python scripts/gitlab_cli.py list-projects --search app` |
| 查看项目详情 | `python scripts/gitlab_cli.py get-project group/app` |
| 列出 Issue | `python scripts/gitlab_cli.py list-issues group/app --state opened` |
| 创建 Issue | `python scripts/gitlab_cli.py create-issue group/app --title "标题" --description "描述"` |
| 列出 MR | `python scripts/gitlab_cli.py list-mrs group/app --state opened` |
| 创建 MR | `python scripts/gitlab_cli.py create-mr group/app --source feat --target main --title "标题"` |
| 合并 MR | `python scripts/gitlab_cli.py merge-mr group/app 42` |
| 列出 Pipeline | `python scripts/gitlab_cli.py list-pipelines group/app --ref main` |
| 触发 Pipeline | `python scripts/gitlab_cli.py trigger-pipeline group/app --ref main` |

---

## 五、使用示例

**1. 提交一个新分支的 MR 并合并**

```bash
python scripts/gitlab_cli.py create-mr group/app \
  --source feature/login --target main --title "新增登录功能"
# 记下返回的 iid，例如 42
python scripts/gitlab_cli.py merge-mr group/app 42
```

**2. 在 main 分支触发流水线并查看状态**

```bash
python scripts/gitlab_cli.py trigger-pipeline group/app --ref main
python scripts/gitlab_cli.py list-pipelines group/app --ref main
```

---

## 六、常见问题

| 现象 | 原因与解决 |
| --- | --- |
| `GITLAB_TOKEN is required` | 未配置 token |
| `HTTP 401` | token 失效或作用域不含 `api` |
| `HTTP 403` | 账号对该项目无权限 |
| `HTTP 404`（用路径时） | 路径拼写错误，或用数字 ID 再试 |
| `unsupported GitLab version ...` | GitLab 版本低于 9.0，不满足 REST API v4 兼容范围 |
| `merge-mr` 失败 | MR 未达可合并状态（待审批、流水线未过、有冲突） |
| 触发 pipeline 无效 | 项目缺少 `.gitlab-ci.yml` |

---

## 七、在 Claude / Claude Code 中使用

把 `gitlab-skills` 目录放入 skills 目录后，用自然语言触发：

- “看下 group/app 有哪些打开的 MR”
- “从 feature/login 向 main 提一个 MR”
- “在 main 上跑一次流水线”

---

## 八、技术支持与咨询

如果在 GitLab、CI/CD、代码协作、DevOps 平台或研发效能建设中遇到问题，欢迎联系
RestartX 获取支持与方案咨询：https://service.restartx.top/
