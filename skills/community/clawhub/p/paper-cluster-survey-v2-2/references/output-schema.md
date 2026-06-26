# Output Schema

Use this when the user asks for a strict structure or when the review will be reused downstream.

## Default deliverable order

1. Corpus summary
2. Classification scheme
3. Classification table
4. Formal literature review
5. References

## Classification table

| Paper | Year | Category | Rationale | Evidence |
| --- | --- | --- | --- | --- |

## Typical review shape

This is a common review-paper shape, not a mandatory template. Adapt section names and ordering when another structure is more natural for the corpus.

```md
# <Title>

## 摘要

## 关键词

## 引言

## <按时间、主题、方法或观点组织的主体部分>
### ...
### ...

## 讨论 / 结论

## 展望 / 未来研究方向

## 参考文献
[1] ...
```

## JSON shape

```json
{
  "corpus_summary": {
    "total_papers": 0,
    "time_span": {"start": null, "end": null},
    "dominant_topics": [],
    "notes": []
  },
  "classification_scheme": {
    "basis": "task|method|application",
    "rationale": "",
    "categories": [
      {
        "name": "",
        "definition": ""
      }
    ]
  },
  "classification_table": [
    {
      "paper": "",
      "year": null,
      "category": "",
      "rationale": "",
      "evidence": []
    }
  ],
  "papers": [
    {
      "source_id": "paper-001",
      "title": "",
      "authors": [],
      "year": null,
      "venue": "",
      "abstract": "",
      "task": "",
      "method": "",
      "datasets": [],
      "metrics": [],
      "main_contribution": "",
      "limitations": "",
      "source": "",
      "extraction_notes": []
    }
  ],
  "review": {
    "title": "",
    "abstract": "",
    "keywords": [],
    "introduction": "",
    "body_sections": [
      {
        "heading": "",
        "content": ""
      }
    ],
    "discussion": "",
    "conclusion": "",
    "future_directions": "",
    "references": []
  }
}
```
