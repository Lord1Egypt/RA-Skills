---
name: gov-service-wechat-layout
description: 民生政务公众号排版：9类内容模板+可换主题色，纯内联样式粘贴即发、不强制135。触发：社保/政务公众号排版、套用模板、换色。
agent_created: true
version: v2.1.0
---

# 民生政务公众号 · 排版模板

Provide nine content-type layout templates plus a swappable theme-color model for 民生政务 WeChat official accounts (社保/医保/公积金/税务/民政/公安政务等). Output is structured HTML an editor pastes directly into the WeChat official-account editor — formatting is preserved without 135 — or imports into 秀米/135 for richer visuals.

## When to use

Trigger when the request is to lay out, format, or apply a template to an article for a 社保 / 政务公众号, e.g. "给这篇社保推文排版"、"套用办事指南模板"、"帮我把这篇政策解读排成公众号格式". Do not trigger for 135 one-click publish packaging (use a 135-publisher skill for that); this skill produces the layout structure and color.

## Content-type routing

Identify the article's content type, then load the matching template from `assets/`:

| Type | Template asset | Use for |
|---|---|---|
| A 误区澄清/政策解读 | `assets/template-A-myth.md.html` | clarifying wrong beliefs about a policy; structured 误区N + ❎/✓ |
| A2 新政解读 | `assets/template-A2-new-policy.md.html` | explaining a new policy with conditions, 举个例子, 办理途径, 热点问答 |
| B 通知公告 | `assets/template-B-notice.md.html` | formal announcements; 落款 + 特此公告 |
| C 办事指南 | `assets/template-C-guide.md.html` | how to apply/fill a form; conditional branches (deep: multi-level nesting + numbered materials) |
| D 案例故事/以案为鉴 | `assets/template-D-case.md.html` | cautionary cases; 案件介绍/结果 + 法律后果 |
| E 互动答疑 | `assets/template-E-qa.md.html` | verified Q&A; Q1…大号 Q + 解答 (tail: 注意事项 + 相关链接) |
| F 活动宣传/工作动态 | `assets/template-F-event.md.html` | event/campaign recap; 大数字高亮 + 图墙 + 时间线 + 展望 |
| G 年度盘点/数据战报 | `assets/template-G-yearreview.md.html` | year-in-review; 大数字 hero + 成果分块 + 大事记时间线 + 展望 |
| H 路线攻略/分类合集 | `assets/template-H-route.md.html` | route/collection list; 并列路线块 + 点位子卡片(标准化字段) + 配套推荐 |

If a piece fits two types, choose the one matching its primary purpose (e.g. a new policy that is mostly a how-to → C; mostly myth-busting → A).

## Apply the color slot model

Use four color roles, but distinguish signals by **form, not just hue** — so a single theme color never reads as "all red". See `references/color-slot-model.md` for the full spec.

- 主题色 brand `#ff6d4d`（A2 默认 `#438EDB` 社保蓝）— **swappable**. Appears in three *distinct forms* so it never collides: (1) **solid bars** = big section dividers — the only full-strength fill, default **text-length** for high-saturation themes; (2) **left-border stripes** on subtitle chips / content boxes; (3) **inline bold words** = content emphasis. Structural only.
- 子标题芯片 — neutral `#F5F6F8` background, **light-red bold text `#E0494D`**, theme left-border stripe. Reads as a "label". **Signal lives on the chip; body text beneath stays plain (no box, no color border)** — use inline ✓/❎/• markers to tell items apart.
- 警示红 warn `#ff0000` — **fixed**; used as inline red emphasis (❎ 错误认知 label, 红字关键词) and as the **red left-border** on Q&A question chips. 警示 / 提醒类（请注意/注意！/IP郑重提醒/温馨提醒/温馨提示）走 **提醒卡**：外层用 `<table>` 容器（微信后台会过滤 `<div>` 的 `border`，`<table>` 边框接受度更高），灰底 `#F5F6F8` + 浅灰细线边框 `1px solid #E5E6EB` + 圆角 `8px`、**无亮色边**；标题浅红字 `#E0494D` + 可选 💡 图标 + 可加主题色下划线（与字异色、`padding-bottom` 留呼吸感），正文深灰纯文本、**不整段/整行同色**。提醒卡与子标题芯片**不同款**（后者满灰底+主题色边）。
- 正确蓝 correct `#5f9cef` — **fixed**; ✓ correct conclusions / positive findings (可算, 可认定, 正确办理方式). The only off-hue positive signal, naturally distinct.

Pick one theme color per article from the candidate library in `references/color-slot-model.md` (default `#ff6d4d` 橙红；**A2 新政解读默认 `#438EDB` 社保蓝**). To recolor, replace the placeholder theme color in the chosen template (A2: `#438EDB`; others: `#ff6d4d`) with the article's theme color; never replace `#ff0000` or `#5f9cef` (both fixed semantic colors). Run `scripts/apply_theme_color.py --input <file> --color <hex>` to do this deterministically, or instruct the editor to find-replace in 秀米/135's one-click theme-color feature.

**Section-title background width**: big section bars default to **text-length** mode (background hugs the title text — far less visual intensity) for the default high-saturation themes (橙红/玫红/粉红/橙); cool themes (blue used as theme) may use full-width. Exact CSS in `references/component-library.md` 「小标题底色 · 宽度模式」.

## Fill placeholders

Templates are de-identified. Replace these placeholders with the account's real values before output:

- `{{IP名}}` — persona name (e.g. 顺小保 / 小保 / 社保小助手)
- `{{城市}}` — city (e.g. 佛山)
- `{{热线}}` — consultation hotline (e.g. 12345)
- `{{公众号名}}` — official-account name (e.g. 顺德社保)
- `{{机构全称}}` — issuing agency full name
- `【…】` — per-article content placeholders (title, dates, amounts, fields)

Keep the fixed footer wording pattern: `温馨提示 + 尊敬的参保人……拨打{{城市}}{{热线}}热线……`. Never fabricate phone numbers, document numbers, QR codes, or links — flag missing ones as `需编辑补充`.

## Workflow

1. Determine content type → load the matching `assets/template-*.md.html`.
2. Apply theme color (replace the placeholder theme color — A2: `#438EDB`; others: `#ff6d4d`) per article; keep warn + correct fixed.
3. Fill `{{…}}` account placeholders and `【…】` content placeholders from the approved copy. Preserve approved wording, dates, amounts, eligibility, and legal names exactly.
4. Return the finished HTML for the editor to paste/import. Optionally note which modules to repeat (误区框 ×N, 案例框 ×N, Q&A ×N).

For the methodology behind the layouts (5-step style-replication SOP, dimension table) and the full component/typography spec, read `references/layout-sop.md` and `references/component-library.md` before non-trivial customization.

## 发布路径：直接粘贴 vs 135

Templates use **inline styles only** — no `<style>` blocks, no `class`, no CSS variables, no scripts, no external fonts (verified). This is exactly the subset the WeChat official-account editor preserves on paste.

- **直接粘贴进公众号后台（推荐，无需 135）**：复制渲染好的 HTML → 公众号后台图文编辑器粘贴 → 格式基本不变 → 发布。换主题色后即可用。适用于本 skill 的全部 9 类模板。
- **走 135/秀米（可选，要富视觉时）**：若需米色网格、卡通插画、复杂卡片等超越内联样式能表达的视觉效果，导入 135/秀米编辑器内排版，再用其"同步到公众号"功能发布。注意：不要把 135/秀米导出的 HTML 直接粘贴进后台——它们靠 `class`+`<style>` 坃局，会被微信剥离导致"css 变形"。

Tradeoff: inline-style-only = 保守视觉 + 直接可发布；135/秀米 = 富视觉 + 必须在编辑器内同步。本 skill 选前者，换取"粘贴即发布"。

## Resources

- `assets/template-*.md.html` — nine de-identified layout templates with the color slot applied.
- `references/color-slot-model.md` — color roles, candidate library, recolor methods.
- `references/component-library.md` — signature components, type scale, fonts, per-type skeletons.
- `references/layout-sop.md` — the 5-step methodology and dissection dimensions for extending to new content types.
- `README.md` — 安装与使用说明（含发布路径详解），随 skill 分发。
- `scripts/apply_theme_color.py` — deterministic theme-color find-replace utility.
