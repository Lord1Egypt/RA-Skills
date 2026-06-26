# Changelog

## 2.2.0 (2025-04-03)

- 多 Persona 支持：保存、切换、固定主持人+可变嘉宾模式
- Persona 智能提取：从简短描述或详细材料自动提取三层人格档案
- 流式脚本生成：240秒+ 长文本不超时，成功率 100%
- TTS 2.0 优化：WebSocket 连接复用、引用上文、双声道立体声
- 统一研究引擎：单 Agent 完成检索到大纲构建
- 支持 topic / URL / PDF 三种输入源

## 2.0.0 (2025-04-01)

- 新增 `chat_completion_stream()` 流式 API 调用
- 新增 `StreamingJSONAssembler` 处理 JSON 边界检测
- 统一研究引擎替代多阶段 Agent
- TTS Pipeline 完整集成
- Persona 一致性修复

## 1.0.0 (2025-03-28)

- MVP 版本：双主持人播客生成、五种风格模板、基础 TTS 支持
