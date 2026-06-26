***
name: "Med-llm-wiki"
description: "管理和维护医疗领域的 LLM Wiki 知识库，支持高精度细节检索与循证推理，针对真实患者病历、临床咨询文档、医患问答进行深度结构化。"
------------------------------------------------------------------------

# Med LLM Wiki Manager

本技能用于将**以患者为中心的临床咨询文档**（包含患者背景、多主题问答、方案建议）转化为高度互联的 Wiki 知识网络。

## 核心设计：四层知识模型

采用以下分层策略：

| 层级 | Wiki 页面类型 | 对应内容 | 检索命中目标 |
| :--- | :--- | :--- | :--- |
| **L1** | 患者实体页 | 患者人口学、既往史、基线检查值 | “张三的 FEV1 是多少？” |
| **L2** | 临床问答页 | **每个独立的“问题+回答”作为一个页面** | “关于呼吸训练有哪些建议？” |
| **L3** | 干预方案页 | 回答中具体的药物/训练/时间表 | “术前蛋白补充的具体剂量？” |
| **L4** | 概念/证据页 | 疾病指南、药物说明书、循证依据 | “GOLD 2 级 COPD 围术期管理原则？” |

**关键原则**：**问题与回答永不合并**。每个问题都值得独立成页，以保留完整的上下文和推理链条。

## 目录结构

```
wiki/
├── index.md                  # 全局索引（按患者/问题类别/关键数值索引）
├── log.md                    # 操作日志
├── patients/                 # L1: 患者实体页
│   └── patient-xxx.md
├── encounters/               # 就诊/检查事件页
│   └── encounter-xxx.md
├── consultations/            # L2: 【核心新增】临床问答页
│   ├── consult-xxx-q01.md    # 每个问题独立文件
│   └── consult-xxx-q02.md
├── interventions/            # L3: 具体干预方案页（可选，复杂方案独立成页）
│   └── intervention-xxx-protein.md
├── concepts/                 # L4: 背景知识概念页
│   └── concept-copd-gold.md
└── comparisons/              # 对比分析页
```

## 页面类型详细规范

### 1. 患者实体页 (`patients/`)

**用途**：锚定所有信息的核心对象。仅包含**静态背景信息**和**基线检查数据摘要**。

**示例结构** (`patients/patient-72male-vats.md`)：
```markdown
---
title: "患者：72岁男性 VATS 右肺上叶切除术候选"
patient_id: p20240415-001
age: 72
gender: male
diagnosis:
  - "右肺占位 (拟行 VATS 右肺上叶切除术)"
  - "COPD (GOLD 2级)"
  - "高血压病"
  - "轻度低蛋白血症"
  - "中度焦虑状态 (GAD-7=10)"
baseline_data:
  fev1: "65% 预计值"
  dlco: "60%"
  6mwt: "320 m"
  albumin: "32 g/L"
  d_dimer: "1.8 mg/L"
  hr: "88 bpm (窦性，偶发房早)"
  bp: "138/86 mmHg"
  spo2_rest: "94%"
  spo2_activity: "88%"
  sleep_awakenings: "3-4 次/夜"
consultation_questions:
  - "[[consult-p20240415-q01]]"
  - "[[consult-p20240415-q02]]"
  # ... 共10个
created: 2026-04-20
updated: 2026-04-20
---

# 患者摘要：72岁男性 VATS 术前评估

## 背景
- 吸烟史：40年，已戒5年。
- 手术计划：VATS 右肺上叶切除术。

## 基线检查结果
（略，详见 Frontmatter 或内嵌表格）
```

### 2. 临床问答页 (`consultations/`) —— **核心原子单元**

**用途**：存储一个完整的“问题 + 回答”对。这是 LLM 回答细节问题的**第一手素材**。

**必须包含的元数据**：
- `patient_id`: 关联患者。
- `question_id`: 原始文档中的问题编号。
- `question_text`: 问题的原文。
- `keywords`: 用于索引的关键词（如：呼吸训练、低蛋白、焦虑）。
- `recommendation_strength`: 方案推荐强度/证据等级（若原文有）。

**示例结构** (`consultations/consult-p20240415-q02.md`)：
```markdown
---
title: "咨询：如何通过呼吸训练改善FEV1值应对术后肺复张？"
type: consultation
patient_id: p20240415-001
question_id: 2
question_text: "如何通过呼吸训练改善FEV1值应对术后肺复张？"
keywords: [呼吸训练, FEV1, 肺复张, 术前康复, COPD]
related_concepts: ["[[concept-incentive-spirometry]]", "[[concept-prehab-copd]]"]
sources: ["病例1.md"]
created: 2026-04-20
---

# 咨询：呼吸训练改善 FEV1 与术后肺复张

## 问题原文
如何通过呼吸训练改善FEV1值应对术后肺复张？

## 回答摘要
为改善 FEV1 和术后肺复张，需综合呼吸训练、营养优化、心理干预及术前风险评估。

## 核心推荐方案

### 1. 术前呼吸训练组合
- **缩唇呼吸**：吸气与呼气时间比 1:2。
- **腹式呼吸**：每日 2 次，每次 15 分钟。
- **激励式肺量计训练**：目标容积 ≥15 ml/kg，每小时 10 次。
- **阈值负荷训练**：强度为最大吸气压的 30-50%。

### 2. 围术期优化要点
- **氧疗支持**：维持 SpO₂ ≥92%，活动时可短暂提高至 95%。
- **营养补充**：高蛋白 + 维生素 D + 抗氧化剂。
- **心理管理**：渐进式肌肉放松训练。

### 3. 术后肺复张策略
- **早期下床活动**：术后 6 小时床旁坐立，24 小时内下床。
- **体位引流**：右侧卧位结合前倾坐位咳嗽。
- **持续气道正压 (CPAP)**：预防肺不张。

## 关键执行要点
- **启动时间**：术前 7 天启动强化训练。
- **多学科协作**：呼吸治疗师、物理治疗师共同参与。

## 风险预警
- D-二聚体升高者训练中需监测血栓风险。
- 房早患者避免 Valsalva 动作。

> 来源：病例1.md - 问题2
```

### 3. 干预方案页 (`interventions/`) —— **可选高级抽象**

**用途**：当某个回答中的方案非常具体且可复用（如“术前蛋白质补充策略”），可单独建页，便于未来其他患者引用。

**示例** (`interventions/intervention-preop-protein-supplement.md`)：
```markdown
---
title: "术前低蛋白血症营养干预方案"
type: intervention
target_condition: "低蛋白血症 (白蛋白 <35 g/L)"
applicable_population: "择期大手术患者"
protocol:
  target_albumin: "≥35 g/L"
  protein_intake: "1.5-2.0 g/kg/d"
  supplementation: "乳清蛋白 40-50 g/d + 酪蛋白 20 g 睡前"
  monitoring: "每3天检测前白蛋白"
evidence_level: "基于临床指南及研究"
---
（具体步骤略）
```

### 4. 概念页 (`concepts/`)

**用途**：解释背景知识，如疾病分级、检查意义、药物机制。**不包含患者特异性数据**。

**示例** (`concepts/concept-copd-gold.md`)：
```markdown
---
title: "COPD GOLD 分级与围术期风险"
type: concept
related_guidelines: ["GOLD 2024"]
---

# COPD GOLD 分级

## GOLD 2 级 (中度)
- FEV1: 50% ≤ FEV1 < 80% 预计值。
- 围术期风险：肺部并发症风险增加，需术前优化。
（略）
```



## 摄入新文件：分析存储患者咨询

当摄入此类**患者背景 + 多问题咨询**文档时，严格遵循以下步骤：

### Step 1: 解析与分割
1. 识别**患者背景区块**（从“我今年72岁…”到“睡眠片段化”）。
2. 识别**问题列表**（如“1，吸烟戒断5年患者是否需要特殊呼吸道准备？”）。
3. 将每个问题的回答内容完整切分，**保留所有子标题、数值和引用**。

### Step 2: 创建/更新页面
1. **患者实体页** (`patients/`)：从背景区块提取静态数据写入 Frontmatter 和正文。
2. **临床问答页** (`consultations/`)：为**每一个问题**创建一个独立文件。
   - 使用模板填充 Frontmatter。
   - 将回答内容原样整理进正文，可适当添加小标题以提升可读性，但**严禁删减数值和具体建议**。
3. **概念页** (`concepts/`)：若回答中反复出现特定术语（如 GOLD 分级、DLCO），则创建或更新对应概念页。
4. **干预方案页** (`interventions/`)：若某回答的步骤性极强（如蛋白质补充时间表），可选择独立建页并建立链接。

### Step 3: 建立交叉引用
- 患者页 → 链接所有问答页。
- 问答页 → 链接相关概念页和干预方案页。
- 问答页之间若有逻辑顺序（如问题 1 和问题 2 相关），在正文中注明 `参见 [[consult-xxx-q01]]`。

### Step 4: 更新索引
在 `index.md` 中：
- 按患者索引：列出该患者所有问答页。
- 按主题索引：列出所有问答页的关键词标签云。
- **数值索引**：将关键基线数值（FEV1、白蛋白）与患者页关联。

## 知识库查询：细节问题精准定位

当用户发起提问后，严格遵循以下步骤：

**检索路径**：
1. 读取 `index.md` → 定位关键词 → 找到相关问答页。
2. 读取相关问答页
3. 若问答页链接了 `interventions/` 页，可进一步读取获取结构化方案。
4. 生成回答，直接引用原文数值并注明来源页面。

**回答示例**：
> 根据病例记录，针对该72岁患者的术前低蛋白血症（白蛋白 32 g/L），建议的蛋白质补充策略为：**每日总蛋白摄入 1.5-2.0 g/kg（若体重70kg则需105-140 g/d），其中乳清蛋白粉每日40-50 g 分两次冲服**。目标是在术前7-10天将白蛋白提升至 ≥35 g/L。详见 [[consult-p20240415-q03]]。

## 知识库维护

- [ ] 每个问答页是否完整保留了原始回答中的所有**数值和单位**？
- [ ] 患者页的 Frontmatter 中是否包含了所有关键检查结果？
- [ ] 问答页之间是否存在未链接的依赖关系？（如问题6的答案引用了问题2的呼吸训练，需建立双向链接）
- [ ] 是否存在重复的概念解释，需统一抽象到概念页？
- [ ] 索引中的关键词是否覆盖了用户可能提问的所有角度？

## 附录：完整页面结构示例

摄入新文件后，预期生成以下 Wiki 文件：

```
wiki/
├── index.md
├── patients/
│   └── patient-72male-vats.md
├── consultations/
│   ├── consult-p20240415-q01-respiratory-prep.md
│   ├── consult-p20240415-q02-breath-training.md
│   ├── consult-p20240415-q03-protein-supplement.md
│   ├── consult-p20240415-q04-anxiety-nonpharma.md
│   ├── consult-p20240415-q05-early-ambulation-oxygen.md
│   ├── consult-p20240415-q06-anticoagulation-d-dimer.md
│   ├── consult-p20240415-q07-muscle-training-analgesia.md
│   ├── consult-p20240415-q08-anxiety-pain-perception.md
│   ├── consult-p20240415-q09-diaphragm-exercise.md
│   └── consult-p20240415-q10-postural-drainage.md
├── interventions/
│   ├── intervention-preop-protein.md
│   └── intervention-diaphragm-training-post-lobectomy.md
├── concepts/
│   ├── concept-copd-gold.md
│   ├── concept-dlco.md
│   ├── concept-gad7.md
│   └── concept-enhanced-recovery-after-surgery.md
└── log.md
```