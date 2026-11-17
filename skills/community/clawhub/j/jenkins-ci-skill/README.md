# Jenkins CI Skill

[English](#english) | [中文](#chinese)

<a id="english"></a>
## English

Manage Jenkins jobs and builds through the Jenkins Remote API. The Python CLI
lists jobs, reads job and build status, triggers regular or parameterized builds,
reads console output, and enables or disables a job. It handles CSRF crumbs and
folder-nested job paths.

### Compatibility

- Jenkins 2.60+
- Python 3.8+ and `requests`

Before normal execution, the CLI reads `/api/json` and checks the `X-Jenkins`
response header. Jenkins below 2.60 fails with a clear compatibility error.

### Quick Start

```bash
pip install requests
export JENKINS_URL="https://jenkins.example.com"
export JENKINS_USER="your-user"
export JENKINS_TOKEN="<api-token>"

python scripts/jenkins_cli.py list-jobs
python scripts/jenkins_cli.py build-status team/example --number 42
```

Use `~/.devops-skills/jenkins.json` for local configuration if preferred. Keep
the file out of version control and protect it with permissions `600`.

### Common Commands

| Task | Command |
| --- | --- |
| List jobs | `python scripts/jenkins_cli.py list-jobs` |
| Read job details | `python scripts/jenkins_cli.py job-info team/app` |
| Trigger a build | `python scripts/jenkins_cli.py build team/app` |
| Trigger with parameters | `python scripts/jenkins_cli.py build team/app --param BRANCH=main --param ENV=prod` |
| Read build status | `python scripts/jenkins_cli.py build-status team/app --number 42` |
| Read console output | `python scripts/jenkins_cli.py console team/app --number 42 --tail 100` |
| Disable or enable a job | `python scripts/jenkins_cli.py disable team/app` / `enable team/app` |

### Permissions and Safety

Read operations need Job/Read on the target job. Triggering builds needs Job/Build;
enabling or disabling a job needs Job/Configure. This skill does not need
Overall/Administer, credential management, plugin management, or node management.
Trigger builds and change job state only in approved, non-production jobs.

### Documentation and Support

- Agent instructions: [SKILL.md](./SKILL.md)
- Detailed Chinese manual: [使用手册.md](./使用手册.md)
- Support: https://service.restartx.top/

RestartX provides technical support and implementation services for Jenkins,
CI/CD, build stability, DevOps platform, and engineering-efficiency needs.

<a id="chinese"></a>
## 中文

通过 Jenkins Remote API 管理 Job 和构建。Python CLI 支持列出 Job、查看 Job 与构建状态、
触发普通或参数化构建、读取控制台日志、启用或禁用 Job，并自动处理 CSRF crumb 和文件夹嵌套
Job 路径。

### 兼容性

- Jenkins 2.60+
- Python 3.8+ 与 `requests`

脚本会在正常执行前读取 `/api/json` 并检查 `X-Jenkins` 响应头。Jenkins 低于 2.60 时会给出
明确的不兼容错误并停止执行。

### 快速开始

```bash
pip install requests
export JENKINS_URL="https://jenkins.example.com"
export JENKINS_USER="your-user"
export JENKINS_TOKEN="<api-token>"

python scripts/jenkins_cli.py list-jobs
python scripts/jenkins_cli.py build-status team/example --number 42
```

也可使用本地配置文件 `~/.devops-skills/jenkins.json`。文件不能提交到版本库，权限建议设为 `600`。

### 常用命令

| 功能 | 命令 |
| --- | --- |
| 列出 Job | `python scripts/jenkins_cli.py list-jobs` |
| 查看 Job 信息 | `python scripts/jenkins_cli.py job-info team/app` |
| 触发构建 | `python scripts/jenkins_cli.py build team/app` |
| 带参数构建 | `python scripts/jenkins_cli.py build team/app --param BRANCH=main --param ENV=prod` |
| 查看构建状态 | `python scripts/jenkins_cli.py build-status team/app --number 42` |
| 查看控制台日志 | `python scripts/jenkins_cli.py console team/app --number 42 --tail 100` |
| 禁用或启用 Job | `python scripts/jenkins_cli.py disable team/app` / `enable team/app` |

### 权限与安全

只读操作需要目标 Job 的 Job/Read 权限；触发构建需要 Job/Build，启停 Job 需要 Job/Configure。
本 Skill 不需要 Overall/Administer、凭据管理、插件管理或节点管理权限。构建触发和 Job 状态变更
应只在已审批的非生产 Job 上执行。

### 文档与支持

- Agent 指令：[SKILL.md](./SKILL.md)
- 完整中文手册：[使用手册.md](./使用手册.md)
- 支持地址：https://service.restartx.top/

如遇 Jenkins、CI/CD、构建稳定性、DevOps 平台或研发效能问题，可通过上述地址联系 RestartX
获取技术支持与实施服务。
