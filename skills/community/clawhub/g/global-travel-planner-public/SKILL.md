# Global Travel & Work Planner v1.14.1
# 出国游全球通版 v1.14.1

## What It Does / 功能介绍

One-stop bilingual travel guide for **48 countries**. Outputs **Word (.docx)** with fully bilingual (CN/EN) content.
一键查询 **48个国家** 的**中英双语Word旅行方案**。

**For users of ALL nationalities. / 面向世界各国公民。**

---

## Output / 输出格式

**All reports are generated as .docx (Word) files with dual-language (user's native language + destination's language) content.**
**所有方案输出为 .docx（Word文档），输入语言 + 目的地语言双语对照。**

**大叔亲授·审题+质检机制（完全自动，无需用户指定！）：**
1. **审题** — 引擎自动判断用户输入的语言（中文/日本語/한국어/English…）
2. **质检** — 自动匹配目的地国家的本地语言
3. **输出** — {输入语言} / {目的地语言}

示例：
| 输入 | 用户 | 目的地 | 输出格式 |
|:----|:----|:------|:--------|
| "帮我做个日本旅游方案" | 🇨🇳 中国人 | 🇯🇵 日本 | `中文: xxx / 日本語: xxx` |
| "日本への旅行計画" | 🇯🇵 日本人 | 🇨🇳 中国 | `日本語: xxx / 中文: xxx` |
| "한국 여행 계획" | 🇰🇷 韩国人 | 🇯🇵 日本 | `한국어: xxx / 日本語: xxx` |
| "Plan a trip to Korea" | 🇺🇸 美国人 | 🇰🇷 韩国 | `English: xxx / 한국어: xxx` |
| "我要查中国旅游" | 🇨🇳 中国人 | 🇨🇳 中国 | `中文: xxx`（单语） |

**同语言自动合并为单语（如中国人查中国→中文单语）**
**无需任何参数，引擎通过审题+质检自动完成！**

```
| Drinking Age / 饮酒年龄 | 21 years old / 21岁 |
```

---

## Modules / 功能模块

| Module / 模块 | Content / 内容 |
|:-------|:----------------|
| **Visa / 签证** | Type, fee, processing, validity + how to apply, where to apply, visa process, required documents, tips (实时搜实时填) / 类型、费用、办理周期、有效期 + 如何申请、去哪里签、签证流程、所需材料、小贴士 |
| **Laws / 法规** | Drinking age, smoking, drugs, photos, tipping, public conduct, driving license / 饮酒、吸烟、毒品、拍照、小费、公共行为、驾照 |
| **Culture / 文化** | Greeting, dining, taboos, dress, gifts / 见面、用餐、禁忌、着装、送礼 |
| **Safety / 安全** | Safety level, scams, night/female safety, emergency phrases, apps / 安全等级、骗局、夜间、女性、应急用语、APP |
| **Consular / 领事** | Emergency procedures (passport loss, detention, medical) + reference China embassy data + guide to find your own embassy / 紧急流程 + 参考中国使领馆数据 + 查找本国使领馆指南 |
| **Travel / 行程** | Budget, accommodation, meal/hotel cost, timezone, currency, language, plug / 预算、住宿、费用、时区、货币、语言、插头 |
| **Work / 工作** | Work visa, tax, bank account, insurance / 工作签证、税务、开户、保险 |
| **Study / 留学** | Student visa, application tips, language, living cost / 学生签证、申请建议、语言、生活费 |
| 🆕 **Attractions / 景点** | Attractions, ticket prices, descriptions / 景点、门票价格、介绍 |
| 🆕 **Food / 美食** | Local cuisine, typical prices / 当地美食、参考价格 |
| 🆕 **Transport / 交通** | Subway, bus, taxi, rideshare, train, flights / 地铁、公交、出租、网约车、火车、航班 |
| 🆕 **Itinerary / 行程** | Day-by-day suggested itinerary / 逐日推荐行程安排 |
| 🆕 **Emergency / 应急** | Emergency numbers (police/ambulance/fire), injury & illness guide, nearby hospitals / 报警电话、受伤处理、附近医院 |
| 🆕 **Risk / 风险** | Travel risk warning, risk categories (natural disasters, crime, scams, health), safety tips / 旅游风险预警、风险分类（自然灾害、治安、骗局、健康）、安全建议 |
| 🆕 **History / 历史** | Historical overview, key events timeline, cultural highlights / 历史概览、关键事件时间轴、文化特色 |
| 🆕 **Accommodation / 住宿** | Budget / Mid-Range / Luxury tiers with prices, features, recommendations / 经济型/中档/豪华型，含价格、特色、推荐 |
| 🆕 **Pre-Departure / 行前准备** | Documents checklist, luggage list, money prep, health prep, final checklist / 证件清单、行李清单、资金准备、健康准备、出发前逐项检查表 |
| 🆕 **Entry & Exit / 出入境** | Arrival process, customs regulations, departure process, tips / 入境流程、海关规定、出境流程、小贴士 |
| 🆕 **Phrases / 常用语** | Greetings, directions, ordering food, numbers, emergencies — with pronunciation / 问候、问路、点餐、数字、紧急用语——含发音 |
| 🆕 **Weather / 天气** | Climate overview, best time to visit, seasonal breakdown (temp + clothing) / 气候概况、最佳旅行时间、分季节气温与着装建议 |
| 🆕 **Budget Detail / 详细预算** | Itemized budget by category (transport, accommodation, food, tickets, shopping) with percentages / 交通/住宿/餐饮/门票/购物逐项预算+占比 |
| 🆕 **Insurance / 保险** | Recommendation, insurance types (medical, trip cancellation, luggage loss), tips / 推荐险种、医疗/行程取消/行李损失保险说明、建议 |
| 🆕 **Shopping / 购物** | Local specialties & prices, shopping areas, tax-free info, tips / 当地特色商品与价格、购物地点、退税信息、购物贴士 |
| 🆕 **Communication / 通讯** | Local SIM, WiFi, roaming info, useful apps (maps, translation, ride-hailing) / 当地SIM卡、WiFi、漫游、实用App（地图/翻译/打车） |

> 💡 All supplement data (attractions, food, transport, itinerary, accommodation, visa details, emergency, risk, history, pre-departure, entry-exit, phrases, weather, budget detail, insurance, shopping, communication) are fetched fresh from the web on each query — always up to date.
> 💡 所有补充数据（景点、美食、交通、行程、住宿、签证详情、应急、风险、历史、行前准备、出入境、常用语、天气、详细预算、保险、购物、通讯）每次查询时实时从网上获取——永远最新。

---

## How to Use / 使用方法

### Via AI Chat / 通过AI对话（推荐）

Just tell me what country to look up — I'll generate a bilingual Word document for you.
直接跟我说要查哪个国家，我给您生成中英双语Word方案。

| You Say / 你说 | Output / 输出 |
|:---------------|:-------------|
| `"查日本旅游"` | 🌍 Japan full guide .docx / 日本完整旅行方案.docx |
| `"看看英国签证"` | 🇬🇧 UK visa + consular .docx / 英国签证+领事方案.docx |
| `"美国安全吗"` | 🇺🇸 US safety + safety + laws .docx |

### Via Command Line / 命令行

```bash
# Full report / 完整方案 (all modules)
python3 global_travel_planner.py JP

# Select modules / 指定模块
python3 global_travel_planner.py US visa safety

# Multiple modules / 多个模块
python3 global_travel_planner.py TH visa consular travel

# List countries / 列出国家
python3 global_travel_planner.py list
```

**Output:** Word files are saved in `./output/` directory.
**输出文件**保存在 `./output/` 目录下。

---

## Environment Variables / 环境变量

| Variable / 变量 | Default / 默认 | Purpose / 用途 |
|:---------------|:--------------|:---------------|
| `CONSULAR_HOTLINE` | `+86-10-12308` | Set your country's consular hotline / 设置本国领事热线 |
| `CONSULAR_NATIONALITY` | `CN` | Set your nationality for consular guidance / 设置国籍 |

```bash
# US citizen querying Japan / 美国公民查日本
CONSULAR_NATIONALITY=US python3 global_travel_planner.py JP
```

---

## Countries Covered / 覆盖国家 (48)

```
AE UAE   AR Argentina   AT Austria   AU Australia   BE Belgium
BR Brazil   CA Canada   CH Switzerland   CL Chile   CN China
CO Colombia   CZ Czech   DE Germany   DK Denmark   EG Egypt
ES Spain   FI Finland   FR France   GB UK   GR Greece
HU Hungary   ID Indonesia   IE Ireland   IL Israel   IN India
IT Italy   JP Japan   KE Kenya   KR South Korea   MX Mexico
MY Malaysia   NG Nigeria   NL Netherlands   NO Norway   NZ New Zealand
PE Peru   PH Philippines   PL Poland   PT Portugal   RU Russia
SA Saudi Arabia   SE Sweden   SG Singapore   TH Thailand
TR Turkey   US USA   VN Vietnam   ZA South Africa
```

---

## Disclaimer / 免责声明

All data for reference only. Verify via official sources before travel.
Users of ALL nationalities: contact your own country's embassy for consular assistance.

所有信息仅供参考，出行前请通过官方渠道核实。
**面向世界各国公民**，如需领事协助请联系本国使领馆。

---

**© 出国游全球通版 v1.8.0 | 媳妇智投Pro出品，必属精品 🦊**
