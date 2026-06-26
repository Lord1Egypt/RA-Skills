# 数据桥接：PDF提取字段 → 方法论需求映射

**定位**：确保PDF提取的每一个数据点都能被下游方法论消费，零遗漏。
**版本**：1.0.0
**创建日期**：2026-04-24

> **来源标签**: 【工具/模板】 — PDF提取→方法论数据桥接映射
---

## 一、映射总览

### 消费关系

```
PDF提取（pdf-chart-reading-guide.md）
    ↓ 数据完整性门（Quality Gate）
    ↓
数据桥接（本文档）→ 确认每个方法论步骤都有输入
    ↓
分析管线（comprehensive-reading-workflow.md）
    ↓
应期模板（timing-prediction-template.md）
    ↓
最终报告
```

---

## 二、逐方法论步骤的数据需求

### 2.1 静态星盘分析

| 分析步骤 | 所需数据 | PDF提取字段 | 映射状态 |
|----------|----------|-------------|----------|
| 行星配置解读 | 9星位置+Dignity | `d1_chart.planets.*` | ✅ |
| 行星相位分析 | 行星间Drishti | `d1_chart.planets.*.aspects_given` | ✅ |
| 逆行分析 | 逆行标记 | `d1_chart.planets.*.retrograde` | ✅ v3.0新增 |
| 燃烧分析 | 燃烧标记+度数差 | `d1_chart.planets.*.combust` | ✅ v3.0新增 |
| 行星战争 | 战争标记+胜负 | `special_flags.planetary_wars` | ✅ v3.0新增 |
| Yoga识别 | 行星位置+宫位+度数 | `d1_chart.planets` + `yogas[]` | ✅ |
| Nakshatra解读 | 每颗星的Nakshatra+Pada | `d1_chart.planets.*.nakshatra/pada` | ✅ |
| 宫位分析 | 12宫宫主星+宫内星+相位 | `d1_chart.houses[]` | ✅ |
| Shadbala评估 | 6种力量分数 | `shadbala.*` | ✅ v3.0新增 |
| Ashtakavarga评估 | BAV+SAV | `ashtakavarga.bav/sav` | ✅ v3.0新增 |
| Ketu双属性分析 | Ketu位置+宫位+星座+相位 | `d1_chart.planets.Ketu` | ✅ |

### 2.2 Jaimini系统

| 分析步骤 | 所需数据 | PDF提取字段 | 映射状态 |
|----------|----------|-------------|----------|
| Karaka识别 | 7个Karakas | `jaimini_karakas.*` | ✅ v3.0新增 |
| Karaka在D1位置 | AK/AmK/DK等在哪个宫 | `jaimini_karakas.*.house_d1` | ✅ v3.0新增 |
| Karaka状态 | Dignity+逆行 | 需交叉引用`d1_chart.planets` | ✅ |
| Karakamsa | AK在D9的星座 | `special_flags.karakamsa_sign` | ✅ v3.0新增 |
| Chara Dasha | 星座大运时间表 | 需从Dasha推算 | ⚠️ 可能需手动 |

### 2.3 KP系统

| 分析步骤 | 所需数据 | PDF提取字段 | 映射状态 |
|----------|----------|-------------|----------|
| Nakshatra识别 | 每颗星的Nakshatra | `d1_chart.planets.*.nakshatra` | ✅ |
| Sub-Lord推导 | Nakshatra+度数→Sub-Lord | 从Nakshatra度数推算 | ✅ |
| Cuspal Sub-Lord | 宫头度数→Sub-Lord | `d1_chart.houses[].cusp_degree` | ✅ v3.0新增 |
| Significator | 行星统治的星座→宫位 | 交叉引用行星位置+宫位 | ✅ |

### 2.4 Transit分析

| 分析步骤 | 所需数据 | PDF提取字段 | 映射状态 |
|----------|----------|-------------|----------|
| Lagna基准 | D1上升星座 | `d1_chart.lagna.sign` | ✅ |
| Chandra Lagna基准 | Moon星座 | `d1_chart.planets.Moon.sign` | ✅ |
| **AL基准** | **Arudha Lagna** | **`d1_chart.special_lagnas.arudha_lagna`** | ✅ v3.0新增 |
| Navamsa Lagna基准 | D9上升 | `divisional_charts.d9.lagna_sign` | ✅ |
| Ashtakavarga评分 | SAV+BAV | `ashtakavarga.*` | ✅ v3.0新增 |
| Double Transit | 土星+木星当前位置 | 需外部Transit数据 | ⚠️ PDF不提供实时Transit |

**⚠️ 关键依赖**：Transit分析需要**当前行星过境位置**，这不在PDF中（PDF是本命盘数据）。
- 解决方案：用户必须提供分析日期，由AI查询当前Transit数据
- 如果用户未提供分析日期，默认使用"今天"

### 2.5 Dasha推运

| 分析步骤 | 所需数据 | PDF提取字段 | 映射状态 |
|----------|----------|-------------|----------|
| Maha Dasha | 大行星+时间 | `dasha.timeline[].maha` | ✅ |
| Antar Dasha | 大行星+时间 | `dasha.timeline[].antar` | ✅ |
| Pratyantar Dasha | 大行星+时间 | `dasha.timeline[].pratyantar` | ✅ |
| Sookshma/Prana | 如有 | `dasha.timeline[]` 扩展 | ⚠️ 部分PDF不含 |

### 2.6 Varshaphala年运盘

| 分析步骤 | 所需数据 | PDF提取字段 | 映射状态 |
|----------|----------|-------------|----------|
| 太阳返照盘 | 出生数据+分析年份 | `birth_info` + 外部计算 | ⚠️ PDF不含年运盘 |
| Muntha | 分析年份-出生年份 | `birth_info.date` + 外部计算 | ⚠️ 需计算 |
| Tajika Yoga | 年运盘行星位置 | 需完整年运盘 | ⚠️ 需计算或额外输入 |

**⚠️ 关键依赖**：Varshaphala需要**年度太阳返照盘**，不在本命PDF中。
- 解决方案：AI根据出生数据和分析年份计算，或用户额外提供

### 2.7 关系占星

| 分析步骤 | 所需数据 | PDF提取字段 | 映射状态 |
|----------|----------|-------------|----------|
| 7宫分析 | 7宫主+宫内星 | `d1_chart.houses[7]` | ✅ |
| D9关系分析 | D9 7宫 | `divisional_charts.d9` | ✅ |
| **DK分析** | **Darakaraka** | **`jaimini_karakas.DK`** | ✅ v3.0新增 |
| **UL分析** | **Upapada Lagna** | **`d1_chart.special_lagnas.upapada_lagna`** | ✅ v3.0新增 |
| **Mangal Dosha** | **火星位置（1/2/4/7/8/12宫）** | `d1_chart.planets.Mars.house` | ✅ |
| **配偶征象星** | **男=Venus 女=Mars+Jupiter** | `birth_info.gender` + 行星位置 | ✅ |

### 2.8 补救措施

| 分析步骤 | 所需数据 | PDF提取字段 | 映射状态 |
|----------|----------|-------------|----------|
| 行星受克评估 | 逆行+燃烧+战争+落陷 | `special_flags.*` + `d1_chart.planets.*` | ✅ v3.0新增 |
| 弱星识别 | Shadbala未达标 | `shadbala.*.qualified` | ✅ v3.0新增 |
| Sade Sati | Moon位置+当前土星位置 | `d1_chart.planets.Moon` + 外部Transit | ⚠️ 需外部数据 |

---

## 三、数据缺口与降级方案

### 3.1 PDF无法提供的数据（需外部来源）

| 数据 | 来源 | 降级方案 |
|------|------|----------|
| **当前Transit位置** | 用户提供分析日期+外部星历表 | AI联网查询或用户手动提供 |
| **Varshaphala年运盘** | 需计算太阳返照盘 | AI计算或用户额外提供 |
| **Chara Dasha时间表** | 需计算 | AI根据D1数据计算 |
| **Sookshma/Prana Dasha** | 需计算 | 仅用Pratyantar级别 |
| **Navamsa Lagna精确度数** | 需从D1推算 | AI从Nakshatra Pada推算 |

### 3.2 处理流程

```
PDF提取完成
    ↓
Quality Gate（完整性检查）
    ↓ 通过
数据桥接检查（本文档）
    ↓ 确认所有P0数据齐全
    ↓ 标记P1缺失项
    ↓ 标记外部数据依赖
进入分析管线
    ↓ 遇到外部数据依赖时
    ├─ Transit位置 → 查询当前星历
    ├─ Varshaphala → 计算太阳返照盘
    ├─ Chara Dasha → 从D1数据计算
    └─ 其他 → 标注"数据不足"
```

---

## 四、更新日志

| 日期 | 版本 | 变更 |
|------|------|------|
| 2026-04-24 | 1.0.0 | 初始版本，覆盖全部方法论步骤的数据映射 |

---

**配套文件**：
- 上游：`pdf-chart-reading-guide.md`（数据提取+质量门）
- 下游：`timing-prediction-template.md`（应期模板）、`comprehensive-reading-workflow.md`（分析流程）
