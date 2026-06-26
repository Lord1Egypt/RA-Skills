# 模型提供商 API 配置

用户提供 API Key 和模型名称后，按以下模板配置：

---

## OpenRouter（推荐，聚合 200+ 模型）

**config.yaml:**
```yaml
model:
  provider: openrouter
  default: MODEL_NAME
```

**.env:**
```bash
OPENROUTER_API_KEY=YOUR_API_KEY
```

**可用模型：**
- `anthropic/claude-sonnet-4`
- `anthropic/claude-opus-4`
- `openai/gpt-4o`
- `google/gemini-pro-1.5`
- `meta-llama/llama-3.1-70b-instruct`

**文档：** https://openrouter.ai/docs

---

## 智谱 GLM Coding Plan（推荐用于 Coding 场景）

**config.yaml:**
```yaml
model:
  provider: custom
  base_url: https://open.bigmodel.cn/api/coding/paas/v4
  default: MODEL_NAME
```

**.env:**
```bash
OPENAI_API_KEY=YOUR_API_KEY
OPENAI_BASE_URL=https://open.bigmodel.cn/api/coding/paas/v4
```

**可用模型：**
- `glm-5`
- `glm-4-plus`
- `glm-4-air`
- `glm-4-flash`
- `glm-4.7`（支持思考模式）

**重要提示：**
- **Coding Plan 端点**：`https://open.bigmodel.cn/api/coding/paas/v4`（消耗 Coding Plan 额度）
- **通用端点**：`https://open.bigmodel.cn/api/paas/v4/`（产生额外费用）

**文档：** https://open.bigmodel.cn/dev/api

---

## z.ai（GLM 国际版）

**config.yaml:**
```yaml
model:
  provider: custom
  base_url: https://api.z.ai/api/paas/v4/
  default: MODEL_NAME
```

**.env:**
```bash
OPENAI_API_KEY=YOUR_API_KEY
OPENAI_BASE_URL=https://api.z.ai/api/paas/v4/
```

**可用模型：**
- `glm-5`
- `glm-4-plus`
- `glm-4-air`
- `glm-4-flash`

**文档：** https://api.z.ai

---

## Kimi Coding Plan（推荐用于 Coding 场景）

**config.yaml:**
```yaml
model:
  provider: custom
  base_url: https://api.kimi.com/coding/v1
  default: MODEL_NAME
```

**.env:**
```bash
OPENAI_API_KEY=YOUR_API_KEY
OPENAI_BASE_URL=https://api.kimi.com/coding/v1
```

**可用模型：**
- `kimi-k2.5`（最新版，支持视觉和思考）

**重要提示：**
- **Coding Plan 端点**：`https://api.kimi.com/coding/v1`（消耗 Coding Plan 额度）
- **通用端点**：`https://api.moonshot.cn/v1`（产生额外费用）

**文档：** https://platform.kimi.com/docs/api/chat

---

## Kimi / Moonshot（通用端点）

**config.yaml:**
```yaml
model:
  provider: custom
  base_url: https://api.moonshot.cn/v1
  default: MODEL_NAME
```

**.env:**
```bash
OPENAI_API_KEY=YOUR_API_KEY
OPENAI_BASE_URL=https://api.moonshot.cn/v1
```

**可用模型：**
- `kimi-k2.5`
- `kimi-k2-thinking`
- `kimi-k2-0905-preview`
- `moonshot-v1-8k`
- `moonshot-v1-32k`
- `moonshot-v1-128k`

**文档：** https://platform.kimi.com/docs/api/chat

---

## 阿里云百炼 Coding Plan（推荐用于 Coding 场景）

**config.yaml:**
```yaml
model:
  provider: custom
  base_url: https://coding.dashscope.aliyuncs.com/v1
  default: MODEL_NAME
```

**.env:**
```bash
OPENAI_API_KEY=sk-sp-xxxxx  # Coding Plan 专属 API Key
OPENAI_BASE_URL=https://coding.dashscope.aliyuncs.com/v1
```

**重要提示：**
- **API Key 格式**：`sk-sp-xxxxx`（Coding Plan 专属）
- **Coding Plan 端点**：`https://coding.dashscope.aliyuncs.com/v1`
- **通用端点**：`https://dashscope.aliyuncs.com/compatible-mode/v1`

**控制台：** https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/coding_plan

---

## 阿里云百炼（通用端点）

**config.yaml:**
```yaml
model:
  provider: custom
  base_url: https://dashscope.aliyuncs.com/compatible-mode/v1
  default: MODEL_NAME
```

**.env:**
```bash
OPENAI_API_KEY=sk-xxxxx
OPENAI_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
```

**可用模型：**
- `qwen-turbo`
- `qwen-plus`
- `qwen-max`
- `qwen-max-longcontext`
- `qwen-vl-plus`
- `qwen-vl-max`

**国际端点：** `https://dashscope-intl.aliyuncs.com/compatible-mode/v1`

---

## 腾讯云 Coding Plan

**config.yaml:**
```yaml
model:
  provider: custom
  base_url: https://api.lkeap.cloud.tencent.com/coding/v3
  default: MODEL_NAME
```

**.env:**
```bash
OPENAI_API_KEY=YOUR_API_KEY
OPENAI_BASE_URL=https://api.lkeap.cloud.tencent.com/coding/v3
```

**重要提示：**
- Coding Plan 端点不含混元模型

---

## 腾讯云混元（通用端点）

**config.yaml:**
```yaml
model:
  provider: custom
  base_url: https://api.hunyuan.cloud.tencent.com/v1
  default: MODEL_NAME
```

**.env:**
```bash
OPENAI_API_KEY=YOUR_API_KEY
OPENAI_BASE_URL=https://api.hunyuan.cloud.tencent.com/v1
```

**可用模型：**
- `hunyuan-turbos-latest`
- `hunyuan-lite`
- `hunyuan-standard`
- `hunyuan-pro`
- `hunyuan-vision`

---

## 火山引擎 Coding Plan

**config.yaml:**
```yaml
model:
  provider: custom
  base_url: https://ark.cn-beijing.volces.com/api/coding/v3
  default: MODEL_NAME
```

**.env:**
```bash
OPENAI_API_KEY=YOUR_API_KEY
OPENAI_BASE_URL=https://ark.cn-beijing.volces.com/api/coding/v3
```

**可用模型：**
- `doubao-seed-2.0-code`
- `doubao-seed-2.0-pro`
- `doubao-seed-2.0-lite`
- `minimax-m2.5`
- `glm-4.7`
- `kimi-k2.5`

---

## 阶跃星辰 Coding Plan（推荐用于 Coding 场景）

**config.yaml:**
```yaml
model:
  provider: custom
  base_url: https://api.stepfun.com/step_plan/v1
  default: MODEL_NAME
```

**.env:**
```bash
OPENAI_API_KEY=YOUR_API_KEY
OPENAI_BASE_URL=https://api.stepfun.com/step_plan/v1
```

**可用模型：**
- `step-1-8k`
- `step-1-32k`
- `step-1-128k`
- `step-1v-8k`（视觉模型）

**重要提示：**
- **Coding Plan 端点**：`https://api.stepfun.com/step_plan/v1`（消耗 Coding Plan 额度）
- **通用端点**：`https://api.stepfun.com/v1`（产生额外费用）

---

## 阶跃星辰 Step（通用端点）

**config.yaml:**
```yaml
model:
  provider: custom
  base_url: https://api.stepfun.com/v1
  default: MODEL_NAME
```

**.env:**
```bash
OPENAI_API_KEY=YOUR_API_KEY
OPENAI_BASE_URL=https://api.stepfun.com/v1
```

**可用模型：**
- `step-1-8k`
- `step-1-32k`
- `step-1-128k`
- `step-1v-8k`

---

## 自定义 OpenAI 兼容端点

**config.yaml:**
```yaml
model:
  provider: custom
  base_url: YOUR_ENDPOINT_URL
  default: YOUR_MODEL_NAME
```

**.env:**
```bash
OPENAI_API_KEY=YOUR_API_KEY
OPENAI_BASE_URL=YOUR_ENDPOINT_URL
```

---

## Coding Plan 端点汇总

| 提供商 | Coding Plan 端点 | API Key 格式 |
|--------|-----------------|--------------|
| 智谱 GLM | `https://open.bigmodel.cn/api/coding/paas/v4` | 标准 |
| Kimi | `https://api.kimi.com/coding/v1` | 标准 |
| 阿里云百炼 | `https://coding.dashscope.aliyuncs.com/v1` | `sk-sp-xxxxx` |
| 火山引擎 | `https://ark.cn-beijing.volces.com/api/coding/v3` | 标准 |
| 腾讯云 | `https://api.lkeap.cloud.tencent.com/coding/v3` | 标准（不含混元） |
| 阶跃星辰 | `https://api.stepfun.com/step_plan/v1` | 标准 |
