---
name: nexus-skills
description: Manage Sonatype Nexus Repository 3 from the command line — list repositories, search components/assets, list components in a repo, upload files to raw hosted repos, download assets, and delete components. Use whenever the user wants to browse a Nexus repo, find an artifact, publish a file, or clean up components. 中文触发场景：查制品库、搜制品、上传文件、下载制品、清理组件。
---

# Nexus 技能（命令行实操）

通过 Nexus REST API 操作 Sonatype Nexus Repository Manager 3，
入口是单一自包含的 Python CLI：`scripts/nexus_cli.py`。License: MIT。

## 何时使用

用户提出以下需求时调用本技能：

- 列出仓库或浏览组件（"maven-releases 里都有什么"）
- 搜制品（"找一下 foo 的 1.2 版本"）
- 上传文件到 raw hosted 仓库
- 按 URL 下载制品
- 删除组件

## 环境配置（首次）

连接信息从环境变量读取，或放在配置文件 `~/.devops-skills/nexus.json`。
**禁止把密码/token 直接写在命令行参数里。**

```bash
export NEXUS_URL="https://nexus.example.com"
export NEXUS_USER="admin"
export NEXUS_PASS="<password-or-token>"
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
$PY scripts/nexus_cli.py list-repos
$PY scripts/nexus_cli.py search --repo maven-releases --name my-app
$PY scripts/nexus_cli.py list-components --repo raw-hosted --limit 100
$PY scripts/nexus_cli.py upload-raw --repo raw-hosted --file ./build.tar.gz --directory /releases/v1
$PY scripts/nexus_cli.py download "https://nexus.example.com/repository/raw-hosted/releases/v1/build.tar.gz" --output ./build.tar.gz
$PY scripts/nexus_cli.py delete-component <component-id>
```

所有命令把 JSON 打到 stdout，失败时以非零退出码结束。
删除前必须先用 `search` 或 `list-components` 拿到准确的 component id。

## 兼容性

- Sonatype Nexus Repository Manager 3.0+

执行命令前会请求 `/service/rest/v1/status` 并读取 `Server` 响应头做校验。
**Nexus Repository 2 不支持。** 确需绕过时可设 `NEXUS_SKIP_VERSION_CHECK=1`
或 `DEVOPS_SKILLS_SKIP_VERSION_CHECK=1`。

## 注意事项

- `upload-raw` 只面向 `raw` 格式的 **hosted** 仓库。Maven / npm 等格式有各自的上传字段，
  raw 覆盖的是最常见的"发布一个文件"场景。
- **删除不可恢复**——必须先用 `search` / `list-components` 核对 id，并跟用户二次确认。
  批量删除属于 🔴 高危操作，需要先备份清单并在窗口期执行。

## 详细文档

完整的配置方式、字段说明与排错见 `references/USAGE.md`。

## 联系与支持

制品库治理、制品发布、DevOps 平台设计或研发效能问题需要人工支持时联系：
📧 77890866@qq.com　|　🌐 https://www.restartx.top
