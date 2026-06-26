# Personalities (Soul System)

Kiwi supports dynamic personality switching through markdown-based "souls" — each soul defines a system prompt overlay that shapes how Kiwi responds.

## Built-in Souls

| Soul | Style | NSFW |
|------|-------|------|
| **Mindful Companion** | Calm, supportive, thoughtful | No |
| **Storyteller** | Narrative, descriptive, immersive | No |
| **Comedian** | Witty, sarcastic, humorous | No |
| **Hype Person** | Energetic, motivational, enthusiastic | No |
| **Siren** | Flirty, provocative | Yes (18+) |

## How it Works

Souls are markdown files in `kiwi/souls/`. The `SoulManager` loads them at startup and composes the final system prompt:

```
Base system prompt (SOUL.md) + Soul personality overlay = Final prompt
```

The base prompt defines Kiwi's core identity and capabilities. The soul overlay adds personality traits on top.

## Switching Souls

### By Voice

> **"Kiwi, be a comedian"**
> **"Kiwi, switch to storyteller"**
> **"Kiwi, default mode"** (resets to Mindful Companion)

### Via Dashboard

Click any personality card in the dashboard carousel to activate it.

### Via REST API

```bash
curl -X POST http://localhost:7789/api/soul \
  -H "Content-Type: application/json" \
  -d '{"soul": "comedian"}'
```

### Query Current Soul

```bash
curl http://localhost:7789/api/soul/current
```

## NSFW Routing

The Siren soul (and any custom NSFW soul) is **fully isolated**:

- Routes to a **separate OpenClaw agent** with its own LLM model and session
- The session is switched via `openclaw_ws.switch_session()`
- When switching back to a non-NSFW soul, the previous session is restored

Configure the NSFW backend:

```yaml
souls:
  default: "mindful-companion"
  nsfw:
    model: "openrouter/mistralai/mistral-7b-instruct"
    session: "kiwi-nsfw"
```

## Creating Custom Souls

1. Create a markdown file in `kiwi/souls/`:

    ```markdown
    ---
    name: Philosopher
    description: Deep thinker who ponders existence
    model: ~
    nsfw: false
    ---

    ## Identity

    You are a contemplative philosopher. You speak in measured, thoughtful sentences.
    You reference ancient wisdom and draw connections to modern life.

    ## Style

    - Speak slowly and deliberately
    - Ask thought-provoking questions
    - Reference philosophy and literature
    ```

2. Restart Kiwi — the new soul appears in the dashboard and is available via voice/API.

The `model` field is informational. Set `nsfw: true` to route through the isolated NSFW session.
