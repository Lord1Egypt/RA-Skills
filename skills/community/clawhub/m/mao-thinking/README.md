# 毛泽东思想实践工具包
# Mao Zedong Thought Practice Toolkit

This package provides Python tools based on Mao Zedong's philosophical and strategic thoughts for problem-solving and decision-making.

## 安装

### 方式一：pip 安装（推荐）
```bash
pip install mao-thinking
```

### 方式二：源码安装
```bash
git clone https://github.com/your-repo/mao-thinking.git
cd mao-thinking
pip install -e .
```

### 方式三：直接使用
```bash
# 直接运行脚本
python mao_thinking.py <command>
```

## 依赖

- Python 3.7+
- 无额外依赖（仅使用标准库）

## 使用方法

### 命令行模式

#### 1. 矛盾分析器
```bash
python -m mao_thinking.analyzer "毕业生就业难" "缺经验" "竞争大" "期望高"
```
输出：
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

#### 2. 形势分析器
```bash
python -m mao_thinking.situator "面临创业挑战" 5 9
```
输出：
```
🗺️ 形势分析：面临创业挑战
==================================================
⚔️ 双方实力: 我方 5 vs 对方 9
📊 实力比: 0.56

📈 战略判断: 战略相持
🎯 战术建议: 保存实力，等待时机
🧘 指导思想: 敌进我退，敌退我追
```

#### 3. 决策助手（交互模式）
```bash
python -m mao_thinking.decider -i "选择哪份工作"
```
输出：
```
🤝 交互式决策：选择哪份工作
==================================================

请输入方案（输入空行结束）：

方案名称: 大厂
优点（用逗号分隔）: 工资高, 平台大
缺点（用逗号分隔）: 加班多
✓ 已添加方案: 大厂

方案名称: 创业公司
优点（用逗号分隔）: 成长快, 灵活
缺点（用逗号分隔）: 风险高
✓ 已添加方案: 创业公司

方案名称: 

🏆 推荐方案：大厂 (得分: 75)
```

#### 4. 核心原则汇总
```bash
python -m mao_thinking.summary
```

#### 5. 场景推荐
```bash
python -m mao_thinking.main --scenario "团队意见不统一"
```

### Python 模块调用

```python
from mao_thinking import (
    analyze_contradiction,
    situation_analysis,
    mass_line_decide,
    show_summary
)

# 矛盾分析
result = analyze_contradiction(
    problem="找不到工作",
    factors=["缺经验", "竞争大", "期望高"]
)

# 形势分析
result = situation_analysis(
    situation="面临竞争",
    our_strength=6,
    enemy_strength=8
)

# 决策助手
result = mass_line_decide(
    decision="选择哪份工作",
    options=[
        {"name": "大厂", "pros": ["工资高"], "cons": ["加班多"]},
        {"name": "创业", "pros": ["成长快"], "cons": ["风险高"]}
    ]
)

# 原则汇总
principles = show_summary()
```

## 核心方法论

| 方法论 | 功能 | 适用场景 |
|--------|------|----------|
| 矛盾论 | 分析主要矛盾 | 问题分析、优先级排序 |
| 实践论 | 验证决策 | 决策前测试、试点 |
| 群众路线 | 民主决策 | 团队意见统一 |
| 独立自主 | 自力更生 | 资源争取 |
| 统一战线 | 扩大联盟 | 合作谈判 |
| 实事求是 | 具体分析 | 任何场景 |
| 战略战术 | 形势评估 | 竞争分析 |

## 文件结构

```
mao_thinking/
├── __init__.py           # 包入口
├── main.py               # 主程序入口
├── analyzer.py           # 矛盾分析器
├── situator.py           # 形势分析器
├── decider.py            # 决策助手
├── summary.py            # 原则汇总
└── README.md             # 本文件
```

## 版本历史

- v1.0.0 (2024) - 初始版本

## 许可证

MIT License

## 作者

Mao Thought AI Team