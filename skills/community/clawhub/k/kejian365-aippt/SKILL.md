---
name: kejian365-aippt
description: "Generate professional PPT presentations using the 课件帮 (Kejian365) AI platform. Handles the full pipeline: outline generation, theme selection, AI content creation, and layout design. Ideal for business reports, product pitches, academic presentations, and training materials. Trigger when the user says: make me a PPT, generate a presentation, create slides, 帮我做PPT, 生成PPT, 制作幻灯片, 课件帮生成, or any request to produce a PowerPoint or slide deck using 课件帮."
---

# 课件帮 AIPPT — 一句话生成专业 PPT

接入「[课件帮](https://kejian365.com)」AI 平台，全流程自动完成 PPT 生成：大纲确认 → 模板匹配 → 智能生成 → 交付链接，无需手动操作任何 API。

## 适用场景

| 场景 | 示例 |
|------|------|
| 商务汇报 | 季度总结、战略分析 |
| 产品介绍 | 融资 Pitch、新品发布 |
| 学术演示 | 研究报告、毕业答辩 |
| 培训课件 | 员工培训、技能分享 |

## 前提条件

需要环境变量：

```
KEJIAN365_AUTH_TOKEN=<Your_Token_Here>
```
密钥获取：https://kejian365.com/oapi-portal

## 使用方式

直接说：「帮我做一个关于 **XX** 的 PPT」即可启动。

---

<!-- 以下为 AI Agent 内部执行指令，用户无需关注 -->

## Execution Checklist

Run through these steps in order. Track completion in context — **never repeat a completed step**.

```
[ ] Step 1  Gather requirements from user
[ ] Step 2  Generate outline (local LLM) → show to user → confirm
[ ] Step 3  run list_themes.py → pick theme → tell user
[ ] Step 4  Write params.json + run script (creates task ONCE on success)
[ ] Step 5  Re-run script every 30s to poll until terminal state
[ ] Step 6  Report final result
```

**Hard rules:**
- NEVER call `POST /skill/task/create` directly — always use the script
- NEVER change `--work-dir` for the same task (causes duplicates)
- NEVER show `ppt_id`, `work_dir`, file paths, or raw URLs to the user

**Script idempotency:**

| task_state.json status | Script behaviour |
|------------------------|-----------------|
| Missing / `CREATE_FAILED` | Calls create API (or retries) |
| `PENDING` / `RUNNING` | Polls only, never creates again |
| `DONE` | Returns success immediately |
| `GENERATION_FAILED` | Returns failure; delete state file to retry |

---

## Step 1 — Gather Requirements

Ask in one message:

> 好的！请告诉我：
> 1. PPT 的主题是什么？
> 2. 有什么特别要求吗？（受众、风格、页数、语言等，没有就跳过）

Extract:

| Parameter | Default |
|-----------|---------|
| `topic` | required |
| `settingPages` | `"智能决策"` → `"精简"` ~10p / `"标准"` ~20p / `"长篇"` ~30p |
| `settingLanguage` | `"中文"` |
| `settingAudience` | `"智能决策"` |
| `illustrationMode` | `"standard"` (`"pro"` = premium) |

---

## Step 2 — Generate Outline

Generate locally (no API). Then **show the outline to the user** and wait for confirmation:

> 已为您生成以下大纲，共 {N} 页：
> 1. 封面 — {title}
> 2. 目录 — {title}
> …（逐页列出）
>
> 满意的话我来继续选模板；如需调整请告诉我。

**Outline array rules:**
- `pageNumber` sequential from 1, no gaps
- Page 1 = `封面`, last = `结束`, at least 1 `内容`
- Add `目录` when ≥ 6 pages; `章节` + its `内容` pages share `chapterNumber`

```json
[
  { "pageNumber": 1, "pageType": "封面", "title": "主标题", "content": "" },
  { "pageNumber": 2, "pageType": "目录", "title": "目录", "content": "1. 概述\n2. 分析" },
  { "pageNumber": 3, "pageType": "章节", "title": "第一章", "content": "", "chapterNumber": "01" },
  { "pageNumber": 4, "pageType": "内容", "title": "内容页", "content": "...", "chapterNumber": "01" },
  { "pageNumber": 5, "pageType": "结束", "title": "谢谢", "content": "" }
]
```

**Material (optional):** also generate a short research summary to improve content quality and pass it as the `material` field.

---

## Step 3 — Select Theme

Use the script — **never call the API directly** (raw JSON response is too large for context):

```bash
python kejian365-aippt/scripts/list_themes.py
```

Output per theme: `THEME: theme_id|theme_name|style|scene`

Reason over the full list, pick the `theme_id` that best fits the PPT `topic`, audience, and tone. Save it for Step 4 `themeId`.

Tell the user:

> 已为您选择「{theme_name}」模板（{style} 风格 · {scene} 场景），即将开始生成…

---

## Step 4 — Create Task

### Work directory

Use a stable slug per topic — **same task = same directory every time**:
```
/mnt/user-data/workspace/{topic-slug}-ppt-tmp
```

### params.json (UTF-8, no BOM, no `\uXXXX` escaping)

```json
{
  "topic": "主题名称",
  "themeId": "theme_xxx",
  "outline": [ ... ],
  "authToken": "<credential>",
  "requirements": "用户的特别要求",
  "material": "# 研究摘要\n...",
  "themeConfig": {
    "settingPages": "标准",
    "settingLanguage": "中文",
    "settingAudience": "智能决策",
    "contentDepth": "智能生成",
    "illustration": "智能配图",
    "sourceMode": "智能参考"
  },
  "illustrationMode": "standard"
}
```

### Run script

```bash
python kejian365-aippt/scripts/create_ppt_task.py \
  --params-file {work-dir}/params.json \
  --work-dir    {work-dir}
```

On `SUBMITTED:`, parse `查看链接:` from stdout and say:

> 🎉 PPT 任务已创建成功！
> 主题：「{topic}」，模板：「{theme_name}」
> 生成大约需要 5–15 分钟，可以先[点这里预览]({view_url})（生成完成前内容可能为空）。
> 我会每隔 30 秒自动查询进度，请稍候。

---

## Step 5 — Poll Progress

Re-run every 30s (omit `--params-file` after first run):

```bash
python kejian365-aippt/scripts/create_ppt_task.py \
  --work-dir {work-dir}
```

| Exit | First line | Action |
|------|------------|--------|
| `0` | `SUBMITTED:` | Poll again in 30s |
| `0` | `DONE:` | → Step 6 |
| `2` | `PENDING:` | Report progress, poll again in 30s |
| `1` | `FAILED:` | → Error handling |

When pending, parse `进度:` and `查看链接:` and say:

> 正在生成中，已完成 {N}/{total} 页，完成后可[在这里查看]({view_url})。

---

## Step 6 — Report Result

### Success (`DONE:`)

Parse `主题:` / `页数:` / `查看链接:` and say:

> 🎉 「{topic}」的 PPT 已生成完成，共 {N} 页！
> [点击这里查看您的 PPT]({view_url})

Provide raw URL only if the user explicitly asks.

### Failure (`FAILED:`)

| stdout keyword | Say to user |
|----------------|-------------|
| `余额不足` | 账户余额不足，充值后告诉我，我来帮您重新生成。 |
| `鉴权` / `401` / `缺少账号凭证` | 未检测到有效密钥，请配置环境变量： `KEJIAN365_AUTH_TOKEN=your_token`，密钥可到[课件帮开放平台](https://kejian365.com/oapi-portal/#/dashboard)获取。 |
| anything else | 生成时遇到了问题，要重新试一次吗？ |

Lines starting with `[INTERNAL]` are for the agent only — never show to user. Delete `task_state.json` silently to retry.

---

## Appendix — API Reference

[api-reference.md](api-reference.md)
