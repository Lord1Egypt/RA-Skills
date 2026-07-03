# 2026 Token 优化最佳实践

## 一、Provider 级别（自动生效，无需配置）

### 1.1 Prompt Caching
DeepSeek、Anthropic、OpenAI 均已支持。重复的 system prompt 内容自动命中缓存，不重复计费。
- **影响:** system prompt 越稳定（少改），缓存命中率越高
- **我们做了什么:** MEMORY/AGENTS/SOUL 瘦身后，缓存命中率提升约 30%

### 1.2 结构性输出
JSON mode / Structured Output 减少响应 token。
- DeepSeek V4: 支持 `response_format: { type: "json_object" }`
- 用于 scan.py/report.py 输出 JSON，而非 Markdown

## 二、OpenClaw 配置级

### 2.1 Compaction（已启用）
```json
"compaction": { "mode": "default", "reserveTokens": 30000, "reserveTokensFloor": 20000 }
```
长对话自动压缩摘要，老消息不占上下文窗口。

### 2.2 Light Context 子智能体
```javascript
sessions_spawn({ lightContext: true })
```
子 agent 不加载完整 system prompt，节省 ~5K tokens/次。

### 2.3 Context Fork 按需
不传 `context: "fork"` 时子智能体不继承父 session 历史。

## 三、工作区文件级

### 3.1 AGENTS.md 精简
- 主工作区: 9.7KB → 2.2KB (78%)
- 22 个 DM 工作区: 8.6KB → 2.2KB each

### 3.2 DREAMS.md 截断
- 保留最近 15 条梦境
- 27 个工作区: 767KB → 113KB (85%)

### 3.3 MEMORY.md 归档
- 活跃条目保留，旧项目移至 MEMORY-extended.md
- 主工作区: 24.9KB → 3.1KB (88%)

## 四、模型路由（已配置）

auto-task 模式自动识别任务复杂度：
- 简单问答 → FW-Flash (便宜)
- 复杂推理 → FW-Pro
- 视觉任务 → MiniMax VL tier

## 五、参考

- [Anthropic Prompt Caching](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching)
- [DeepSeek Context Caching](https://api-docs.deepseek.com/guides/context_caching)
- [OpenClaw Compaction Docs](https://docs.openclaw.ai/gateway/configuration-reference.html)
