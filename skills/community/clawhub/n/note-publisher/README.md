# note-publisher

一个通用的「图文笔记发布」Skill：把本地 Markdown 文案 + 配图，通过**你指定的 MCP 发布后端**，一键发布为图文笔记。

只做两件事——**登录**、**发布**，不碰内容创作。

## 设计原则

- **不绑定任何平台**：本 Skill 不内置任何平台的发布能力，也不在文档里宣传具体平台。
- **配置驱动**：平台相关的后端地址由用户在运行时提供，公开发布包内零平台关联。
- **零依赖的编排层**：只负责解析 Markdown、调用 MCP、回查 `note_id`。

## 它解决什么

- 已有文案 + 配图，想自动推送到你用的图文/笔记社区
- 定时任务 / 自动化流水线里的「最后一公里」发布环节
- 避免手动上传多图、填标题、点标签的重复劳动

## 工作原理

1. 解析 Markdown（标题 / 正文 / 话题标签 / 配图路径）
2. 通过 **MCP（Streamable HTTP）** 调用你配置的后端服务
3. 完成登录态维护、图文上传、标签解析、发布后回查 `note_id`

## 前置条件

你需要自备一个 MCP 发布后端，且它暴露这三个工具：

| 工具 | 用途 |
|------|------|
| `check_login_status` | 查询登录状态 |
| `publish_content` | 发布（入参 `title` / `content` / `images` / `tags`） |
| `get_my_profile` | 拉取最近发布列表，用于回查 `note_id` |

> 后端是什么、从哪下载、怎么启动，由你的目标平台决定。本 Skill 不附带后端。

## 快速开始

### 1. 配置后端地址（二选一）

```bash
export MCP_PUBLISHER_URL="http://localhost:18060/mcp"
```

或在 Skill 目录放 `config.json`：

```json
{ "mcp_url": "http://localhost:18060/mcp" }
```

### 2. 检查登录

```bash
python3 scripts/publish.py check
```

首次登录通常需扫码（cookies 约 30 天有效期）。

### 3. 发布

```bash
# 单篇
python3 scripts/publish.py /path/to/note.md

# 批量
python3 scripts/publish.py --dir /path/to/posts/
```

### Markdown 输入格式

```markdown
# 标题（≤20 字）
正文第一段……（口语化，可带 emoji）

#话题1 #话题2 #话题3
---
## 配图（可选：表格列出图片路径，相对路径相对于 md 所在目录）
| # | 文件 |
|---|------|
| 1 | ./img/cover.jpg |
| 2 | ./img/chart.png |
```

- 标题：`# ` 开头的那行，超过 20 字会告警
- 正文：标题之后、`---` 之前的所有内容（含 `#话题` 行）
- 标签：从 `#话题` 自动提取、去重
- 图片：从表格里任意 `.jpg/.png/.jpeg/.webp` 路径提取，按顺序上传

## 环境变量

| 变量 | 说明 |
|------|------|
| `MCP_PUBLISHER_URL` | 后端 MCP 端点（也可用 `config.json` 替代） |

## 许可证

[MIT](./LICENSE)
