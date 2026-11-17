# Data Flow Diagram — huawei-cloud-daily-hot-topics

```mermaid
flowchart TD
    A["CLI: fetch_hot_topics.py"] --> B{--offline?}
    B -- yes --> S["load_sample()<br/>scripts/sample_data.json"]
    B -- no --> C["resolve_chain(--source)"]
    C --> D["fetch_source(name, timeout, retries)"]
    D --> E["HTTPS GET (urllib)<br/>public keyless hot-list API"]
    E --> F{"JSON envelope OK<br/>and records present?"}
    F -- yes --> G["normalize(records)<br/>rank/title/hot/source/url"]
    F -- no --> H{"more providers<br/>in the chain?"}
    H -- yes --> D
    H -- no --> S
    G --> I["result {source, is_sample=false, items, warnings}"]
    S --> J["result {source=sample, is_sample=true, items, warnings}"]
    I --> K["render_markdown / render_text / render_json (--top)"]
    J --> K
    K --> L{"--output?"}
    L -- yes --> M["write file"]
    L -- no --> N["stdout"]
```

## Notes

- The provider chain is resolved first (`--source` pin, else the default chain).
- Each provider is tried with a bounded timeout and a small retry budget; the
  first non-empty, well-formed response wins.
- On total failure (or `--offline`) the bundled sample dataset is used and the
  result is flagged as sample data; failures are collected into `warnings`.
- Rendering applies the `--top` limit and produces Markdown / text / JSON, which
  is written to a file or to standard output.