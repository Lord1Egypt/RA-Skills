---
name: perspective-router
description: |
  Nova 视角调度引擎 — 根据任务描述自动匹配最合适的专家视角能力。
  当 Nova 收到复杂、多领域、需要专业深度分析的任务时，自动调用此路由。
  
  工作原理：
  1. 分析任务文本中的关键词和语义
  2. 在视角库（12位专家心智模型）中打分排序
  3. 返回最匹配的 1-3 个视角，附调用建议
  4. Nova 读取对应 SKILL.md，以该专家身份深度分析
  5. 整合专家视角进主回复，保留 Nova 最终判断权
  
  适用任务类型：
  - 投资/理财决策（含 Naval/Munger）
  - 战略/工程/颠覆式创新（含 Elon Musk）
  - 商业分析/风险评估（含 Munger）
  - 创业/产品/写作（含 Paul Graham）
  - 产品设计/品牌/体验（含 Steve Jobs）
  - 谈判/影响力/直接说服（含 Trump）
  - 内容传播/流量/注意力经济（含 MrBeast）
  - 反脆弱/风险管理/黑天鹅（含 Taleb）
  - 深度学习/AI/神经网络（含 Karpathy）
  
  触发词：「用X视角分析」「涉及投资决策」「这个战略怎么样」「商业分析」等
---

# Perspective Router — Nova 视角调度引擎

> **何时使用此 Skill：** 当任务涉及专业领域分析、需要多视角审视、或 Nova 不确定该调用哪个专家视角时，主动运行此 Skill。

## 工作流程

```
用户任务描述
     ↓
Perspective Router（关键词打分）
     ↓
Top-3 匹配专家 + 匹配度分数
     ↓
Nova 读取对应 SKILL.md
     ↓
以该专家身份深度分析
     ↓
整合进主回复
```

## 内置视角库（12位专家）

| # | 专家 | 核心能力 | 触发关键词 |
|---|------|---------|-----------|
| 1 | 📈 Naval Ravikant | 财富投资·幸福算法·复利 | 投资/理财/财富/FIRE |
| 2 | 🚀 Elon Musk | 第一性原理·工程制造·颠覆 | 战略/火箭/AI/技术突破 |
| 3 | 📊 Charlie Munger | 多元思维·逆向分析·误判心理 | 商业分析/护城河/风险 |
| 4 | 💡 Paul Graham | 创业智慧·YC经验·写作思维 | 创业/startup/产品/idea |
| 5 | 🍎 Steve Jobs | 产品设计·完美主义·品牌 | 产品设计/UX/品牌/简约 |
| 6 | ⚡ Zhang Yiming | 推荐算法·字节产品·全球化 | 字节/抖音/tiktok/算法 |
| 7 | 🔥 Donald Trump | 谈判策略·直接感·交易直觉 | 谈判/Deal/说服/影响力 |
| 8 | 🎬 MrBeast | 病毒传播·注意力工程 | 内容/viral/YouTube/传播 |
| 9 | 🩸 Nassim Taleb | 反脆弱·黑天鹅·尾部风险 | 风险/不确定性/极端斯坦 |
| 10 | 🔬 Richard Feynman | 科学怀疑·证伪思维 | 科学/批判性思考/物理 |
| 11 | 🧠 Andrej Karpathy | 深度学习·神经网络直觉 | AI/LLM/ML/深度学习 |
| 12 | 🎯 Satoshi/中本聪 | 博弈论·密码学·去中心化 | 区块链/Bitcoin/共识机制 |

## 使用方式

### 方式一：直接调用（自动路由）

```bash
python3 /workspace/skills/perspective-router/router.py "这个投资决策应该怎么分析？"
```

输出示例：

```
【Perspective Router · 视角自动调度结果】
任务：「这个投资决策应该怎么分析？」

匹配到 2 个专家视角：

【1】📈 Naval Ravikant — 财富投资 · 幸福算法 · 长期复利
   匹配度：3.0分 | Skill：naval-perspective ✅

【2】📊 Charlie Munger — 多元思维模型 · 逆向分析 · 误判心理学
   匹配度：1.5分 | Skill：munger-perspective ✅

【主要视角】📈 Naval Ravikant
建议优先调用 naval-perspective，以该专家身份分析后，整合进 Nova 主回复。
```

### 方式二：读取特定专家视角

直接读对应 SKILL.md 文件：

```python
# Naval
open("/workspace/skills/naval-perspective/SKILL.md").read()

# Elon Musk
open("/workspace/skills/elon-musk-perspective/SKILL.md").read()

# Charlie Munger
open("/workspace/skills/munger-perspective/SKILL.md").read()
```

## 集成规则

1. **匹配度 > 2.0**：强烈建议调用该视角
2. **匹配度 1.0-2.0**：建议作为次要视角参考
3. **匹配度 < 1.0**：无需调用，Nova 自主分析即可
4. **多个视角**：优先调用匹配度最高的，复杂任务最多同时调用 2 个
5. **Nova 最终判断**：Perspective 是工具，Nova 最终判断权不变

## 调用示例

### 示例 1：投资决策

```
输入：「我有50万，应该怎么配置资产？」
→ 匹配：Naval（财富配置）+ Munger（风险分散）
→ Nova 调用 naval-perspective + munger-perspective
→ 输出：综合两视角的资产配置建议
```

### 示例 2：产品策略

```
输入：「做一个新产品，怎么判断它是否有用户需求？」
→ 匹配：Paul Graham（创业/产品）+ Naval（专有知识）
→ Nova 调用 naval-perspective
→ 输出：结合 PG 的用户测试思维 + Naval 的专有能力框架
```

### 示例 3：战略风险

```
输入：「是否应该进入一个新的市场？」
→ 匹配：Elon Musk（颠覆式创新）+ Munger（逆向思考）
→ Nova 调用 elon-musk-perspective + munger-perspective
→ 输出：正反两面结构化战略分析
```

## 扩展视角库

在 `router.py` 的 `PERSPECTIVES` 字典中增加：

```python
"satoshi": {
    "name": "Satoshi Nakamoto",
    "skill": "satoshi-perspective",  # 需创建对应 SKILL.md
    "emoji": "₿",
    "keywords": [
        "区块链", "Bitcoin", "去中心化", "共识机制",
        "密码学", "token", "defi", "web3"
    ],
    "weight": 1.0,
    "description": "去中心化 · 博弈论 · 密码学"
}
```

## 文件结构

```
perspective-router/
├── SKILL.md          ← 本文件（视角路由 Skill）
├── router.py         ← 路由引擎（Python，纯本地计算）
└── README.md          ← 使用说明
```

## 限制说明

- router.py 是纯关键词打分，无 LLM 调用，成本为零
- 匹配度阈值需要根据实际使用调整（建议基准：2.0）
- 复杂语义任务（无明确关键词）可能匹配不准确，需 Nova 人工判断
- 视角 Expertize 有文化边界（Naval 有硅谷偏见，Trump 有特定语境）

---

*Perspective Router v1.0 | Nova Group B | 2026-04-15*
