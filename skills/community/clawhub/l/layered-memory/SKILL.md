---
name: layered-memory
description: 基于 L0/L1/L2 三层结构的分层记忆管理系统，大幅减少 Token 消耗。L0 节省 99% Token（摘要层），L1 节省 88%（概览层），L2 为完整内容。支持自动生成分层文件、智能按需加载、防重复写入。适用于需要高效管理大型记忆文件的场景。
license: MIT
---

# Layered Memory Management System

分层记忆管理系统，通过 L0/L1/L2 三层结构智能加载记忆，减少 Token 消耗。

## 层级说明

- **L0 (Abstract)**: 极简摘要，节省 ~99% Token
- **L1 (Overview)**: 结构概览，节省 ~88% Token  
- **L2 (Full)**: 完整内容，按需加载

## 使用方式

```bash
# 生成所有记忆文件的分层
node index.js generate --all

# 为单个文件生成分层
node index.js generate ~/clawd/MEMORY.md
```

## 参考文档

- [集成指南](INTEGRATION.md)
- [自动触发](AUTO-TRIGGER.md)
- [防重复写入](ANTI-DUPLICATE.md)
