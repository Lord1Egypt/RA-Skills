---
name: meeting-minutes-craft
version: 1.0.0
description: 将杂乱会议记录转化为结构化、可搜索、带7种模板的格式化HTML纪要
author: wuwenbin-beijing-st
homepage: https://github.com/wwbwin/clawhub-skills
tags: [visualization, html, tool]
---

# 【简介】

本 Skill 的设计初衷是解决团队会议记录格式混乱、信息难以归档追踪的痛点。同事们开完会后，记录往往散落在聊天记录、邮件或 Word 中，要点淹没在大段文字里，决策、行动项、责任人分离，查找历史纪要困难重重。

该 Skill 通过场景诊断 + 智能格式化 + 一键生成 HTML 的方式，将杂乱的会议记录转化为结构化、可搜索、可筛选的归档页面。支持 7 种会议类型模板（标准、决策导向、行动追踪、复盘、站会、研讨、董事会），每种都有自己的视觉风格和内容布局，让团队从"记了找不到"变成"边查边用"。

---

# Meeting Minutes Craft — 会议纪要格式化 Skill

> 将杂乱的会议记录转化为结构清晰、易于归档和分享的格式化会议纪要 HTML。
>
> 作者：wuwenbin-beijing-st

## 使用说明

运行此 Skill 后，按以下步骤操作：

1. **粘贴原始记录**：将会议中记录的原始文本粘贴给 AI
2. **选择会议类型**：从映射表中选择对应的会议类型
3. **选择配色方案**：从配色方案库中选择喜欢的颜色主题
4. **生成纪要**：AI 自动提取结构化内容，输出单文件 HTML

### 输入格式建议

- 直接粘贴会议记录文本（支持中英文混合）
- 说明会议名称、日期、参会人
- 告知期望的纪要风格（如：重点突出决策、或重点突出行动项）

## 场景-模式映射表

| 会议类型 | 推荐模式 | 特点 |
|---------|---------|------|
| 常规项目周会 | standard（标准） | 议题 → 讨论 → 决策 → 行动项 |
| 方案评审/决策会 | decision-focus（决策导向） | 选项分析 → 决策依据 → 最终结论 |
| 进度同步会 | action-tracker（行动追踪） | 上次行动 → 进度 → 新行动项 |
| 项目回顾/复盘 | retro（复盘回顾） | 做得好 → 待改进 → 改进方案 |
| 每日站会 | standup（每日站会） | 昨日 → 今日 → 阻塞 |
| 需求/设计研讨 | workshop（研讨工作坊） | 议题 → 讨论要点 → 结论 → 待办 |
| 董事会/高管会 | board（董事会） | 摘要 → 关键决策 → 财务 → 风险 |

## 配色方案库

### 4 套主题配色

#### 1. 商务蓝（推荐日常使用）
```
--primary: #1a73e8
--primary-light: #e8f0fe
--accent: #0d47a1
--bg: #ffffff
--text: #202124
--border: #dadce0
--success: #34a853
--warning: #fbbc04
--danger: #ea4335
```

#### 2. 科技绿
```
--primary: #0d9488
--primary-light: #ccfbf1
--accent: #0f766e
--bg: #fafdfb
--text: #134e4a
--border: #99f6e4
--success: #10b981
--warning: #f59e0b
--danger: #ef4444
```

#### 3. 温暖橙
```
--primary: #ea580c
--primary-light: #fff7ed
--accent: #c2410c
--bg: #fffcf5
--text: #431407
--border: #fed7aa
--success: #16a34a
--warning: #d97706
--danger: #dc2626
```

#### 4. 严肃灰（正式报告/对外文档）
```
--primary: #374151
--primary-light: #f3f4f6
--accent: #111827
--bg: #ffffff
--text: #1f2937
--border: #d1d5db
--success: #059669
--warning: #d97706
--danger: #dc2626
```

## 交互增强包列表

### 基础交互
- 折叠/展开讨论详情
- 快速跳转至各个议题
- 复制决策摘要
- 高亮搜索关键词

### 高级交互
- 行动项筛选（按状态：未开始/进行中/已完成）
- 责任人过滤（按人员查看分配项）
- 截止日期排序（按时间线排列行动项）
- 一键导出 Markdown/纯文本
- 打印优化（隐藏交互元素）

## 限制说明

- **单文件 HTML**：所有输出均为单一 HTML 文件，CSS 和 JS 全部内联
- **零外部依赖**：不加载任何 CDN 资源、字体、图标库
- **系统字体栈**：font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Noto Sans SC", sans-serif
- **浏览器兼容**：Chrome/Firefox/Safari/Edge 最新两版
- **响应式布局**：桌面和移动端均可正常浏览

## 命令定义

### `/meeting-minutes`
主入口命令。粘贴会议记录后，AI 引导完成：
1. 选择会议类型
2. 选择配色方案
3. 生成格式化 HTML 纪要

### `/meeting-template`
生成空白纪要模板供会前使用。输出包含结构化占位符的 HTML 模板，参会人可在会议中直接填写。

## 文件结构

```
skills/meeting-minutes-craft/
├── SKILL.md
├── patterns/
│   ├── standard.json        # 标准会议纪要
│   ├── decision-focus.json  # 决策导向型
│   ├── action-tracker.json  # 行动项追踪型
│   ├── retro.json           # 复盘回顾型
│   ├── standup.json         # 每日站会型
│   ├── workshop.json        # 研讨工作坊型
│   └── board.json           # 董事会/高管会议型
└── templates/
    ├── base.html
    ├── standard.html
    ├── decision-focus.html
    ├── action-tracker.html
    ├── retro.html
    ├── standup.html
    ├── workshop.html
    └── board.html
```
