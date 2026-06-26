# Ollama first-pass template

Use local/Ollama only for compact structured output.

Target tasks:
- classify lesson type
- compress user feedback
- suggest storage level

Desired output schema:

```json
{
  "lessonType": "preference|rule|mistake|priority",
  "compressedLesson": "string, max 160 chars",
  "storage": "daily|candidate-long-term",
  "needsEscalation": true,
  "reason": "short reason"
}
```

Escalate when the case touches:
- money / billing / auth
- safety / trust
- permanent defaults
- unclear user intent
