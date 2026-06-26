---
name: news-research-summary-examples
description: Example prompts and expected outputs for the news-research-summary skill.
---

# Examples

## Example 1: 行业动态周报

**User prompt**

“检索过去 7 天 AIGC 视频生成领域的重要资讯，中文输出，给产品经理看。要包含来源链接，最多 10 条，尽量找一手发布或官方信息。”

**Expected output shape**

- Use the template in `SKILL.md`
- 6–10 sources, deduplicated
- “关键要点”每条都有链接
- “影响评估”明确标注为判断

## Example 2: 政策解读（带时间窗口）

**User prompt**

“检索 2026 年 1 月以来欧盟与 AI 监管相关的最新进展，重点关注执法/指南/合规要求变化。输出为 5 条关键要点 + 一段风险提示。附来源。”

**Expected output shape**

- Queries include `EU`, `guidance`, `enforcement`, `commission`, `EDPB` 等
- Sources prioritize EU official sites and regulators

## Example 3: 竞品更新（指定公司/产品）

**User prompt**

“帮我查一下 Sonos 最近一个月在官方渠道发布了哪些产品/软件更新，整理成时间线，附链接。”

**Expected output shape**

- Primary sources: Sonos release notes / official blog / IR
- Timeline section under “详情（按主题/时间线）”

