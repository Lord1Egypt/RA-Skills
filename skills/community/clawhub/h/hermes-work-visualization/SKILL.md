---
name: hermes-work-visualization
description: 将Hermes Agent的工作过程可视化 - 包括任务进度、技能使用、代码改动、会话统计等
description_en: Visualize Hermes Agent's work process - including task progress, skill usage, code changes, session statistics, etc.
category: productivity
version: 1.1.4
author: erich1566
email: jxmerich@gmail.com
github: https://github.com/Erich1566
tags: [visualization, dashboard, analytics, monitoring, i18n, bilingual]
languages: [zh, en]
---

# 工作可视化 | Work Visualization

将Hermes Agent的工作过程和结果进行可视化展示，帮助你更好地了解、追踪和分析AI的工作情况。

Visualize Hermes Agent's work process and results to help you better understand, track, and analyze AI performance.

---

## 语言设置 | Language Settings

### 中文说明

本技能支持**自动语言检测**，会根据您的系统语言环境自动选择中文或英文。

**手动设置语言**：
```bash
# 设置为中文
export HERMES_LANG=zh

# 设置为英文
export HERMES_LANG=en
```

### English Instructions

This skill supports **automatic language detection** and will automatically select Chinese or English based on your system language.

**Manually set language**:
```bash
# Set to Chinese
export HERMES_LANG=zh

# Set to English
export HERMES_LANG=en
```

---

## 适用场景 | Use Cases

### 中文
- **任务进度追踪** - 实时查看当前任务完成情况
- **工作统计分析** - 了解技能使用频率、工具调用次数等
- **代码改动追踪** - 可视化代码编辑历史和影响范围
- **会话总结** - 自动生成工作摘要和关键指标
- **性能监控** - 监控AI工作的效率和资源使用

### English
- **Task Progress Tracking** - View current task completion status in real-time
- **Work Statistics Analysis** - Understand skill usage frequency, tool call counts, etc.
- **Code Change Tracking** - Visualize code editing history and impact scope
- **Session Summary** - Automatically generate work summaries and key metrics
- **Performance Monitoring** - Monitor AI work efficiency and resource usage

---

## 使用方法 | Usage

### 生成工作摘要 | Generate Session Summary

#### 中文
当完成一项重要工作后，运行以下命令生成可视化摘要：

```bash
# 生成当前会话的工作摘要
python3 ~/.hermes/skills/work-visualization/scripts/session_summary.py

# 生成特定时间范围的工作报告
python3 ~/.hermes/skills/work-visualization/scripts/generate_report.py --days 7

# 查看技能使用统计
python3 ~/.hermes/skills/work-visualization/scripts/skill_stats.py
```

#### English
After completing important work, run the following command to generate a visual summary:

```bash
# Generate current session summary
python3 ~/.hermes/skills/work-visualization/scripts/session_summary.py

# Generate work report for specific time range
python3 ~/.hermes/skills/work-visualization/scripts/generate_report.py --days 7

# View skill usage statistics
python3 ~/.hermes/skills/work-visualization/scripts/skill_stats.py
```

---

## 可视化类型 | Visualization Types

### 1. 任务进度可视化 | Task Progress Visualization

#### 中文
- 显示当前待办任务列表
- 任务完成状态和进度条
- 任务优先级和时间预估
- 任务依赖关系图

#### English
- Display current todo task list
- Task completion status and progress bar
- Task priority and time estimation
- Task dependency graph

### 2. 技能使用分析 | Skill Usage Analysis

#### 中文
- 最常用技能排行榜
- 技能调用趋势图
- 技能成功率统计
- 技能组合使用模式

#### English
- Most used skills ranking
- Skill call trend chart
- Skill success rate statistics
- Skill combination usage patterns

### 3. 工具调用统计 | Tool Call Statistics

#### 中文
- 工具使用频率排行
- 工具调用时间分布
- 工具失败率和错误类型
- 工具执行耗时分析

#### English
- Tool usage frequency ranking
- Tool call time distribution
- Tool failure rate and error types
- Tool execution time analysis

### 4. 代码改动追踪 | Code Change Tracking

#### 中文
- 文件编辑历史时间线
- 代码改动统计（增删行数）
- 文件修改频率热力图
- 改动影响范围分析

#### English
- File editing history timeline
- Code change statistics (added/deleted lines)
- File modification frequency heatmap
- Change impact scope analysis

### 5. 会话概览 | Session Overview

#### 中文
- 会话关键指标卡片
- 工作时间轴
- 重要决策节点
- 输出成果摘要

#### English
- Session key metrics cards
- Work timeline
- Important decision nodes
- Output summary

---

## 可视化输出示例 | Visualization Output Examples

### 任务进度图 | Task Progress Chart

#### 中文
```
[===================== 75%]  修复登录问题 (3/4 子任务完成)
[=============------ 65%]  优化数据库查询 (13/20 子任务完成)
[======-------------- 30%]  编写API文档 (3/10 子任务完成)
```

#### English
```
[===================== 75%]  Fix login issues (3/4 subtasks completed)
[=============------ 65%]  Optimize database queries (13/20 subtasks completed)
[======-------------- 30%]  Write API documentation (3/10 subtasks completed)
```

---

## 配置选项 | Configuration Options

### 中文
在 `~/.hermes/skills/work-visualization/config.json` 中配置：

### English
Configure in `~/.hermes/skills/work-visualization/config.json`:

```json
{
  "enabled_metrics": [
    "task_progress",
    "skill_usage",
    "tool_calls",
    "code_changes",
    "session_summary"
  ],
  "report_frequency": "daily",
  "export_formats": ["html", "markdown"],
  "charts": {
    "type": "ascii",
    "show_legend": true,
    "max_items": 10
  }
}
```

---

## 语言配置 | Language Configuration

### 自动检测 | Auto Detection (默认/Default)
系统会自动检测以下环境变量：
- `HERMES_LANG` - 优先级最高
- `LANG` - 系统语言环境
- 其他语言相关的环境变量

System automatically detects the following environment variables:
- `HERMES_LANG` - Highest priority
- `LANG` - System language environment
- Other language-related environment variables

### 支持的语言 | Supported Languages

| 语言代码 | 语言 | Language Code | Language |
|---------|------|--------------|----------|
| zh      | 中文  | zh           | Chinese  |
| en      | 英文  | en           | English  |

---

## 扩展建议 | Extension Suggestions

### 中文
- 集成更多图表类型（饼图、热力图）
- 支持自定义可视化模板
- 添加工作流分析
- 实现跨会话工作追踪
- 支持团队协作视图

### English
- Integrate more chart types (pie chart, heatmap)
- Support custom visualization templates
- Add workflow analysis
- Implement cross-session work tracking
- Support team collaboration view

---

## 相关技能 | Related Skills

### 中文
- **jupyter-live-kernel** - 交互式数据分析
- **note-taking** - 工作笔记记录
- **obsidian** - 知识库管理
- **github-code-review** - 代码审查

### English
- **jupyter-live-kernel** - Interactive data analysis
- **note-taking** - Work note taking
- **obsidian** - Knowledge base management
- **github-code-review** - Code review

