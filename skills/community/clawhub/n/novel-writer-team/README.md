# 写小说 Skill — novel-writer-team

## 简介

多Agent协作的小说创作系统，8个专业角色覆盖从灵感到成品的完整流程。

## 触发方式

在 Claude Code 中说：
- "写小说" / "帮我写小说"
- "小说创作" / "创作小说"
- "写个故事" / "帮我写个故事"
- "我想写一部小说"
- "我有个想法想写下来"

## 工作模式

- **自动模式**（默认）：提供灵感后自动跑完全流程
- **分步模式**：说"一步步来"，每阶段暂停确认

## 支持平台

- 起点中文网
- 番茄小说
- 晋江文学城
- 知乎盐选
- 豆瓣阅读

## 目录结构

```
novel-writer-team/
├── SKILL.md                  # 主文件（触发条件+工作流）
├── README.md                 # 本文件
└── references/
    ├── agents.md             # 8个Agent详细定义
    ├── platforms.md          # 5大平台适配规则
    ├── workflows.md          # 工作流程说明
    ├── templates.md          # 输出模板
    └── example-project.md    # 示例项目
```
