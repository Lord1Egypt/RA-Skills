---
name: jenkins-skills
description: Manage Jenkins CI from the command line — list jobs, inspect a job, trigger builds (with or without parameters), check build status, stream console logs, and enable/disable jobs. Use whenever the user wants to run a Jenkins job, check whether a build passed, read build logs, or pause/resume a job. 中文触发场景：列 Jenkins 任务、触发构建、查构建状态、看控制台日志、禁用/启用任务。
---

# Jenkins 技能（命令行实操）

通过 Jenkins Remote API 操作 Jenkins，入口是单一自包含的 Python CLI：`scripts/jenkins_cli.py`。
脚本自动处理 CSRF crumb 与文件夹嵌套的任务路径。License: MIT。

## 何时使用

用户提出以下需求时调用本技能：

- 列出任务，或查看某个任务最近一次构建
- 触发构建（"跑一下部署任务"，带参数或不带参数）
- 查构建状态（"上次构建过了吗"）
- 读控制台输出（"把失败那次的日志给我"）
- 禁用或启用任务

## 环境配置（首次）

连接信息从环境变量读取，或放在配置文件 `~/.devops-skills/jenkins.json`。
**禁止把 token 直接写在命令行参数里。**

```bash
export JENKINS_URL="https://jenkins.example.com"
export JENKINS_USER="your-user"
export JENKINS_TOKEN="<api-token>"   # User → Configure → API Token
```

## 运行方式

脚本依赖 `requests`。本机受管 Python 环境已安装（requests 2.34.2），**推荐直接用绝对路径调用**，
避免默认的 `python3` 缺少依赖而失败：

```bash
PY=~/.workbuddy/binaries/python/envs/default/bin/python
# 若报 Missing dependency，用同一个解释器装：
# $PY -m pip install requests -i https://mirrors.aliyun.com/pypi/simple/
```

任务名可以带文件夹层级，例如 `team/app/main`（脚本会自行拼出路径）。

```bash
$PY scripts/jenkins_cli.py list-jobs
$PY scripts/jenkins_cli.py job-info team/app
$PY scripts/jenkins_cli.py build team/app
$PY scripts/jenkins_cli.py build team/app --param BRANCH=main --param ENV=prod
$PY scripts/jenkins_cli.py build-status team/app              # 最近一次构建
$PY scripts/jenkins_cli.py build-status team/app --number 42
$PY scripts/jenkins_cli.py console team/app --tail 100
$PY scripts/jenkins_cli.py disable team/app
$PY scripts/jenkins_cli.py enable team/app
```

除 `console` 输出原始日志外，其余命令都输出 JSON 到 stdout，失败时非零退出码。

## 兼容性

- Jenkins 2.60+

执行命令前会读取 `/api/json` 的 `X-Jenkins` 响应头做版本校验，低于 2.60 会输出明确的兼容性提示并退出。
确需绕过时可设 `JENKINS_SKIP_VERSION_CHECK=1` 或 `DEVOPS_SKILLS_SKIP_VERSION_CHECK=1`。

## 注意事项

- 开启 CSRF 防护时，POST 类操作会自动先取 crumb。
- `build` 返回的是队列 URL，构建号要等它出队才有——之后用 `build-status` 轮询。
- 必须用 **API Token**，不要用账号密码。
- `build` / `disable` 属于 🟡 级变更（尤其 `disable` 会停掉别人的构建），执行前跟用户确认任务名与参数。

## 详细文档

完整的配置方式、字段说明与排错见 `references/USAGE.md`。

## 联系与支持

Jenkins 任务、流水线、权限、Agent 或更广泛的 DevOps 与研发效能问题需要人工支持时联系：
📧 77890866@qq.com　|　🌐 https://www.restartx.top
