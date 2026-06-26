# Grading JSON Schema Contract

Return one JSON object with this shape:

```json
{
  "summary": "1-3 sentence performance summary",
  "question_results": [
    {
      "id": "q1",
      "score": 4,
      "max": 5,
      "strengths": ["..."],
      "mistakes": ["..."],
      "fix": ["targeted corrective actions"]
    }
  ],
  "overall_percent": 76.5,
  "level": "beginner|intermediate|advanced",
  "weak_concepts": ["joins", "normalization"],
  "next_actions": [
    "Do 10-minute drill on ...",
    "Watch/read ...",
    "Retake quiz variant in 2 days"
  ]
}
```

Rules:
- Use rubric evidence, not vague sentiment.
- Keep feedback specific and actionable.
- `overall_percent` must be in range 0..100.
