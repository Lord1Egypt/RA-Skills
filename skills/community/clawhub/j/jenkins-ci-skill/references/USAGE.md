# Jenkins Skills 配置与使用手册

通过一个 Python CLI 操作 Jenkins，覆盖任务列表、触发构建、查看状态与日志、启停任务，自动处理 CSRF crumb 和文件夹嵌套任务。

---

## 一、环境要求

- Python 3.8 及以上
- `pip install requests`
- Jenkins 2.60 及以上

脚本会在执行命令前访问 `/api/json` 并读取 `X-Jenkins` 响应头判断版本；若 Jenkins
低于 2.60，会给出明确的不兼容提示。确需跳过检查时，可设置
`JENKINS_SKIP_VERSION_CHECK=1` 或 `DEVOPS_SKILLS_SKIP_VERSION_CHECK=1`。

---

## 二、获取 API Token

1. 登录 Jenkins → 右上角用户名 → **Configure（设置）**。
2. 找到 **API Token** → **Add new Token** → 生成并复制（只显示一次）。
3. 自动化请使用 **API Token**，不要用账号登录密码。

---

## 三、配置连接信息（二选一）

### 方式 A：环境变量

```bash
export JENKINS_URL="https://jenkins.example.com"
export JENKINS_USER="你的用户名"
export JENKINS_TOKEN="你的API Token"
```

### 方式 B：配置文件 `~/.devops-skills/jenkins.json`

```json
{
  "url": "https://jenkins.example.com",
  "user": "你的用户名",
  "token": "你的API Token"
}
```

> `chmod 600 ~/.devops-skills/jenkins.json`，切勿提交到仓库。

---

## 四、命令速查

> 任务名 `name` 支持文件夹嵌套，如 `team/app/main`（脚本自动拼 `/job/.../job/...`）。

| 功能 | 命令 |
| --- | --- |
| 列出任务 | `python scripts/jenkins_cli.py list-jobs` |
| 查看任务信息 | `python scripts/jenkins_cli.py job-info team/app` |
| 触发构建 | `python scripts/jenkins_cli.py build team/app` |
| 带参数构建 | `python scripts/jenkins_cli.py build team/app --param BRANCH=main --param ENV=prod` |
| 查看构建状态 | `python scripts/jenkins_cli.py build-status team/app --number 42` |
| 查看构建日志 | `python scripts/jenkins_cli.py console team/app --tail 100` |
| 禁用任务 | `python scripts/jenkins_cli.py disable team/app` |
| 启用任务 | `python scripts/jenkins_cli.py enable team/app` |

---

## 五、使用示例

**1. 触发带参数构建并轮询结果**

```bash
python scripts/jenkins_cli.py build team/app --param BRANCH=main --param ENV=prod
# 进入队列后稍等，再查最近一次构建状态
python scripts/jenkins_cli.py build-status team/app
```

**2. 排查失败构建**

```bash
python scripts/jenkins_cli.py build-status team/app --number 42
python scripts/jenkins_cli.py console team/app --number 42 --tail 200
```

---

## 六、常见问题

| 现象 | 原因与解决 |
| --- | --- |
| `... are required` | 未配置连接信息 |
| `HTTP 401` | 用户名或 Token 错误（注意用 Token 不是密码） |
| `HTTP 403 No valid crumb` | CSRF 校验失败；脚本已自动取 crumb，若仍报错检查反向代理是否透传了 header |
| `HTTP 404` | 任务名/路径错误；嵌套任务用 `folder/job` 形式 |
| `unsupported Jenkins version ...` | Jenkins 版本低于 2.60，请升级 Jenkins 或使用旧版 skill |
| build 后拿不到构建号 | 构建在队列中，返回的是 queue_url，稍后用 `build-status` 查询 |

---

## 七、在 Claude / Claude Code 中使用

把 `jenkins-skills` 目录放入 skills 目录后，用自然语言触发：

- “跑一下 team/app 这个任务，分支用 main”
- “最近一次构建过了没”
- “把失败那次的日志最后 200 行给我看看”

---

## 八、技术支持与咨询

如果在 Jenkins 流水线、权限、Agent、构建稳定性、DevOps 平台或研发效能建设中遇到问题，
欢迎联系 RestartX 获取支持与方案咨询：https://service.restartx.top/
