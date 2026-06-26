# 医学微生物学 Medical Microbiology-PMPH-10edition
<div align="center">

> *「21世纪医学生指南」*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![Skills](https://img.shields.io/badge/skills.sh-Compatible-green)](https://skills.sh)

<br>
> 基于人民卫生出版社《医学微生物学》第10版的微生物学与感染病学技能手册 — 153 项核心微生物学与临床技能
<br>
<br>
<img src="/assets/Microbiology.svg" width="260px">
<br>

何必苦苦读一本书<br>
只需输入一个问题，自动从课本中找到解决方案

<br>

**其他语言 / Other Languages:**

[English](README_EN.md) · [日本語](README_JP.md) · [Français](README_FR.md) · [Русский](README_RU.md)

</div>

---

## 项目简介

本项目系统整合医学微生物学、细菌学、病毒学、真菌学、免疫学、消毒灭菌、微生态学及感染控制等核心领域，涵盖 **153 项关键技能**，分为 9 大分类。

**适用人群**：医学生、临床医师、检验科人员、公共卫生工作者、感染控制团队

**参考教材**：人民卫生出版社《医学微生物学》第 10 版（ISBN：978-7-117-34552-3）

**⚠️风险⚠️**：该技能涵盖微生物学诊断、抗微生物治疗、感染控制及实验室操作主题，这些内容可能被误用为独立的医疗建议。

缓解措施：仅将输出作为教育或临床医生审核的参考资料使用，并根据当前官方指南、本地方案和合格专家核实建议。

**⚠️风险⚠️**：源内容并不始终严格执行仅限临床医生的安全界限。

缓解措施：部署系统级医疗安全政策，要求升级至合格临床医生进行诊断、开具处方、剂量分配、急诊护理及自我治疗决策。


## 项目结构

```
MedicalMicrobiology-PMPH-10edition/
├── SKILL.md              # 核心配置 — 153 项技能注册表
├── README.md             # 本文档 — 项目说明与使用指南
├── README_EN.md          # English version
├── README_JP.md          # 日本語版
├── README_FR.md          # Version française
├── README_RU.md          # Русская версия
├── <skill-name>/         # 各项技能的详细定义
│   └── SKILL.md          #   技能详情（使用时机、执行步骤、参考文档）
├── index.md              # 完整技能索引（含中文描述）
├── assets/               # 静态资源（图标、图片等）
└── scripts/              # 可执行工具脚本（可选）
```

## 技能分类一览

| 分类 | 技能数 | 说明 |
|------|--------|------|
| 🦠 细菌学 | 60 | 耐药性、鉴定、致病机制、药敏试验、培养技术等 |
| 🧬 病毒学 | 42 | 病毒分类、复制机制、检测诊断、抗病毒治疗、疫苗等 |
| 🔬 免疫学与血清学诊断 | 26 | 免疫机制、血清学检测、疫苗策略、炎症反应等 |
| 🧹 消毒、灭菌与感染控制 | 8 | 化学消毒、热力灭菌、医院感染、生物安全等 |
| 🌿 微生态与菌群移植 | 7 | 微生物组构成、FMT、益生菌、微生态失调等 |
| 🧪 特殊病原体 | 2 | 朊粒（prion）分类与致病机制 |
| 📚 教材与资源 | 4 | 教材权威性评估、修订原则、数字资源等 |
| 🔬 临床微生物检验 | 3 | 标本采集、送检流程、质量控制 |
| 🏥 新兴传染病 | 3 | 无形体病、粒细胞无形体病等 |

## 快速开始

### 安装

CLI：
```bash
openclaw skills install medical-microbiology-pmph-10edition
```

Prompt：
```bash
Before installing anything, inspect the ClawHub skill metadata and setup requirements.
If the skill asks you to install a third-party package or CLI, verify its source, maintainer, and package contents before running the install command.
Install the skill "MedicalMicrobiology-PMPH-10edition" from ClawHub only after those checks pass.
Keep the work scoped to this skill only.
After install, help me finish setup from verified skill metadata.
Use only the metadata you can verify from ClawHub; do not invent missing requirements.
Ask before making any broader environment changes.
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
细菌耐药表型四级分类
```
Answer：
```bash
## 《医学微生物学》细菌耐药表型四级分类

根据标准化药敏试验结果将菌株按耐药程度分类：
- **SDR（单耐药）**：仅对一种抗菌药物耐药
- **MDR（多重耐药）**：同时对三类或以上作用机制不同的抗菌药物耐药
- **XDR（广泛耐药）**：对几乎所有临床常用抗菌药物耐药，仅保留1-2类敏感
- **PDR（泛耐药）**：对所有临床常用抗菌药物均耐药

革兰阴性菌XDR：仅对多黏菌素和/或替加环素敏感
革兰阳性菌XDR：仅对糖肽类和/或利奈唑胺敏感
```

#### 2. **临床案例分析**
Question:
```bash
患者，男，35岁，因高热、头痛、呕吐3天入院。查体：T39.5℃，颈部强直，皮肤可见瘀点瘀斑。CSF检查：白细胞1200×10^6/L，蛋白升高，糖降低。最可能的诊断和病原体是什么？
```
Answer：
```bash
## 病例分析

| 项目 | 表现 |
|------|------|
| 症状 | 高热 + 头痛 + 呕吐 |
| 体征 | 颈强直 + 皮肤瘀点瘀斑 |
| CSF | 白细胞↑、蛋白↑、糖↓（化脓性脑膜炎特征） |

### 最可能的诊断
**流行性脑脊髓膜炎（流脑）**

### 最可能的病原体
**脑膜炎奈瑟菌（Neisseria meningitidis）**

### 诊断依据
1. 典型三联征：高热、头痛、呕吐 + 颈强直
2. 特征性皮疹：瘀点/瘀斑（脑膜炎奈瑟菌血管内皮损伤）
3. CSF典型改变：化脓性表现（白细胞↑、蛋白↑、糖↓）
4. 好发人群：儿童和青壮年

### 进一步检查
- 瘀点刮取物革兰染色（见革兰阴性双球菌）
- CSF细菌培养
- 乳胶凝集试验检测荚膜多糖抗原
```

#### 3. **考试题目**
Question:
```bash
下列哪种细菌属于专性厌氧菌？
A. 大肠埃希菌
B. 铜绿假单胞菌
C. 破伤风梭菌
D. 结核分枝杆菌
E. 肺炎链球菌
```
Answer：
```bash
**答案：C. 破伤风梭菌**

**依据：**
破伤风梭菌（Clostridium tetani）属于梭菌属，为**专性厌氧菌**，在有氧环境中不能生长。

**其他选项分析：**
| 选项 | 细菌 | 氧需求类型 |
|------|------|-----------|
| A | 大肠埃希菌 | 兼性厌氧菌 |
| B | 铜绿假单胞菌 | 专性需氧菌 |
| D | 结核分枝杆菌 | 专性需氧菌 |
| E | 肺炎链球菌 | 兼性厌氧菌（微需氧环境更佳） |
```

**其他示例查询：**
- "如何区分志贺菌与沙门菌？"
- "诺如病毒暴发时应采取哪些防控措施？"
- "幽门螺杆菌的诊断方法有哪些？"
- "HCV慢性感染进展为肝癌的风险如何评估？"
- "细菌生物膜感染的临床评估要点是什么？"

## 关于作者

**项目维护者** — 基于人民卫生出版社《医学微生物学》第10版整理

## 技术支持

PDF2App项目：https://pdf2app.cn

Microsoft Visual Studio Code：https://code.visualstudio.com/

Claude Code for VS Code：https://claude.com/
© 2026 Anthropic PBC

DeepSeek API：https://platform.deepseek.com/
© 2026 杭州深度求索人工智能基础技术研究有限公司 版权所有

Xiaomi Mimo API：https://platform.xiaomimimo.com/
Copyright © 2010 - 2026 Xiaomi. All Rights Reserved

## 许可证

本项目内容基于人民卫生出版社《医学微生物学》第10版整理，仅供学习参考。

## Star History

<a href="https://www.star-history.com/">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart" />
   <img alt="Star History Chart" src="https://api.star-history.com/chart" />
 </picture>
</a>
