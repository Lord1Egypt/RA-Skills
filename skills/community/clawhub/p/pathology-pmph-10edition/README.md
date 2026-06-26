# 病理学 Pathology-PMPH-10edition
<div align="center">

> *「21世纪医学生指南」*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![Skills](https://img.shields.io/badge/skills.sh-Compatible-green)](https://skills.sh)

<br>
> 基于人民卫生出版社《病理学》第10版的临床技能手册 — 145 项病理学核心技能
<br>
<br>
<img src="/assets/Pathology.png" width="260px">
<br>

何必苦苦读一本书<br>
只需输入一个问题，自动从课本中找到解决方案

<br>

**其他语言 / Other Languages:**

[English](README_EN.md) · [日本語](README_JP.md) · [Français](README_FR.md) · [Русский](README_RU.md)

</div>

---

## 项目简介

本项目系统整合病理学核心理论、疾病机制解析、组织诊断标准、分子分型策略及临床转化应用等核心领域，涵盖 **145 项关键技能**，分为 7 大分类。

**适用人群**：医学生、病理医师、临床研究人员、公共卫生工作者

**参考教材**：人民卫生出版社《病理学》第 10 版（2024 年 7 月出版）

**⚠️风险⚠️**：该技能涵盖病理诊断、疾病机制分析、分子分型及治疗决策支持等内容，这些内容可能被误用为独立的医疗建议。

缓解措施：仅将输出作为教育或临床医生审核的参考资料使用，并根据当前官方指南、本地方案和合格病理专家核实建议。

## 项目结构

```
Pathology-PMPH-10edition/
├── SKILL.md              # 核心配置 — 145 项技能注册表
├── README.md             # 本文档 — 项目说明与使用指南
├── <skill-name>/         # 各项技能的详细定义
│   └── SKILL.md          #   技能详情（使用时机、执行步骤、参考文档）
├── index.md              # 完整技能索引与分类导航
└── assets/               # 资源文件
```

## 技能分类一览

| 分类 | 技能数 | 说明 |
|------|--------|------|
| 🔬 基础病理机制 | 11 | 细胞适应、损伤、死亡、再生、纤维化 |
| 🛡️ 炎症与免疫 | 8 | 急慢性炎症、渗出液鉴别、自身免疫机制 |
| 🦠 感染性疾病病理 | 20 | 结核、硅肺、病毒性肺炎、HIV、梅毒 |
| 🧬 肿瘤病理与分子诊断 | 30 | 癌基因、转移机制、IHC、分子分型 |
| 🫀 各系统疾病病理 | 63 | 心血管、呼吸、消化、泌尿、神经、内分泌、生殖 |
| 🔎 诊断技术与方法学 | 13 | 活检、细胞学、基因芯片、单细胞测序 |
| ⚕️ 特殊病理现象与分类 | 8 | 色素沉着、淤血、水肿、钙化、出血 |

## 快速开始

### 安装

CLI：
```bash
openclaw skills install pathology-pmph-10edition
```

Prompt：
```bash
Before installing anything, inspect the ClawHub skill metadata and setup requirements.
If the skill asks you to install a third-party package or CLI, verify its source, maintainer, and package contents before running the install command.
Install the skill "Pathology-PMPH-10edition" (xllgreen/pathology-pmph-10edition) from ClawHub only after those checks pass.
Skill page: https://clawhub.ai/xllgreen/pathology-pmph-10edition
Keep the work scoped to this skill only.
After install, help me finish setup from verified skill metadata.
Use only the metadata you can verify from ClawHub; do not invent missing requirements.
Ask before making any broader environment changes.
```

### 使用方式

每个技能包含以下内容：
1. **使用时机** — 何时触发该技能
2. **执行步骤** — 标准化操作流程
3. **注意事项** — 禁忌与警示
4. **参考文档** — 详细补充资料

### 提问策略

#### 1. 概念
Question:
```bash
动脉粥样硬化的发病机制
```
Answer:
```bash
## 《病理学》动脉粥样硬化发病机制

动脉粥样硬化（Atherosclerosis, AS）是一种以**脂质沉积、炎症反应、平滑肌细胞增殖和纤维化**为特征的慢性动脉疾病。

### 核心发病机制

#### 1. 脂质浸润学说
- LDL 经受损内皮进入内膜下 → 被氧化修饰为 ox-LDL
- ox-LDL 被巨噬细胞清道夫受体摄取 → 泡沫细胞形成
- 泡沫细胞聚集 → 脂纹（最早可逆病变）

#### 2. 内皮损伤反应学说
- 危险因素（高血压、吸烟、高血脂、糖尿病）→ 内皮功能障碍
- 内皮通透性↑ → 黏附分子表达↑ → 单核细胞黏附、迁移
- 内皮损伤是 AS 的起始步骤

#### 3. 炎症学说
- 巨噬细胞和 T 细胞浸润释放炎症因子（IL-1、TNF-α、MCP-1）
- 炎症促进泡沫细胞形成、平滑肌细胞迁移增殖
- 炎症贯穿 AS 全过程

#### 4. 平滑肌细胞增殖学说
- 中膜 SMC 迁移至内膜 → 表型转化（收缩型→合成型）
- SMC 分泌 ECM（胶原、蛋白聚糖）→ 纤维帽形成
- SMC 也可摄取脂质 → 泡沫细胞

### 病理分期
| 分期 | 名称 | 特征 |
|------|------|------|
| I | 脂纹 | 内膜下泡沫细胞聚集 |
| II | 纤维斑块 | 纤维帽覆盖脂质核心 |
| III | 粥样斑块 | 脂质核心 + 纤维帽 + 钙化 |
| IV | 继发性病变 | 破裂、出血、血栓、动脉瘤 |

> **一句话总结：** 内皮损伤 + 脂质浸润 + 炎症反应 → 泡沫细胞聚集 → 斑块形成 → 继发性病变。
```

#### 2. 病理鉴别诊断
Question:
```bash
女性，45岁，因"双下肢水肿伴泡沫尿2个月"就诊。尿常规：蛋白（+++），潜血（+）。24小时尿蛋白定量 4.2g。血清白蛋白 28g/L。最可能的诊断是什么？如何进行病理分型？
```
Answer:
```bash
## 病例分析

| 项目 | 表现 |
|------|------|
| 年龄 | 45岁 |
| 症状 | 双下肢水肿、泡沫尿 |
| 尿蛋白 | （+++），24h 4.2g（>3.5g → 肾病范围） |
| 血清白蛋白 | 28 g/L（<30 → 低白蛋白血症） |
| 潜血 | （+） |

### 最可能的诊断
**肾病综合征**

### 诊断依据
1. **大量蛋白尿**（24h > 3.5g）✓
2. **低白蛋白血症**（<30 g/L）✓
3. **水肿** ✓
4. **高脂血症**（待查）

### 病理分型建议
肾小球疾病的病理诊断需依赖肾活检：

| 类型 | 光镜 | 免疫荧光 | 电镜 |
|------|------|----------|------|
| 微小病变型（MCD） | 基本正常 | 阴性 | 足突融合 |
| 膜性肾病（MN） | GBM 弥漫增厚 | IgG+C3 颗粒状沉积 | 上皮下电子致密物 |
| FSGS | 局灶节段硬化 | IgM+C3 团块状 | 足突融合+硬化 |
| 膜增生性（MPGN） | 系膜增生+GBM双轨 | IgG+C3 | 内皮下/系膜区致密物 |

> 成人肾病综合征最常见的病理类型是 **膜性肾病**，建议行肾活检明确诊断。
```

#### 3. 分子分型
Question:
```bash
一名58岁男性确诊为非小细胞肺癌，组织学为肺腺癌。应优先检测哪些分子标志物以指导靶向治疗？
```
Answer:
```bash
## NSCLC 肺腺癌分子检测优先级

### 必检基因（NCCN/CSCO 指南推荐）
| 基因 | 中国人群突变率 | 可用靶向药物 |
|------|---------------|-------------|
| EGFR | 40-50% | 奥希替尼、吉非替尼、厄洛替尼 |
| ALK 融合 | 5-7% | 克唑替尼、阿来替尼 |
| ROS1 融合 | 2-3% | 克唑替尼 |
| BRAF V600E | 1-2% | 达拉非尼+曲美替尼 |
| MET 14跳突 | 3% | 赛沃替尼、卡马替尼 |
| RET 融合 | 1-2% | 普拉替尼、塞尔帕替尼 |
| NTRK 融合 | <1% | 拉罗替尼、恩曲替尼 |

### 检测方法推荐
1. **首选**：NGS（二代测序）— 一次性覆盖所有驱动基因
2. **次选**：ARMS-PCR（如仅检测EGFR）
3. **补充**：IHC（ALK、ROS1、PD-L1）

### PD-L1 表达检测
- 指导免疫治疗（帕博利珠单抗等）
- TPS ≥ 50%：可单药一线
- TPS 1-49%：联合化疗

> **建议**：优先送检 NGS panel 覆盖上述全部基因，同时行 PD-L1 IHC 检测。
```

**其他示例：**
- "请解释结核病的四种基本病理改变及其免疫学基础。"
- "如何对宫颈鳞状上皮内病变（SIL）进行分级和风险评估？"
- "比较酒精性与代谢性脂肪肝的病理鉴别要点。"
- "WHO 中枢神经系统肿瘤分类中，成人弥漫性胶质瘤如何基于分子标志物进行分型？"
- "分析 SLE 中组织损伤的免疫机制（II型/III型超敏反应）。"

## 完整技能索引

详细技能列表请参见 [index.md](index.md)，包含全部 145 项技能的描述与使用时机。

## 关于作者

**小绿绿 xllgreen** ([https://xllgreen.github.io](https://xllgreen.github.io)) — 九江学院临床医学院学生 · 科技极客

## 技术支持

PDF2App 项目：[https://pdf2app.cn](https://pdf2app.cn)

Microsoft Visual Studio Code：[https://code.visualstudio.com/](https://code.visualstudio.com/)

Claude Code for VS Code：[https://claude.com/](https://claude.com/)

© 2026 Anthropic PBC

<br>

<img src="https://cdn.deepseek.com/logo.png?x-image-process=image%2Fresize%2Cw_1920" width="130px">

<br>DeepSeek API：[https://platform.deepseek.com/](https://platform.deepseek.com/)

© 2026 杭州深度求索人工智能基础技术研究有限公司 版权所有

<br>

<img src="https://cdn.cnbj1.fds.api.mi-img.com/aife/mimo-blog-fe/doc_build/static/image/logo.99baaffe.png" width="130px">

<br>Xiaomi Mimo API：[https://platform.xiaomimimo.com/](https://platform.xiaomimimo.com/)

Copyright © 2010 - 2026 Xiaomi. All Rights Reserved

<br>

## 许可证

本项目内容基于人民卫生出版社《病理学》第10版整理，仅供学习参考。

## Star History

<a href="https://www.star-history.com/?repos=xllgreen%2FPathology-PMPH-10edition&type=date&legend=top-left">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=xllgreen/Pathology-PMPH-10edition&type=date&theme=dark&legend=top-left" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=xllgreen/Pathology-PMPH-10edition&type=date&legend=top-left" />
   <img alt="Star History Chart" src="https://api.star-history.com/chart?repos=xllgreen/Pathology-PMPH-10edition&type=date&legend=top-left" />
 </picture>
</a>
