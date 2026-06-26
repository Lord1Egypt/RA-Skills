# EXTEND.md 配置 Schema

## 文件位置

按优先级从高到低：

| 路径 | 范围 |
|------|------|
| `.panda-skills/panda-imagine/EXTEND.md` | 当前项目 |
| `~/.panda-skills/panda-imagine/EXTEND.md` | 用户全局 |
| `.baoyu-skills/baoyu-imagine/EXTEND.md` | 兼容 fallback |
| `~/.baoyu-skills/baoyu-imagine/EXTEND.md` | 兼容 fallback |

## 完整 Schema

EXTEND.md 使用 YAML 前置元数据格式：

```yaml
---
version: 1
default_provider: dashscope
default_quality: 2k
default_aspect_ratio: null
default_image_size: null
default_model:
  openai: gpt-image-1.5
  azure: null
  google: gemini-3-pro-image-preview
  openrouter: google/gemini-3.1-flash-image-preview
  dashscope: qwen-image-2.0-pro
  minimax: image-01
  replicate: google/nano-banana-pro
  jimeng: null
  seedream: null
batch:
  max_workers: 10
  provider_limits:
    replicate:
      concurrency: 5
      start_interval_ms: 700
    google:
      concurrency: 3
      start_interval_ms: 1100
---
```

## 字段说明

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `version` | number | 1 | Schema 版本 |
| `default_provider` | string\|null | null | 默认 Provider |
| `default_quality` | string\|null | null | `normal` 或 `2k`（null → 2k） |
| `default_aspect_ratio` | string\|null | null | 默认宽高比 |
| `default_image_size` | string\|null | null | `1K`/`2K`/`4K`（Google/OpenRouter） |
| `default_model.<provider>` | string\|null | null | 各 Provider 默认模型 |
| `batch.max_workers` | number\|null | 10 | 批量模式最大 worker 数 |
| `batch.provider_limits.<provider>.concurrency` | number\|null | 3-5 | Provider 并发数 |
| `batch.provider_limits.<provider>.start_interval_ms` | number\|null | 700-1100 | 请求间隔（毫秒） |

## 加载优先级

```
CLI 参数 > EXTEND.md > 环境变量 > .panda-skills/.env > ~/.panda-skills/.env
```

EXTEND.md 中的配置优先于环境变量。例如 EXTEND.md 设置了 `default_model.google: gemini-3-pro-image-preview`，即使环境变量中有 `GOOGLE_IMAGE_MODEL=其他模型`，也会使用 EXTEND.md 的值。
