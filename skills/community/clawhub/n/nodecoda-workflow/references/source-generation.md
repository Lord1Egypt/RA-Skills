# NodeCoda Source 快速上手

完整语法见 [language-reference.md](language-reference.md)。

## 最小 Source

```nodecoda
@language nodecoda/1
@mode workflow

function main(string query) -> string {
    let response = llm("openai_api_compatible/gpt-5.4", {
        "messages": [{ "role": "user", "content": query }]
    });
    return response.text;
}
```

## 五个核心操作

| 操作 | 语法 | 结果访问 |
|---|---|---|
| LLM | `llm(model, { messages })` | `.text` |
| 工具 | `tool("name", "action", params)` | `.result` |
| HTTP | `http("GET", url, opts)` | `.body`, `.status_code` |
| 知识库 | `knowledge("ds-id", query, opts)` | `.result` |
| 结构化抽取 | `extract<T>(model, text, opts)` | `.ok`, `.value.field` |

## 两个模式

- `@mode workflow`：单次请求响应，使用 `return` 输出。
- `@mode advanced-chat`：多轮会话，可使用 `answer()` 和会话变量。

Source 必须保存为 `.ncoda`，并通过 `build_dify_workflow` 生成目标相关的 Dify Workflow artifact。
