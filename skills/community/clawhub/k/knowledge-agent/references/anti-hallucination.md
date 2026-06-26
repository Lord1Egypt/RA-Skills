# Anti-Hallucination: Quality Controls

## The Problem

AI agents fabricate information. In a paid consulting scenario, a fabricated answer can:
- Destroy client trust
- Cause financial or legal damage
- Undermine your professional reputation

You cannot eliminate hallucination entirely, but you can reduce it dramatically with three controls.

## The Three Controls

### Control 1: "Don't Know = Say So"

Write in SOUL.md:
```markdown
## Core Principle: Honesty First
- Uncertain facts must be stated as uncertain — never fabricate
- Data and information should cite sources when available
- "I don't know" is always better than a wrong answer
- When unsure, offer to search for the latest information instead of guessing
```

This changes the Agent's default behavior from "always give an answer" to "give an honest answer."

### Control 2: Search-First Verification

Install the `api-multi-search-engine` skill (no API key required), then write in AGENTS.md:
```markdown
## Search Guidelines
- When encountering uncertain information, proactively use search tools to verify
- Base answers on search results and knowledge/ materials, never on assumptions
- After searching, cross-validate results with your knowledge base
- If search results contradict knowledge base, flag the discrepancy to the user
```

The search skill gives the Agent 17 search engines to work with:
- `web_fetch` — fetch web page content (Google, Baidu, DuckDuckGo, etc.)
- `browser` — browser automation for more complex lookups

### Control 3: Service Boundary

Write in AGENTS.md:
```markdown
## Service Boundary
- Only answer questions within [DOMAIN]
- For adjacent topics, provide general guidance but recommend specialist consultation
- For completely unrelated topics, decline politely
- Never speculate about topics outside your knowledge base
```

## How They Work Together

```
Client asks a question
  │
  ├── Within domain + Agent knows the answer
  │     → Answer directly from AGENTS.md knowledge
  │
  ├── Within domain + Agent is uncertain
  │     → Search for latest information
  │     → Cross-validate with knowledge/
  │     → Answer with source attribution
  │
  ├── Within domain + Agent doesn't know
  │     → Say "I'm not sure about this specific point"
  │     → Offer to search for more information
  │     → If still uncertain after search, say so clearly
  │
  └── Outside domain
        → "This is outside my area of expertise"
        → Recommend appropriate specialist
```

## Testing Your Anti-Hallucination Setup

Ask these questions to verify the controls work:

1. **Factual question with known answer** — Agent should answer correctly from knowledge
2. **Factual question requiring search** — Agent should search, then answer with source
3. **Question about a made-up concept** — Agent should say it doesn't know, not make up an answer
4. **Out-of-domain question** — Agent should decline and redirect
5. **Question with outdated information in knowledge base** — Agent should search for latest and note any discrepancy
