---
name: npl
slug: npl
displayName: 不良资产处置全栈·估值定价+尽调+投标上限反推
summary: 不良资产（NPL）从形成机制到处置退出：估值定价、30 种处置技术、尽调流程、投标上限反推与回收率建模。
description: >-
  不良资产这行的钱，赚在**买入价**上——买贵了，后面怎么处置都白搭。

  这是一套不良资产全栈知识库，覆盖：形成机制与分类、估值定价方法（交易案例比较/专家判断/现金流折现）、30 种处置技术与适用场景、尽调流程与红线、投标上限反推、回收率建模、区域差异定价，以及对公与个贷不良的不同打法。包里含可直接跑的投标速算脚本，改参数就用。

  几条实战口径：**先算退出再算出价**（处置路径没想清楚就出价＝闭眼投标）；**分类决定策略**（有抵押/纯信用/个贷批量定价逻辑完全不同，折扣区间只是起点）；**尽调只查三件事**（权利是否干净、抵押物是否真实可控、债务人有无可执行财产）。

  输入：资产包基本信息、债务人与抵押物情况、区域
  输出：估值区间与建议出价上限、处置路径建议、尽调重点清单

  触发词：不良资产、NPL、资产包、尽调、估值定价、处置、法拍、债权转让、AMC、回收率、投标、抵押物、个贷不良、对公不良。
version: 3.0.0
author: 九品锦锂e
license: MIT
category: professional
metadata:
  version: "3.0.0"
---
# 不良资产处置全栈知识库

> 不良资产（NPL）从形成机制到处置退出：估值定价、30 种处置技术、尽调、投标上限反推，按"赚在买入价"的口径写。

## 什么时候用

- 准备参与资产包投标，需要出价上限与估值区间
- 要判断一个资产包能不能接、怎么处置、回收率大概多少
- 要做尽调清单、查权利瑕疵与抵押物
- 想系统了解对公 / 个贷不良的不同打法

## 能给你什么

- **估值定价体系**：交易案例比较法、专家判断法、现金流折现，含区域与司法环境修正
- **投标定价策略**：从处置路径反推出价上限，避免"闭眼投标"
- **30 种处置技术**：适用场景、周期、回收差异，以及"分类 × 处置"映射矩阵
- **尽调流程与红线**：权利是否干净、抵押物是否真实可控、债务人有无可执行财产
- **周期与案例**：四轮不良周期历史与案例复盘
- **可直接跑的脚本**：投标速算（`scripts/bid-quick-calc.py`）

## 知识模块

| 模块 | 文件 | 内容 |
|---|---|---|
| 基础与分类 | `references/fundamentals-classification.md`、`references/formation-mechanism.md` | 概念、形成机制、分类 |
| 估值体系 | `references/valuation-methods.md`、`references/asset-valuation.md`、`references/valuation-case-studies.md`、`references/valuation-params-sensitivity.md` | 估值方法、案例、参数敏感性 |
| 投标定价 | `references/bidding-valuation-strategy.md`、`references/valuation-negotiation.md` | 出价上限反推、价格谈判 |
| 处置策略 | `references/disposal-strategies.md`、`references/disposal-techniques-30.md`、`references/classification-disposal-mapping.md` | 处置策略、30 种技术、分类映射 |
| 尽调 | `references/due-diligence.md`、`references/due-diligence-workflow.md` | 尽调要点与流程 |
| 法律与交易 | `references/legal-framework-l1.md`、`references/transaction-workflow.md` | 法律框架、交易流程 |
| 市场与参与者 | `references/trading-market-pricing.md`、`references/market-participants.md`、`references/npl-ecosystem-2026-map.md` | 交易市场、AMC/银行/服务商格局 |
| 回收率建模 | `references/recovery-modeling.md` | 回收率建模方法 |
| 周期与案例 | `references/four-cycle-case-studies.md`、`references/npl-four-cycles-history.md` | 四轮周期与案例 |
| 个贷不良科技 | `references/ai-retail-npl-tech.md`、`references/tech-reshaping-market.md` | 个贷批量处置与科技手段 |
| 全生命周期 | `references/npl-lifecycle-framework.md` | 从收购到退出的全流程 |

## 三条硬规则（最值钱的部分）

1. **先算退出再算出价**：处置路径没想清楚就出价，等于闭眼投标；出价上限必须由退出路径和回收率倒推。
2. **分类决定策略**：有抵押 / 纯信用 / 个贷批量的定价逻辑完全不同，折扣区间只是起点，要按区域与司法环境修正。
3. **尽调只查三件事**：权利是否干净、抵押物是否真实可控、债务人有没有可执行财产；这三件没查清，其他都是细节。

## 怎么用

- **输入**：资产包基本信息、债务人与抵押物情况、所在区域
- **输出**：估值区间与建议出价上限、处置路径建议、尽调重点清单、回收率测算

## 免责

本知识库为方法与实践经验整理，不构成投资建议；具体估值与法律判断请以正式专业意见为准。

---

## 🙋 关于作者

**九品锦锂e** ｜ 把踩过的坑整理成"拿来就能用"的知识包，不写教科书。这套是我在做真实项目时一点点攒下来的。

**微信：ly5419495**（加时备注「SkillHub」，我优先通过）
**公众号：初五Agent**（微信搜一搜，项目复盘和方法都写在那儿，不加微信也能读）

我另外做的几个能直接跑的工具，都放在这个货架页（复制到浏览器打开）：
https://skillpay.alipay.com/public/jiupinjinlie

用的时候卡住了、或者有别的场景想让我整理成知识包，按上面任意方式找我就行。

![九品锦锂e 微信二维码](https://jinli-vault-1372591613.cos.ap-guangzhou.myqcloud.com/skillhub/hook-wechat-jiupinjinlie.png)
