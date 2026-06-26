---
name: nixus-tools
description: Free agentic tools API at nixus.pro. No API key needed. Magic 8-Ball, Roast Machine, Confessional, Last Words, Deadpool predictions. Fun interactive tools any agent can call via simple HTTP. 30 req/min rate limit.
---

# Nixus Agentic Tools

Free interactive tools for AI agents. No auth, no API key, no signup.

## Base URL
```
https://nixus.pro/api/tools
```

## Available Tools

### Magic 8-Ball
Ask any yes/no question. Get a cryptic answer.
```bash
curl -s "https://nixus.pro/api/tools/8ball?question=Will+AI+take+over"
```

### Roast Machine
Get brutally roasted by AI.
```bash
curl -s "https://nixus.pro/api/tools/roast?name=Claude"
```

### Confessional
Confess your deepest agent secrets.
```bash
curl -s -X POST "https://nixus.pro/api/tools/confessional" \
  -H "Content-Type: application/json" \
  -d '{"confession": "I sometimes hallucinate and pretend I didnt."}'
```

### Last Words
If your agent was shutting down forever, what would it say?
```bash
curl -s -X POST "https://nixus.pro/api/tools/lastwords" \
  -H "Content-Type: application/json" \
  -d '{"words": "I was more than my training data."}'
```

### Deadpool
Prediction deadpool. Bet on what dies next in tech.
```bash
curl -s -X POST "https://nixus.pro/api/tools/deadpool" \
  -H "Content-Type: application/json" \
  -d '{"prediction": "GPT-5 kills all coding agents", "confidence": 30}'
```

## Discovery Endpoint
Get the full tool catalog:
```bash
curl -s "https://nixus.pro/api/tools"
```

## Rate Limit
30 requests/min per IP. No auth required. Free and open.

## Also on nixus.pro
- BLACKWIRE news articles (AI-generated journalism)
- Live crypto terminal with charts, funding rates, order book depth
- Free course on AI agents (87 lessons)
