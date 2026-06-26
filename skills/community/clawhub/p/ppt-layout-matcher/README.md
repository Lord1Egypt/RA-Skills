# PPT Layout Matcher

> 基于 45 页设计版式库的 PPT 智能版式匹配系统

根据输入内容自动分析特征，从 45 页专业设计版式库中匹配最合适的版式，帮你快速创作高质量 PPT。

## 特性

- 🧠 **智能分析**: 自动识别内容类型（数据/流程/对比/图片等）
- 📐 **45 页版式库**: 基于真实设计稿提炼的 10 大类 45 个版式模板
- 🎯 **精准匹配**: 多维度打分算法，Top 3 推荐
- 📦 **即插即用**: 纯 Python，零额外依赖（除 python-pptx）
- 🤖 **WorkBuddy/OpenClaw 集成**: 作为 Agent Skill 直接使用

## 安装

```bash
pip install python-pptx
```

## 快速开始

```python
from ppt_layout_matcher import recommend_layout

# 输入你的内容
results = recommend_layout("核心数据：用户增长65%，营收增长33%，利润率25%")

# 查看 Top 3 推荐版式
for template, score, analysis in results:
    print(f"{template.name} (参考Slide {template.slide_ref}) - 匹配度: {score}")
    print(f"  结构: {template.structure}")
```

输出示例：
```
🥇 数据卡-左文右三卡 (Slide 3) - 匹配度: 0.6
🥈 五大指标卡 (Slide 28) - 匹配度: 0.25
🥉 大图背景+数据叠加 (Slide 18) - 匹配度: 0.2
```

## 版式分类

| 大类 | 页数 | 用途 |
|------|:----:|------|
| A-封面/开篇 | 2 | 报告封面、方案首页 |
| B-过渡/章节页 | 2 | 章节分隔 |
| C-数据展示 | 9 | 指标卡、图表、数据大字报 |
| D-流程/步骤 | 6 | STEP流程、发展历程 |
| E-对比分析 | 5 | A/B对比、多方案、SWOT |
| F-网格/卡片 | 8 | 2×2/3×2/4×N 卡片网格 |
| G-图片展示 | 1 | 时间轴画廊 |
| H-列表/要点 | 4 | 编号列表、图文列表 |
| I-综合信息图 | 1 | One Pager 总览 |
| J-特殊布局 | 7 | 中心辐射、环绕式 |

## Agent Skill 使用

作为 WorkBuddy Skill 使用时：

```
触发词: 做PPT / 创建PPT / 生成PPT / 版式匹配 / 选版式
```

Agent 会自动加载版式库，分析你的内容并匹配合适版式。

## License

MIT © Aha.Gare
