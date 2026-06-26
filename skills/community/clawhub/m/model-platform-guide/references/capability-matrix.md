# 平台能力矩阵

> 这个矩阵用于做平台选型和能力对比。
>
> 重要：其中很多能力属于高变信息，尤其是“某个具体模型是否支持某能力”。本表用于提供方向感，不替代实时核验。

| 平台 | OpenAI SDK 兼容 | 常见聊天接口 | 流式输出 | Tool Calling | 多模态 | Reasoning/Thinking | 联网搜索/外部搜索 | 官方 SDK/生态 | 备注 |
|---|---|---|---|---|---|---|---|---|---|
| Moonshot / Kimi | 是 | `/chat/completions` | 支持 | 支持 | 支持 | 文档中可见 `thinking` 相关字段 | **需动态核验** | OpenAI SDK 兼容 | 模型变化较快，能力以模型页为准 |
| 阿里云百炼 | 是 | `/compatible-mode/v1/chat/completions` | 通常支持 | **需动态核验** | **需动态核验** | **需动态核验** | **需动态核验** | OpenAI SDK + DashScope SDK | 区域、模型族、兼容模式差异要注意 |
| SiliconFlow | 是 | `/chat/completions` | 支持 | 支持 | 支持图像输入 | 响应中可见 reasoning 内容 | **需动态核验** | OpenAI SDK 兼容 | 模型名格式差异大 |
| DeepSeek | 是 | `/chat/completions` | 支持 | **需动态核验** | **需动态核验** | `deepseek-reasoner` 明确存在 | **需动态核验** | OpenAI SDK 兼容 | `deepseek-chat` / `deepseek-reasoner` 区分明显 |
| OpenRouter | 通常是 | `/chat/completions` | 通常支持 | **取决于路由模型** | **取决于路由模型** | **取决于路由模型** | **取决于路由模型** | 聚合层 | 更像统一路由，不是单一模型平台 |
| BigModel | 支持 | 需按文档确认 | **需动态核验** | **需动态核验** | 支持多模态生态 | **需动态核验** | **需动态核验** | HTTP + Python SDK + Java SDK + OpenAI 兼容 | 文档体系完整，适合按需查 |
| Ark | 需按文档确认 | 文本生成/Responses API | **需动态核验** | 文档目录可见工具调用 | 多模态生态明显 | **需动态核验** | **需动态核验** | 火山生态完整 | 适合现场按能力文档查 |
| Hunyuan | 需按文档确认 | 需按文档确认 | **需动态核验** | **需动态核验** | **需动态核验** | **需动态核验** | **需动态核验** | 腾讯云文档体系 | 当前 skill 以导航为主 |
| Qianfan | 需按文档确认 | 需按文档确认 | **需动态核验** | **需动态核验** | **需动态核验** | **需动态核验** | **需动态核验** | 模型服务 + Agent 平台 | 偏平台化，不只是单一 chat API |
| MiniMax | 非完全同路径 | `/v1/text/chatcompletion_v2` | 支持 | **需动态核验** | 支持图文输入 | 响应中可见 reasoning tokens | **需动态核验** | 官方文档清晰 | endpoint 路径和 OpenAI 不同 |

## 使用建议

### 用这个矩阵做什么

适合回答：

- 哪个平台更容易迁移 OpenAI 代码？
- 哪个平台更像“统一接入层”？
- 哪个平台多模态更明确？
- 哪个平台目前更适合需要 reasoning 的场景？

### 不适合直接断言什么

不要仅凭这个矩阵下结论：

- “某平台所有模型都支持联网搜索”
- “某模型现在一定支持 tools”
- “某平台最新模型一定保留旧能力”

这些都要按 `references/live-check-policy.md` 再查一遍。

## 推荐用法

- 做平台选型：先看本矩阵
- 做接入实现：再看 `python-recipes.md` / `nodejs-recipes.md` / `curl-recipes.md`
- 做最新能力判断：最后走 `live-check-policy.md`
