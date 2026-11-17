# Nexus Skills 配置与使用手册

通过一个 Python CLI 操作 Sonatype Nexus Repository 3，覆盖仓库浏览、组件搜索、上传/下载、删除。

---

## 一、环境要求

- Python 3.8 及以上
- `pip install requests`
- Nexus Repository **3.0 及以上**（REST API 路径 `/service/rest/v1`）

脚本会在执行命令前访问 `/service/rest/v1/status` 并读取 `Server` 头判断版本；
Nexus Repository 2 不在支持范围内，会给出明确的不兼容提示。确需跳过检查时，可设置
`NEXUS_SKIP_VERSION_CHECK=1` 或 `DEVOPS_SKILLS_SKIP_VERSION_CHECK=1`。

---

## 二、准备账号凭证

1. 使用具备相应权限的 Nexus 账号（如 `admin` 或配置了对应角色的用户）。
2. 推荐为自动化创建独立用户，并只授予所需仓库的读/写/删权限。
3. 也可在「用户 → User Token」生成 token 代替密码（若实例启用了该特性）。

---

## 三、配置连接信息（二选一）

### 方式 A：环境变量

```bash
export NEXUS_URL="https://nexus.example.com"
export NEXUS_USER="admin"
export NEXUS_PASS="你的密码或token"
```

### 方式 B：配置文件 `~/.devops-skills/nexus.json`

```json
{
  "url": "https://nexus.example.com",
  "user": "admin",
  "pass": "你的密码或token"
}
```

> `chmod 600 ~/.devops-skills/nexus.json`，切勿提交到仓库。

---

## 四、命令速查

| 功能 | 命令 |
| --- | --- |
| 列出所有仓库 | `python scripts/nexus_cli.py list-repos` |
| 搜索组件/资产 | `python scripts/nexus_cli.py search --repo maven-releases --name my-app` |
| 列出仓库组件 | `python scripts/nexus_cli.py list-components --repo raw-hosted --limit 100` |
| 上传文件到 raw 仓库 | `python scripts/nexus_cli.py upload-raw --repo raw-hosted --file ./build.tar.gz --directory /releases/v1` |
| 按 URL 下载资产 | `python scripts/nexus_cli.py download "https://nexus.example.com/repository/raw-hosted/releases/v1/build.tar.gz"` |
| 删除组件 | `python scripts/nexus_cli.py delete-component <component-id>` |

---

## 五、使用示例

**1. 发布一个构建产物到 raw 仓库**

```bash
python scripts/nexus_cli.py upload-raw \
  --repo raw-hosted \
  --file ./dist/app-1.2.0.tar.gz \
  --directory /releases/1.2.0
```

**2. 搜索并删除旧版本组件**

```bash
# 先搜索拿到 component id
python scripts/nexus_cli.py search --repo raw-hosted --name app
# 确认无误后删除
python scripts/nexus_cli.py delete-component <上一步返回的 id>
```

> 删除不可恢复，务必先用 search/list-components 核对 id。

---

## 六、常见问题

| 现象 | 原因与解决 |
| --- | --- |
| `NEXUS_URL, NEXUS_USER and NEXUS_PASS are required` | 未配置连接信息 |
| `HTTP 401` | 账号/密码错误 |
| `HTTP 403` | 账号对该仓库无对应权限 |
| `HTTP 404` | 仓库名拼写错误，或该实例不是 Nexus 3 |
| `unsupported Nexus version ...` | Nexus 版本低于 3.0，或目标是 Nexus 2 |
| 上传报 400 | 目标不是 raw 格式的 hosted 仓库；其它格式（maven/npm）需用对应上传字段 |

---

## 七、在 Claude / Claude Code 中使用

把 `nexus-skills` 目录放入 skills 目录后，用自然语言触发：

- “列一下 Nexus 上都有哪些仓库”
- “把 dist/app-1.2.0.tar.gz 传到 raw-hosted 的 /releases/1.2.0”
- “在 maven-releases 里搜一下 my-app”

---

## 八、技术支持与咨询

如果在 Nexus 仓库治理、制品发布、权限设计、DevOps 平台或研发效能建设中遇到问题，
欢迎联系 RestartX 获取支持与方案咨询：https://service.restartx.top/
