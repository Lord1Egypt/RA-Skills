# Memory-related errors

## 何时读取

当用户的问题涉及 n8n 文档 `hosting/scaling/memory-errors.md` 的主题、配置、概念或操作步骤时读取。

## 核心要点

- n8n doesn't restrict the amount of data each node can fetch and process. While this gives you freedom, it can lead to errors when workflow executions require more memory than available. This page explains how to identify and avoid these errors. n8n provides error messages that warn you in some out of memory situations. For example, messages such as **Execution stopped at this node (n8n may have run out of memory while executing it)**.

## 快速定位

- Identifying out of memory situations
- Typical causes
- Avoiding out of memory situations
- Increase available memory
- Reduce memory consumption
- Increase old memory

