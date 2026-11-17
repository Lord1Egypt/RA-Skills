---
slug: project-evm-check-free
displayName: 项目挣值分析核对（免费版）
version: 1.0.30
summary: 挣值分析表逐项核对，每条结论都带原文行号，不需要付款，也不需要注册。
tags: [项目挣值分析核对,挣值分析表,核算核对,财务,免费]
license: Proprietary
name: project-evm-check-free
display_name: 项目挣值分析核对（免费）
display_name_en: Project EVM Check (Free)
description: 挣值分析表逐项核对（逐行复算、合计勾稽、重复与空缺检测），每条结论引用原文行号。本免费版执行引擎声明的免费检查项。触发词包括 挣值分析核对、EVM、CPI、SPI、项目绩效。
description_zh: 挣值分析表逐项核对（逐行复算、合计勾稽、重复与空缺检测），每条结论引用原文行号。本免费版执行引擎声明的免费检查项。触发词包括 挣值分析核对、EVM、CPI、SPI、项目绩效。
description_en: A free deterministic check for project evm check worksheets. Every finding cites the source line. No payment, no registration, no API key, no network.
category: business-ops
author: WorkBuddy 开放平台开发者
allowed-tools: Read, Bash
---

# 项目挣值分析核对（免费）

> **完全本地运行**：引擎已经打包在本技能里（`engine/` 目录）。
> 核对过程不需要联网、不需要 API Key、**没有调用次数上限**。

## 什么时候用

**谁会在什么时候用**：做项目（工程/IT/研发）的人**每月报进度与成本**时，标准做法是挣值分析 ——
CV = EV − AC、SV = EV − PV、CPI = EV ÷ AC、SPI = EV ÷ PV。
式子极简，但**分母写错（CPI 用 AC、SPI 用 PV）是最常见的错**，而它直接决定"要不要追加预算/延工期"。

**这张表会逐项核对什么**：
· CV = EV − AC；SV = EV − PV
· CPI = EV ÷ AC；SPI = EV ÷ PV（**分子永远是 EV**）
· 合计行逐列复核（**比率不能按行相加**，整体指标要用合计重算）；重复与空缺检测

每条结论都带**原文行号与出处**，可被第三方用同一口径复算；
材料不足时**不给结论**，会明确列出还缺什么。

## 这个免费版查什么

（检查项由引擎的 `CHECKS_*` 导出，跑 `--sample` 会打印实际执行了哪些。）

## 怎么用

```bash
node scripts/run.mjs --sample                 # 先看样例
node scripts/run.mjs --input 你的材料.json     # 跑自己的材料
```

## 常见错法（这张表里真的会有人这么填）

1. 请补上这些再跑；材料不足时本工具不做任何认定，也不套用默认值。
2. CV（成本偏差）与 SV（进度偏差）都要用 **EV 打头**：CV = EV − AC，SV = EV − PV；写反是最常见的错。
3. SV = EV − PV（都按"价值"口径）；用 AC 去减 PV 会把成本差异混进进度差异里。
4. 同一工作包按子项分行是正常的；但若本表按工作包汇总，重复行会让 PV/EV/AC 一起翻倍。
5. 缺这一格这条绩效指标就算不出来；补齐前本工具不会用 0 或默认值替你填。

## 需要完整档时（可选）

本免费版是**完整可用的核心产出**，本版本**不包含**下面这些项：

- CPI / SPI 与「好于/差于 1」的定性结论一致性检测
- PV / EV / AC 为负检测
- 完工预测 EAC（BAC ÷ CPI）与表内值一致性检测
- 完工尚需估算 ETC（EAC − AC）一致性检测
- BAC 小于 EV（已完成价值超过总预算）异常检测

同名工具的**完整档**是另一个独立商品（条款与条件以它自己的商品页为准）；两档的差别**就是上面这些，没有别的**。

## 边界（请务必知道）

本工具**不做**引擎 `CHECKS_OUT_OF_SCOPE` 里列的那些判断；
材料不足时**不给结论**，也不会输出「未发现问题」。
