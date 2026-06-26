# API 集成说明

## 支持的 API 提供商

### 1. OpenAI（推荐）

**适用模型**：
- `gpt-4o` — 角色扮演最强，适合生产环境
- `gpt-4o-mini` — 性价比高，适合测试和轻度使用

**配置方式**：
```
OPENAI_API_KEY=sk-...
MODEL=gpt-4o
BASE_URL=https://api.openai.com/v1  # 可选，默认
```

**特点**：
- 指令遵循力最强，5个咨询师人设区分度最高
- JSON 输出稳定性最好
- 中文理解力优秀

---

### 2. DeepSeek

**适用模型**：
- `deepseek-chat` (V3) — 中文原生，性价比极高
- `deepseek-reasoner` (R1) — 推理能力强，但会暴露思考链

**配置方式**：
```
OPENAI_API_KEY=sk-...
MODEL=deepseek-chat
BASE_URL=https://api.deepseek.com/v1
```

**特点**：
- 价格是 GPT-4o 的 1/20
- 中文长文本理解力强
- **注意**：R1 会暴露推理过程（"我是AI"的内层思维），与项目"永远不要暴露你是AI"的要求冲突。生产环境建议使用 V3。

---

### 3. 其他兼容 OpenAI 格式的 API

任何支持 OpenAI SDK 的 API 都可以使用，只需配置 `BASE_URL` 和 `MODEL`：

```
OPENAI_API_KEY=your-key
MODEL=your-model-name
BASE_URL=https://your-api-provider.com/v1
```

---

## 环境变量配置

复制 `.env.example` 为 `.env`，填入实际值：

```bash
cp .env.example .env
```

`.env` 文件内容：
```
OPENAI_API_KEY=your-api-key-here
MODEL=gpt-4o
BASE_URL=          # 留空使用默认 OpenAI 地址
```

---

## 成本估算

以 GPT-4o-mini 为例：

| 场景 | 输入 Token | 输出 Token | 单次对话成本 |
|------|-----------|-----------|-------------|
| 普通对话 | ~1,000 | ~200 | ~$0.0003 |
| 人格分析 | ~3,000 | ~500 | ~$0.001 |
| 完整 10 轮对话（含 2 次分析） | ~8,000 | ~1,500 | ~$0.003 |

**结论**：GPT-4o-mini 足够使用，成本几乎可忽略。如需最强效果使用 GPT-4o，成本约高 15-20 倍但仍属低廉。
