# 病理生理学 Pathophysiology-PMPH-10edition
<div align="center">

> *「揭示疾病机制，架接基础与临床」*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![Skills](https://img.shields.io/badge/skills.sh-Compatible-green)](https://skills.sh)

<br>
> 基于人民卫生出版社《病理生理学》第 10 版的临床技能手册 — 145 项病理生理学核心技能
<br>
<br>
<br>

**其他语言 / Other Languages:**

[English](README_EN.md) · [日本語](README_JP.md) · [Français](README_FR.md) · [Русский](README_RU.md)

</div>

---

## 项目简介

本项目系统整合病理生理学领域的 **145 项核心能力**，内容横跨酸碱平衡紊乱、休克与多器官功能障碍、水电解质代谢异常、炎症与免疫应答、细胞信号转导、肿瘤发生机制、衰老相关病理过程、呼吸与循环功能障碍、神经精神障碍、肾脏病理生理、内分泌代谢疾病等多个关键主题。

**适用人群**：医学生、病理生理学教师、临床医师、基础医学研究者

**参考教材**：人民卫生出版社《病理生理学》第 10 版

**⚠️ 风险⚠️**：该技能涵盖疾病机制分析、诊断推理和治疗原则等内容，可能被误用为独立的临床决策依据。

缓解措施：仅将输出作为教育或临床医生审核的参考资料使用，并根据当前官方指南、本地方案和合格专家核实建议。

## 项目结构

```
Pathophysiology-PMPH-10edition/
├── SKILL.md              # 核心配置 — 145 项技能注册表
├── README.md             # 本文档 — 项目说明与使用指南
├── <skill-name>/         # 各项技能的详细定义
│   └── SKILL.md          #   技能详情（使用时机、执行步骤、参考文档）
└── tests/                # 验证与测试
```

## 技能分类一览

| 分类 | 技能数 | 说明 |
|------|--------|------|
| ⚖️ 酸碱平衡与电解质紊乱 | 22 | 呼吸/代谢性酸碱失衡、钾镁钙磷代谢异常等 |
| 🚑 休克、循环障碍与多器官功能障碍 | 8 | 休克分期、MODS、血流动力学分型等 |
| 💧 水肿与液体分布异常 | 3 | 水肿分类、机制、分布模式 |
| 🫁 呼吸功能障碍 | 7 | 低氧应答、V/Q失衡、ARDS、氧疗等 |
| 🫘 肾脏病理生理 | 9 | AKI分期、CRF水钠钙磷代谢等 |
| ❤️ 心血管病理生理 | 7 | 心肌肥大、心衰分类、兴奋-收缩耦联等 |
| 🌡️ 发热与体温调节 | 6 | 发热机制、免疫防御、代谢调整等 |
| 🧠 应激与神经内分泌调控 | 8 | HPA轴、应激性高血压、应激性溃疡等 |
| 📡 细胞信号转导与调控 | 4 | RTK、GPCR、JAK-STAT通路等 |
| 🔬 细胞周期、凋亡与肿瘤发生 | 10 | 细胞周期检查点、凋亡通路、RAS/BRAF突变等 |
| 🛡️ 炎症、感染与免疫 | 7 | DIC、急性期蛋白、内毒素血症等 |
| 🔄 缺血-再灌注损伤 | 5 | 钙超载、自由基、保护策略等 |
| 🩺 代谢综合征与脂质异常 | 8 | 高脂血症分型、低脂血症、脂蛋白代谢等 |
| 👴 衰老与退行性疾病 | 6 | 炎性衰老、肌少症、AD蛋白聚集等 |
| 🫃 肝性脑病与氨中毒 | 3 | 氨中毒、假性神经递质等 |
| 🩸 凝血与出血障碍 | 3 | 凝血因子缺陷、血管源性出血等 |
| 🧬 神经系统与意识障碍 | 5 | 脑死亡判定、昏迷分级、意识障碍等 |
| 🍬 糖尿病与代谢紊乱 | 3 | 糖尿病酮症酸中毒、高血糖代谢紊乱等 |
| 🔴 红细胞与氧运输 | 2 | 2,3-DPG调节、血氨分析 |
| 📚 教学与课程体系 | 11 | 学习方法、课程结构、教材编写等 |
| **总计** | **145** | — |

## 快速开始

### 安装

CLI：
```bash
openclaw skills install pathophysiology-pmph-10edition
```

### 使用方式

每个技能包含四部分内容：
1. **使用时机** — 何时触发该技能
2. **执行步骤** — 标准化操作流程
3. **注意事项** — 禁忌与警示
4. **参考文档** — 详细补充资料

### 提问策略

#### 1. **概念理解**
```
请解释 hypoxic-pulmonary-vasoconstriction-mechanism 的生理意义及在ARDS中的变化。
```

#### 2. **机制分析**
```
如何应用 dic-diagnosis-and-classification 标准进行临床判断？
```

#### 3. **综合推理**
```
请结合 stress-induced-cardiac-sudden-death-mechanism 分析应激性心肌病的猝死风险。
```

## 关于作者

**小绿绿 (xllgreen)** — 九江学院临床医学院学生 · 科技极客

- GitHub: https://xllgreen.github.io

## 技术支持

PDF2App项目：https://pdf2app.cn

Microsoft Visual Studio Code：https://code.visualstudio.com/

Claude Code for VS Code：https://claude.com/
© 2026 Anthropic PBC

DeepSeek API：https://platform.deepseek.com/
© 2026 杭州深度求索人工智能基础技术研究有限公司

Xiaomi Mimo API：https://platform.xiaomimimo.com/
Copyright © 2010 - 2026 Xiaomi. All Rights Reserved

## 许可证

本项目内容基于人民卫生出版社《病理生理学》第10版整理，仅供学习参考。

## Star History

<a href="https://www.star-history.com/#repos=&type=date&legend=top-left">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="" />
   <source media="(prefers-color-scheme: light)" srcset="" />
   <img alt="Star History Chart" src="" />
 </picture>
</a>
