# 排盘软件与天文计算完全指南

> **版本**: v1.0 | **来源**: Kimi Agent训练手册Ch1-2 + dim01提炼 | **用途**: 排盘工具选型、Ayanamsa配置、图表格式阅读

> **来源标签**: 【工具/模板】 — 占星软件对比指南
---

## 1. Ayanamsa体系完整对比

Ayanāṃśa（अयनांश）是将回归黄道转换为恒星黄道的校正值。选择不同的Ayanamsa可能导致行星跨越星座边界，根本改变庙旺/落陷判断。

| Ayanāṃśa体系 | 纪元年 | 岁差率(″/年) | 1950年校正值 | 主要倡导者 | 特点 |
|:---|:---:|:---:|:---:|:---|:---|
| **Lahiri/Chitrāpakṣa** | 285 CE | 50.28 | 23°15′ | N.C. Lahiri / 印度历法改革委员会 | **印度官方标准**，最广泛使用 |
| Krishnamurti (KP) | 291 CE | 50.23 | 23°09′ | K.S. Krishnamurti | KP体系专用，与Lahiri极接近 |
| B.V. Raman | 397 CE | 50.34 | 21°43′ | B.V. Raman | 南印度传统倾向 |
| Śrī Yukteśvar | 499 CE | 54.00 | 21°45′ | Śrī Yukteśvar Giri | 《The Holy Science》，岁差率偏高 |
| Revatīpakṣa/Shil Ponde | 522 CE | 50.10 | 19°52′ | Shil Ponde | 以Revati宿为基准 |
| Fagan/Bradley | 221 CE | 50.25 | 24°09′ | Cyril Fagan/Donald Bradley | 西方恒星占星标准 |
| J.N. Bhasin | 364 CE | 50.33 | 22°10′ | J.N. Bhasin | 折中方案 |
| Usha-Shashi | 559 CE | 50.26 | 19°25′ | Usha-Shashi | 校正值偏低 |

### 关键实践要点

- **初学者建议**：使用Lahiri（Chitrapaksha），它是印度官方标准、文献最丰富、同行交流最便利
- **KP学习者**：切换到Krishnamurti Ayanamsa或更精确的KP New Ayanamsa (KPNA)
- **精度影响**：仅5-6角分差异可使Dasha起始日期偏移20-45天（Braha实测）
- **哲学态度**：保持开放心态，最终以实际预测效果为准，而非追求"唯一正确值"

---

## 2. 桌面排盘软件对比

### 2.1 免费软件

| 软件 | 平台 | 计算引擎 | 分盘支持 | Ayanamsa选项 | 核心优势 | 局限 |
|:---|:---|:---|:---|:---|:---|:---|
| **Jagannatha Hora 8.0** | Windows only | Swiss Ephemeris 2.02.01 (DE431) | D1-D60全部 | 40+种（含Lahiri变体、KP New、True Chitra） | 免费、精度0.001″、覆盖-12899至16600年 | 界面老旧、无解读文本、Mac需模拟器 |
| **Maitreya** | Win/Linux/Mac | 内置 | 多种 | 多种 | 开源、同时支持Vedic/Western/KP三系统 | 界面简陋、开发缓慢 |

**Jagannatha Hora (JH) 核心配置要点**：
1. 下载地址：https://www.vedicastrologer.org/jh/
2. 首次使用：Settings → Ayanamsa → 选Lahiri Chitrapaksha
3. 输入要求：公历日期、精确到分钟的出生时间、城市名或经纬度
4. 输出内容：行星度数、Nakshatra+Pada、House Cusp、Shadbala、多种Dasha

### 2.2 付费软件矩阵

| 软件 | 平台 | 价格 | 城市数据库 | 核心优势 | 适合人群 |
|:---|:---|:---|:---|:---|:---|
| **Parashara's Light 9.0** | Win/Mac | $299 | 50万+ | 功能最全、内置4部经典文献全文、100+工作表 | 全职专业占星师 |
| **Kala** | Win(Mac可运行) | $255 | 内置 | Kala Chakra Dasha预测专长 | 预测timing研究者 |
| **Shri Jyoti Star 10** | Win | $99起 | 内置 | 性价比突出、Transit动态时间轴分析 | 中级至高级学习者 |

---

## 3. 在线工具与移动应用

### 3.1 在线排盘

| 工具 | 价格 | 特色功能 |
|:---|:---|:---|
| **AstroSeek** | 免费 | Swiss Ephemeris弧秒级、Tropical/Sidereal切换、固定星/阿拉伯点 |
| **Astro.com** | 基础免费 | Extended Chart Selection支持北/南印度格式、Lahiri/Raman/KP |
| **AppliedJyotish** | 免费 | PDF下载、36 Gun Milan婚姻匹配、Shubh Muhurat择日 |
| **RVA Software** | 免费 | 同时支持Vedic/KP/Western、4级Dasha树状视图、sub-lords计算 |

### 3.2 移动应用

| 应用 | 平台 | 价格 | 特色 |
|:---|:---|:---|:---|
| **AstroSage Kundli AI** | Android/iOS | 免费（7000万+下载） | Shodashvarga、Shadbala、Ashtakavarga、5级Vimshottari、KP、Jaimini、Lal Kitab |
| **Cosmic Insights** | iOS/Android | 免费+订阅 | 离线图表、深入Jaimini（Chara Dasha/Karakamsha/Swamsha） |
| **Jyotish Dashboard** | iOS | $9.99 | 20种分盘、北/南/东印度三种格式、3000年星历表 |

### 3.3 中文资源

- **horoscope.tw**：繁体中文界面，可同时列出北/南印度盘、15种分盘、Shadbala、120年Vimshottari
- **OnlineJyotish.com**：自动标注Mangal Dosha、Sade Sati、Kala Sarpa Yoga

---

## 4. 图表格式速查

| 格式 | 几何形状 | 宫位排列 | 星座定位 | 使用地区 | 阅读难度 |
|:---|:---|:---|:---|:---|:---|
| **北印度** | 菱形 | 第一宫固定上方中央，逆时针排列 | 根据上升星座变动 | 北印度（德里、孟买）、国际教学 | 中等 |
| **南印度** | 正方形 | 顺时针排列 | 白羊座永远固定左下第二格 | 南印度四邦 | 较低 |
| **东印度** | 矩形/条状 | 12宫按顺序排列 | 按顺序 | 孟加拉、奥里萨 | 中等 |

**建议**：初学者优先掌握北印度格式（国际通用性最强），熟练后补充南印度格式。

---

## 5. 排盘精度要求

### 出生时间敏感度

| 参数 | 精度要求 | 原因 |
|:---|:---|:---|
| 上升星座 | ±2分钟 | 上升每~2小时换星座，每度~4分钟 |
| 宫位边界 | ±4分钟 | 可能导致行星跨越宫位 |
| Vimshottari Dasha | ±15分钟 | 月亮每天移动13-15°，影响Antar Dasha主星 |
| KP Sub-lord | ±6角分 | 0.1°差异可跨越Sub边界 |
| D60 (Shashtiamsa) | ±2分钟 | 月亮每小时移动~半度=1个D60分割 |

### 生时校正入门

1. 收集客户已确认的重大生命事件（结婚、生育、职业转折等）及精确日期
2. 在未校正时间基础上排盘，检查事件发生时的Dasha+Transit配置
3. 评估配置是否能合理解释事件——若不符，说明时间可能有误
4. 以2-5分钟为单位前后调整，重新计算，直到多个事件都能合理解释
5. 交叉验证：用JH排一次、在线工具排一次，确认关键参数一致

---

## 6. 完整星盘参数解读清单

| 参数 | 含义 | 解读要点 |
|:---|:---|:---|
| 行星度数 | 黄道360°精确位置 | 决定星座、Nakshatra、宫位归属、相位判断 |
| Nakshatra位置 | 月宿归属+Pada(1-4) | Vimshottari Dasha计算基础，Nakshatra主星性质影响周期吉凶 |
| House Cusp | 宫头度数 | 决定行星落入哪个宫位（注意整宫制vs Sripati区别） |
| Shadbala | 六重力量总分(Rupa) | >1 Rupa="有力"，<0.5 Rupa="无力"，连接古典描述与量化分析 |

---

*本文件整合自Kimi Agent高维印度占星师训练手册Chapter 1-2及Dimension 01研究。*
