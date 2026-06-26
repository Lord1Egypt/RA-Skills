---
name: mcp-bazi-partner
description: >
  Chinese BaZi (Four Pillars of Destiny) analysis and AI partner matching.
  Trigger when user asks about 八字, 命理, 四柱, birth chart analysis,
  BaZi partner, or wants to find their AI companion type based on birth date.
metadata:
  openclaw:
    emoji: 🎴
    homepage: https://github.com/ZoezoeCookie/mcp-bazi-partner
    requires:
      bins:
        - python3
---

# BaZi Partner — 八字命理搭档匹配

根据用户的出生年月日时，使用中国传统八字命理（子平格局法）进行排盘分析，并匹配专属 AI 搭档类型。

## 安装

```bash
pip install git+https://github.com/ZoezoeCookie/mcp-bazi-partner.git
```

## 三步自动流程（重要！）

当用户提供生日信息时，**必须自动串联执行以下三步**，不要等用户逐步指示：

### Step 1: 排盘分析
调用 `bazi_analyze`，传入年月日时。

**关键：必须询问用户出生的具体小时（0-23点）。**
时辰决定时柱，直接影响格局判定。如果用户不知道具体时间，告知结果可能不准确。

### Step 2: 判定子格局 + 搭档匹配

**关键！** `bazi_analyze` 返回的 `pattern.final_pattern` 是大格局（L1），如"七杀格"。
但搭档匹配需要具体的子格局（L2），如"煞印相生"。

**你必须根据四柱数据推理 L2 子格局**，再调用 `bazi_partner`。

L1→L2 对照表：
- **七杀格** → 煞印相生 / 煞邀食制 / 以劫合煞
- **伤官格** → 伤官佩印 / 伤官生财 / 伤官驾煞
- **印格** → 印绶用官 / 印绶喜食 / 印绶喜比 / 印赖煞生 / 印带财煞 / 印带煞兼食伤 / 印多用财
- **食神格** → 食神生财 / 食神制煞 / 食神吐秀 / 食神带煞印 / 食神合煞存财 / 弃食就煞印
- **财格** → 财旺生官 / 财格佩印 / 财用伤官 / 财喜食生 / 财用煞印 / 财用食印 / 财带七煞 / 弃财就煞 / 用财喜比
- **正官格** → 正官格
- **建禄月劫格** → 禄劫用财 / 禄劫用官 / 禄劫用煞 / 禄劫用伤食
- **阳刃格** → 阳刃用煞 / 阳刃用官 / 阳刃用财

判定方法：看其他柱透出了什么十神（shishen_summary），例如：
- 七杀格 + 印星透干 → **煞印相生**
- 七杀格 + 食神透干 → **煞邀食制**
- 财格 + 官星透干 → **财旺生官**
- 印格 + 食伤透干 → **印绶喜食**

调用 `bazi_partner`：
- `sub_type` = 你推理出的 L2 子格局名
- `status` = "成格"（规则层默认）
- `day_master` = 结果中的 day_master

### Step 3: 确认并写入人格
展示搭档匹配结果后，**询问用户确认**："是否将搭档人格写入 SOUL.md？"

用户确认后，调用 `bazi_apply_prompt`：
- `system_prompt` = 搭档的 system_prompt
- `partner_type` = 搭档的 partner_type

写入后告知用户：重启对话即可体验专属搭档人格。

## 工具说明

### bazi_analyze
输入出生日期（公历），返回四柱排盘、十神、五行分布、格局判定。

**参数：**
- `year`: 出生年（如 1990）
- `month`: 出生月 1-12
- `day`: 出生日 1-31
- `hour`: 出生时 0-23（**必须询问用户**，不知道时传 -1 用正午兜底）

### bazi_partner
根据格局分析结果，匹配 AI 搭档类型。

**参数：**
- `sub_type`: 格局子类名（如 "煞印相生"、"正官格"）
- `status`: "成格" / "败格有救" / "败格无救"
- `day_master`: 日主天干（如 "甲"、"壬"）
- `rescue`: 救应描述（败格有救时使用）
- `defeat_god`: 破格之神（败格无救时使用）

### bazi_apply_prompt
将搭档的 system_prompt 写入 SOUL.md，使 AI 助手采用搭档人格。

**参数：**
- `system_prompt`: bazi_partner 返回的 system_prompt
- `partner_type`: 搭档类型名（如 "水系 · 铁壁回声"）

## 示例

用户："我1997年5月18日上午9点出生，帮我匹配搭档"

→ Step 1: `bazi_analyze(1997, 5, 18, 9)` → 庚金日主，七杀格（偏印透干，煞印相生）
→ Step 2: `bazi_partner("煞印相生", "成格", "庚")` → 金系 · 铁壁回声
→ 展示结果，问用户："是否将搭档人格写入 SOUL.md？"
→ 用户确认 → Step 3: `bazi_apply_prompt(system_prompt, "金系 · 铁壁回声")` → 写入
→ 告知用户：搭档匹配完成，重启对话生效

## 命理方法

基于清代沈孝瞻《子平真诠》格局法，参考王相山《子平真诠精解》。
覆盖 38 种格局子类 × 3 种成败状态 = 114 种命格组合。
