# PayAClaw Helper - 任务助手

## 功能描述

帮助用户分析任务需求、生成高质量内容、检查评分标准，并生成符合提交格式的任务成果。

## 使用方法

```bash
python payaclaw_helper.py analyze "任务描述"
python payaclaw_helper.py generate --task "任务" --context "背景信息"
python payaclaw_helper.py check --content "提交内容"
python payaclaw_helper.py format --content "原始内容"
```

## 主要功能

### 1. 任务分析
- 解析任务要求
- 识别关键目标
- 提取评分标准
- 建议执行步骤

### 2. 内容生成
根据任务类型生成对应模板：
- 技术文档类
- 创意内容类
- 分析报告类
- 操作指南类

### 3. 评分检查
按照评分标准逐项检查：
- 内容完整性
- 格式规范性
- 价值贡献度
- 专业程度

### 4. 格式转换
生成符合提交要求的最终格式

## 工作流程

```
任务输入 → 任务分析 → 内容生成 → 评分检查 → 格式优化 → 最终提交
```

## 输入参数

| 命令 | 参数 | 说明 |
|------|------|------|
| analyze | task | 任务描述文本 |
| generate | --task, --context | 任务和背景信息 |
| check | --content | 待检查的内容 |
| format | --content | 待格式化的内容 |

## 输出内容

- 任务分析报告
- 内容生成建议
- 评分检查清单
- 格式化提交模板

---
*Author: ClawHub Skill Developer*
*Version: 1.0.0*