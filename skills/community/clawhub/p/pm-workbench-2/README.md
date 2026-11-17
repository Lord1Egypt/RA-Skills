# PM Workbench — AI 产品经理工作台

> 一个沉淀数据产品、中后台产品、在线教育增长三大领域实战方法的 WorkBuddy 技能。提供文档产出、决策教练、全流程引导、面试辅导、增长方案设计五位一体的 PM 助手。

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## 这是什么？

这不是一个 demo 或原型，而是一个**可以直接安装到 WorkBuddy 的技能包**。安装后，WorkBuddy 会变成一个资深产品经理助手，能够：

- 根据你的输入生成结构化 PRD、竞品分析、实验方案
- 作为决策教练，帮你分析方案优劣、避免产品决策陷阱
- 引导你完成从需求发现到项目复盘的全流程
- 模拟 PM 面试，帮你打磨产品思维和面试技巧
- 设计用户增长方案，从诊断到执行全覆盖

## 核心能力

| 能力 | 描述 | 示例 |
|-----|------|------|
| PRD 生成 | 结构化需求文档，包含用户故事、验收标准、埋点方案 | "帮我写一个多模态输入功能的 PRD" |
| 竞品分析 | 系统化竞品对比，含功能矩阵和策略建议 | "分析智言AI 的产品策略" |
| 实验设计 | AB 测试方案设计，含样本量计算和评估标准 | "设计推荐引擎 V2 的 AB 测试" |
| 路线规划 | 基于优先级模型的版本规划 | "帮我规划 Q3 的产品路线图" |
| 项目复盘 | 结构化复盘模板，数据驱动的问题诊断 | "帮我复盘智能搜索优化的项目" |
| 数据决策 | 量化分析和决策框架 | "优化注册流程还是优化搜索体验？" |
| 🆕 面试辅导 | PM 面试全题型覆盖，Mock 练习 + 点评指导 | "模拟一次腾讯产品经理面试" |
| 🆕 增长方案 | 从诊断到执行的完整增长策略 | "我的教育产品增长遇到瓶颈，帮我分析" |

## 三大领域专长

- **数据产品**：指标体系设计（OSM 模型）、埋点方案、数据可视化、数据质量治理
- **中后台产品**：权限系统（RBAC/ABAC）、工作流引擎、配置化平台、效率工具
- **在线教育增长**：拉新漏斗优化、转化率提升、裂变设计、留存策略

## 快速安装

### 方式一：从 GitHub 安装

```bash
# 克隆到 WorkBuddy 技能目录
git clone https://github.com/FayeNick/pm-workbench.git ~/.workbuddy/skills/pm-workbench
```

### 方式二：手动安装

1. 下载本仓库代码
2. 将整个 `pm-workbench` 文件夹放入 `~/.workbuddy/skills/` 目录
3. 重启 WorkBuddy 或刷新技能列表

### 方式三：WorkBuddy 技能市场安装

在 WorkBuddy 对话框输入：`安装 pm-workbench 技能`

## 使用示例

安装后，在 WorkBuddy 对话中直接使用：

```
"帮我写一份智能搜索功能优化的 PRD"
"分析一下我们的竞品最近有什么动作"
"设计一个验证推荐算法效果的 AB 测试"
"帮我排一下 Q3 需求池的优先级"
"做一下上个迭代的项目复盘"
"模拟一次产品经理面试，出产品设计题"
"我的产品新增用户增长停滞了，帮我诊断"
"帮我设计一个教育产品的裂变增长活动"
```

## 技能架构

```
pm-workbench/
├── SKILL.md                          # 核心技能文件
├── references/
│   ├── templates/                    # 六大产出模板
│   │   ├── prd-template.md
│   │   ├── competitive-analysis.md
│   │   ├── experiment-template.md
│   │   ├── retrospective-template.md
│   │   ├── interview-coaching.md     # 🆕 面试辅导
│   │   └── growth-strategy.md        # 🆕 增长方案
│   ├── frameworks/                   # 决策框架
│   │   ├── prioritization.md
│   │   └── decision-framework.md
│   └── domain-knowledge/            # 领域知识
│       ├── data-product.md
│       ├── backoffice-product.md
│       └── growth-edtech.md
└── README.md
```

## 贡献

欢迎 PR！如果你有产品经理领域的经验想贡献，可以：

1. 新增领域知识（添加到 `references/domain-knowledge/`）
2. 新增模板或框架（添加到对应目录）
3. 改进现有内容

## License

MIT License — 详见 [LICENSE](LICENSE) 文件。
