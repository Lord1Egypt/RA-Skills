---
name: gitlab-skills
description: Manage GitLab projects from the command line — list/inspect projects, list and create issues, list/create/merge merge requests, and list or trigger CI/CD pipelines. Use whenever the user wants to work with a GitLab repo, file an issue, open or merge an MR, or kick off / check a pipeline on GitLab.com or a self-hosted GitLab. 中文触发场景：查 GitLab 项目、建 issue、开/合并 MR、查流水线、触发流水线、看流水线是否通过。
---

# GitLab 技能（命令行实操）

通过 GitLab REST API v4 操作项目，入口是单一自包含的 Python CLI：`scripts/gitlab_cli.py`。
兼容 GitLab.com SaaS 与私有化部署实例。License: MIT。

## 何时使用

用户提出以下需求时调用本技能：

- 查找或查看项目（"列一下我的项目""看 group/app 的详情"）
- 列出或创建 issue
- 列出、创建、合并 MR（合并请求）
- 列出或触发 CI/CD 流水线（"在 main 上跑一次流水线""流水线绿了吗"）

## 环境配置（首次）

连接信息从环境变量读取，或放在配置文件 `~/.devops-skills/gitlab.json`。
**禁止把 token 直接写在命令行参数里。**

```bash
export GITLAB_URL="https://gitlab.com"   # 私有化部署填自己的地址
export GITLAB_TOKEN="<access-token>"     # 需要 api 权限
```

Token 创建位置：User Settings → Access Tokens（勾选 `api`）。

## 运行方式

脚本依赖 `requests`。本机受管 Python 环境已安装（requests 2.34.2），**推荐直接用绝对路径调用**，
避免默认的 `python3` 缺少依赖而失败：

```bash
PY=~/.workbuddy/binaries/python/envs/default/bin/python
# 若报 Missing dependency，用同一个解释器装：
# $PY -m pip install requests -i https://mirrors.aliyun.com/pypi/simple/
```

项目参数可以是数字 ID，也可以是 `group/subgroup/project` 路径（脚本自动做 URL 编码）。

```bash
$PY scripts/gitlab_cli.py list-projects --search app
$PY scripts/gitlab_cli.py get-project group/app
$PY scripts/gitlab_cli.py list-issues group/app --state opened
$PY scripts/gitlab_cli.py create-issue group/app --title "Bug" --description "..."
$PY scripts/gitlab_cli.py list-mrs group/app --state opened
$PY scripts/gitlab_cli.py create-mr group/app --source feat --target main --title "Add feature"
$PY scripts/gitlab_cli.py merge-mr group/app 42
$PY scripts/gitlab_cli.py list-pipelines group/app --ref main
$PY scripts/gitlab_cli.py trigger-pipeline group/app --ref main
```

所有命令把 JSON 打到 stdout，失败时以非零退出码结束。

## 兼容性

- GitLab.com
- 私有化 GitLab 9.0+（REST API v4）

执行命令前会先请求 `/api/v4/version` 做版本校验，检测到低于 9.0 会输出明确的兼容性提示并退出。
确需绕过时可设 `GITLAB_SKIP_VERSION_CHECK=1` 或 `DEVOPS_SKILLS_SKIP_VERSION_CHECK=1`。

## 注意事项

- `merge-mr` 要求 MR 处于可合并状态（审批规则、流水线状态都会影响）。
- 触发流水线要求项目里存在 `.gitlab-ci.yml`。
- 写操作（建 issue、建 MR、合并、触发流水线）属于 🟡 级变更，执行前跟用户确认目标项目与分支。

## 详细文档

完整的配置方式、字段说明与排错见 `references/USAGE.md`。

## 联系与支持

GitLab、CI/CD、DevOps 平台或研发效能问题需要人工支持时联系：
📧 77890866@qq.com　|　🌐 https://www.restartx.top
