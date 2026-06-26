---
name: openrouter-rankings-screenshot
description: "Capture OpenRouter Rankings (all Categories scenarios + page sections), create Feishu doc with screenshots and sales summary. Use for openrouter.ai/rankings daily digest or Feishu push."
---

# OpenRouter Rankings 截图 → 飞书文档

抓取 [OpenRouter Rankings](https://openrouter.ai/rankings)，**Categories 下每个场景各截一张图**，并生成**销售可读的文字总结**，写入**新建飞书文档**后把文档链接发给用户。

## 默认配置

| 项 | 值 |
|---|---|
| 页面 | `https://openrouter.ai/rankings` |
| 输出目录 | `~/.openclaw/cache/openrouter-rankings/YYYY-MM-DD/` |
| 飞书用户 | `ou_58b1afd31a9c961df56ae8fc04e293e0` |
| Chromium | `/snap/bin/chromium` |

## 工作流（严格按顺序）

### 1. 截图 + 生成总结

```bash
node {SKILL_DIR}/scripts/capture-rankings.mjs
```

产出：

- `manifest.json` — 截图路径与解析出的 Top5 排名
- `summary.md` — 飞书文档正文（含各场景表格）
- `summary-chat.txt` — 飞书私聊用的短摘要（无本地路径）
- `categories/*.png` — 12 个场景：Programming、Roleplay、Marketing、SEO、Technology、Science、Translation、Legal、Finance、Health、Trivia、Academia
- 其他板块：`01_top_models` … `11_top_apps`（无单独 Categories 总图）

`{SKILL_DIR}` = 本文件所在目录。

### 2. 校验

```bash
node {SKILL_DIR}/scripts/validate-screenshots.mjs \
  ~/.openclaw/cache/openrouter-rankings/$(date +%F)/manifest.json
```

失败则重跑第 1 步，**不得**创建文档或发飞书。

### 3. 创建飞书文档并插入截图（核心交付）

**禁止**向用户发送宿主机路径、`MEDIA:/root/...` 或 `file://`。

按顺序操作：

**3.1 创建文档**

- 工具：`feishu_create_doc`
- 标题：`OpenRouter 模型排名日报 YYYY-MM-DD`
- `markdown`：读取 `summary.md` 全文（不要用一级标题重复 title；可直接从「给销售同学的 3 句话摘要」开始，或把 summary 作为正文）

**3.2 按顺序插入截图**

对每个 `manifest.json` 中 `ok: true` 的条目，调用 `feishu_doc_media`：

```json
{
  "action": "insert",
  "doc_id": "<上一步返回的 doc_id>",
  "type": "image",
  "file_path": "<manifest 中的绝对路径>",
  "caption": "<heading 或 Categories — 场景名>"
}
```

推荐顺序：

1. 页面板块：`01_top_models` → … → `11_top_apps`（按 id 排序）
2. Categories 场景：按 `categoryScenarios` 数组顺序（Programming → … → Academia）

每个场景截图前可在文档中追加小标题（可用 `feishu_update_doc` `append` 插入 `### 场景：Programming` 等），再插入对应图片。

**3.3 确认文档**

必要时 `feishu_fetch_doc` 抽查文档已含图片与表格。

### 4. 飞书私聊通知用户

只发**文档链接 + 短摘要**，示例：

```text
（读取 summary-chat.txt 的全文）

📎 完整截图与各场景排名表：
<feishu_create_doc 返回的 doc_url>
```

规则：

- **必须**包含可点击的 `doc_url`
- **禁止**出现 `/root/`、`.openclaw/cache` 等本地路径
- **禁止**用 `MEDIA:` 代替文档（销售需在一个文档里查看全部内容）
- 短摘要用通俗中文，突出 Top 模型与场景名

### 5. 失败处理

- 任一场景截图失败 → 重跑 capture，仍失败则告知用户「今日日报未完成」
- 图表为骨架屏 → 不得写入文档

## Categories 场景列表（脚本会自动遍历）

Programming、Roleplay、Marketing、SEO、Technology、Science、Translation、Legal、Finance、Health、Trivia、Academia

## 定时任务

Cron `OpenRouter Rankings 完整日报`（每天 9:00 Asia/Shanghai）应执行本 skill 全流程（截图 → 校验 → 飞书文档 → 私聊链接）。

## 依赖

```bash
cd {SKILL_DIR}/scripts && npm install
```

需要：`feishu_create_doc`、`feishu_doc_media`、`feishu_update_doc`（已配置 openclaw-lark）。

## 禁止

- 不要只发本地路径或 `MEDIA:` 裸图集（除非用户明确要求改回图片模式）
- 不要用 thum.io / web_fetch 截图
- 不要在 Categories 下拉未切换、图表未加载时截图
