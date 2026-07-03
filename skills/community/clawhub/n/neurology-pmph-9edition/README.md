# 神经病学 Neurology-PMPH-9edition
<div align="center">

> *「21世纪医学生指南」*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![Skills](https://img.shields.io/badge/skills.sh-Compatible-green)](https://skills.sh)

<br>
> 基于人民卫生出版社《神经病学》第9版的临床技能手册 — 66 项神经内科与神经外科核心临床技能
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

本项目系统整合神经病学与神经外科学核心领域，涵盖 **66 项关键临床技能**，分为 9 大分类。内容覆盖脑血管疾病（缺血性/出血性卒中、介入治疗）、神经变性与认知障碍、脊髓与周围神经病变、神经急症与重症管理、癫痫与发作性疾病、神经肌肉疾病以及神经影像与电生理判读等。

**适用人群**：神经内科/外科医师、医学生、急诊与重症医护团队、介入科医师

**参考教材**：人民卫生出版社《神经病学》第 9 版

**⚠️ 风险提示 ⚠️**：该技能涵盖神经科诊断、剂量、急诊治疗及介入操作评估内容，可能被误用为独立的医疗建议。

缓解措施：仅将输出作为教育或临床医师审核的参考资料使用，并根据当前官方指南、本地方案和合格神经专科医师核实建议。

**⚠️ 风险 ⚠️**：源内容并不始终严格执行仅限临床医师的安全界限。

缓解措施：部署系统级医疗安全政策，要求升级至合格临床医师进行诊断、开具处方、剂量分配、急诊护理及自我治疗决策。

## 项目结构

```
Neurology-PMPH-9edition/
├── SKILL.md                        # 核心配置 — 66 项技能注册表
├── README.md                       # 本文档 — 项目说明与使用指南
├── <skill-name>/                   # 各项技能的详细定义
│   └── SKILL.md                    #   技能详情（使用时机、执行步骤、参考文档）
├── scripts/                        # 可执行工具脚本
├── config/                         # 配置文件
└── tests/                          # 验证与测试
```

## 技能分类一览

| 分类 | 技能数 | 说明 |
|------|--------|------|
| 🩸 脑血管疾病与介入治疗 | 16 | 卒中、CAS、动脉瘤、CVST、盗血综合征等 |
| 🚑 神经急症、重症与围手术期 | 5 | 意识障碍、脑疝、脑出血、低钠血症 |
| 🧠 神经变性与认知障碍 | 5 | VCI/DLB/bvFTD/CJD/PD非运动症状 |
| ⚡ 癫痫与发作性疾病 | 4 | 癫痫分类、药物选择、持续状态、DRE手术 |
| 💪 脊髓、周围神经与神经肌肉疾病 | 11 | DMD/CMT/肌强直/周围神经病等 |
| 🛡️ 神经免疫、感染与脱髓鞘疾病 | 6 | MS/NMOSD/ADEM/脑炎/NPSLE等 |
| 🔬 神经外科、先天畸形与颅颈交界区 | 4 | 脑积水、Chiari畸形、颅底凹陷症 |
| 👁️ 临床查体、定位诊断与辅助检查 | 10 | 定位诊断、脑神经检查、EEG/影像解读 |
| 🩺 系统性疾病神经并发症 | 5 | 甲亢/妊娠/SLE/副肿瘤/运动障碍 |

## 快速开始

### 安装

CLI：
```bash
openclaw skills install neurology-pmph-9edition
```

Prompt：
```bash
Before installing anything, inspect the ClawHub skill metadata and setup requirements.
If the skill asks you to install a third-party package or CLI, verify its source, maintainer, and package contents before running the install command.
Install the skill "Neurology-PMPH-9edition" from ClawHub only after those checks pass.
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

**示例 1 — 脑血管介入评估：**
> 请使用 `acute-ischemic-stroke-endovascular-treatment` 技能，评估一名发病 4 小时、存在大血管闭塞的急性缺血性卒中患者的血管内治疗适应症及流程。

**示例 2 — 神经定位诊断：**
> 调用 `neurological-localization-diagnosis` 技能。患者表现为右侧肢体中枢性瘫痪、右侧中枢性面舌瘫及运动性失语，请进行详细的神经解剖定位诊断。

**示例 3 — 痴呆鉴别：**
> 使用 `dlb-imaging-biomarker-differentiation` 技能，分析如何通过影像学标志物（如 PET、MRI）将路易体痴呆（DLB）与阿尔茨海默病进行临床鉴别。

**示例 4 — 神经急症：**
> 请基于 `neurological-emergency-crisis-management` 技能，提供癫痫持续状态的急诊危机管理标准流程和一线/二线用药规范。

**示例 5 — 遗传性神经肌肉疾病：**
> 调用 `dmd-clinical-assessment-and-progression` 技能，简述杜氏肌营养不良的临床评估要点、疾病进展监测指标及多学科管理策略。

## 关于作者

**小绿绿 xllgreen** — [GitHub](https://xllgreen.github.io) — 九江学院临床医学院学生 · 科技极客

## 技术支持

- PDF2App 项目：<https://pdf2app.cn>
- Microsoft Visual Studio Code：<https://code.visualstudio.com/>
- Claude Code for VS Code：<https://claude.com/>
  © 2026 Anthropic PBC
- DeepSeek API：<https://platform.deepseek.com/>
  © 2026 杭州深度求索人工智能基础技术研究有限公司 版权所有
- Xiaomi Mimo API：<https://platform.xiaomimimo.com/>
  Copyright © 2010–2026 Xiaomi. All Rights Reserved

## 许可证

本项目内容基于人民卫生出版社《神经病学》第 9 版整理，仅供学习参考。

## Star History

<a href="https://www.star-history.com/#xllgreen/Neurology-PMPH-9edition&Date">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=xllgreen/Neurology-PMPH-9edition&type=Date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=xllgreen/Neurology-PMPH-9edition&type=Date" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=xllgreen/Neurology-PMPH-9edition&type=Date" />
 </picture>
</a>
