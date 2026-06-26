---
name: joplin-api
description: 通过 Joplin Data API（Clipper Server）查询和管理笔记、笔记本、标签。支持本地直连和 SSH 远程两种模式。包含读写删全部操作，写/删需用户确认。触发词："查 Joplin"、"Joplin 笔记"、"joplin search"、"create note in joplin" 等。
version: 1.4.1
metadata:
  openclaw:
    requires:
      env:
      - JOPLIN_TOKEN
      bins: []
    primaryEnv: JOPLIN_TOKEN
---

# Joplin Data API Skill

Access Joplin data via the local HTTP REST API (clipper server).

## 快速开始

### 初次设置

```bash
cd ~/.openclaw/skills/joplin-api
cp .env.example .env
nano .env   # 填入 api_token 和 joplin_host
```

**获取 Token：**
1. 打开 Joplin 桌面端
2. 选项/偏好设置 → Web Clipper
3. 复制 "Access password"（访问密码）
4. 粘贴到 `.env` 的 `api_token=` 后面

**配置 joplin_host：**
- Joplin 在本地 → 留空 `joplin_host=`
- Joplin 在远程 → 填 SSH 别名，如 `joplin_host=m1y`

### 测试连接

```bash
# Linux / macOS（推荐，速度快）
bash scripts/joplin.sh ping

# Windows / 无 bash 环境（Python 3 标准库，无需额外依赖）
python scripts/joplin.py ping

# 输出: ✅ Joplin Clipper Server running (JoplinClipperServer)
```

## 使用脚本

两个脚本功能完全一致，按环境选择：

- **`joplin.sh`** — Linux/macOS，bash 脚本，速度快
- **`joplin.py`** — Windows/无 bash 环境，Python 3 标准库，无需额外依赖

```bash
# bash 脚本
bash scripts/joplin.sh <command> [args...]

# Python 脚本
python scripts/joplin.py <command> [args...]
```

### 命令一览

| 命令 | 说明 | 示例 |
|------|------|------|
| `ping` | 测试连接 | `joplin.sh ping` |
| `get <id> [fields]` | 读取笔记（JSON） | `joplin.sh get <id>` |
| `note <id>` | 友好显示笔记（标题+正文预览） | `joplin.sh note <id>` |
| `create <folder> <title> <file>` | 在笔记本下创建笔记 | `joplin.sh create <folder_id> "标题" body.md` |
| `update <id> <file>` | 更新笔记正文 | `joplin.sh update <id> body.md` |
| `delete <id> [--permanent]` | 删除笔记（默认软删除） | `joplin.sh delete <id>` |
| `search <query> [fields] [limit]` | 搜索笔记 | `joplin.sh search "散热"` |
| `list <folder_id> [fields] [limit]` | 列出笔记本下笔记 | `joplin.sh list <folder_id>` |
| `folders [query]` | 列出/搜索笔记本 | `joplin.sh folders "r730"` |
| `tags [query]` | 列出/搜索标签 | `joplin.sh tags` |
| `tree` | 打印笔记本树形结构 | `joplin.sh tree` |

### 读取笔记

```bash
# 读取笔记（JSON 格式，标题+正文）
bash scripts/joplin.sh get <note_id>

# 友好显示（标题 + 正文预览，最多 50 行）
bash scripts/joplin.sh note <note_id>

# 只读标题
bash scripts/joplin.sh get <note_id> id,title
```

### 创建笔记

```bash
# 在指定笔记本下创建笔记（正文从文件读取）
bash scripts/joplin.sh create <folder_id> "笔记标题" /path/to/body.md
```

### 更新笔记

```bash
# 将文件内容写入笔记正文
bash scripts/joplin.sh update <note_id> <body_file>
```

### 删除笔记

```bash
# 软删除（移至回收站，可恢复）
bash scripts/joplin.sh delete <note_id>

# 永久删除
bash scripts/joplin.sh delete <note_id> --permanent
```

### 搜索笔记

```bash
# 搜索（只返回 id,title，快速）
bash scripts/joplin.sh search "散热"

# 限制结果数
bash scripts/joplin.sh search "散热" id,title 10
```

### 列出笔记本下的笔记

```bash
bash scripts/joplin.sh list <folder_id>
```

### 搜索/列出笔记本

```bash
# 搜索笔记本
bash scripts/joplin.sh folders "r730"

# 列出所有笔记本
bash scripts/joplin.sh folders
```

### 列出/搜索标签

```bash
# 列出所有标签
bash scripts/joplin.sh tags

# 搜索标签
bash scripts/joplin.sh tags "工作"
```

### 笔记本树形结构

```bash
# 以树形格式打印笔记本层级
bash scripts/joplin.sh tree
```

## 架构

Joplin data model:

```
Folders (笔记本/Notebooks)          Notes (笔记)
├── 顶层笔记本                       ├── 笔记属于某个 folder (parent_id → folder.id)
│   ├── 子笔记本 (parent_id→父ID)    ├── 笔记内容是 Markdown 格式 (body 字段)
│   │   ├── 孙笔记本                  └── 可附加标签(tags)、资源(resources)
│   │   │   └── ...无限层级
│   │   └── 孙笔记本
│   └── 子笔记本
└── 顶层笔记本
```

### Key Concepts

- **Folders（笔记本）** = 目录/文件夹，通过 `parent_id` 形成**无限层级的树形结构**。每个 folder 可以有任意多个子 folder，没有层级深度限制。顶级 folder 的 `parent_id` 为空或指向一个不在当前列表中的父 ID。
- **Notes（笔记）** = 内容载体，每条笔记通过 `parent_id` 归属到**一个且仅一个** folder 下。笔记内容是 Markdown 格式（`body` 字段）。
- **Tags（标签）** = 跨笔记本的分类标记，可附加到任意笔记上，不受 folder 层级限制。
- **Resources（资源）** = 附件文件（图片、文档等），可关联到笔记上。

### parent_id 关系说明

| 对象 | parent_id 含义 | 示例 |
|------|---------------|------|
| Folder | 指向父 folder ID；顶级 folder 为空/根 | `parent_id: "abc123..."` 表示该笔记本是 `abc123...` 的子目录 |
| Note | 指向所属 folder ID | `parent_id: "folder_xyz"` 表示该笔记在 `folder_xyz` 笔记本下 |

## 配置

### .env 文件

```ini
# Token — 从 Joplin 桌面端获取
api_token=xxx

# Joplin 所在主机（SSH 别名；留空表示本地 localhost）
joplin_host=

# 如果 joplin_host 留空，用下面的 base_url
base_url=http://localhost:41184
```

**注意：**
- `api_token` 不要加引号
- `joplin_host` 填 SSH 别名（如 `m1y`），脚本会通过 SSH 转发请求到远程 Joplin
- 如果 Joplin 在本地，留空 `joplin_host=` 或注释掉
- `base_url` 仅在本地模式使用，默认 `http://localhost:41184`

## 铁律（Iron Rules）

1. **GET free** — 读取笔记、笔记本、标签可自由执行，无需额外批准
2. **写/删操作必须经过用户明确批准** — POST（创建）、PUT（更新）、DELETE（删除）均为高影响操作：
   - **创建**：展示标题、内容摘要、目标笔记本，确认后再执行
   - **更新**：展示笔记标题、当前内容摘要、拟修改内容，确认后再执行
   - **删除**：展示笔记标题和 ID，说明操作后果（移至回收站/永久删除），确认后再执行
3. **默认软删除** — 删除笔记时默认移至回收站（可恢复）；除非用户明确说"永久删除"，否则不加 `permanent=1`
4. **Search without body first** — 搜索时用 `fields=id,title` 提速，找到目标后再获取 `body`
5. **Use parent_id for hierarchy** — folders 和 notes 都通过 `parent_id` 构建树形关系
6. **Remote mode warning** — 当 `joplin_host` 非空时，所有笔记内容会经 SSH 发送到远程主机再访问 Joplin。执行写操作前先告知用户"当前走远程模式，目标主机：$HOST"

## 安全说明

### 运行模式
- **本地模式**（默认）：请求直连 `localhost:41184`，数据不离开本机
- **远程 SSH 模式**（`joplin_host` 非空）：请求通过 SSH 隧道转发到远程主机，再由远程主机访问本地 Joplin。笔记内容和 API token 会经 SSH 链路传输

### API Token 安全
- Token 通过 URL 查询参数传递（`?token=xxx`），这是 Joplin Clipper API 的设计
- 注意：URL 可能被记录在 shell 历史、SSH 日志、代理日志中
- 建议：`.env` 文件权限设为 `600`（`chmod 600 .env`），并通过 `.gitignore` 排除

### 删除操作警告
- `delete <id>` 默认**软删除**（移至回收站，可在 Joplin 中恢复）
- `delete <id> --permanent` 为**永久删除**（不可恢复），使用前务必确认笔记标题
- AI 驱动场景下，建议先 `note <id>` 预览再删除
