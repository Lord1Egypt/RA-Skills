# 鬼谷子七十二术 · 现代博弈认知工具

> 将古老博弈智慧编译为可执行的现代认知工具。不做"知识库"，做"认知维度的健身房"。
> 
> **商业 + 金融双轨体系**。9个Skill覆盖商业博弈和金融博弈全场景。

---

## 快速开始

### 你在什么处境？→ 选对应 Skill

```
商业场景:
─────────────────────────────────────────────────────────
"我要说服/影响一个关键人物"              → /influence-architect
"我要去谈判 / 正在谈判中"                → /negotiation-tactics
"我处于劣势，需要找到翻盘的路径"          → /adversity-turnaround
"我需要分析局势/对手/市场，信息不够"      → /intelligence-analysis
"我跟大家都在内卷，想找到新的赛道"        → /competition-reframe
"我需要建立团队/瓦解对手联盟/找人"        → /alliance-talent
"我在做长期规划，如何布局才能赢到最后"    → /long-game-strategist

金融场景:
─────────────────────────────────────────────────────────
"我要判断市场情绪 / 控制自己的投资偏误"   → /investment-psychology
"我在做交易/融资/并购/对赌谈判"           → /financial-counterparty
"我需要做投资尽调 / 分析管理层/市场信号" → /intelligence-analysis
"我的基金在亏损/回撤 / 投资心理崩溃"     → /adversity-turnaround
```

### 组合使用（飞轮联动）

```
标准链路（商业）:
  S2情报解析 → S4维度重构 → S3影响力/S7谈判 → S5人才联盟
      ↑                                           │
      └────────── S6长期博弈 ←────────────────────┘
                      │
                S1逆境翻盘（任何时候陷入劣势时启动）

标准链路（金融）:
  S2情报解析 → S8认知博弈 → S9交易对手博弈
      ↑                           │
      └── S6长期（资产配置）←──────┘
              │
        S1逆境（回撤/心理崩溃时启动）
```

---

## Skill 全景

### 商业核心（7个Skill）

| # | Skill | 命令 | 优先级 | 核心JTBD |
|:--|:--|:--|:--:|:--|
| S3 | 影响力架构师 | `/influence-architect` | P0 | 让关键人物无法拒绝 |
| S7 | 谈判即兴战术包 | `/negotiation-tactics` | P0 | 谈判桌实时应对 |
| S1 | 逆境翻盘引擎 | `/adversity-turnaround` | P1 | 非对称翻盘 |
| S2 | 深度情报解析器 | `/intelligence-analysis` | P1 | 从有限信息提取最大信号 |
| S4 | 竞争维度重构器 | `/competition-reframe` | P2 | 红海突围 |
| S5 | 联盟与人才操盘手 | `/alliance-talent` | P2 | 人际网络构建 |
| S6 | 长期博弈战略家 | `/long-game-strategist` | P2 | 跨周期布局 |

### 金融专属（2个Skill）

| # | Skill | 命令 | 优先级 | 核心JTBD |
|:--|:--|:--|:--:|:--|
| S8 | 投资认知博弈 | `/investment-psychology` | P0 | 对抗认知偏误，识别市场叙事 |
| S9 | 金融交易对手博弈 | `/financial-counterparty` | P0 | 融资/并购/对赌/条款博弈 |

---

## 金融适配说明

所有商业核心Skill（S1-S7）均已适配金融场景。详见: `references/financial-adaptation.md`

```
金融三层博弈 → Skill映射

  Layer 1: 人与市场（择时/预测）→ ⚠️ 硬边界，不适用鬼谷子
  Layer 2: 人与信息（研究/分析）→ ✅ S2/S8/S6
  Layer 3: 人与人（募资/谈判）  → ✅ S3/S7/S9/S5
```

---

## 设计铁律

1. **场景锚定** — 每个skill绑定一个高频具体场景
2. **输出可执行** — 输出必须是"下一步做什么"
3. **认知升维** — 让用户看到之前没看到的维度
4. **反常识性** — 包含逆直觉但正确的洞察
5. **伦理边界** — 内置伦理检查，拒绝恶意使用

---

## 三条元策略

> **❶ 永远比对手多知道一点**（信息不对称是你的核心优势）
>
> **❷ 永远比对手多准备一套方案**（可选性越多，越能等得起）
>
> **❸ 永远让对手不知道你在想什么**（信息遮蔽保护你的行动空间）

---

## 项目结构

```
CLAUDE.md                          # 项目上下文
README.md                          # 本文件
references/
  guiguzi-72-strategies.md         # 72术完整原文+现代转译
  financial-adaptation.md          # 6大商业Skill的金融场景适配指南
.claude/skills/
  --- 商业核心(7) ---
  influence-architect.md           # S3 影响力架构师 (P0)
  negotiation-tactics.md           # S7 谈判即兴战术包 (P0)
  adversity-turnaround.md          # S1 逆境翻盘引擎 (P1)
  intelligence-analysis.md         # S2 深度情报解析器 (P1)
  competition-reframe.md           # S4 竞争维度重构器 (P2)
  alliance-talent.md               # S5 联盟与人才操盘手 (P2)
  long-game-strategist.md          # S6 长期博弈战略家 (P2)
  --- 金融专属(2) ---
  investment-psychology.md         # S8 投资认知博弈 (P0·金融)
  financial-counterparty.md        # S9 金融交易对手博弈 (P0·金融)
```
