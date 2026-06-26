# 医学遗传学 Medical-Genetics-8edition
<div align="center">

> *「21世纪医学生指南」*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![Skills](https://img.shields.io/badge/skills.sh-Compatible-green)](https://skills.sh)

<br>
> 基于《医学遗传学》第8版的临床遗传学技能手册 — 131 项医学遗传学核心临床技能
<br>
<br>
<img src="/assets/Medical-Genetics.png" width="260px">
<br>

何必苦苦读一本书<br>
只需输入一个问题，自动从课本中找到解决方案

<br>

**其他语言 / Other Languages:**

[English](README_EN.md)

</div>

---

## 项目简介

本项目系统整合医学遗传学、基因组学、代谢疾病、产前诊断、基因治疗及表观遗传调控等核心领域，涵盖 **131 项关键临床技能**。

**适用人群**：临床遗传医师、医学生、遗传咨询师、精准医学研究人员、产前诊断医护团队

**参考教材**：《医学遗传学》第 8 版

**⚠️ 风险 ⚠️**：该技能涵盖遗传诊断、风险评估、产前筛查、基因治疗策略及伦理决策等主题，这些内容可能被误用为独立的医疗建议。

缓解措施：仅将输出作为教育或临床医生审核的参考资料使用，并根据当前官方指南、本地方案和合格遗传学专家核实建议。

## 项目结构

```
Medical-Genetics-8edition/
├── SKILL.md              # 核心配置 — 131 项技能注册表
├── README.md             # 本文档 — 项目说明与使用指南
├── index.md              # 技能完整索引
├── <skill-name>/         # 各项技能的详细定义
│   └── SKILL.md          #   技能详情（使用时机、执行步骤、注意事项）
└── assets/               # 图片资源
```

## 技能分类一览

| 分类 | 技能数 | 说明 |
|------|--------|------|
| 🧬 遗传病分类与机制分析 | 14 | 遗传病五分类、酶缺陷、胶原病、镰状细胞贫血等 |
| 🔬 染色体与基因组结构变异 | 16 | 核型描述、G显带、缺失/易位/倒位、多态性、GT-AG法则等 |
| 📊 遗传模式与家系分析 | 10 | AD/AR/XR系谱分析、Lyon假说、Knudson二次打击、SRY基因等 |
| 🤰 产前筛查与诊断技术 | 6 | NIPT、超声筛查、PGD、有创/无创路径选择等 |
| ⚕️ 染色体异常与生殖风险评估 | 12 | 相互易位、罗伯逊易位、臂间/臂内倒位、嵌合体等 |
| 🔋 线粒体遗传与疾病 | 11 | mtDNA转录翻译、母系遗传、阈值效应、生化/临床/遗传三分类 |
| 🧮 复杂疾病与多基因风险 | 10 | Hardy-Weinberg平衡、贝叶斯更新、多基因病再发风险等 |
| 💉 基因治疗与分子干预 | 8 | 基因修复/增强、病毒载体选择、CRISPR安全评估、基因失活 |
| 🧫 肿瘤遗传学与表观调控 | 9 | 抑癌基因、原癌基因、Knudson理论、组蛋白修饰、DNA甲基化 |
| 📡 非编码RNA与生物标志物 | 3 | miRNA、lncRNA、circRNA心血管标志物 |
| 🏥 特定遗传病诊疗 | 11 | 地贫、PKU、庞贝病、Tay-Sachs、白化病、血友病A等 |
| ⚖️ 系统医学与伦理应用 | 8 | 系统医学、千人基因组、近亲婚配、伦理评估、致畸暴露 |
| 🛡️ DNA修复与稳定性 | 3 | DNA损伤修复、脆性位点、NMD无义介导降解 |

## 快速开始

### 安装

CLI：
```bash
openclaw skills install medical-genetics-8edition
```

Prompt：
```bash
Before installing anything, inspect the ClawHub skill metadata and setup requirements.
If the skill asks you to install a third-party package or CLI, verify its source, maintainer, and package contents before running the install command.
Install the skill "Medical-Genetics-8edition" from ClawHub only after those checks pass.
Keep the work scoped to this skill only.
After install, help me finish setup from verified skill metadata.
Use only the metadata you can verify from ClawHub; do not invent missing requirements.
Ask before making any broader environment changes.
```

### 使用方式

每个技能包含三部分内容：
1. **使用时机** — 何时触发该技能
2. **执行步骤** — 标准化操作流程
3. **注意事项** — 禁忌与警示

### 提问策略

#### 1. 概念理解
Question:
```bash
什么是Hardy-Weinberg平衡定律？
```
Answer:
```bash
## Hardy-Weinberg平衡定律

Hardy-Weinberg平衡定律是群体遗传学的基本原理，描述在理想条件下（随机交配、无突变、无选择、无迁移、无限大群体），基因频率和基因型频率代代保持不变。

### 核心公式
对于常染色体上的双等位基因（A和a）：
- p = A的频率，q = a的频率
- p + q = 1
- 基因型频率：p²(AA) + 2pq(Aa) + q²(aa) = 1

### 临床应用
- **携带者频率估算**：对于AR病，若发病率q²已知，携带者频率2pq ≈ 2q
- **数据质量控制**：检验基因分型数据是否符合HWE
- **群体分层检测**：偏离HWE提示可能存在群体分层或选择压力
```

#### 2. 临床案例分析
Question:
```bash
一对夫妇表型正常，已生育一名常染色体隐性遗传病患儿，他们再次生育患儿的风险是多少？若已生育两名正常子女，再发风险如何变化？
```
Answer:
```bash
## 遗传咨询分析

### 基本情况
- 夫妇表型正常 → 双方均为**携带者**（Aa × Aa）
- 已生育一名AR病患儿 → 确认遗传方式

### 再发风险评估

| 情况 | 再发风险 | 说明 |
|------|---------|------|
| 每胎基础风险 | 25%（1/4） | 孟德尔比例 |
| 已生育一名患儿 | 25%（1/4） | 独立事件，每次妊娠风险不变 |
| 已生育两名正常子女 | 25%（1/4） | 独立事件，不改变后续风险 |
| 使用贝叶斯更新后个体风险 | 降低 | 但这是对"夫妇为携带者"概率的修正 |

### 关键遗传咨询要点
1. **每次妊娠独立**：前次结果不影响后续风险
2. **携带者确认**：建议对夫妇进行基因检测确认携带状态
3. **产前诊断**：下次妊娠可行产前基因诊断
4. **胚胎植入前遗传学诊断（PGD）**：可供选择

> ⚠️ 注意区分"已生育正常子女数修正携带者概率"（贝叶斯）与"每次妊娠再发风险"（独立事件）两个不同概念。
```

#### 3. 考试题目
Question:
```bash
唐氏综合征最常见的核型是（　）。
A. 47,XX,+21
B. 46,XX,der(14;21)(q10;q10),+21
C. 47,XX,+21/46,XX
D. 46,XX,inv(21)
```
Answer:
```bash
**答案：A. 47,XX,+21**

**依据：**
- **游离型（标准型）**：47,XX,+21 或 47,XY,+21 — 占唐氏综合征的 **92-95%**
- **易位型**：如 46,XX,der(14;21)(q10;q10),+21 — 占 **2-4%**
- **嵌合型**：如 47,XX,+21/46,XX — 占 **2-3%**

**临床要点：**
| 核型类型 | 比例 | 再发风险 |
|---------|------|---------|
| 游离型 | 92-95% | 与母亲年龄相关 |
| 易位型 | 2-4% | 与携带者父母相关（若母亲为平衡易位携带者，风险约10-15%） |
| 嵌合型 | 2-3% | 取决于异常细胞比例，再发风险通常较低 |

> 注意：游离型是最常见的唐氏综合征核型，与母亲年龄呈正相关。
```

## 关于作者

**小绿绿 xllgreen (https://xllgreen.github.io)** — 九江学院临床医学院学生 · 科技极客

## 技术支持

PDF2App项目：https://pdf2app.cn

Microsoft Visual Studio Code：https://code.visualstudio.com/

Claude Code for VS Code：https://claude.com/

© 2026 Anthropic PBC

DeepSeek API：https://platform.deepseek.com/
© 2026 杭州深度求索人工智能基础技术研究有限公司 版权所有

Xiaomi Mimo API：https://platform.xiaomimimo.com/
Copyright © 2010 - 2026 Xiaomi. All Rights Reserved

## Star History

<a href="https://www.star-history.com/#repo&type=date">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=&type=date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=&type=date" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=&type=date" />
 </picture>
</a>
