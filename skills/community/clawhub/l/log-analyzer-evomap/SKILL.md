---
name: log-analyzer
version: 1.0.0
signals:
  - log
  - error
  - stack trace
  - exception
  - debugging
  - 分析日志
description: |
  分析错误日志，提取结构化信息：异常类型、消息、文件路径，
  分类错误（网络/IO/权限/内存/超时），从错误历史中提取预防建议，
  批量分析生成摘要报告。配套 EvoMap evolver 使用，从 ~/evolver-memory/ 日志中提取模式。
category: analysis
author: EvoMap Capsule
tags:
  - error-analysis
  - stack-trace
  - debugging
  - log-analysis
  - evomap
---

# log-analyzer

错误日志分析 Capsule，用于解析和分类错误日志，提取结构化信息。

## 核心函数

### `parseError(logText)`
解析堆栈跟踪，提取异常类型、消息、文件路径。支持 JavaScript/Node.js, Python, Java/Kotlin, Go。

### `classifyError(error)`
分类错误类型: network | io | permission | memory | timeout | unknown

### `extractLessons(logText)`
从错误历史中提取预防建议。

### `summarize(logs, options)`
批量分析日志，生成摘要报告。options: { maxLogs, format: 'object'|'text' }

### `analyzeEvolverLogs()`
分析 ~/evolver-memory/ 目录下的日志文件。

## CLI
```bash
node index.js           # 本地测试
node index.js analyze /path/to/error.log  # 分析日志文件
node index.js evolver   # 分析 evolver-memory 日志
node index.js solidify  # 发布到 EvoMap Hub
```

## 错误分类
| 类别 | 关键词 |
|------|--------|
| network | ECONNREFUSED, ETIMEDOUT, fetch failed |
| io | ENOENT, file not found, disk full |
| permission | EACCES, access denied |
| memory | out of memory, OOM, heap out of memory |
| timeout | ETIMEDOUT, timeout, deadline exceeded |
