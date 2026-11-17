# OnePress Deck — ClawHub Skill

A ClawHub/OpenClaw skill for building polished, data-rich slide decks. **It works out of the box** — install it and ask for a deck, no account required.

## Two modes

| Mode | Trigger | What happens |
|---|---|---|
| **Local** (default) | No config needed | Your agent builds a real self-contained HTML deck right now, using the bundled `LOCAL-RECIPE.md` — 16:9 slides, ECharts, keyboard/click navigation. Open the file in a browser and present. |
| **Connected** | `ONEPRESS_API_KEY` set | Delegates to [OnePress](https://www.getonepress.com)'s full pipeline: cited live research, generated images, official PDF / editable-PPTX export, narrated video. |

The local recipe is the distilled craft of OnePress's production slide pipeline — the parts that don't need our infrastructure. The full pipeline lives at getonepress.com.

## Install

```bash
clawhub install onepress-deck
```

Or clone this repo and drop the directory into your agent's skills folder.

## Usage

Just ask your agent:

> "I need a 10-slide competitive landscape deck on AI coding agents for a partner meeting Friday."

- **No key**: you get `competitive-landscape.html` in your working directory — a real deck, ready to present.
- **With a key**: the skill submits the task, polls until done, and reports the agent's answer + where the deck lives (open https://www.getonepress.com/app to preview, share, or export).

## Connect your account (optional, unlocks the full pipeline)

1. Sign in at https://www.getonepress.com → **Settings → Account → API keys** → create a key (shown once, `opk_…`).
2. Export it:

```bash
export ONEPRESS_API_KEY=opk_...
```

Or configure the MCP server:

```json
{
  "mcpServers": {
    "onepress": {
      "url": "https://www.getonepress.com/api/mcp",
      "headers": { "Authorization": "Bearer opk_..." }
    }
  }
}
```

## API surface used (connected mode)

| Call | Purpose |
|---|---|
| `POST /api/v1/conversations` | create task (returns `conversationId`) |
| `GET /api/v1/conversations/:id` | poll status → `running`/`done` + `answer` + `preview_path` |
| `POST /api/v1/conversations/:id` | follow-up in the same conversation |
| `GET /api/v1/conversations?limit=` | list recent tasks |

MCP equivalents: `onepress_create_task`, `onepress_task_status`, `onepress_list_tasks`.

## Roadmap

- **v3.0.0** — local mode: builds a real deck with the bundled recipe, no account needed
- **v2.0.0** — connected mode: direct API/MCP submission + polling
- **v1.0.0** — handoff flow
- **Future** — file download over API once OnePress exposes workspace file endpoints

Issues and feedback welcome — they directly shape the next API surface.
