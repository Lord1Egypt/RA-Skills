---
name: instructor-structured-output
description: |-
  Instructor：声明 Pydantic BaseModel 即可从 20 个 LLM provider 拿到类型化实例。核心是 monkey-patch（instructor.patch / from_*）拦截 create()，注入 schema-aware kwargs，tenacity 重试 +
  Instructor: declare a Pydantic BaseModel and receive a typed instance back from any of 20 LLM providers. Core mechanism is a monkey-patch (instructor.patch / from_*) that intercepts create(), injects schema-aware kwargs, runs the call inside a tenacity retry loop, and rewrites fa
license: MIT-0
compatibility: AI engineering knowledge skill — host AI consumes seed.yaml directly. No installation required.
metadata:
  version: "v0.1.0"
  blueprint_id: "finance-bp-139"
  blueprint_source: "jxnl/instructor"
  blueprint_commit: "3f1d6ddb084b8a0da3eb0665051293d381383b41"
  category: ai-engineering
  doramagic_url: "https://doramagic.ai/zh/crystal/instructor-structured-output"
  openclaw:
    skillKey: instructor-structured-output
    category: ai-engineering
    primaryEnv: knowledge
---
# 这个 skill 适合什么用户？能做哪些任务？

## 概览

Instructor 是把 Pydantic BaseModel 直接绑到 LLM 输出的 Python 框架（github.com/jxnl/instructor）。核心机制：monkey-patch（instructor.patch / instructor.from_*）拦截 provider client 的 create() 调用，注入 schema-aware kwargs，在 tenacity 重试循环里跑，验证 JSON 响应到模型，ValidationError 时把 failed_attempts 作为 XML 重写 prompt 再试。

支持 20 个 provider...

**Doramagic 晶体页**: https://doramagic.ai/zh/crystal/instructor-structured-output

## 知识规模

- **47 条约束** (4 fatal + 43 non-fatal)
- 上游源码: `jxnl/instructor` @ commit `3f1d6ddb`
- 蓝图 ID: `finance-bp-139`

## 用法

Host AI（Claude Code / Cursor / OpenClaw）读 `references/seed.yaml`，按其中的：
- `intent_router` 匹配用户意图
- `architecture` 理解项目架构
- `constraints` 应用 anti-pattern 约束
- `business_decisions` 参考核心设计决策

## FAQ 摘要

### 这个 skill 适合什么用户？能做哪些任务？
适合需要从 LLM 拿到强类型结构化输出的工程师：信息抽取、表单解析、JSON API 直接返回 Pydantic 模型、agent 工具调用参数解析等。20 个 provider 一致 API。访问 doramagic.ai/r/instructor 查看完整用例。

### 需要准备什么环境？依赖什么？
Python 3.9+（instructor 在 pyproject 中声明 >=3.9）。Pydantic v2 事实上必须（function_calls.py 用 model_validate_json + TypeAdapter，都是 v2-only，v1 在 Partial 路径上 AttributeError）。

### 会踩哪些坑？这个 skill 怎么防护？
本 skill 内置 47 条约束（4 条 fatal）。典型踩坑：(1) failed_attempts XML 每次重试线性增长，max_retries=5 可超 context window；(2) from_openai 的 mode 验证用 assert，python -O 下静默剥离；

---

完整文档: 见 `references/seed.yaml` (v6.1 schema). 浏览页: https://doramagic.ai/zh/crystal/instructor-structured-output
