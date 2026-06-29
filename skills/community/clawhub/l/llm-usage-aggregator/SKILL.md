---
name: llm-usage-aggregator
description: LLM使用流水数据汇总工具。将LLM调用日志CSV文件按Provider、Model、用户维度进行汇总统计，输出多Sheet Excel报表，并基于pricing_config.json计算成本。适用场景：(1) 用户提供LLM流水CSV文件需要汇总分析；(2) 需要区分内部/外部用户使用情况；(3) 需要统计prompt_tokens、completion_tokens、generated_image_count、duration_seconds等指标；(4) 需要计算各维度成本费用。
---

# LLM Usage Aggregator

## 快速使用

运行脚本处理CSV文件：

```bash
python scripts/aggregate_llm_usage.py <csv_path> [output_path] [pricing_config_path]
```

## 处理逻辑

### 用户标识合并
- 优先使用 `email` 字段作为用户标识
- 若 `email` 为空，则使用 `phone` 字段

### 内部/外部用户判定
- **内部用户**：email包含 `footprint`、`maybe` 或 `fastest`（不区分大小写）
- **外部用户**：其他所有用户

### 成本计算逻辑

基于 `references/pricing_config.json` 中的模型定价配置，优先按 `model_type` 计算：

| model_type | 计价方式 | 公式 |
|-----------|---------|------|
| `图片` | 按张计价 | `price_per_request × generated_image_count`（若generated_image_count为空或为0则默认1） |
| `视频` | 按秒计价 | 根据`generate_audio`判断有声/无声选择单价，再 `× duration_seconds`（若duration_seconds为空或为0则默认5） |
| `文本` | 按token计价 | `prompt_tokens / 1,000,000 × prompt_price + completion_tokens / 1,000,000 × completion_price` |

补充说明：
- `model_type` 由 `pricing_config.json` 中每个模型的配置决定，值为 `图片`、`视频`、`文本`
- `generation_type` 仍保留在原始流水中，用于辅助识别图片/视频调用场景，但文本模型是否按 token 计价以 `model_type=文本` 为准
- `model_aliases` 用于将原始 `llm_model` 归一化到统一简称后再计价和汇总

### 校验机制

运行时自动执行以下校验，异常信息输出到终端：

| 校验项 | 说明 |
|-------|------|
| 模型未配置 | `llm_model` 不在 pricing_config.json 中，列出模型名及影响行数 |
| llm_model为空 | 原始数据中模型名为空，无法计价 |
| pricing_type不匹配 | `图片/视频` 需要 `per_request`，`文本` 需要 `per_million_tokens` |
| 配置字段缺失 | 视频缺audio_price对应key、文本计价缺prompt_price/completion_price等 |
| 未识别的model_type | 配置中的 `model_type` 不属于 `图片/视频/文本` |
| token计价行成本为0 | `model_type=文本` 的行应逐行有token计价，成本为0属异常，按模型汇总输出 |

#### 视频类型有声/无声判断
- `generate_audio` 为 `True` → 有声，使用 `audio_price.with_audio`
- `generate_audio` 为 `False` 或空值 → 无声，使用 `audio_price.without_audio`
- 若模型配置无 `audio_price` 字段，则使用 `price_per_request`

### 汇总维度
输出Excel为单Sheet（汇总报表），4个区块由上至下排列，每个区块末尾有**合计行**：

| 顺序 | 区块标题 | 汇总维度 |
|-----|---------|----------|
| 1 | 按内外部用户 | 内部用户/外部用户 |
| 2 | 按模型平台 | llm_provider |
| 3 | 按模型 | llm_model |
| 4 | 按用户 | email/phone合并后的用户标识 |

### 汇总字段
- `prompt_tokens` - 输入token数
- `completion_tokens` - 输出token数
- `generated_image_count` - 生成图片数
- `duration_seconds` - 耗时秒数
- `成本(USD)` - 基于定价配置计算的成本
- `记录数` - 调用次数

## CSV文件要求

必需字段：
- `email` 或 `phone` - 用户标识
- `llm_provider` - LLM提供商
- `llm_model` - 模型名称

可选字段：
- `prompt_tokens`、`completion_tokens`、`generated_image_count`、`duration_seconds`
- `generation_type` - 生成类型（image/video/空）
- `generate_audio` - 是否生成音频（布尔值，视频类型使用）

## 参考文件

- `references/pricing_config.json` — 定价配置（与llm-cost-aggregator共用）

### 新增模型（本次更新）

| 模型 | 类型 | 定价 | 说明 |
|-----|------|-----|------|
| `kling-video/v3/standard/image-to-video` | 视频 | 720p无声$0.08/秒，720p有声$0.13/秒 | 可灵v3标准版 |
| `z-ai/glm-5v-turbo` | 文本 | $1.13/M token in, $4.00/M token out | OpenRouter |
| `doubao-seedance-2.0-fast` | 视频 | $6.968/M token | tokenhot |
| `doubao-seedance-2.0` | 视频 | $8.658/M token | tokenhot |
| `fal-ai/kling-video/o1/reference-to-video` | 视频 | $0.11/秒 | 可灵o1 |
| `fal-ai/kling-video/o3/pro/reference-to-video` | 视频 | 无声$0.11/秒，有声$0.14/秒 | 可灵o3 pro |
| `fal-ai/kling-video/o3/standard/reference-to-video` | 视频 | 无声$0.08/秒，有声$0.11/秒 | 可灵o3标准 |
