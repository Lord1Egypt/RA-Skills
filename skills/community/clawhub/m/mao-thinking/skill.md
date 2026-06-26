# 毛泽东思想实践工具 Skill

> 基于毛泽东选集核心思想的方法论工具包，可直接调用进行问题分析和决策

## 概述

这个 skill 封装了毛泽东思想的核心方法论，提供以下功能：
- **矛盾分析器** - 用矛盾论分析问题主要矛盾
- **形势分析器** - 用战略思想分析竞争形势
- **决策助手** - 用群众路线做民主决策
- **原则汇总** - 快速查阅核心方法论

## 安装

```bash
# 方式一：直接使用（推荐）
cd skills/mao_thinking
pip install -e .

# 方式二：无需安装，直接运行
python mao_thinking/main.py <command>
```

## 使用方法

### 1. 矛盾分析（命令行）

```bash
python mao_thinking/main.py analyze "毕业生就业难" "缺经验" "竞争大" "期望高"
```

**输出示例**：
```
🔍 矛盾分析：毕业生就业难
==================================================
  1. 缺经验 (权重: 9)
  2. 竞争大 (权重: 7)
  3. 期望高 (权重: 5)

💡 主要矛盾：缺经验
📌 行动建议：先解决最重要的事
⚔️ 方法论：抓住主要矛盾，集中力量解决关键问题
```

### 2. 形势分析（命令行）

```bash
python mao_thinking/main.py situation "面临创业挑战" 5 9
```

**输出示例**：
```
🗺️ 形势分析：面临创业挑战
==================================================
⚔️ 双方实力: 我方 5 vs 对方 9
📊 实力比: 0.56

📈 战略判断: 战略相持
🎯 战术建议: 保存实力，等待时机
🧘 指导思想: 敌进我退，敌退我追
```

### 3. 决策助手（交互模式）

```bash
python mao_thinking/main.py decide "选择哪份工作"
```

会进入交互式问答，帮你分析多个方案的优劣。

### 4. 原则汇总

```bash
python mao_thinking/main.py summary
```

### 5. 场景推荐

```bash
python mao_thinking/main.py --scenario "团队意见不统一"
```

---

## Python 模块调用

```python
from mao_thinking import (
    analyze_contradiction,
    situation_analysis,
    mass_line_decide,
    show_summary
)

# 1. 矛盾分析
result = analyze_contradiction(
    problem="找不到工作",
    factors=["缺经验", "竞争大", "期望高"]
)
print(result["主要矛盾"])

# 2. 形势分析
result = situation_analysis(
    situation="面临竞争",
    our_strength=6,
    enemy_strength=8
)
print(result["战略判断"])

# 3. 决策助手
result = mass_line_decide(
    decision="选择哪份工作",
    options=[
        {"name": "大厂", "pros": ["工资高", "平台大"], "cons": ["加班多"]},
        {"name": "创业", "pros": ["成长快", "灵活"], "cons": ["风险高"]}
    ]
)
print(result["推荐方案"])

# 4. 原则汇总
principles = show_summary()
```

---

## 核心方法论说明

| 方法论 | 功能 | 关键方法 | 适用场景 |
|--------|------|----------|----------|
| **矛盾论** | 分析主要矛盾 | 抓住主要矛盾 | 问题分析、优先级排序 |
| **实践论** | 验证决策 | 调查出真知 | 决策前测试、试点验证 |
| **群众路线** | 民主决策 | 从群众中来 | 团队意见统一 |
| **独立自主** | 自力更生 | 主要靠自己也要求 | 资源争取 |
| **统一战线** | 扩大联盟 | 团结多数 | 合作谈判 |
| **实事求是** | 具体分析 | 具体问题具体分析 | 任何场景 |
| **战略战术** | 形势评估 | 战略藐视，战术重视 | 竞争分析 |

---

## 文件结构

```
mao_thinking/
├── __init__.py           # 包入口，导出主要函数
├── main.py               # 主程序入口
├── analyzer.py           # 矛盾分析器模块
├── situator.py           # 形势分析器模块
├── decider.py            # 决策助手模块
├── summary.py            # 原则汇总模块
├── setup.py              # pip 安装配置
├── requirements.txt      # 依赖列表
├── README.md             # 英文使用说明
└── manifest.json         # Skill 元信息
```

---

## 快速口诀

```
矛盾论：抓主要矛盾
实践论：调查出真知
群众路线：从群众中来，到群众中去
独立自主：自力更生
统一战线：团结多数
实事求是：具体问题具体分析
战略战术：战略藐视，战术重视
```

---

## 示例：毕业生找工作分析

```python
from mao_thinking import analyze_contradiction, situation_analysis

# 矛盾分析
result = analyze_contradiction(
    problem="毕业生找不到工作",
    factors=["经济形势不好", "缺乏工作经验", "专业不对口", "竞争激烈", "期望太高"]
)
# 主要矛盾：经济形势不好

# 形势分析
result = situation_analysis(
    situation="就业市场竞争激烈",
    our_strength=5,
    enemy_strength=9
)
# 战略判断：战略相持
# 战术建议：保存实力，等待时机
# 行动建议：农村包围城市，先就业再择业
```

---

## 上传到 ClawHub

1. 打包发布：
```bash
python setup.py sdist bdist_wheel
```

2. 或直接上传整个目录：
```bash
# 整个 mao_thinking 目录即可使用
```

---

*整理自毛泽东选集核心思想，编号：MAO-2024-001*