# 儿科学 Pediatrics-PMPH-10edition
<div align="center">

> *「21世纪医学生指南」*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![Skills](https://img.shields.io/badge/skills.sh-Compatible-green)](https://skills.sh)

<br>
> 基于人民卫生出版社《儿科学》第10版的临床技能手册 — 184 项儿科核心临床技能
<br>
<br>

何必苦苦读一本书<br>
只需输入一个问题，自动从课本中找到解决方案

<br>

**其他语言 / Other Languages:**

[English](README_EN.md) · [日本語](README_JP.md) · [Français](README_FR.md) · [Русский](README_RU.md)

</div>

---

## 项目简介

本项目系统整合儿科学、新生儿医学、儿童生长发育、感染性疾病防控、遗传代谢病诊疗及急重症抢救等核心领域，涵盖 **184 项关键临床技能**，分为 **15 大分类**。

**适用人群**：儿科医师、医学生、新生儿科医护团队、公共卫生工作者、住院医师规范化培训学员

**参考教材**：人民卫生出版社《儿科学》第 10 版

**⚠️风险⚠️**：高风险临床治疗、程序和剂量指导可能不适合一般安装或无监督使用。

**缓解措施**：仅适用于合格的儿科医师、新生儿科医师、儿童重症医师或有监督的医学教育环境，并在处理输出前要求临床医生审核。

**⚠️风险⚠️**：指导可能与当前当地指南、机构规程或患者特定禁忌相冲突。

**缓解措施**：在使用前核实方案、程序、阈值和后续计划是否符合当地最新标准和机构政策。

**⚠️风险⚠️**：紧急、侵入性手术、新生儿抢救、儿童用药剂量计算以及敏感的发展行为话题如果处理得太随意，可能会造成患者安全或隐私的危害。

**缓解措施**：针对这些情景添加明确警告，将紧急情况引导至急诊/ICU护理，并限制有适当临床或监督教育需求的用户访问。

## 项目结构

```
Pediatrics-PMPH-10edition/
├── SKILL.md                  # 核心配置 — 184 项技能注册表
├── README.md                 # 本文档 — 项目说明与使用指南
├── <skill-name>/             # 各项技能的详细定义
│   └── SKILL.md              #   技能详情（使用时机、执行步骤、参考文档）
├── scripts/                  # 可执行工具脚本
│   └── .gitkeep
├── config/                   # 配置文件
│   └── .gitkeep
└── tests/                    # 验证与测试
    └── .gitkeep
```

## 技能分类一览

| 分类 | 技能数 | 说明 |
|------|--------|------|
| 👶 新生儿与围产期医学 | 18 | 黄疸、RDS、溶血、出血、NEC、ROP、BPD 等 |
| 📏 生长发育与营养 | 18 | 体格生长评价、辅食、睡眠、微量营养素等 |
| 💉 免疫接种与传染病防控 | 20 | 计划免疫、麻疹、手足口、结核、川崎病等 |
| 🫁 呼吸系统疾病 | 12 | 肺炎、哮喘、支原体、支气管镜、血气分析等 |
| ❤️ 心血管系统疾病 | 10 | 先心病分类、心衰、心肌炎、Duke 标准等 |
| 🫃 消化与肝胆系统疾病 | 12 | 肠套叠、巨结肠、IBD、胆道闭锁、GERD 等 |
| 🫘 泌尿与肾脏疾病 | 10 | 血尿、肾炎、肾病综合征、AKI、RTA 等 |
| ⚖️ 内分泌与代谢疾病 | 13 | GHD、性早熟、甲减、糖尿病、DKA 等 |
| 🩸 血液与肿瘤疾病 | 9 | ITP、AIHA、血友病、地贫、LCH 等 |
| 🧠 神经与精神行为疾病 | 12 | 癫痫、热性惊厥、ADHD、GBS、重症肌无力等 |
| 🚑 急诊与重症抢救 | 10 | CPR、创伤、溺水、呼吸衰竭、脱水等 |
| 🧬 遗传与先天性疾病 | 7 | 三级预防、遗传病分类、CHARGE、DMD/BMD 等 |
| 🔬 实验室与辅助检查 | 11 | CSF、PKU、CAH、佝偻病、MRI、超声等 |
| 📚 教材与循证医学 | 7 | 教材权威性评估、修订原则、文献推荐等 |
| 🏋️ 综合健康管理 | 9 | 运动、膳食、免疫系统、药物剂量、体格检查等 |

## 快速开始

### 安装

CLI：
```bash
openclaw skills install pediatrics-pmph-10edition
```

Prompt：
```bash
Before installing anything, inspect the ClawHub skill metadata and setup requirements.
If the skill asks you to install a third-party package or CLI, verify its source, maintainer, and package contents before running the install command.
Install the skill "Pediatrics-PMPH-10edition" from ClawHub only after those checks pass.
Keep the work scoped to this skill only.
After install, help me finish setup from verified skill metadata.
Use only the metadata you can verify from ClawHub; do not invent missing requirements.
Ask before making any broader environment changes.
```

### 查找技能

```bash
# 按关键词搜索
bash scripts/skill-search.sh 新生儿黄疸

# 生成技能清单
bash scripts/skill-report.sh
```

### 使用方式

每个技能包含四部分内容：
1. **使用时机** — 何时触发该技能
2. **执行步骤** — 标准化操作流程
3. **注意事项** — 禁忌与警示
4. **参考文档** — 详细补充资料

### 提问策略

#### 1. **概念**

Question:
```bash
新生儿生理性黄疸的概念
```

Answer：
```bash
## 新生儿生理性黄疸的概念

**新生儿生理性黄疸**是指因胆红素代谢特点导致新生儿期出现的暂时性血清未结合胆红素升高，通常无需特殊干预即可自行消退的良性过程。

### 诊断标准

| 参数 | 足月儿 | 早产儿 |
|------|--------|--------|
| 出现时间 | 生后2～3天 | 生后3～5天 |
| 高峰时间 | 生后4～5天 | 生后5～7天 |
| 消退时间 | 生后5～7天 | 生后7～9天 |
| 血清胆红素峰值 | < 221 μmol/L (12.9 mg/dL) | < 256 μmol/L (15 mg/dL) |
| 每日上升幅度 | < 85 μmol/L (5 mg/dL) | < 85 μmol/L (5 mg/dL) |

### 核心鉴别

- **生理性黄疸**：符合上述时间窗和阈值，一般情况好
- **病理性黄疸**：出现过早（<24h）、程度过重、持续时间长、每日上升过快、或直接胆红素升高
- **母乳性黄疸**：生后1周出现，延迟至2～3周达峰，停母乳3天可明显下降

### 处理原则

无需特殊治疗，保证充足喂养促进胎便排出即可。若TSB接近干预阈值，需启动光疗评估。

---

**相关技能：** [新生儿黄疸风险评估与生理性黄疸诊断](neonatal-jaundice-risk-assessment-diagnosis/SKILL.md)
```

#### 2. **临床案例分析**

Question:
```bash
新生儿，胎龄38周，顺产，出生体重3.2kg。生后24小时内出现皮肤黄染，并迅速加重。生后36小时TSB 15mg/dL，以未结合胆红素升高为主。母亲血型O型Rh(+)，患儿血型A型Rh(+)。最可能的诊断是什么？
```

Answer：
```bash
## 病例分析

**最可能的诊断：ABO血型不合所致新生儿溶血病**

### 诊断依据

| 临床特征 | 指向 |
|---------|------|
| **生后24小时内出现黄疸** | 病理性黄疸 — 出现时间过早 |
| **血清总胆红素15mg/dL（257μmol/L）** | 显著高于生理范围（正常峰值<12.9mg/dL） |
| **以未结合胆红素升高为主** | 符合溶血性黄疸特点 |
| **母亲O型 + 患儿A型** | ABO溶血病最常见组合（母体抗A IgG通过胎盘） |
| **Coombs试验阳性** | 确诊免疫介导溶血的直接证据 |

### 后续处理

1. **立即启动光疗** — 高强度蓝光照射（425~475nm）
2. **监测TSB q4~6h** — 评估是否需要换血
3. **检查血常规+网织红细胞** — 评估贫血程度
4. **静脉输注丙种球蛋白（IVIG）** — 0.5~1g/kg，阻断溶血
5. **换血指征评估** — 若TSB ≥ 换血阈值或光疗无效

---

**相关技能：** [新生儿黄疸风险评估与生理性黄疸诊断](neonatal-jaundice-risk-assessment-diagnosis/SKILL.md) · [胆红素脑病分期与诊断](bilirubin-encephalopathy-staging-and-diagnosis/SKILL.md)
```

#### 3. **考试题目**

Question:
```bash
婴幼儿，8个月，发热3天，热退后出现皮疹。最可能的诊断是:
A. 麻疹
B. 风疹
C. 幼儿急疹
D. 猩红热
E. 水痘
```

Answer：
```bash
**答案：C. 幼儿急疹（Exanthem subitum）**

### 鉴别要点

| 疾病 | 发热与皮疹关系 | 皮疹特点 | 其他特征 |
|------|---------------|---------|---------|
| A. 麻疹 | 发热**出疹**（热盛疹出） | 暗红色斑丘疹，从耳后发际→面部→躯干→四肢 | Koplik斑、卡他症状 |
| B. 风疹 | 发热**出疹** | 淡红色斑丘疹，先面部→迅速蔓延全身 | 耳后/枕后淋巴结肿大 |
| **✅ C. 幼儿急疹** | **热退疹出** | 玫瑰色斑丘疹，先躯干→面部→四肢，1~2天消退 | 高热（39~40℃），一般情况好 |
| D. 猩红热 | 发热**出疹** | 针尖大小充血性皮疹，皮肤皱褶处呈帕氏线 | 草莓舌、咽峡炎、杨梅舌 |
| E. 水痘 | 发热**出疹** | 向心性分布斑→丘→疱→痂"四世同堂" | 剧烈瘙痒 |

### 为什么是 C？

题干的关键线索：
- **8个月** → 幼儿急疹最常见于6~18月龄婴幼儿
- **发热3天，热退后出现皮疹** → **"热退疹出"是幼儿急疹的经典特征**，与其他出疹性疾病的"热盛疹出"形成鲜明对比
- 玫瑰色斑丘疹，先躯干再蔓延 → 符合幼儿急疹的出疹顺序

### 处理要点

该病为自限性疾病，无需特殊抗病毒治疗，重点为对症支持：
- 控制高热（物理降温、退热剂）
- 保证液体摄入
- 警惕热性惊厥（高热抽搐）

---

**相关技能：** [儿童传染病诊断与防治](er-tong-chuan-ran-bing-zhen-duan-yu-fang-zhi/SKILL.md)
```

## 关于作者

**小绿绿 xllgreen(https://xllgreen.github.io)** — 九江学院临床医学院学生·科技极客

## 技术支持
<br>
PDF2App项目：https://pdf2app.cn
<br>
Microsoft Visual Studio Code：https://code.visualstudio.com/
<br>
Claude Code for VS Code：https://claude.com/
© 2026 Anthropic PBC
<br>
<br>
<img src="https://cdn.deepseek.com/logo.png?x-image-process=image%2Fresize%2Cw_1920" width="130px">
<br>DeepSeek API：https://platform.deepseek.com/
© 2026 杭州深度求索人工智能基础技术研究有限公司 版权所有
<br>
<br>
<img src="https://cdn.cnbj1.fds.api.mi-img.com/aife/mimo-blog-fe/doc_build/static/image/logo.99baaffe.png" width="130px">
<br>Xiaomi Mimo API：https://platform.xiaomimimo.com/
Copyright © 2010 - 2026 Xiaomi. All Rights Reserved
<br>

## 许可证

本项目内容基于人民卫生出版社《儿科学》第10版整理，仅供学习参考。

## Star History

<a href="https://www.star-history.com/#">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=&type=date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=&type=date" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=&type=date" />
 </picture>
</a>
