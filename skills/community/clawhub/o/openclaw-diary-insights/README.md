# Note Extractor Skill

从日记中提取洞察，生成可交互的本地可视化页面（思维卡片 + 知识图谱 + 情绪日历 + 成长雷达图）。

## 前置条件

- 已完成 onboarding（运行过 `setup my journal`）
- 已有日记数据（通过 diary skill 记录过内容）

## 使用方式

在对话中说以下任意一句：

```
分析日记
生成洞察
我的思考花园
insights
```

Skill 会自动：
1. 读取 `~/write_me/00inbox/journal/` 下的日记文件
2. 提取思维卡片、情绪标签、成长维度、知识图谱
3. 生成 HTML 可视化页面到 `~/write_me/02notes/insights/`
4. 在浏览器中打开

## 输出文件

```
~/write_me/02notes/insights/
├── insights-2026-03.html    # 可视化页面（浏览器直接打开）
└── data-2026-03.json        # 结构化数据（供其他工具使用）
```

## 可视化包含四个视图

| 视图 | 说明 |
|------|------|
| 思维卡片 | 从日记中提炼的核心洞察，按分类筛选 |
| 知识图谱 | 2D 卡片式关联图，展示主题、概念、人物之间的连接 |
| 情绪日历 | 时间线式日记浏览，按月分组，点击展开当天记录 |
| 成长雷达 | 六维度（职业/学习/投资/社交/健康/创造）月度对比 |

## 文件结构

```
note-extractor/
├── SKILL.md                 # Skill 定义（核心逻辑）
├── README.md                # 本文件
└── demo/
    ├── insights.html        # HTML 可视化模板
    └── mock-diary-data.json # 模拟数据（开发测试用）
```

## 开发说明

- `demo/insights.html` 是可视化模板，内含模拟数据，可直接打开预览效果
- SKILL.md 运行时会读取真实日记数据，替换模板中的数据部分，生成最终 HTML
- 依赖 Chart.js（CDN），需联网加载雷达图；其余功能纯 Canvas/CSS，离线可用
