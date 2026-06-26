# 生理学 Physiology-PMPH-10edition

<div align="center">

> *「生理学是医学的基石 — 理解功能，方能理解疾病」*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![Skills](https://img.shields.io/badge/skills.sh-Compatible-green)](https://skills.sh)
[![ClawHub](https://img.shields.io/badge/ClawHub-PMPH--10edition-orange)](https://clawhub.ai/)

<br>

> 基于人民卫生出版社《生理学》第10版的系统化生理学技能集合 — 165项核心生理学技能
> Systematic physiology skill collection based on PMPH *Physiology*, 10th Edition — 165 core physiology skills

<br>

<img src="/assets/Physiology.png" width="260px">

<br>

📖 **何必苦苦读一本书 · 只需输入一个问题，自动从课本中找到解决方案**
📖 **Don't just read a textbook — ask a question, get a structured answer rooted in the source**

<br>

**多语言 README / Multi-language README:**

[English](README_EN.md) · [日本語](README_JP.md) · [Français](README_FR.md) · [Русский](README_RU.md) · [한국어](README_KO.md)

</div>

---

## 📋 项目简介 / Project Introduction

本项目系统整合人体生理学核心知识体系，涵盖神经与感觉系统、内分泌与代谢调节、心血管生理、呼吸系统、泌尿与水盐平衡、消化与营养吸收、血液与免疫、能量代谢与体温调节、细胞与分子机制、生殖与发育、整合生理与临床评估等 **12 大分类**，共计 **165 项关键生理学技能**。

**适用人群 / Target Audience**：
- 🏗️ 医学生 / Medical Students
- 🏥 临床医师 / Clinicians
- 🔬 生理学教师 / Physiology Educators
- 📚 科研人员 / Researchers

**参考教材 / Reference Textbook**：
人民卫生出版社《生理学》第 10 版（"十四五"普通高等教育规划教材）
PMPH *Physiology*, 10th Edition (National "14th Five-Year" Higher Education Planning Textbook)

**⚠️ 风险提示 / Risk Notice ⚠️**：
- 本技能集合涵盖生理学基础知识与临床评估技能，其内容可能被误用为独立医疗诊断依据。
- **缓解措施**：仅将输出作为教育或临床医生审核的参考资料，根据当前权威指南和临床判断核实建议。
- **Mitigation**: Use outputs solely as educational references or materials for clinician review. Verify all recommendations against current official guidelines and qualified clinical judgment.

---

## 📁 项目结构 / Project Structure

```
Physiology-PMPH-10edition/
├── SKILL.md                  # 核心配置 — 165 项技能注册表（中英双语）
├── README.md                 # 本文档 — 项目说明与使用指南（中文主版本）
├── README_EN.md              # 英文说明文档
├── README_JP.md              # 日文说明文档
├── README_FR.md              # 法文说明文档
├── README_RU.md              # 俄文说明文档
├── README_KO.md              # 韩文说明文档
├── index.md                  # 完整技能索引与快速导航
├── config/
│   └── settings.json         # 技能集合配置文件
├── scripts/                  # 工具脚本
├── tests/                    # 验证与测试
├── assets/                   # 静态资源（图片等）
└── <skill-name>/             # 各项技能的详细定义（165项）
    └── SKILL.md              #   技能详情（使用时机、执行步骤、注意事项、参考文档）
```

---

## 📊 技能分类一览 / Skill Categories Overview

| 分类 (Category) | 技能数 (Count) | 说明 (Description) |
|---|---|---|
| 🧠 神经与感觉系统 | 27 | EEG、睡眠、躯体/特殊感觉、突触可塑性、学习记忆等 |
| 🔬 内分泌与代谢调节 | 21 | 下丘脑-垂体-靶腺轴、胰岛功能、甲状腺、肾上腺、骨代谢等 |
| ❤️ 心血管生理 | 16 | 心动周期、心输出量、血压调控、冠脉血流、抗凝机制等 |
| 🫁 呼吸系统 | 12 | 肺通气力学、血气分析、氧解离曲线、呼吸反射等 |
| 🫘 泌尿与水盐平衡 | 14 | 肾小球滤过、肾小管转运、ADH调节、酸碱平衡等 |
| 🫃 消化与营养吸收 | 12 | 胃液分泌、胃排空、微量营养素吸收、胆汁酸反馈等 |
| 🩸 血液与免疫 | 10 | ABO血型、生理性止血、凝血通路、血小板功能等 |
| ⚡ 能量代谢与体温调节 | 8 | 基础代谢率、间接测热法、体温调定点、热量限制等 |
| 🧬 细胞与分子机制 | 18 | 离子通道、主动/被动转运、G蛋白信号、平滑肌收缩等 |
| 👶 生殖与发育 | 7 | 卵泡发育、月经周期、雌激素合成、胎盘功能等 |
| 🏥 整合生理与临床评估 | 16 | 稳态调节、脑血流、内脏痛、排尿反射、情绪生理等 |
| 📚 方法学与教材资源 | 6 | 研究方法、伦理审查、教材认证、数字资源获取等 |

---

## 🚀 快速开始 / Quick Start

### 安装 / Installation

**CLI：**
```bash
openclaw skills install physiology-pmph-10edition
```

**Prompt：**
```bash
Before installing anything, inspect the ClawHub skill metadata and setup requirements.
If the skill asks you to install a third-party package or CLI, verify its source, maintainer, and package contents before running the install command.
Install the skill "Physiology-PMPH-10edition" (xllgreen/physiology-pmph-10edition) from ClawHub only after those checks pass.
Skill page: https://clawhub.ai/xllgreen/physiology-pmph-10edition
Keep the work scoped to this skill only.
After install, help me finish setup from verified skill metadata.
Use only the metadata you can verify from ClawHub; do not invent missing requirements.
Ask before making any broader environment changes.
```

### 使用方式 / How to Use

每个技能包含四部分内容 / Each skill includes four parts:
1. **使用时机 / Use When** — 何时触发该技能
2. **执行步骤 / Execution Steps** — 标准化操作流程
3. **注意事项 / Cautions** — 禁忌与警示
4. **参考文档 / References** — 详细补充资料

### 提问策略 / Query Strategies

#### 1️⃣ 概念查询 / Concept Query

**Question:**
```bash
请解释 insulin-signaling-transduction-pathway 的关键步骤
Explain the key steps of insulin-signaling-transduction-pathway
```

**Answer:**
```bash
## Insulin Signaling Transduction Pathway

### Overview
Insulin regulates glucose metabolism by binding to its receptor tyrosine kinase (IRTK) on target cells (liver, skeletal muscle, adipose tissue).

### Key Steps
1. **Receptor Activation**: Insulin binds to α-subunit → conformational change → β-subunit autophosphorylation
2. **IRS Phosphorylation**: IRS-1/2 (Insulin Receptor Substrate) is phosphorylated at tyrosine residues
3. **PI3K Activation**: p85 regulatory subunit binds IRS → p110 catalytic subunit activates
4. **PIP3 Generation**: PI3K converts PIP₂ → PIP₃ at the plasma membrane
5. **Akt/PKB Activation**: PDK1 phosphorylates Akt at Thr308 → mTORC2 phosphorylates at Ser473
6. **GLUT4 Translocation**: Akt signaling triggers GLUT4-containing vesicles to fuse with plasma membrane
7. **Glucose Uptake**: Glucose enters the cell via GLUT4 for metabolism or storage

### Clinical Relevance
- **Insulin Resistance**: Impaired IRS-PI3K-Akt signaling leads to reduced GLUT4 translocation
- **Type 2 Diabetes**: Chronic hyperglycemia due to defective insulin signaling
- **Pharmacological Targets**: Metformin (AMPK activation), Thiazolidinediones (PPARγ agonists)
```

#### 2️⃣ 机制分析 / Mechanism Analysis

**Question:**
```bash
详细说明 gastric-secretion-three-phase-regulation-mechanism 中头期、胃期和肠期的神经-体液调控
```

**Answer:**
```bash
## 胃液分泌三时相调节机制

### 头期（Cephalic Phase）
- **触发**: 食物视觉、嗅觉、味觉、咀嚼、吞咽
- **神经通路**: 迷走神经（传出纤维）→ 刺激壁细胞、G细胞
- **介质**: ACh（壁细胞）、GRP（G细胞→促胃液素）
- **分泌量**: 约占进食后总分泌量的30%

### 胃期（Gastric Phase）
- **触发**: 胃扩张（食物进入）、蛋白质消化产物
- **机制**: 
  - 机械扩张 → 迷走-迷走长反射 + 壁内神经丛短反射
  - 化学刺激 → G细胞释放促胃液素
- **分泌量**: 约占60%

### 肠期（Intestinal Phase）
- **触发**: 食糜进入十二指肠
- **机制**: 
  - 早期：十二指肠G细胞释放促胃液素（少量）
  - 晚期：促胰液素、胆囊收缩素（CCK）、抑胃肽（GIP）抑制胃分泌
- **分泌量**: 约占10%

### 临床意义
- 迷走神经切断术可显著减少头期和胃期分泌
- H₂受体拮抗剂和质子泵抑制剂主要抑制壁细胞泌酸
```

#### 3️⃣ 案例分析 / Case Analysis

**Question:**
```bash
使用 arterial-blood-gas-interpretation 分析：PaO₂ 55 mmHg, PaCO₂ 60 mmHg, pH 7.25
```

**Answer:**
```bash
## 动脉血气分析结果判读

| 参数 | 数值 | 正常范围 | 评判 |
|------|------|----------|------|
| PaO₂ | 55 mmHg | 80-100 | 严重低氧血症 |
| PaCO₂ | 60 mmHg | 35-45 | 高碳酸血症（通气不足） |
| pH | 7.25 | 7.35-7.45 | 酸中毒 |

### 综合判断
- **呼吸性酸中毒**（PaCO₂↑ + pH↓）
- **II型呼吸衰竭**（PaO₂ < 60 mmHg + PaCO₂ > 50 mmHg）
- 考虑慢性阻塞性肺疾病急性加重或中枢性呼吸抑制

### 处理原则
1. 改善通气（无创/有创正压通气）
2. 氧疗（低流量氧疗，目标SpO₂ 88-92%）
3. 治疗原发病（支气管扩张剂、糖皮质激素、抗感染）
```

---

## 👥 关于作者 / About the Author

**小绿绿 xllgreen** ([xllgreen.github.io](https://xllgreen.github.io)) — 九江学院临床医学院学生 · 科技极客
Medical student at Jiujiang University · Tech geek

---

## 💻 技术支持 / Tech Support

- **PDF2App 项目 / Project**: https://pdf2app.cn
- **Visual Studio Code**: https://code.visualstudio.com/
- **Claude Code for VS Code**: https://claude.com/
- © 2026 Anthropic PBC

<img src="https://cdn.deepseek.com/logo.png?x-image-process=image%2Fresize%2Cw_1920" width="130px">
<br>**DeepSeek API**: https://platform.deepseek.com/
<br>© 2026 杭州深度求索人工智能基础技术研究有限公司 版权所有

<img src="https://cdn.cnbj1.fds.api.mi-img.com/aife/mimo-blog-fe/doc_build/static/image/logo.99baaffe.png" width="130px">
<br>**Xiaomi Mimo API**: https://platform.xiaomimimo.com/
<br>Copyright © 2010 - 2026 Xiaomi. All Rights Reserved

---

## 📜 许可证 / License

本项目内容基于人民卫生出版社《生理学》第10版整理，仅供学习参考。
This project is organized based on PMPH *Physiology*, 10th Edition, for educational purposes only.

---

## ⭐ Star History

<a href="https://www.star-history.com/#xllgreen/Physiology-PMPH-10edition&Date">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=xllgreen/Physiology-PMPH-10edition&type=Date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=xllgreen/Physiology-PMPH-10edition&type=Date" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=xllgreen/Physiology-PMPH-10edition&type=Date" />
 </picture>
</a>
