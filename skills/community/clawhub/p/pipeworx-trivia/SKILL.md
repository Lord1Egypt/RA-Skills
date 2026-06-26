---
name: pipeworx-trivia
description: Trivia questions from the Open Trivia Database — 4,000+ questions across 24 categories with difficulty levels
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - curl
    emoji: "🧠"
    homepage: https://pipeworx.io/packs/trivia
---

# Open Trivia Database

Over 4,000 trivia questions across 24 categories including Science, History, Sports, Geography, Entertainment, and more. Filter by difficulty (easy, medium, hard) and question type (multiple choice or true/false).

## Tools

- **`get_questions`** — Fetch trivia questions with optional category, difficulty, and type filters
- **`list_categories`** — All 24 trivia categories with their IDs
- **`get_category_stats`** — Question counts by difficulty for a specific category

## Great for

- Building a trivia game or quiz app
- "Quiz me on world history" — filter by category and difficulty
- Team-building icebreakers with random trivia
- Educational apps that gamify learning

## Example: 5 medium-difficulty science questions

```bash
curl -s -X POST https://gateway.pipeworx.io/trivia/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"get_questions","arguments":{"amount":5,"category":17,"difficulty":"medium"}}}'
```

Each question includes the question text, correct answer, incorrect answers, category, and difficulty.

## Popular category IDs

| Category | ID |
|----------|----|
| General Knowledge | 9 |
| Science & Nature | 17 |
| History | 23 |
| Geography | 22 |
| Sports | 21 |
| Computers | 18 |

## MCP config

```json
{
  "mcpServers": {
    "pipeworx-trivia": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "https://gateway.pipeworx.io/trivia/mcp"]
    }
  }
}
```
