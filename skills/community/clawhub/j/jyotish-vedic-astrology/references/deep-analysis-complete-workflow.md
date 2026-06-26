# 综合深度分析完整工作流——12模块系统化方法

> **版本**：v1.0（2026-04-25）
> **定位**：从零散分析到系统化12模块深度解盘的完整方法论
> **前置**：所有其他参考文件（本文件是顶层工作流，整合所有模块）

> **来源标签**: 【工具/模板】 — 12模块深度解盘工作流
---

## 一、核心理念

### 什么是"深度分析"？

深度分析不是"多看几个指标"，而是**系统化地构建星盘的全息画像**——从行星力量到宫位承载力，从分盘频率到多Dasha收敛，从本命征象到推运时机，形成完整的"诊断报告"。

### 12模块矩阵

| # | 模块 | 核心问题 | 输入 | 输出 |
|---|------|---------|------|------|
| 1 | D1基础星盘 | "星盘的基本配置是什么？" | 出生数据/PDF | 行星位置+尊严+宫位 |
| 2 | 特殊Lagna | "特殊参考点在哪里？" | PDF P1 | AL/UL/HL/GL |
| 3 | Jaimini Karaka | "灵魂的优先级是什么？" | PDF P1/引擎计算 | AK/DK/AmK等 |
| 4 | Shadbala | "每颗行星有多强？" | 引擎计算 | 6维力量评分 |
| 5 | Avastha | "每颗行星的内在状态？" | PDF P1-2 | 三维度状态 |
| 6 | Bhava Bala | "每个宫位有多强？" | PDF P1-2 | 4维宫位评分 |
| 7 | Vimsopaka | "行星在分盘层面如何？" | PDF P1-2 | 分盘综合评分 |
| 8 | 19分盘 | "行星在不同层面的模式？" | 引擎计算+PDF P9-11 | 频率分析+Vargottama |
| 9 | Ashtakavarga | "行星的接收力如何？" | 引擎计算 | BAV/SAV矩阵 |
| 10 | 多Dasha收敛 | "何时发生？" | PDF P1-8 | 6系统收敛窗口 |
| 11 | Navamsa婚姻 | "婚姻的深层画像？" | 模块8的D9数据 | 8步旗标评分 |
| 12 | 综合结论 | "整体画像是什么？" | 模块1-11汇总 | 行星画像+领域画像+时间线 |

---

## 二、12模块详细流程

### 模块1：D1基础星盘

**输入**：出生数据（年月日时分+经纬度+时区）或PDF P1

**分析项**：
- [ ] 9行星+Lagna的位置（星座+度数）
- [ ] 每颗行星的Dignity状态（入庙/入旺/友星/中性/敌星/落陷）
- [ ] 逆行/燃烧/行星战争标记
- [ ] 12宫位的主星和入驻行星
- [ ] 关键合相（Orb ≤ 10°）

**输出格式**：
```
D1星盘概览：
- 上升：Leo 12.54°
- 太阳：Aries 3°31'（9宫，中性）
- 月亮：Aquarius 11°47'（7宫，中性）
- ...
关键配置：
- Mars(DK) Cancer 1°20' 落陷（12宫）
- Venus(PK) Pisces 入庙（8宫）
- Saturn(PK) Aquarius 入庙（7宫）
```

### 模块2：特殊Lagna

**输入**：PDF P1（特殊Lagna数据）

**分析项**：
- [ ] Arudha Lagna（AL）——公众形象
- [ ] Upapada Lagna（UL）——婚姻指标
- [ ] Hora Lagna（HL）——财富指标
- [ ] Ghati Lagna（GL）——权力指标

**关键检查**：
- AL与UL的关系 → 公众形象与婚姻的关系
- UL与DK的关系 → 婚姻指标与配偶星的关系

### 模块3：Jaimini Karaka

**输入**：PDF P1（Karaka标记）或引擎计算

**分析项**：
- [ ] 7星系统：AK/AmK/BK/MK/PK/GK/DK
- [ ] 8星系统（Sanjay Rath）：+PK-8，DK可能不同
- [ ] AK的星座和度数 → 灵魂方向
- [ ] DK的星座和度数 → 配偶方向

**关键检查**：
- ⚠️ 必须确认使用7星还是8星系统（PDF标记8个Karaka = 8星系统）
- ⚠️ DK在7星和8星中可能不同（例：7星DK=Mars vs 8星DK=Sun）

### 模块4：Shadbala

**输入**：引擎计算 `shadbala` 子命令

**分析项**：
- [ ] 每颗行星的6维分数
- [ ] 总Rupas和Ishta Bala百分比
- [ ] 行星力量排名（最强→最弱）
- [ ] 达标线检查（每颗行星是否达到最低要求）

**关键检查**：
- 最弱行星 = 最大的功课（如果最弱行星是DK = 婚姻是核心功课）
- 最强行星 = 最大的护法（如果最强行星是AK = 灵魂智慧是最大保护）

**参见**：`shadbala-interpretation-methodology.md`

### 模块5：Avastha

**输入**：PDF P1-2（Avastha表格）

**分析项**：
- [ ] Baladi Avastha（3岁阶段：婴儿/青年/成年）
- [ ] Jagratadi Avastha（警觉度：清醒/做梦/深睡）
- [ ] Lajjitadi Avastha（情绪：羞愧/欢欣/沮丧等）

**关键检查**：
- 全负面Avastha = "浴火重生"型（所有维度都是负面状态）
- Mrita（死亡态）= 该行星征象需要"从零重建"

**参见**：`shadbala-interpretation-methodology.md` §三

### 模块6：Bhava Bala

**输入**：PDF P1-2（House Bhava Bala表格）

**分析项**：
- [ ] 12宫位的Shirshodaya/Dig/Drig/总Bala
- [ ] 最强宫位和最弱宫位
- [ ] DrigBala负值宫位（被凶星相位压制的领域）

**关键检查**：
- 7宫DrigBala为负 = 婚姻领域有外部压力
- 最强宫位 = 人生最顺畅的领域

### 模块7：Vimsopaka

**输入**：PDF P1-2（Vimsopaka Bala表格）

**分析项**：
- [ ] 每颗行星的5/6/7/Shodasavarga四套评分
- [ ] 百分比排名
- [ ] D1强但Vimsopaka弱 = "表面强，实质弱"

### 模块8：19分盘

**输入**：引擎计算 `varga-full` + PDF P9-11

**分析项**：
- [ ] 每颗行星在19个分盘中的位置
- [ ] 行星频率分析（某行星在某星座出现次数/19）
- [ ] Vargottama检测（D1=D9同星座）
- [ ] Pushkara Navamsa检测

**关键检查**：
- 频率≥40%的行星-星座组合 = "核心主题"
- 唯一Vargottama行星 = 整个星盘的"锚点"

**参见**：`divisional-chart-deep-reading.md`

### 模块9：Ashtakavarga

**输入**：引擎计算 `ashtakavarga` + PDF P2

**分析项**：
- [ ] 7行星BAV完整分配
- [ ] SAV 12宫评分
- [ ] SAV总分验证（=337）
- [ ] 7宫SAV分数 = 婚姻领域的"接收力"

### 模块10：多Dasha收敛

**输入**：PDF P1-8（所有Dasha系统）

**分析项**：
- [ ] Vimshottari当前/下一周期
- [ ] Ashtottari当前/下一周期
- [ ] Yogini当前周期
- [ ] Moola当前周期
- [ ] Narayana当前周期
- [ ] Chara Dasha当前/下一周期
- [ ] 6系统交叉收敛 → 时间窗口

**参见**：`multi-dasha-convergence-protocol.md`

### 模块11：Navamsa婚姻

**输入**：模块8的D9数据 + 模块3的DK数据

**分析项**：
- [ ] D9 8步旗标算法（绿/黄/旗评分）
- [ ] DK在D9的位置和状态
- [ ] D9上升分析
- [ ] Venus在D9分析
- [ ] Vargottama婚姻意义
- [ ] Pushkara Navamsa检测

**参见**：`navamsa-marriage-deep-analysis.md`

### 模块12：综合结论

**输入**：模块1-11的所有输出

**综合方法**：

#### 12a. 行星画像

为每颗关键行星生成综合画像：

```
Mars（DK + Yogakaraka + 女性日盘丈夫星）：
├─ Shadbala: 5.34（刚达标，排名最弱）
├─ Avastha: Mrita（死亡态，全部负面）
├─ D1: Cancer落陷（12宫，情感困境）
├─ D9: Cancer入庙（1宫，灵魂层面强）
├─ Vargottama: ✅（D1=D9=Cancer，唯一Vargottama行星）
├─ 频率: Cancer 8/19 (42%) = 核心主题：情感/家庭
├─ 综合判断: "浴火重生型"——表面有挑战，灵魂层面准备好
└─ 时间线: Chara Dasha Scorpio (2028.07-...) = DK全面激活
```

#### 12b. 领域画像

为每个关键领域生成综合画像：

```
婚姻领域：
├─ D1: 7宫主Saturn入庙Aquarius（婚姻运作稳定）
├─ D9: 8步旗标7/8分（Green Zone）
├─ DK: Mars（最弱行星但Vargottama+D9 1宫）
├─ 7宫SAV: [X]分（接收力）
├─ Bhava Bala: DrigBala=-9.80（相位压力）
├─ 多Dasha收敛: 5/6系统支持2027.06-2028.07
└─ 综合判断: 婚姻承诺强烈，时机在2027-2028，需要经营但结果向好
```

#### 12c. 时间线总结

```
人生关键时间线：
├─ 当前(2026): [Dasha描述]
├─ 2027.06-2028.07: 婚姻最强窗口（5/6系统收敛）
├─ 2028.07+: Chara Dasha Scorpio（DK全面激活）
├─ [其他关键时间点]
└─ 长期趋势: [基于Saturn/Jupiter周期的趋势]
```

---

## 三、PDF数据提取最佳实践

### 11页JH PDF页面映射

| 页面 | 数据内容 | 提取要点 |
|------|---------|---------|
| **P1** | 行星位置+度数+Dignity+Karaka+特殊Lagna | 核心数据页，P0级 |
| **P2** | Ashtakavarga+Shadbala+Vimsopaka+Avastha+Bhava Bala | 力量数据页，P0级 |
| **P3** | Ashtottari+Yogini+Kalachakra Dasha | 替代推运系统 |
| **P4** | Kalachakra详细 | 补充推运 |
| **P5** | Moola Dasha | 补充推运 |
| **P6** | Narayana+其他Dasha | 补充推运 |
| **P7-8** | 更多Dasha系统 | 条件性使用 |
| **P9-11** | 分盘图（D2-D60） | D9交叉验证+频率分析 |

### 数据完整性门

| 级别 | 可缺失数据 | 不可缺失数据 |
|------|-----------|------------|
| **P0**（完整分析） | 特殊Lagna、部分Dasha | 行星位置+度数+Dignity+7Karaka |
| **P1**（基础分析） | Avastha、Bhava Bala、分盘 | 行星位置+度数+D1配置 |
| **P2**（仅概览） | — | 至少有行星位置和星座 |

---

## 四、引擎调用流程

### 完整12模块调用

```bash
PYTHON=/Library/Frameworks/Python.framework/Versions/3.11/bin/python3
SCRIPT=~/.workbuddy/skills/jyotish-vedic-astrology/scripts/jyotish_engine.py

# 一键全链路（模块1-9 + 验证 + 审计）
$PYTHON $SCRIPT full-reading --year 1993 --month 4 --day 17 --hour 14 --minute 45 --lat 36.6 --lon 114.5 --tz 8

# 补充：16分盘精确计算（模块8）
$PYTHON $SCRIPT varga-full --year 1993 --month 4 --day 17 --hour 14 --minute 45 --lat 36.6 --lon 114.5 --tz 8 --divisions D2,D3,D4,D7,D9,D10,D12,D16,D20,D24,D27,D30,D40,D45,D60

# 补充：6维力量（模块4）
$PYTHON $SCRIPT shadbala --year 1993 --month 4 --day 17 --hour 14 --minute 45 --lat 36.6 --lon 114.5 --tz 8

# 补充：BAV/SAV（模块9）
$PYTHON $SCRIPT ashtakavarga --year 1993 --month 4 --day 17 --hour 14 --minute 45 --lat 36.6 --lon 114.5 --tz 8
```

### 最小调用（路径B：PDF数据可用时）

如果PDF数据完整（P0级），则只需引擎补充计算：
- `full-reading`（13模块自动串行）
- `varga-full`（16分盘精确计算，用于频率分析）

模块5/6/7/10直接从PDF提取数据，无需引擎。

---

## 五、报告生成

### 输出结构

```markdown
# [姓名] 星盘完整深度分析报告

## 第一章：D1基础星盘概览
## 第二章：Shadbala六重力量分析
## 第三章：Avastha内在状态分析
## 第四章：Bhava Bala宫位力量分析
## 第五章：Vimsopaka分盘综合评分
## 第六章：十六分盘精确计算与频率分析
## 第七章：多Dasha收敛婚姻时机分析
## 第八章：关键行星综合画像
  - Mars（DK）画像
  - Saturn（7宫主）画像
  - Jupiter（AK）画像
## 第九章：Navamsa婚姻深度分析
## 第十章：Ashtakavarga分析
## 第十一章：综合结论与时间线
## 第十二章：附录（原始数据+引擎输出）
```

### HTML报告生成

```bash
# 用report_builder生成羊皮纸主题HTML
$PYTHON $SCRIPT report ./report_folder --name "姓名" --lagna "上升星座"
```

---

## 六、质量检查清单

### 数据准确性检查

- [ ] 行星度数与PDF偏差 < 0.5°（Lahiri模式下）
- [ ] D9 Navamsa与PDF 10/10匹配
- [ ] Karaka排序与PDF一致
- [ ] SAV总分 = 337
- [ ] Dasha起始年份与PDF一致

### 分析完整性检查

- [ ] 12个模块全部完成
- [ ] 每颗关键行星都有综合画像
- [ ] 每个关键领域都有领域画像
- [ ] 时间线至少覆盖当前Dasha + 下一Dasha
- [ ] 多Dasha收敛等级已量化

### 解读质量检查

- [ ] 没有使用绝对断言（"一定会..."→"大概率会..."）
- [ ] 标注了预测置信度
- [ ] 矛盾信号已标注（D1弱但D9强等）
- [ ] 使用现代措辞（传统术语→现代映射）

---

*来源：2026-04-25 一楠11页PDF完整深度分析实战（12模块全链路系统化方法论提炼）*
