# Quiz JSON Schema Contract

Return one JSON object with this shape:

```json
{
  "metadata": {
    "subject": "string",
    "topic": "string",
    "difficulty": "easy|medium|hard",
    "blooms_level": "remember|understand|apply|analyze|evaluate|create",
    "time_budget_min": 25
  },
  "questions": [
    {
      "id": "q1",
      "type": "mcq|short|explain|case",
      "prompt": "string",
      "options": ["A", "B", "C", "D"],
      "points": 5,
      "concept": "string"
    }
  ],
  "answer_key": [
    {"id": "q1", "expected": "B", "explanation": "string"}
  ],
  "grading_rubric": [
    {
      "id": "q1",
      "criteria": ["correctness", "reasoning", "clarity"],
      "point_rules": "How points are assigned"
    }
  ],
  "feedback_rules": {
    "mistake_to_action": [
      {"pattern": "confuses X and Y", "action": "do drill Z"}
    ]
  }
}
```

Rules:
- Keep IDs unique and aligned across `questions`, `answer_key`, and `grading_rubric`.
- Mix cognitive levels; avoid only recall questions.
- Make at least 30% application or case-based questions for intermediate+ learners.
