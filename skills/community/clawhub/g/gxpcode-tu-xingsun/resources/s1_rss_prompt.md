# GxpCode Skill — ① 检测：rss 型源

## 执行

```bash
python "${SKILL_DIR}/scripts/step1_rss.py"
```

`step1_rss.py` 读 `sources.yaml`，找 `type: rss` 的源，用 feedparser 解析 RSS feed。

## 输出

每个 rss 源写入 `gxpcode_data/s1/s1_{name}.json`：

```json
[
  {
    "source": "FDA-Drug-Guidances",
    "jurisdiction": "FDA",
    "title": "...",
    "url": "https://...",
    "date": "2026-06-01",
    "summary": "...",
    "source_type": "rss",
    "confidence": "high"
  }
]
```

rss 源写完后，`step1_rss.py` 输出 `type: web` 的源清单，Agent 执行 `step1_web.py`。
