# API 与提示词约定

本 Skill 通过 **OpenAI 兼容 `chat/completions` 协议**调用多模态 VLM。同一份代码可对接：

| Provider | API Key 环境变量 | 默认 base_url | 默认模型 |
|----------|---------------------|---------------|----------|
| `ark`（火山方舟，推荐） | `ARK_API_KEY` | `https://ark.cn-beijing.volces.com/api/v3` | `doubao-1.5-vision-pro` |
| `dashscope`（阿里通义） | `DASHSCOPE_API_KEY` | `https://dashscope.aliyuncs.com/compatible-mode/v1` | `qwen-vl-max` |
| `openai` | `OPENAI_API_KEY` | （SDK 默认） | `gpt-4o-mini` |
| `ollama`（本地） | （可选）`OLLAMA_API_KEY` | `http://localhost:11434/v1` | `qwen2.5-vl:7b` |

显式指定 provider：`VLM_PROVIDER=ark|openai|dashscope|ollama`。

## 单次调用结构

```python
client.chat.completions.create(
    model=cfg.model,
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": <prompts.build_prompt(mode)>},
            {"type": "image_url", "image_url": {"url": "data:image/png;base64,<...>"}},
        ],
    }],
    temperature=0.0,
    response_format={"type": "json_object"},   # 不支持时自动剥掉
)
```

模型返回单个 JSON object，schema 见下。

## 模型应返回的页级 JSON Schema

```jsonc
{
  "page_no": 3,
  "markdown": "## 合并资产负债表\n\n| 项目 | 2024 | 2023 |\n...",
  "blocks": [
    {"type": "heading", "level": 2, "text": "合并资产负债表",
     "source_page": 3, "source_bbox": [72.0, 90.5, 480.0, 110.0]}
  ],
  "tables": [
    {"caption": "合并资产负债表（单位：人民币元）",
     "n_rows": 25, "n_cols": 3, "header_rows": 1,
     "source_page": 3, "source_bbox": [60.0, 130.0, 540.0, 720.0],
     "cells": [
       {"row": 0, "col": 0, "rowspan": 1, "colspan": 1, "text": "项目"},
       {"row": 1, "col": 0, "text": "货币资金"},
       {"row": 1, "col": 1, "text": "1,234,567,890.12",
        "value": 1234567890.12, "unit": "yuan"}
     ]}
  ],
  "confidence": 0.92
}
```

字段约束的全文见 [prompts.md](prompts.md) 与 [../assets/output_schema.json](../assets/output_schema.json)。

## 重试与错误处理

- HTTP / 网络错误：指数退避 `[1, 2, 4, 8]` 秒重试，默认 3 次
- 模型返回非 JSON：尝试剥 Markdown 围栏 → 兜底从首个 `{` 到末尾 `}` 切片 → 仍失败抛 `VLMError`
- `VLMError` 由调用方在 `parse` / `check-and-notify` 中捕获，记入 `meta.json.failed_pages`，不会中断整篇文档

## Rate limit 注意

- ARK Doubao Vision：约 60 RPM；本 Skill 单进程串行调用，正常使用不会触发
- 多文档批跑时请**避免并发**（不要 `xargs -P`），如需提速优先升 QPS 配额而非并发本地进程
