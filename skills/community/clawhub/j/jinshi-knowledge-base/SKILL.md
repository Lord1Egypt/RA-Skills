---
name: jinshi-knowledge-base
description: 金石知识库管理技能。监控钉钉多维表格中的项目管理事项状态，当事项状态为已完成时自动归档并生成知识文档。
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - python3
        - mcporter
      env:
        - DINGTALK_MCP_URL
    triggers:
      - "归档"
      - "知识库"
      - "生成文档"
      - "项目事项"
---

# 项目知识库管理

## 功能

1. **监控项目管理事项**：定期检查钉钉多维表格中的已完成事项
2. **自动归档**：当事项状态为已完成时，自动生成知识文档
3. **知识文档生成**：
   - 问题类 → 问题分析报告（含AI分析输出）
   - 需求类 → 需求说明文档
   - 任务类 → 任务总结
   - 事件类 → 事件报告

## 配置

### 环境变量

```bash
export DINGTALK_MCP_URL="<钉钉AI表格MCP服务器地址>"
```

### 钉钉表格配置

- **Base**: 金谷信托项目管理系统
- **Base ID**: QOG9lyrgJP3Oo757S9wn4AyZVzN67Mw4
- **Table**: 项目事项管理表
- **Table ID**: atLkTeV
- **监控视图**: 上周已完成事项 (viewId: dGoortH)

## 使用方式

### 手动执行归档检查

```bash
python3 skills/knowledge-base/archive_checker.py
```

### 定时任务

系统会自动在每个工作日上午9点执行归档检查。

## 输出

生成的文档保存在 `skills/knowledge-base/docs/` 目录下，文件命名格式：

```
{事项类型}_{标题}_{recordId}_{日期}.md
```

## 依赖技能

- dingtalk-ai-table: 钉钉多维表格操作
