# 主流模型官方参考分锚点表

判分时的**起点**，不是终点。使用方法：

1. 判分前**必须**点来源链接复核最新官方值——模型会更新版本，分数会变；
2. 注意口径：官方常报 avg@k/pass@k 或带工具的分数，我们跑的是 temp=1.0 单 epoch
   无工具，**判定用区间不用点值**（GPQA 50 题噪声 ±5pp，AIME 15 题 ±2 题）；
3. 表中数值为约数，最后人工核对日期：**2026-08**。超过一两个月未复核就当过期处理。

## 锚点表

| 模型 | GPQA Diamond | AIME 2025 | 口径备注 | 官方来源 |
|---|---|---|---|---|
| Kimi K3 (thinking) | ≈85.7 | ≈80+ (pass@32) | 文本推理官方公布值；各正规供应商分数接近 | [Kimi-Vendor-Verifier](https://github.com/MoonshotAI/Kimi-Vendor-Verifier) |
| Kimi K2 Thinking | ≈92 (待复核) | ≈99（含工具口径，待复核） | 发布时主打 agentic，注意是否含工具调用 | 同上 + 官方博客 |
| DeepSeek R1 | 71.5 | —（AIME 2024: 79.8） | R1 论文值 | [DeepSeek-R1 README](https://github.com/deepseek-ai/DeepSeek-R1) |
| DeepSeek R1-0528 | ≈81.0 | ≈87.5 | 0528 刷新版 | 同上 |
| DeepSeek V3.2 系列 | 待查 | 待查 | thinking/non-thinking 差异大，分行查 | [DeepSeek GitHub](https://github.com/deepseek-ai) |
| GPT-5 | ≈85–87 | ≈94.6（无工具） | OpenAI 发布值 | [OpenAI GPT-5](https://openai.com/index/introducing-gpt-5/) |
| Gemini 3 Pro | ≈91.9 | ≈95.0（无工具） | Google 发布值 | [Gemini 模型页](https://deepmind.google/models/gemini/) |
| Claude Opus 4.x | 待查 | 待查 | 按具体小版本查 | [Anthropic News](https://www.anthropic.com/news) |
| Grok 4 / 4.x | 待查 | 待查 | 注意 Heavy 多智能体口径单列 | [x.ai News](https://x.ai/news) |
| Qwen3 系列 | 待查 | 待查 | 按尺寸/thinking 模式分行 | [Qwen GitHub](https://github.com/QwenLM) |
| GLM 系列 | 待查 | 待查 | 同上 | [智谱开放平台](https://docs.bigmodel.cn/) |

"待查" = 我没把握的值，**不许脑补**，按来源列或搜索引擎查实后填入，并把"最后核对日期"改到当天。

## 权威查询渠道（优先级从高到低）

1. 官方技术报告 / 模型卡 / 发布博客（上表来源列）
2. 官方 vendor-verifier（如 Kimi-Vendor-Verifier 对各供应商同模型的复测表）
3. 第三方复测（Artificial Analysis 等）——仅作旁证，口径常与官方不同

## 新增模型行的格式

```
| <模型名> | <GPQA 分数> | <AIME 分数> | <口径: avg@k? 工具? thinking?> | <可点击来源链接> |
```

同时更新本文顶部的"最后人工核对日期"。
