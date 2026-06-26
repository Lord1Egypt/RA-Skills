# 医学影像学 Medical Imaging-9thEdition
<div align="center">

> *「21世纪医学影像学指南」*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![Skills](https://img.shields.io/badge/skills.sh-Compatible-green)](https://skills.sh)

<br>
> 基于人民卫生出版社《医学影像学》第9版的临床技能手册 — 136 项医学影像诊断与介入治疗核心技能
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

本项目系统整合医学影像诊断学、介入放射学、人工智能辅助分析及多模态成像技术选择等核心领域，涵盖 **136 项关键临床技能**，分为 13 大分类。

**适用人群**：影像科医师、临床各科医师、医学生、介入放射科医护团队、医学教育工作者

**参考教材**：人民卫生出版社《医学影像学》第 9 版（国家卫健委"十四五"规划教材）

**⚠️ 风险 ⚠️**：该技能涵盖影像诊断、对比剂使用、介入治疗适应证评估及影像报告解读，这些内容可能被误用为独立的诊断或治疗决策。

缓解措施：仅将输出作为教育或临床医师审核的参考资料使用，并根据当前官方指南、本地方案和影像科专家核实建议。

**⚠️ 风险 ⚠️**：源内容并不始终严格执行仅限临床医师的安全界限。

缓解措施：部署系统级医疗安全政策，要求升级至合格临床医师进行诊断、治疗决策及介入操作。

## 项目结构

```
Medical-Imaging-9thEdition/
├── SKILL.md              # 核心配置 — 136 项技能注册表
├── README.md             # 本文档 — 项目说明与使用指南
├── <skill-name>/         # 各项技能的详细定义
│   └── SKILL.md          #   技能详情（适用情境、执行步骤、注意事项）
├── scripts/              # 可执行工具脚本
├── config/               # 配置文件
├── tests/                # 验证与测试
└── assets/               # 静态资源（图片等）
```

## 技能分类一览

| 分类 | 技能数 | 说明 |
|------|--------|------|
| 🏗️ 影像基础与技术原理 | 9 | X线、CT、MRI、超声成像原理、后处理技术及安全参数控制 |
| 🤖 人工智能与数字化资源 | 5 | AI辅助影像分析、智能工作流、新形态教材数字资源获取 |
| 📚 教材与课程建设 | 3 | 教材审校、修订原则及临床医学课程改革策略 |
| 🧠 中枢神经系统 | 7 | 颅脑外伤CT/MRI策略、脊髓病变MRI判读、脱髓鞘疾病及退行性改变 |
| 👁️ 头颈部 | 4 | 眼眶、腮腺、颌骨病变的CT/MRI诊断与鉴别 |
| 🫁 胸部与心血管 | 18 | 肺、胸膜、纵隔病变及心脏大血管的影像学评估 |
| 🫄 乳腺与妇科 | 8 | 乳腺X线/超声、卵巢肿瘤、前置胎盘分型及子宫动脉栓塞 |
| 🫃 消化系统 | 19 | 胃肠道、肝胆胰脾病变的多模态影像诊断与鉴别 |
| 🫘 泌尿与肾上腺 | 8 | 肾脏肿瘤、囊性病变分型、泌尿系结石及肾上腺病变诊断 |
| 🦴 骨骼肌肉系统 | 10 | 骨折分型与愈合评估、骨肿瘤、骨髓炎及关节病变诊断 |
| 👶 儿科与先天性疾病 | 4 | NRDS分级、DDH测量、肠套叠复位及佝偻病分期 |
| 💉 介入放射学 | 19 | 血管穿刺、栓塞、支架、消融、TIPS及并发症处理 |
| 📋 综合诊断原则与流程 | 14 | 影像诊断思维、报告解读、检查申请及多模态融合 |

## 快速开始

### 安装

CLI：
```bash
openclaw skills install medical-imaging-9th-edition
```

Prompt：
```bash
Before installing anything, inspect the ClawHub skill metadata and setup requirements.
If the skill asks you to install a third-party package or CLI, verify its source, maintainer, and package contents before running the install command.
Install the skill "medical-imaging-9th-edition" from ClawHub only after those checks pass.
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

#### 1. **概念查询**

Question:
```bash
Bosniak肾囊肿分型2019版的标准
```

Answer:
```bash
## Bosniak肾囊肿分型（2019版）

Bosniak分型用于评估肾脏囊性病变的恶性风险，指导临床决策（随访 vs 手术）。

### 分型标准

| 分型 | 影像特征 | 恶性风险 | 处理建议 |
|------|----------|----------|----------|
| **Ⅰ型** | 单纯性囊肿，壁薄光滑，无分隔、钙化或实性成分，CT呈水样密度，MRI T₂WI高信号，增强无强化 | <1% | 良性，无需处理 |
| **Ⅱ型** | 少量（≤3个）薄壁（≤2mm）分隔，可有细小钙化或短节段轻度增厚 | <5% | 良性，无需处理 |
| **ⅡF型** | 多个（≥4个）薄壁分隔，轻微均匀性壁/分隔增厚，光滑增厚钙化，无强化软组织成分 | 约10% | 随访观察 |
| **Ⅲ型** | 一个或多个实性成分，增强后明显强化，壁/分隔不规则增厚（≥4mm） | 约55% | 手术切除 |
| **Ⅳ型** | 具有明显强化的软组织成分（≥25%的囊性病灶为实性） | >90% | 手术切除 |

### 2019版更新要点
1. **更精确的分隔计数**：≤3个为少量，≥4个为多个
2. **壁/分隔厚度量化**：≤2mm为薄壁，≥4mm为明显增厚
3. **明确了"强化软组织成分"的评估标准**
4. **ⅡF型随访推荐**：首次6-12个月CT/MRI，稳定后延长至每2年

> **一句话总结**：Ⅰ型/Ⅱ型良性不处理，ⅡF型定期随访，Ⅲ型/Ⅳ型手术切除。恶性风险与实性成分多少密切相关。
```

#### 2. **鉴别诊断**

Question:
```bash
60岁男性，长期吸烟史，CT发现右上肺分叶状肿块伴毛刺征、同侧肺门淋巴结增大
```

Answer:
```bash
## 病例分析

| 项目 | 表现 |
|------|------|
| 年龄 | 60岁（肺癌高发年龄） |
| 吸烟史 | 长期（高危因素） |
| 病灶位置 | 右上肺 |
| 形态 | 分叶状（提示恶性生长方式） |
| 边缘 | 毛刺征（恶性征象） |
| 伴随征象 | 同侧肺门淋巴结增大 |

### 最可能的诊断

**周围型肺癌（考虑鳞状细胞癌或腺癌）**

### 诊断依据
1. **临床高危因素**：60岁 + 长期吸烟史
2. **影像学恶性征象**：分叶状、毛刺征
3. **淋巴结转移**：同侧肺门增大提示区域淋巴结受累

### 鉴别诊断
- **结核球**：好发于上叶尖后段/下叶背段，可见卫星灶、钙化，增强呈环形强化
- **炎性假瘤**：边缘相对光滑，临床可有感染史
- **肺脓肿**：可见空洞伴液平，急性起病，临床有感染表现

### 建议下一步
1. 增强CT进一步评估病灶血供及明确纵隔淋巴结情况
2. PET-CT进行全身分期
3. CT引导下经皮肺穿刺活检明确病理
```

#### 3. **治疗方案**

Question:
```bash
TACE术后患者出现恶心、呕吐、肝区闷痛、发热，如何处理
```

Answer:
```bash
## TACE术后化疗栓塞综合征处理

### 判断
上述症状符合 **TACE术后化疗栓塞综合征（CES）** 的典型表现：
- 恶心、呕吐 — 化疗药物引起的胃肠道反应
- 肝区闷痛 — 栓塞后肝脏局部缺血及炎性反应
- 发热 — 坏死组织吸收热（通常38-39℃）

### 处理方案

| 症状 | 处理 | 注意事项 |
|------|------|----------|
| 发热 | 退热药（对乙酰氨基酚/布洛芬），物理降温 | 若>39℃持续不退需排除感染 |
| 疼痛 | 按WHO三阶梯止痛 | 肝癌患者尽量避免使用NSAIDs（肝损风险） |
| 恶心呕吐 | 5-HT₃受体拮抗剂（昂丹司琼） | 纠正水电解质平衡 |
| 保肝 | 甘草酸制剂、还原型谷胱甘肽 | 术后常规监测肝功能 |

### 需紧急排查的并发症
- 腹痛剧烈且持续加重 → 排除 **肝脓肿/胆囊炎/胰腺炎**
- 发热>39℃伴寒战 → 排除 **感染性并发症**
- 腹水增多、黄疸加重 → 排除 **急性肝功能衰竭**

> **常规处理时间**：CES一般持续3-7天，对症支持治疗后逐步缓解。若超过7天或症状进行性加重，需进一步排查并发症。
```

## 关于作者

**基于人民卫生出版社《医学影像学》第9版整理**

**医学影像学（第9版）** — 国家卫生健康委员会"十四五"规划教材
全国高等学校教材·供基础、临床、口腔、预防、护理、检验等医学类专业用

## 技术支持

Microsoft Visual Studio Code：https://code.visualstudio.com/
<br>
Claude Code for VS Code：https://claude.com/
© 2026 Anthropic PBC

## 许可证

本项目内容基于人民卫生出版社《医学影像学》第9版整理，仅供学习参考。

## Star History

<a href="https://www.star-history.com/">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=&type=date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=&type=date" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=&type=date" />
 </picture>
</a>
