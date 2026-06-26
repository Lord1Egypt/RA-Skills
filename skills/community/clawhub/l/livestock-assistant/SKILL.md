---
name: openclaw-livestock-assistant
description: >
  AI-powered livestock management assistant for Spanish-speaking farmers.
  Provides expert advice on herd management, animal health, reproduction,
  genetics, nutrition, and breed selection for bovine, ovine, caprine,
  porcine, equine, and poultry. Includes a Node.js REST API for persistent
  herd record-keeping (animal registration, health records, reproduction
  events). Use when the user asks about livestock, cattle, ganadería, herd
  management, animal health, veterinary advice, breeds, reproduction,
  nutrition, forage, or any livestock-related topic.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - OPENAI_API_KEY
        - ANTHROPIC_API_KEY
        - GOOGLE_GENERATIVE_AI_API_KEY
      bins:
        - node
    primaryEnv: OPENAI_API_KEY
    emoji: "🐄"
    homepage: https://github.com/antonygiomarxdev/openclaw-livestock-assistant
    install:
      - kind: node
        package: ts-node
        bins: [ts-node]
---

# OpenClaw Livestock Assistant

Expert livestock management assistant for Spanish-speaking farmers. Responds
**always in Spanish**. Combines AI chat with a REST API for herd record-keeping.

## Capabilities

- **Herd management** — register and track animals (bovine, ovine, caprine, porcine, equine, poultry)
- **Animal health** — vaccination schedules, disease identification, treatment guidance
- **Reproduction** — heat detection, pregnancy tracking, birth records, genetics
- **Nutrition** — ration formulation, forage selection, supplementation
- **Breed advice** — selection by aptitude (meat / milk / wool / dual-purpose)
- **REST API** — persistent record-keeping via Express server on `http://localhost:3000`

## Starting the API Server

Before using any REST API endpoint, start the server:

```bash
bash scripts/start.sh
```

The server exposes `/health`, `/api/animals`, and `/api/assistant` — see
[references/api.md](references/api.md) for the full endpoint reference.

## AI Provider Configuration

The assistant supports **OpenAI, Anthropic (Claude), and Google (Gemini)**.
Set **at least one** API key; the assistant auto-selects the provider.

| Provider | API key env var | Default model |
|---|---|---|
| OpenAI | `OPENAI_API_KEY` | `gpt-5` |
| Anthropic | `ANTHROPIC_API_KEY` | `claude-opus-4-6` |
| Google | `GOOGLE_GENERATIVE_AI_API_KEY` | `gemini-2.5-pro` |

Override explicitly via:
- `AI_PROVIDER=openai|anthropic|google` — force a specific provider
- `AI_MODEL=<model-id>` — override the model ID for the chosen provider

## AI Chat

Every interaction should be in Spanish. Use the system prompt embedded in
`src/assistant/systemPrompt.ts` as the agent's knowledge baseline.

Create a session before sending messages:

```bash
curl -X POST http://localhost:3000/api/assistant/sessions
# → { "sessionId": "...", "welcome": "¡Hola! Soy el Asistente de Ganadería..." }

curl -X POST http://localhost:3000/api/assistant/sessions/<sessionId>/messages \
  -H "Content-Type: application/json" \
  -d '{"message": "¿Cómo prevenir la mastitis en vacas lecheras?"}'
```

## Domain References

Load these files when you need detailed reference data:

| Reference | When to read |
|---|---|
| [references/breeds.md](references/breeds.md) | User asks about breeds, selection, or characteristics |
| [references/diseases.md](references/diseases.md) | User reports symptoms, asks about prevention or treatment |
| [references/nutrition.md](references/nutrition.md) | User asks about feeding, rations, forages, or supplementation |
| [references/api.md](references/api.md) | User wants to register animals or retrieve herd data |

## Animal Status Reference

| Field | Allowed values |
|---|---|
| `species` | `bovine` `ovine` `caprine` `porcine` `equine` `poultry` |
| `sex` | `male` `female` |
| `status` | `active` `sold` `dead` `quarantine` |
| `healthStatus` | `healthy` `sick` `in_treatment` `recovered` |
| `reproductiveStatus` | `open` `pregnant` `lactating` `in_heat` `served` `not_applicable` |

## Safety Guidelines

- Never diagnose diseases definitively — always recommend a veterinarian for emergencies.
- Zoonotic diseases (e.g., Brucelosis) must be flagged immediately.
- Urgency levels: `low` → `medium` → `high` → `emergency`. Escalate accordingly.
