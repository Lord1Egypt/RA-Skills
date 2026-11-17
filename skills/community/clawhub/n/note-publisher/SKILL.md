---
name: note-publisher
slug: note-publisher
displayName: 图文笔记发布
version: 1.0.0
description: |
  通用「图文笔记发布」框架：把本地 markdown 文案 + 配图，通过你指定的 MCP 发布后端，一键发布为图文笔记（含 note_id 回查）。
  只负责登录与发布编排，不碰内容创作；不绑定任何特定平台，后端地址由用户自己配置。
  触发词：图文笔记发布、笔记发布、社交笔记发布、登录发布、发布失败重试。
description_zh: 图文笔记发布（通用 MCP 后端）
description_en: Publish image-text notes via a user-configured MCP backend
disable: false
agent_created: true
---

# note-publisher — 图文笔记发布

把本地 markdown 文案 + 配图，通过**你指定的 MCP 发布后端**，一键发布为图文笔记。

只做两件事：**登录**、**发布**。不碰内容创作。

> ⚠️ **本 skill 是纯通用框架，不内置任何平台的发布能力。**
> 你必须先提供一个暴露 `check_login_status` / `publish_content` / `get_my_profile` 这三个工具的 MCP 发布服务地址，配置好之后才能工作。没有后端地址 = 无法发布。

## 第一步：配置 MCP 发布后端（必做）

本 skill 通过环境变量 `MCP_PUBLISHER_URL` 读取你的后端地址：

```bash
export MCP_PUBLISHER_URL="http://localhost:18060/mcp"
```

也可以把地址写进 `config.json`（放在本 skill 目录下，脚本会优先读它）：

```json
{ "mcp_url": "http://localhost:18060/mcp" }
```

> 后端是什么、从哪下载、怎么启动，由**你的目标平台**决定——任何暴露上述三个 MCP 工具的发布服务都能接。参考 `config.example.json`。

配置好后自检：

```bash
python3 scripts/publish.py check
```

## 第二步：发布

```bash
# 发布单篇（标题缺省取 md 第一行 `# 标题`，可用 --title 覆盖）
python3 scripts/publish.py /path/to/note.md

# 批量发布目录下所有 .md
python3 scripts/publish.py --dir /path/to/posts/
```

脚本内部走 MCP Streamable HTTP（长超时 300s），发布后自动调个人主页回查并打印 `NOTE_ID`。

### markdown 输入格式约定

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

- **标题**：`# ` 开头的那行；超过 20 字会告警，建议 `--title` 传入短标题。
- **正文**：标题之后、`---` 分隔线之前的所有内容（含 `#话题` 行）。
- **标签**：从正文里的 `#话题` 自动提取；重复自动去重。
- **图片**：从表格里任意 `.jpg/.png/.jpeg/.webp` 路径提取，按出现顺序上传；至少 1 张。

## 接入你自己的后端

任何后端，只要满足下面三点即可接入，无需改本 skill：

1. 暴露 `check_login_status` 工具（返回登录状态）
2. 暴露 `publish_content` 工具（入参 `title` / `content` / `images` / `tags`）
3. 暴露 `get_my_profile` 工具（返回最近发布的笔记列表，用于回查 `note_id`）

## Pitfalls（踩过的坑）

1. **后端版本要足够新**：旧版发布时会报"没有找到发布 TAB - 上传图文"，是创作者中心改版、旧选择器失效。
2. **登录二维码只调一次**：后端 `get_login_qrcode` 有单会话约束，「开新的取消旧的」。连续调用会让用户扫到被取代的旧码。
3. **配图路径要精确到扩展名**：表格里路径后常带全角括号尺寸注释 `（1920×1280）`，解析用 `[\w\-./]+\.(?:jpg|png|jpeg|webp)` 精确匹配，别用 `[^\s）)]+`（会连括号内容一起吞 → 图片文件不存在 → 发布卡死超时）。
4. **发布超时**：单篇约 2 分钟（上传多图 + 填标题正文 + 点标签）。本脚本自带 300s 长超时。
5. **note_id 不在 publish 返回值里**：`publish_content` 成功只回"内容发布成功"，note_id 要从个人主页按标题匹配，脚本已内置。
6. **cookies 服务端会提前失效**：客户端 expires 可能显示很久，但服务端长期不用会踢。自动化开始先 `check`，未登录先扫码再继续。

## 验证清单

- [ ] 已配置 `MCP_PUBLISHER_URL`（或 `config.json`）
- [ ] `publish.py check` 返回「已登录」
- [ ] 标题 ≤ 20 字、正文 ≤ 1000 字、图片 ≥ 1 张
- [ ] 发布后拿到 `NOTE_ID`，回查时标题能对上

## 依赖

- 一个自备的 MCP 发布后端（本 skill 不自带）。本 skill 只负责流程编排 + 解析 + 长超时调用。
