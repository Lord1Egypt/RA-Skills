# Groq Bot Skill

## Purpose
Fast, low-latency text generation using Groq's **free-tier models** for quick summaries, reasoning, trading analysis, and tool-assisted responses.

## Free Tier Models (alle getestet ✅)
| Model | Größe | Nutzung |
|-------|-------|---------|
| `llama-3.1-8b-instant` | 8B | Schnelle Antworten, Zusammenfassungen |
| `llama-3.3-70b-versatile` | 70B | Komplexe Analysen, Trading-Entscheidungen |
| `qwen/qwen3-32b` | 32B | Allrounder, gutes Preis-Leistungs-Verhältnis |
| `meta-llama/llama-4-scout-17b-16e-instruct` | 17B | **Primär** — schnell + intelligent |
| `openai/gpt-oss-20b` | 20B | Open-Source GPT Alternative |
| `openai/gpt-oss-120b` | 120B | Maximale Qualität für komplexe Aufgaben |

## Primäre Model-Reihenfolge (Free Tier)
1. `meta-llama/llama-4-scout-17b-16e-instant` — Standard (schnell + gut)
2. `llama-3.1-8b-instant` — Für schnelle Antworten
3. `llama-3.3-70b-versatile` — Für komplexe Analysen
4. `qwen/qwen3-32b` — Wenn die anderen rate-limited sind
5. `openai/gpt-oss-120b` — Maximale Qualität (langsamer)
6. `openai/gpt-oss-20b` — GPT Alternative

## Configuration
- Provider: groq
- API key: aus .env (GROQ_API_KEY)
- Rate Limit: ~100 requests/min (Free Tier)
- Alle Models sind **kostenlos**

## Usage
- Via `sessions_send` oder `sessions_spawn`
- Model override möglich
- Automatisches Fallback wenn Rate-Limit erreicht

## Safety
- Rate limit aware: <100 requests/min empfohlen
- API key nie in Logs oder Output exposen
- Bei Rate Limit: automatisch auf nächstes Model fallback
- Keine destruktiven Aktionen ohne Bestätigung

## Integration
- Agent ID: groq-bot
- Env File: groq-bot/.env (GROQ_API_KEY)
- Fallback Model: llama-3.1-8b-instant (schnellste Option)
