# PDF星盘读取指南（v3.0）

**定位**：从PDF星盘报告中提取**方法论所需的全部数据**，确保下游分析管线零缺失。
**版本**：3.0.0
**更新**：2026-04-24 — 重写，补全P0数据断层+数据完整性门+精确11页映射

> **来源标签**: 【工具/模板】 — PDF星盘数据提取指南
---

## 一、支持的PDF格式

### 1. Jagannatha Hora（主力格式）

典型11页PDF结构：

| 页码 | 内容 | 提取优先级 |
|------|------|-----------|
| **P1** | 出生信息 + D1 Rasi Chart（南/北印度方格） | P0 |
| **P2** | 行星位置总表（9星+度数+星座+Nakshatra+Pada+状态标记） | P0 |
| **P3** | Bhava表（12宫宫头度数）+ 特殊Lagna表（AL/HL/GL） | P0 |
| **P4** | 分盘组1：D2 Hora + D3 Drekkana + D4 Chaturthamsa + D7 Saptamsa | P0 |
| **P5** | 分盘组2：D9 Navamsa + D10 Dasamsa + D12 Dwadasamsa + D16 Shodasamsa | P0 |
| **P6** | 分盘组3：D20 Vimsamsa + D24 Chaturvimsamsa + D27 Bhamsa + D30 Trimsamsa | P1 |
| **P7** | 分盘组4：D40 Khavedamsa + D45 Akshavedamsa + D60 Shashtiamsha | P1 |
| **P8** | Shadbala总表（6种力量分数+Rupa值+是否达标） | P0 |
| **P9** | Ashtakavarga表（BAV分配+SAV聚合） | P0 |
| **P10** | Vimshottari Dasha周期表（Maha+Antar+Pratyantar时间范围） | P0 |
| **P11** | Yoga清单 + 特殊标注（Jaimini Karakas/AL/UL等） | P0 |

**注意**：不同版本的JH页面布局可能略有差异。以实际内容为准，不依赖页码顺序。
**关键原则**：识别内容类型（D1/行星表/Bhava表/分盘/Shadbala/AV/Dasha/Yoga），而非依赖页码。

### 2. Parashara's Light
- 类似JH，但包含更多分析报告和Yoga详细说明
- 提取逻辑相同，按内容类型识别

### 3. 其他印度占星软件
- **最低要求**：出生信息 + D1 + 行星位置 + Dasha周期
- **推荐**：完整11页数据

---

## 二、数据提取清单（方法论全量映射）

### ⚠️ 核心原则：提取一切可用数据，宁可多不可少

下游方法论需要的**所有数据点**必须从PDF中提取。以下清单按优先级排列：

### 2.1 出生基本信息（P0，必须）

| 数据点 | 示例 | 说明 |
|--------|------|------|
| 出生日期 | 1993-04-17 | 年月日 |
| 出生时间 | 14:45:19 | 时分秒，越精确越好 |
| 出生地点 | 邯郸 | 城市名 |
| 经度 | 115.5°E | 东经/西经 |
| 纬度 | 36.6°N | 北纬/南纬 |
| 时区 | UTC+8 | 相对于UTC |
| 性别 | Male/Female | 用于关系分析征象星选择 |
| Ayanamsa | Lahiri 23°51'11" | 恒星黄道校正值 |

### 2.2 D1本命盘数据（P0，必须）

#### 2.2.1 上升星座（Lagna）

| 数据点 | 示例 |
|--------|------|
| 上升星座 | Leo |
| 上升度数 | 12°38' |
| 上升Nakshatra | Magha |
| 上升Pada | 4 |

#### 2.2.2 十二宫数据

每个宫位提取：

| 数据点 | 说明 |
|--------|------|
| 宫位序号 | 1-12 |
| 宫头星座 | 该宫起始星座 |
| 宫头度数 | 精确度数 |
| 宫主星 | 该星座的统治行星 |
| 宫内行星 | 落在该宫的所有行星 |
| 宫位受到的相位 | 其他行星对该宫的Drishti |

#### 2.2.3 九大行星数据（含Rahu/Ketu）

每颗行星提取：

| 数据点 | 示例 | 必要性 |
|--------|------|--------|
| 行星名 | Sun | P0 |
| 所在星座 | Aries | P0 |
| 精确度数 | 28°33' | P0 |
| 所在Nakshatra | Uttara Phalguni | P0 |
| 所在Pada | 1 | P0 |
| 所在宫位（D1） | 9 | P0 |
| **尊贵状态（Dignity）** | own sign / exalted / debilitated / friend / enemy | P0 |
| **逆行标记（Retrograde）** | R 或 空 | **P0** |
| **燃烧标记（Combustion）** | C 或 空（与太阳度数差<阈值） | **P0** |
| **行星战争标记（War）** | W 或 空（与另一星同星座且度数差<1°） | **P0** |
| 该行星发出的相位 | 7th aspect to X, special aspects to Y | P0 |
| 该行星受到的相位 | 被A、B、C行星相位 | P0 |

**逆行/燃烧/行星战争的提取标准**：
- 逆行：行星名旁标有"R"或"Ret"
- 燃烧：行星与太阳同星座且度数差<阈值（月亮12°、火星17°、水星14°、木星11°、金星10°、土星15°）
- 行星战争：两颗行星同星座且度数差<1°，度数大者胜

### 2.3 特殊Lagna（P0，必须）

| 数据点 | 说明 | 方法论用途 |
|--------|------|-----------|
| **Arudha Lagna (AL)** | 公众形象上升点 | Transit四参考点之一（P0） |
| **Upapada Lagna (UL)** | 婚姻上升点 | 关系占星核心 |
| **Hora Lagna (HL)** | 财富上升点 | 财富分析 |
| **Ghati Lagna (GL)** | 权力上升点 | 权力/地位分析 |
| **Pranapada Lagna** | 生命能量点 | 进阶分析 |

**提取位置**：通常在Bhava表或行星表附近标注。

### 2.4 Jaimini Karakas（P0，必须）

从行星度数表计算/提取（度数最大者为AK，依次递减）：

| Karaka | 含义 | 提取方式 |
|--------|------|----------|
| **Atmakaraka (AK)** | 灵魂征象星 | 度数最大的行星 |
| **Amatyakaraka (AmK)** | 事业征象星 | 度数第二大的行星 |
| **Bhratrukaraka (BK)** | 兄弟征象星 | 度数第三大的行星 |
| **Matrukaraka (MK)** | 母亲征象星 | 度数第四大的行星 |
| **Putrakaraka (PK)** | 子女征象星 | 度数第五大的行星 |
| **Gnatikaraka (GK)** | 竞争征象星 | 度数第六大的行星 |
| **Darakaraka (DK)** | 配偶征象星 | 度数第七大的行星（排除Rahu） |

**计算规则**：
- 排除Rahu（部分流派含Rahu则为8个Karaka）
- 度数相同者，取Pada较高者
- JH通常在Yoga页或特殊标注页列出

### 2.5 分盘数据（P0，D2/D9/D10必须；P1，其他分盘推荐）

| 分盘 | 用途 | 必须提取 | 方法论用途 |
|------|------|----------|-----------|
| **D2 Hora** | 财富 | P0 | 财富分析 |
| **D3 Drekkana** | 兄弟/沟通 | P1 | 关系分析 |
| **D4 Chaturthamsa** | 资产/家产 | P1 | 财富分析 |
| **D7 Saptamsa** | 子女 | P0 | 子女分析 |
| **D9 Navamsa** | 婚姻/灵魂 | **P0** | 关系+力量确认 |
| **D10 Dasamsa** | 事业 | **P0** | 事业分析 |
| **D12 Dwadasamsa** | 父母 | P1 | 家庭分析 |
| **D16 Shodasamsa** | 车辆/便利 | P2 | 物质分析 |
| **D20 Vimsamsa** | 灵性修行 | P1 | 灵性分析 |
| **D24 Chaturvimsamsa** | 教育 | P1 | 教育分析 |
| **D27 Bhamsa** | 优缺点 | P1 | 性格分析 |
| **D30 Trimsamsa** | 不幸/痛苦 | P1 | 挑战分析 |
| **D40 Khavedamsa** | 吉凶 | P2 | 进阶分析 |
| **D45 Akshavedamsa** | 综合吉凶 | P2 | 进阶分析 |
| **D60 Shashtiamsha** | 业力/前世 | P1 | 业力分析 |

**每个分盘提取**：上升星座 + 所有行星位置 + 关键行星状态（庙旺落陷）

### 2.6 Shadbala数据（P0，必须）

从Shadbala表提取每颗行星的六种力量分数：

| 力量类型 | 英文名 | 说明 |
|----------|--------|------|
| 位置力量 | Sthana Bala | 庙旺落陷+角宫加分 |
| 方向力量 | Dig Bala | 角宫位置方向力量 |
| 时间力量 | Kala Bala | 昼夜/月相/年行 |
| 运动力量 | Chesta Bala | 逆行/速度变化 |
| 天然力量 | Naisargika Bala | 固定先天等级 |
| 相位力量 | Drik Bala | 吉凶相位加减 |

**额外提取**：
- 总Rupa值（需>最低标准方为合格）
- 是否达标（Ishtaphala/Kashtaphala）
- 行星强度排名

### 2.7 Ashtakavarga数据（P0，必须）

从Ashtakavarga表提取：

| 数据点 | 说明 | 方法论用途 |
|--------|------|-----------|
| **7行星BAV分配表** | 每颗行星在12宫的Bindhu点数 | Transit评分 |
| **Lagna BAV** | 上升在12宫的Bindhu点数 | Transit评分 |
| **SAV聚合表** | 12宫各宫总点数（理论总和337） | 宫位力量排名 |
| **SAV关键阈值** | <20=弱宫，25-30=中等，>30=强宫 | 预测质量评估 |

### 2.8 Dasha周期数据（P0，必须）

| 层级 | 提取内容 | 精度 |
|------|----------|------|
| **Maha Dasha** | 行星名+开始时间+结束时间 | 年-月-日 |
| **Antar Dasha** | 行星名+开始时间+结束时间 | 年-月-日 |
| **Pratyantar Dasha** | 行星名+开始时间+结束时间 | 年-月-日 |
| **Sookshma Dasha**（如有） | 行星名+时间范围 | 年-月-日 |
| **Prana Dasha**（如有） | 行星名+时间范围 | 年-月-日 |

**特别标注**：
- 当前正处于哪个Maha+Antar+Pratyantar
- 未来2-3年的Dasha变化时间表

### 2.9 Yoga清单（P0，必须）

从Yoga页面提取：

| 数据点 | 说明 |
|--------|------|
| Yoga名称 | 如 Raja Yoga、Neechabhanga Raja Yoga、Dhana Yoga等 |
| 构成行星 | 哪些行星参与该Yoga |
| 精确度数 | 参与行星的度数（用于Orb计算） |
| 形成位置 | 哪个宫位/星座 |
| 强度评估 | 如果PDF中标注了强度 |

### 2.10 其他特殊标注

| 数据点 | 优先级 | 说明 |
|--------|--------|------|
| **Karakamsa** | P1 | Navamsa盘中的AK位置 |
| **Vargottama行星** | P1 | D1和D9同星座的行星 |
| **Atmakaraka在D1和D9的位置** | P0 | Jaimini核心 |
| **Ista/Kashta Phala** | P2 | Shadbala补充 |
| ** planetary war 胜负** | P0 | 度数大者胜 |

---

## 三、结构化输出格式

### 3.1 完整JSON Schema

```json
{
  "meta": {
    "source_software": "Jagannatha Hora",
    "extraction_date": "2026-04-24",
    "pdf_pages": 11,
    "data_completeness": "95%"
  },
  
  "birth_info": {
    "date": "1993-04-17",
    "time": "14:45:19",
    "location": "Handan",
    "latitude": 36.6,
    "longitude": 115.5,
    "timezone": "UTC+8",
    "gender": "Male",
    "ayanamsa": "Lahiri 23°51'11\""
  },
  
  "d1_chart": {
    "lagna": {
      "sign": "Leo",
      "degree": 12.633,
      "nakshatra": "Magha",
      "pada": 4
    },
    "special_lagnas": {
      "arudha_lagna": { "sign": "Sagittarius", "degree": 0 },
      "upapada_lagna": { "sign": "Virgo", "degree": 0 },
      "hora_lagna": { "sign": "TBD", "degree": 0 },
      "ghati_lagna": { "sign": "TBD", "degree": 0 }
    },
    "houses": [
      {
        "house_number": 1,
        "sign": "Leo",
        "cusp_degree": 12.633,
        "lord": "Sun",
        "planets_in_house": ["Sun"],
        "aspects_received": []
      }
    ],
    "planets": {
      "Sun": {
        "sign": "Aries",
        "degree": 28.55,
        "nakshatra": "Krittika",
        "pada": 1,
        "house": 9,
        "dignity": "own_sign",
        "retrograde": false,
        "combust": false,
        "planetary_war": false,
        "aspects_given": ["7th to Libra"],
        "aspects_received": []
      },
      "Moon": {
        "sign": "Aquarius",
        "degree": 0,
        "nakshatra": "Dhanishta",
        "pada": 1,
        "house": 7,
        "dignity": "neutral",
        "retrograde": false,
        "combust": false,
        "planetary_war": false,
        "aspects_given": ["7th to Leo"],
        "aspects_received": []
      }
    }
  },
  
  "jaimini_karakas": {
    "AK": { "planet": "Saturn", "degree_d1": 4.3, "sign_d1": "Aquarius", "house_d1": 7 },
    "AmK": { "planet": "Jupiter", "degree_d1": 13.82, "sign_d1": "Virgo", "house_d1": 2 },
    "BK": { "planet": "Mars", "degree_d1": 1.32, "sign_d1": "Cancer", "house_d1": 12 },
    "MK": { "planet": "Venus", "degree_d1": 10.55, "sign_d1": "Pisces", "house_d1": 8 },
    "PK": { "planet": "Saturn", "degree_d1": 4.3, "sign_d1": "Aquarius", "house_d1": 7 },
    "GK": { "planet": "Mercury", "degree_d1": 8.53, "sign_d1": "Pisces", "house_d1": 8 },
    "DK": { "planet": "Mars", "degree_d1": 1.32, "sign_d1": "Cancer", "house_d1": 12 }
  },
  
  "divisional_charts": {
    "d2": { "lagna_sign": "TBD", "planets": {} },
    "d9": {
      "lagna_sign": "Scorpio",
      "planets": {
        "Venus": { "sign": "Libra", "dignity": "own_sign" }
      }
    },
    "d10": {
      "lagna_sign": "Sagittarius",
      "planets": {}
    }
  },
  
  "shadbala": {
    "Sun": { "sthana": 0, "dig": 0, "kala": 0, "chesta": 0, "naisargika": 0, "drik": 0, "total_rupa": 0, "required": 0, "qualified": true },
    "Moon": { "sthana": 0, "dig": 0, "kala": 0, "chesta": 0, "naisargika": 0, "drik": 0, "total_rupa": 0, "required": 0, "qualified": false }
  },
  
  "ashtakavarga": {
    "bav": {
      "Sun": [0,0,0,0,0,0,0,0,0,0,0,0],
      "Moon": [0,0,0,0,0,0,0,0,0,0,0,0],
      "Mars": [0,0,0,0,0,0,0,0,0,0,0,0],
      "Mercury": [0,0,0,0,0,0,0,0,0,0,0,0],
      "Jupiter": [0,0,0,0,0,0,0,0,0,0,0,0],
      "Venus": [0,0,0,0,0,0,0,0,0,0,0,0],
      "Saturn": [0,0,0,0,0,0,0,0,0,0,0,0],
      "Lagna": [0,0,0,0,0,0,0,0,0,0,0,0]
    },
    "sav": [0,0,0,0,0,0,0,0,0,0,0,0],
    "total_points": 337
  },
  
  "dasha": {
    "current": {
      "maha": { "planet": "Saturn", "start": "2020-01-01", "end": "2039-01-01" },
      "antar": { "planet": "Ketu", "start": "2026-01-01", "end": "2027-03-10" },
      "pratyantar": { "planet": "Venus", "start": "2026-04-01", "end": "2026-06-01" }
    },
    "timeline": [
      { "maha": "Saturn", "antar": "Ketu", "pratyantar": "Venus", "start": "2026-04-01", "end": "2026-06-01" }
    ]
  },
  
  "yogas": [
    { "name": "Neechabhanga Raja Yoga", "planets": ["Mercury", "Jupiter"], "house": 8, "strength": "Strong" }
  ],
  
  "special_flags": {
    "vargottama_planets": [],
    "retrograde_planets": [],
    "combust_planets": [],
    "planetary_wars": [],
    "karakamsa_sign": "TBD"
  }
}
```

---

## 四、数据完整性门（Quality Gate）

### ⚠️ 强制规则：缺失P0数据时，禁止进入完整分析

提取完成后，必须执行以下完整性检查：

### 4.1 P0数据必须项（缺一不可）

| # | 数据点 | 检查方式 | 缺失处理 |
|---|--------|----------|----------|
| 1 | 出生时间（精确到分钟） | time字段非空且格式正确 | ⛔ 要求用户提供 |
| 2 | D1上升星座+度数 | lagna.sign + lagna.degree非空 | ⛔ 要求重新提供PDF |
| 3 | 9颗行星位置+度数 | 9个planet条目均含sign+degree | ⛔ 要求重新提供PDF |
| 4 | 逆行/燃烧/战争标记 | 每颗行星retrograde/combust/war字段已填 | ⚠️ 可从未标记推算 |
| 5 | Arudha Lagna | special_lagnas.arudha_lagna非空 | ⚠️ 可从公式计算 |
| 6 | Jaimini Karakas | 7个Karaka均分配 | ⚠️ 可从行星度数计算 |
| 7 | D9 Navamsa盘 | d9.lagna_sign + d9.planets非空 | ⛔ 要求完整PDF |
| 8 | D10 Dasamsa盘 | d10.lagna_sign + d10.planets非空 | ⛔ 要求完整PDF |
| 9 | Dasha周期 | dasha.current三个层级非空 | ⛔ 要求完整PDF |
| 10 | Shadbala | 9星×6力量分数 | ⚠️ 可降级为估算 |
| 11 | Ashtakavarga SAV | 12宫点数 | ⚠️ 可降级为估算 |

### 4.2 P1数据推荐项（缺失可降级分析）

| 数据点 | 缺失影响 | 降级方案 |
|--------|----------|----------|
| AL精确度数 | Transit精度略降 | 从公式估算 |
| D7子女盘 | 子女分析无分盘确认 | 仅D1分析 |
| Yoga清单 | 需手动识别 | 人工逐条检查 |
| Bhava宫头度数 | 宫位边界模糊 | 用整星座宫位制 |
| Upapada Lagna | 关系分析精度降低 | 从D9推算 |

### 4.3 完整性评分规则

| 完整度 | P0齐全？ | 允许的分析级别 |
|--------|----------|---------------|
| **100%** | 全部P0+P1齐全 | Level 3 完整解盘 |
| **90%+** | P0齐全，少量P1缺失 | Level 2 专项分析（标注降级项） |
| **70-90%** | P0大部分齐全 | Level 2（多标注限制） |
| **<70%** | P0关键项缺失 | Level 1 快速概览（明确告知用户数据不足） |

---

## 五、数据校验规则

### 5.1 交叉校验（提取后必须执行）

| 校验项 | 方法 | 错误处理 |
|--------|------|----------|
| D1 Nakshatra与D9一致性 | D1行星Nakshatra Pada应对应D9位置 | 标记不一致 |
| Moon Nakshatra与Dasha起始日 | Vimshottari Dasha从Moon的Nakshatra主星开始 | 核对Dasha起始行星 |
| SAV总和=337 | 8个BAV对应位置求和=SAV，SAV总和=337 | 重新提取或标记异常 |
| Shadbala合格率 | 检查是否Rupa值>最低要求 | 标记弱星 |
| 行星度数和星座匹配 | 度数范围应在对应星座范围内（0-30°） | 标记提取错误 |
| 逆行行星合理性 | 太阳/月亮不逆行；Rahu/Ketu永远逆行 | 标记异常 |

### 5.2 度数→Nakshatra→Pada→D9映射校验

每颗行星的度数必须满足：
```
Nakshatra = floor((degree_in_sign + sign_offset) / 13.3333)
Pada = floor((degree_in_sign + sign_offset) % 13.3333 / 3.3333) + 1
D9_sign = 从Nakshatra+Pada推算
```

如果D9中的行星位置与推算不一致 → 标记提取错误。

---

## 六、提取后输出

### 6.1 提取报告格式

```
═══════════════════════════════════════
  PDF星盘数据提取报告
═══════════════════════════════════════

【来源】Jagannatha Hora | 11页PDF
【提取日期】2026-04-24
【数据完整度】92%

【基本信息】
  姓名/代号：[填写]
  出生时间：[YYYY-MM-DD HH:MM:SS]
  出生地点：[城市] ([纬度]°N, [经度]°E)
  性别：[M/F]

【D1本命盘摘要】
  上升：[星座] [度数]° ([Nakshatra] P[Pada])
  AL：[星座]    UL：[星座]
  
  行星配置：
  ┌──────┬──────┬──────┬─────────┬──────┬──────┬──────┐
  │ 行星 │ 星座 │ 宫位 │ 度数     │ NK   │ Pada │ 状态 │
  ├──────┼──────┼──────┼─────────┼──────┼──────┼──────┤
  │ Sun  │ Ari  │ 9    │ 28°33'  │ Krt  │ 1    │ 庙   │
  │ Moon │ Aqu  │ 7    │ 00°19'  │ Dha  │ 1    │ 中   │
  │ Mars │ Can  │ 12   │ 01°19'  │ 劫   │ 落   │ 陷R  │
  │ ...  │      │      │         │      │      │      │
  └──────┴──────┴──────┴─────────┴──────┴──────┴──────┘
  
  逆行：[Mars]
  燃烧：[无]
  行星战争：[无]
  
【Jaimini Karakas】
  AK=[Saturn] AmK=[Jupiter] BK=[Mars] 
  MK=[Venus] PK=[Saturn] GK=[Mercury] DK=[Mars]

【关键分盘】
  D9上升：[星座]    D10上升：[星座]

【当前Dasha】
  Maha：[Saturn] (2020-2039)
  Antar：[Ketu] (2026.01-2027.03)
  Pratyantar：[Venus] (2026.04-2026.06)

【Yoga清单】
  - [Yoga1]：[行星]在[X宫]
  - [Yoga2]：[行星]在[Y宫]

【Shadbala摘要】
  最强：[行星] [分数]R
  最弱：[行星] [分数]R

【Ashtakavarga SAV】
  宫位：1  2  3  4  5  6  7  8  9  10 11 12
  点数：[XX XX XX XX XX XX XX XX XX XX XX XX]

【数据完整性】
  ✅ P0全部齐全（11/11）
  ⚠️ P1缺失：[列出]
  ❌ 缺失：[列出或"无"]

═══════════════════════════════════════
```

### 6.2 质量门判定

根据4.3节的完整性评分规则，输出分析级别建议：

```
质量门判定：
  完整度 92% → P0全部齐全 → ✅ 允许 Level 3 完整解盘
  P1缺失：D6 Shashtamsa → 健康分析无分盘确认
```

---

## 七、常见问题

### Q1：PDF中找不到Arudha Lagna怎么办？
**A**：AL不在标准行星表中。JH通常在Bhava表或特殊标注页列出。如果PDF中确实没有，可以从以下公式计算：
- AL = 上升主星所在星座起算，上升主星到该星座主星的宫位数×该星座
- 简化法：AL = 上升主星所在宫位的第12个星座（具体需查Parashara规则）

### Q2：PDF中没有Shadbala表怎么办？
**A**：降级为估算模式。根据行星庙旺/落陷/角宫/逆行等信息做定性判断，标注"估算，非精确分数"。

### Q3：如何区分行星的Drishti（相位）？
**A**：
- 所有行星都有第7宫相位（对面宫）
- 火星额外有第4宫和第8宫相位
- 木星额外有第5宫和第9宫相位
- 土星额外有第3宫和第10宫相位
- JH通常不直接标注Drishti表，需要从行星位置推算

### Q4：Jaimini Karakas需要自己计算吗？
**A**：JH通常在Yoga页面或特殊页面列出。如果未列出，按以下规则手动计算：
1. 将9颗行星（排除Rahu）按度数从大到小排列
2. 度数最大=AK，第二大=AmK，...第七大=DK
3. 如果两星度数完全相同，看Pada较高者优先

### Q5：PDF只有D1没有分盘怎么办？
**A**：P0数据不齐全，降级为Level 1快速概览。明确告知用户："分盘数据缺失，无法进行精确推运应期预测。建议使用Jagannatha Hora生成完整11页PDF。"

---

## 八、与下游管线的桥接

提取完成并通过质量门后，数据直接喂入以下分析管线：

| 管线阶段 | 所需数据 | 来源参考文件 |
|----------|----------|-------------|
| 静态星盘分析 | D1全部+Dignity+相位+逆行/燃烧/战争 | `planets.md`、`signs-and-houses.md` |
| Yoga识别 | 行星位置+宫位+度数 | `yoga_list.md`、`yoga-phala-timing-guide.md` |
| Nakshatra分析 | 行星Nakshatra+Pada | `nakshatra_deities.md`、`nakshatra-chinese-quick-ref.md` |
| Shadbala评估 | Shadbala分数 | `shadbala-complete-methodology.md` |
| Ashtakavarga评估 | BAV/SAV | `ashtakavarga-complete-system.md` |
| Jaimini分析 | Karakas+Chara Dasha | `jaimini-complete-system.md` |
| KP分析 | Sub-Lord（从Nakshatra推导） | `kp-astrology-complete-system.md` |
| Transit分析 | Lagna+AL+Moon+Navamsa Lagna | `transit-comprehensive-guide.md` |
| Dasha推运 | Dasha周期表 | `vimshottari_dasha_guide.md`、`pratyantar-calculation-guide.md` |
| 应期预测 | 全部数据综合 | `timing-prediction-template.md`、`comprehensive-reading-workflow.md` |

**桥接规则**：
1. 提取阶段不删减任何数据
2. 分析阶段按需取用，但所有P0数据必须可访问
3. 如果某分析步骤发现所需数据缺失，标注"数据不足"而非跳过

---

**版本**：3.0.0
**创建日期**：2026-04-20
**最后更新**：2026-04-24（v3.0 重写：补全9个P0数据断层+数据完整性门+精确11页映射+交叉校验规则+管线桥接）
