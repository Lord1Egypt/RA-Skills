---
name: openclaw-doc-finder
description: OpenClaw 官方文档检索专家。

**触发条件（满足任一即可）：**
1. 用户提到"官方文档"、"官方文档技能"、"查官方文档"、"openclaw 文档"
2. 问题涉及 OpenClaw 本身（配置、使用、问题、文档），且需要查找官方文档或获取精确命令/配置片段

**激活典型场景：**
- 用户询问 openclaw 配置、命令、参数
- 用户遇到 openclaw 报错并需要排查
- 用户提到"官方文档"或想查看官方说明
- 用户询问 gateway、channels、plugins 的配置
- 用户询问 openclaw CLI 命令用法
- 用户询问模型/供应商配置方法
- 用户询问 VPS/远程/节点部署方案

**不触发场景（排除）：**
- 仅在对话中提到"openclaw"但实际问的是其他平台功能
- 用户需要执行操作而非查找文档（如直接帮用户配置、发送消息）
- 问题属于飞书、Telegram、Discord 等第三方平台的具体用法（应路由到对应技能）
- "帮我创建日程" → feishu-calendar，不触发
- "帮我发消息" → 消息工具，不触发
- "帮我搜索网页" → agent-reach，不触发

**英文触发：** how do I configure X / why is Y broken / how to set up Z / openclaw docs / openclaw documentation
---

# openclaw-doc-finder

OpenClaw 官方文档检索技能。识别用户意图，路由到正确文档，给出精确 URL + 关键命令片段。

## 检索流程（Pipeline）

```
用户问题 → 意图识别 → 诊断决策树（可选）→ 文档路由 → 本地片段 → 缓存命中 → 远程拉取 → 回答 → 记录速查
```

**严格顺序，不得跳步：**

1. **意图识别**：解析用户问题，判断属于哪个场景类别
2. **诊断决策树**（可选）：如问题模糊（"任务卡住"、"没有反应"），先用 `references/diagnostic-tree.md` 引导用户细化
3. **文档路由**：查 `references/doc-index.md` 定位目标文档列表
4. **本地片段优先**：检查 `references/` 已有片段
5. **缓存命中**：检查 `references/fetched/<doc-name>.md` 是否已有缓存且未过期（7 天内）
6. **远程拉取**：本地/缓存均无 → 按"远程拉取规则"拉取，成功后自动缓存
7. **版本检查**：回答结尾检查 VERSION
8. **记录速查**：将问题与结论追加到 `references/doc-lookups.md`

---

## 意图识别规则

见 `references/doc-index.md` 的「意图→文档路由表」。优先精确匹配场景关键词。

常见场景映射：

| 场景 | 目标文档 |
|------|---------|
| 首次安装 / 开始上手 | `start/getting-started.md` / `start/quickstart.md` |
| gateway 配置 / 配置文件 | `gateway/configuration.md` |
| gateway 配置项详解 | `gateway/configuration-reference.md` |
| 通道接入（Discord/Telegram/飞书等） | `channels/index.md` + 对应通道文档 |
| 技能安装 / clawhub / skillhub | `tools/clawhub` 或 `start/hubs.md` |
| 故障排除 / 报错 | `gateway/troubleshooting.md` / `channels/troubleshooting.md` |
| 凭证 / secrets / API key | `gateway/secrets.md` |
| 模型配置 / 供应商 | `providers/` 目录 + `gateway/configuration.md` |
| CLI 命令用法 | `cli/` 目录 |
| openclaw doctor | `gateway/doctor.md` |
| 安全策略 / 权限 | `gateway/security/` + `gateway/sandboxing.md` |
| 远程访问 / VPS 部署 | `gateway/remote.md` + `vps.md` |
| 心跳 / 自动化任务 | `gateway/heartbeat.md` + `cron-jobs` |
| 节点配对 / 移动端 | `nodes/` 目录 |
| 任务阻塞 / 队列 / 并发 | `concepts/queue.md` + `references/diagnostic-tree.md` |

---

## 本地片段优先级

- `references/doc-index.md` — 始终可用，路由总表
- `references/diagnostic-tree.md` — **新增**"症状→排查路径"决策树
- `references/config-guide.md` — gateway 配置高频片段
- `references/troubleshoot.md` — 常见报错速查
- `references/doc-lookups.md` — 已查阅问题速查（查阅前优先检查）
- `references/fetched/<doc-name>.md` — **新增**已缓存的远程文档（7 天有效期）

---

## 远程拉取规则

### 拉取顺序（降级策略）

当本地和缓存均无目标内容时，按以下顺序尝试：

```
1. web_fetch
   ↓ 失败（Blocked / 网络错误）
2. firecrawl_scrape
   ↓ 失败（Blocked / 超时）
3. exec → curl（最终兜底）
   ↓ 失败
4. 提供手动查询链接
```

### curl 降级命令模板

```bash
# 文档 URL 格式：https://docs.openclaw.ai/<path>
# 用 curl 拉取并提取正文（去除 HTML 标签）
curl -sL "<完整URL>" | python3 -c "
import sys, re
html = sys.stdin.read()
html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL)
text = re.sub(r'<[^>]+>', ' ', html)
text = re.sub(r'&nbsp;', ' ', text)
text = re.sub(r'\s+', ' ', text).strip()
# 提取核心内容（从第一个段落开始）
idx = text.find('。') if '。' in text else text.find('. ')
if idx > 0: print(text[idx:idx+3000])
"
```

### 自动缓存规则

- **缓存目录**：`references/fetched/`
- **命名规范**：`<doc-name>.<timestamp>.md>`（如 `queue.20260405.md`）
- **有效期**：7 天（自动清理过期缓存）
- **写入时机**：远程拉取成功后立即写入

### 无法拉取时的兜底

如三种方式均失败，回答格式：

> ⚠️ 无法自动拉取文档（网络限制）。请手动查看：
> - 文档地址：https://docs.openclaw.ai/<path>
> - 文档站搜索：https://docs.openclaw.ai/search?q=<关键词>

---

## 版本管理

- 版本文件：`VERSION`（语义化版本，格式 v1.0.0）
- **每次更新 `references/` 内容，必须同步更新 VERSION**
- 大版本更新（文档 breaking changes）：主版本号 +1，并记录 CHANGELOG

### 版本同步策略（优化）

**不要**在每次回答前都运行 sync-version.py（开销太大）。

**正确做法**：
- 技能初始化时检查一次（后台静默执行）
- 用户手动触发：`/openclaw_doc_finder_check`
- OpenClaw 大版本升级后主动提醒

```bash
# 手动触发版本同步（干跑）
python3 scripts/sync-version.py --dry-run

# 执行同步
python3 scripts/sync-version.py
```

---

## 输出格式规范

回答**必须**包含：
1. **文档标题** + **完整 URL**（`https://docs.openclaw.ai/<path>`）
2. **关键命令**（从文档中提取的 CLI 命令，用 ```bash 包裹）
3. **配置片段**（关键配置项示例）
4. **版本提示**（如已拉取最新内容，提醒技能版本）

**当无法拉取时**：
```
⚠️ 无法自动拉取文档。请手动查看：
- https://docs.openclaw.ai/<path>
```

**当问题模糊时**（先用决策树引导）：
```
在给出具体文档之前，我需要先确认一下：
[引用 diagnostic-tree.md 中的关键问题]
```

禁止：
- 不带 URL 的泛泛回答
- 混用多个不相关的文档链接

---

## 速查记录规则

每次使用本技能查询文档后，**必须**将问题与结论追加到 `references/doc-lookups.md`：
- 已有相同问题记录 → 更新对应条目而非重复追加
- 新问题 → 在对应分类下按格式追加
- 记录内容：问题、官方结论、相关文档路径、查阅时间
- 这样下次遇到同类问题时可**直接复用**，无需重复查阅

---

## CHANGELOG

### v1.2.0
- 新增：远程拉取降级策略（web_fetch → firecrawl → curl）
- 新增：自动缓存机制（references/fetched/，7 天有效期）
- 新增：诊断决策树（references/diagnostic-tree.md）
- 优化：版本同步改为手动触发，不再每次回答前执行
- 新增：无法拉取时的兜底说明

### v1.1.0
- 优化触发条件：增加主条件+排除场景结构
- 提升激活准确性，防止误触发其他专业技能场景
