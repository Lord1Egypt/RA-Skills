---
name: guide-generator
description: "Generates practical lifestyle guides (攻略) by researching recommendations on social media. Covers travel guides (weekend trips, long trips, road trips 自驾游, hiking 徒步, mountaineering 登山, city walks), sports guides (venues 场地, equipment 装备, beginner training), food guides (探店, local cuisine), shopping guides (malls, souvenirs, duty-free), and more. Searches Xiaohongshu, Zhihu, Mafengwo, Dianping, Bilibili plus official sources in parallel, cross-validates recommendations to filter out ads, and integrates findings into one medium-length concrete ready-to-use guide. Use when the user asks for 攻略 / 旅行攻略 / 美食攻略 / 购物攻略 / 运动攻略 / 自驾 / 徒步 / 登山 / 探店 / 装备推荐 / 行程规划 or similar requests."
agent_created: true
---

# 攻略生成 Skill（多类型生活攻略）

## 功能目的

从小红书、知乎、马蜂窝、大众点评、B站等社交平台搜集推荐信息，**交叉验证并过滤软文广告**，按用户需求整合成一篇**篇幅中等（正文 2000–3500 字，不含表格清单）的具体可执行攻略**。

适用类型：长短途旅行（自驾游 / 徒步 / 登山 / 城市游）、运动攻略（场地 / 装备 / 训练）、美食攻略、购物攻略等。各类型模板见 [references/output_templates.md](references/output_templates.md)。

---

## 触发条件（Trigger Conditions）

**中文触发词：**
- 帮我做一份 XX 攻略 / 写一篇 XX 攻略 / 规划 XX 行程
- 旅行攻略 / 自驾游攻略 / 徒步攻略 / 登山攻略 / 周末去哪儿
- 美食攻略 / 探店 / 找好吃的 / XX 有什么必吃的
- 购物攻略 / 伴手礼 / 免税店 / 商场攻略 / 海淘
- 运动场地推荐 / 运动装备推荐 / XX 运动怎么入门
- XX 值得去吗 / XX 值不值得买

**English trigger phrases:**
- "make a guide for / write a travel guide / itinerary for [place]"
- "food recommendations in [city]" / "what to eat in [place]"
- "shopping guide / souvenirs from [place]"
- "gear recommendations for [sport]" / "best venues for [sport]"

---

## 支持的攻略类型

| 类型 | 子类型 | 模板位置 |
|---|---|---|
| 旅行 | 短途周末游（1–3天）· 长途旅行（4天+）· 自驾游 · 徒步/登山 · 城市漫步 | 模板 §1a–§1e |
| 运动 | 场地选择 · 装备选购 · 入门训练 | 模板 §2a–§2c |
| 美食 | 目的地美食 · 单品探店测评 | 模板 §3a–§3b |
| 购物 | 商圈/商场 · 特产伴手礼 · 折扣季/免税/海淘 | 模板 §4a–§4c |

---

## 执行工作流（Workflow）

### Step 0 — 需求确认

用户已给出的信息不重复问；缺失信息用 AskUserQuestion **一次性**问清（不超过 4 题）：

- **所有类型必问**（若未说明）：攻略类型、目的地/主题
- **旅行类**：天数、预算档位、同行人（独自/情侣/亲子/带老人）、出行月份
- **运动类**：水平（新手/进阶）、预算、场地位置偏好
- **美食类**：口味偏好（本地菜/网红打卡/不吃辣等）、人均预算
- **购物类**：品类（衣服/数码/美妆/特产）、预算

未问到的参数用默认值：2–3 天、中档预算、大众口味。

### Step 1 — 信息收集（多平台并行搜索）

1. 按对应模板的「信息清单」逐维度搜索，**一次并行发出 6–10 个 WebSearch**：
   - `关键词 site:xiaohongshu.com` / `site:zhihu.com` / `site:mafengwo.cn` / `site:dianping.com`
   - `XX 攻略 2026` / `XX 避雷` / `XX 必去 值得去吗` / `XX 人均` / `XX 本地人推荐`
   - 目的地为中英文通用的，补一轮英文 query（如 `Chiang Mai itinerary`）
2. **平台策略**：
   - 小红书反爬严格，WebFetch xiaohongshu.com 大概率被登录墙/验证码拦截 → **属预期情况，不要死磕重试**；以 WebSearch 结果摘要为主要来源
   - 知乎专栏、马蜂窝游记、B站专栏、公众号转载页通常可 WebFetch，优先抓取细节
   - 微信文章链接用本机 PowerShell `curl.exe` 抓取
   - **官方信息单独核验**：门票/开放时间（景区官网、官方公众号）、交通班次（12306、航司官网）、场馆价格与营业状态（大众点评、官方小程序）、装备参数（品牌官网）
3. **时效**：优先近 1–2 年内容；季节性内容（赏花、滑雪、登山窗口期）按用户出行月份定向检索。

### Step 2 — 信息筛选与交叉验证（防软文）

1. 同一推荐出现在 **≥2 个独立来源**，且含具体细节（价格、排队时长、具体菜品/路线、实拍描述）→ **采用**
2. 单一来源 + 营销词密集（"绝绝子""闭眼入""天花板""yyds"）且无具体信息 → **存疑**，仅在无替代时保留并注明"少数博主推荐"
3. 避雷帖、差评等**负面信息必须纳入**攻略的「避坑」部分，不删除
4. 价格、开放时间以官方/近期信息为准，社交平台价格只作区间参考
5. 已停业、政策变化等过时信息剔除
6. 信息确实很少时：换关键词再搜一轮（如 城市名+菜市场/市集/本地人吃什么），仍不足则如实告知"该主题公开信息较少，以下为有限来源整理"

### Step 3 — 整合成稿

- 严格按 [references/output_templates.md](references/output_templates.md) 中对应类型的模板结构组织
- **篇幅控制**：正文 2000–3500 字（表格、清单不计入），信息密度优先，不凑字数
- **写作原则**：
  1. 每个推荐至少给出 3 项具体信息：多少钱 / 怎么去 / 什么时间去 / 要多久 / 注意什么
  2. 按行程顺序组织（Day 1 → Day N，或路线 A → B），标注时间点与交通衔接
  3. 热门点给备选方案：人少版 / 省钱版
  4. 路线、预算、装备、店铺等清单用表格呈现
  5. 去 AI 味：不写"以上就是""值得一提的是""总之"式空话
  6. 文末附「信息来源」小清单（平台 + 内容要点，无需逐条链接）
- **户外类（徒步/登山/自驾/潜水等）必须含「安全提示」小节**：季节窗口与天气、体能要求、必备装备、信号盲区与下撤方案、保险建议
- 文末统一注明：`信息截至 <当前日期>，价格与开放情况请以官方为准`

### Step 4 — 输出与保存

1. 对话中输出完整攻略（Markdown 渲染）
2. 询问是否保存为文件；默认保存到 `d:\Documents\vscode\攻略\YYYY-MM-DD_<类型>-<目的地>.md`（用户指定路径优先），保存后一句话告知路径

---

## 注意事项

- 小红书等平台内容只作**线索与事实来源，改写整合、不整段照搬原文**
- 高风险户外活动**不以"小红书小白也能去"的口径降低安全标准**，安全信息以官方/专业来源为准
- 攻略是静态快照，必须标注信息截止日期
