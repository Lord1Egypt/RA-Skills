# Output Schema

`scripts/search.py --json` 的结果结构：

```json
{
  "query": "调查研究",
  "mode": "hybrid",
  "filters": {
    "volume": null,
    "chapter": null,
    "title": null
  },
  "results": [
    {
      "doc_id": 12,
      "passage_id": 105,
      "volume": "第一卷",
      "volume_no": 1,
      "article_no": 7,
      "article_title": "反对本本主义",
      "date": "1930-05",
      "source_path": "data/01-07-反对本本主义.md",
      "retrieval": "hybrid-rerank",
      "score": 17.42,
      "snippet": "没有调查，没有发言权……"
    }
  ]
}
```

说明：

- `catalog` 模式只返回文章级结果，可以没有 `passage_id`
- `show` 模式返回完整文章正文
- `search` 模式优先返回段落级命中，并附带所属文章信息
- 如果文档来自 `01-03-标题.md` 这类命名，结果里会带 `volume_no` 和 `article_no`
- `retrieval` 可能是 `lexical`、`lexical-like`、`hybrid` 或 `hybrid-rerank`
