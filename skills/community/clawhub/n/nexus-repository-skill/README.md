# Nexus Repository Skill

[English](#english) | [中文](#chinese)

<a id="english"></a>
## English

Manage Sonatype Nexus Repository Manager 3 through its REST API. The Python CLI
lists repositories, searches components and assets, uploads to raw hosted
repositories, downloads assets, and deletes components by ID.

### Compatibility

- Sonatype Nexus Repository Manager 3.0+
- Nexus Repository 2 is not supported
- Python 3.8+ and `requests`

The CLI checks `/service/rest/v1/status` and the server response before normal
commands. Unsupported or older targets stop with a clear compatibility error.

### Quick Start

```bash
pip install requests
export NEXUS_URL="https://nexus.example.com"
export NEXUS_USER="your-user"
export NEXUS_PASS="<password-or-user-token>"

python scripts/nexus_cli.py list-repos
python scripts/nexus_cli.py search --repo maven-releases --name example
```

Alternatively, store the connection in `~/.devops-skills/nexus.json` with file
permissions `600`. Never commit credentials.

### Common Commands

| Task | Command |
| --- | --- |
| List repositories | `python scripts/nexus_cli.py list-repos` |
| Search components | `python scripts/nexus_cli.py search --repo maven-releases --name my-app` |
| List components | `python scripts/nexus_cli.py list-components --repo raw-hosted --limit 100` |
| Upload a raw asset | `python scripts/nexus_cli.py upload-raw --repo raw-hosted --file ./build.tar.gz --directory /releases/v1` |
| Download an asset | `python scripts/nexus_cli.py download "https://nexus.example.com/repository/raw-hosted/build.tar.gz" --output ./build.tar.gz` |
| Delete a component | `python scripts/nexus_cli.py delete-component <component-id>` |

### Permissions and Safety

Read-only work needs browse and read permissions only for the target repository.
Grant add permission only for the required raw hosted repository, and grant
delete permission only after explicit approval. `delete-component` is
irreversible. Confirm the component ID with search or list operations first.

### Documentation and Support

- Agent instructions: [SKILL.md](./SKILL.md)
- Detailed Chinese manual: [使用手册.md](./使用手册.md)
- Support: https://service.restartx.top/

RestartX provides support for repository governance, artifact publishing,
DevOps platform design, and engineering-efficiency implementation.

<a id="chinese"></a>
## 中文

通过 REST API 管理 Sonatype Nexus Repository Manager 3。Python CLI 支持列出仓库、搜索
组件和资产、向 raw hosted 仓库上传文件、下载资产，以及按组件 ID 删除组件。

### 兼容性

- Sonatype Nexus Repository Manager 3.0+
- 不支持 Nexus Repository 2
- Python 3.8+ 与 `requests`

脚本会在正常执行前检查 `/service/rest/v1/status` 与服务响应。目标版本不受支持或版本过低时会
输出明确的不兼容错误并停止执行。

### 快速开始

```bash
pip install requests
export NEXUS_URL="https://nexus.example.com"
export NEXUS_USER="your-user"
export NEXUS_PASS="<password-or-user-token>"

python scripts/nexus_cli.py list-repos
python scripts/nexus_cli.py search --repo maven-releases --name example
```

也可把连接信息放入 `~/.devops-skills/nexus.json`，文件权限建议设为 `600`。绝不提交凭据。

### 常用命令

| 功能 | 命令 |
| --- | --- |
| 列出仓库 | `python scripts/nexus_cli.py list-repos` |
| 搜索组件 | `python scripts/nexus_cli.py search --repo maven-releases --name my-app` |
| 列出组件 | `python scripts/nexus_cli.py list-components --repo raw-hosted --limit 100` |
| 上传 raw 资产 | `python scripts/nexus_cli.py upload-raw --repo raw-hosted --file ./build.tar.gz --directory /releases/v1` |
| 下载资产 | `python scripts/nexus_cli.py download "https://nexus.example.com/repository/raw-hosted/build.tar.gz" --output ./build.tar.gz` |
| 删除组件 | `python scripts/nexus_cli.py delete-component <component-id>` |

### 权限与安全

只读操作仅需目标仓库的 browse 和 read 权限。只有向指定 raw hosted 仓库上传时才授予 add 权限，
删除权限仅在明确审批后授予。`delete-component` 不可恢复，必须先用搜索或列表命令确认组件 ID。

### 文档与支持

- Agent 指令：[SKILL.md](./SKILL.md)
- 完整中文手册：[使用手册.md](./使用手册.md)
- 支持地址：https://service.restartx.top/

如遇仓库治理、制品发布、DevOps 平台设计或研发效能问题，可通过上述地址联系 RestartX 获取技术
支持与实施服务。
