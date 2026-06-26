---
name: memory-auto-manager
description: Automatic memory management based on built-in memory-lancedb-local-storage. Auto-extract key points, compress conversation, write to MEMORY.md and update vector index after session ends.
---

# memory-auto-manager

基于内置 `memory-lancedb-local-storage` 的自动记忆管理 Skill。

## 功能

- ✅ **会话结束自动触发** → 无需手动输入指令，会话结束自动运行
- ✅ **自动压缩提炼** → 调用 LLM 去掉闲聊、重复内容，保留核心信息
- ✅ **自动分类** → 将内容分为 `decision`/`fact`/`preference`/`entity` 四类
- ✅ **自动写入** → 提炼后的核心内容自动追加到 `MEMORY.md` 永久记忆
- ✅ **自动更新索引** → 写入完成后自动执行 `openclaw memory index --force` 更新本地向量语义索引
- ✅ **完全兼容** → 不修改原有 `memory-lancedb-local-storage` 配置和数据，只是在上层增加自动管理功能

## 配置

无需额外配置，使用当前 OpenClaw 默认 LLM 进行提炼。

## 工作流程

1. 会话结束 → 触发 `session:end` hook
2. 获取完整会话对话
3. 调用 LLM 提炼核心要点，分类
4. 判断是否值得长期保存（内容太短/无价值跳过）
5. 值得保存 → 追加写入 `MEMORY.md`
6. 执行 `openclaw memory index --force` 更新向量索引
7. 完成，日志输出结果

## 作者

OpenClaw auto generated
