# 🎭 Memegen Skill

**Framework-agnostic meme generation knowledge for AI agents.**

Give your AI agent the ability to create memes. This isn't a library or API wrapper — it's a structured knowledge file that teaches any LLM how to pick the right meme template, format the text, and generate the image via the free [memegen.link](https://api.memegen.link) API.

## Why?

LLMs are bad at memes out of the box. They don't know which template fits which joke structure, they mess up the text encoding, and they pick Drake for everything.

This skill solves that by providing:
- **Rhetorical pattern taxonomy** — match joke structure to template (the most valuable part)
- **35+ template profiles** with formulas, tone tags, and anti-patterns
- **URL encoding rules** for memegen.link's special character system
- **30 hardcoded fallback templates** with stable image URLs
- **Trending template sources** (Imgflip, Reddit, Giphy)
- **Known issues** and workarounds for broken templates
- **Pillow renderer** for offline generation

## Quick Start

### Option 1: Include in your system prompt (any LLM)

```python
with open("SKILL.md") as f:
    system_prompt = f"You can generate memes.\n\n{f.read()}"
```

That's it. The LLM reads the template guide and picks the right meme.

### Option 2: Generate a meme URL directly

```bash
# Drake meme
curl -s -o meme.png "https://api.memegen.link/images/drake/Writing_docs/Writing_memes.png?width=800"

# Custom background from Imgflip
curl -s -o meme.png "https://api.memegen.link/images/custom/Top/Bottom.png?background=https%3A//i.imgflip.com/30b1gx.jpg&width=800"
```

## Template Preview

| Template | ID | Pattern | Best For |
|----------|----|---------|----------|
| 🔄 Drake | `drake` | Reject A / Prefer B | Guilty pleasures, obvious choices |
| 🔥 This is Fine | `fine` | Denial / Cope | Production outages, Monday mornings |
| 🧠 Galaxy Brain | `gb` | Escalation (4 levels) | Increasingly absurd takes |
| 📋 Gru's Plan | `gru` | Plan backfires (4 panels) | Unintended consequences |
| 🤝 Epic Handshake | `handshake` | A and B agree on C | Unlikely common ground |
| 😏 Tuxedo Pooh | `pooh` | Basic vs Refined | "We say it differently here" |
| 🐻 Mocking SpongeBob | `spongebob` | Mocking repetition | Sarcasm, "sure buddy" |
| 😐 Hide the Pain Harold | `harold` | Pain behind a smile | "I'm fine" moments |
| ☕ Change My Mind | `cmm` | Hot take (1 line) | Controversial opinions |
| 🕵️ Scooby Doo Reveal | `reveal` | X was Y all along | Unmasking hidden truths |

See [SKILL.md](SKILL.md) for the full 35+ template catalog with rhetorical formulas.

## Rhetorical Patterns

The key insight: **pick templates by joke structure, not by keyword.**

| Pattern | Templates | When to Use |
|---------|-----------|-------------|
| Binary comparison | Drake, Pooh, Distracted Boyfriend | Rejecting one thing for another |
| Escalation | Galaxy Brain | Ideas getting increasingly absurd |
| Dramatic irony | Gru's Plan, Anakin/Padmé | Confident plan with obvious flaw |
| Denial / cope | This Is Fine, Harold | Pretending everything's okay |
| Obvious solution | Khaby Lame, Roll Safe | The answer was simple all along |
| Mockery | SpongeBob, Wonka, Kermit | Making fun of a take |
| Identity confusion | Spider-Man Pointing, Pigeon | Things that are the same |
| Revelation | Scooby Doo, Peter Parker Glasses | Discovering hidden truth |
| Hot take | Change My Mind | Controversial opinion |
| Agreement | Epic Handshake | Common ground |

## 🎛️ Humor Profiles

Not all memes hit the same. The **humor profile system** is an equalizer — adjust darkness, dankness, humor style, and regional flavor to produce memes that match your audience.

### The Equalizer

| Slider | Options | Default |
|--------|---------|--------|
| 🌡️ **Darkness** | 1: Clean → 5: Nuclear ☢️ | Level 2 (Light) |
| 📊 **Dank Meter** | Normie → Dank → Deep Fried → Surreal → Shitpost | Normie-Dank |
| 🎨 **Style** | Sarcasm · Absurdist · Self-deprecating · Deadpan · Wholesome · Roast · Meta · Shitpost | Contextual |
| 🌎 **Geo** | 🇲🇽 MX · 🇦🇷 AR · 🇪🇸 ES · 🇺🇸 US · 🇧🇷 BR · 🇨🇴 CO · 🌎 LATAM | Neutral |

### Darkness Levels at a Glance

| Level | Name | Vibe | Example |
|-------|------|------|---------|
| 1 | ☀️ Clean | Grandma-approved | Success Kid: "Finished my homework / Before midnight" |
| 2 | 🌤️ Light | Water cooler | Drake: "Writing docs" / "Writing memes" |
| 3 | 🌶️ Spicy | Close friends | This is Fine: "Production down" / "This is fine" |
| 4 | 🌑 Dark | That one group chat | Harold hiding pain about real problems |
| 5 | ☢️ Nuclear | Opt-in only | Deep fried, distorted, 💀💀💀 |

### Deep Fry Script

For Level 5 / Deep Fried memes, use the included image processor:

```bash
python3 scripts/deep-fry.py input.png output.png --level 4 --emojis --flare
```

📖 **Full reference:** [humor-profiles.md](humor-profiles.md) — includes regional humor guides for 🇲🇽🇦🇷🇪🇸🇺🇸🇧🇷🇨🇴, Pillow code snippets for visual effects, style definitions with template affinities, and combination examples.

## Getting Trending Templates

### Imgflip API (free, no auth)

```bash
curl -s "https://api.imgflip.com/get_memes" | python3 -c "
import sys, json
for m in json.load(sys.stdin)['data']['memes'][:10]:
    print(f\"{m['name']}: {m['url']}\")
"
```

### Imgflip Scraper (trending/new)

```bash
python3 scripts/imgflip-trending.py --limit 20
```

### Reddit OAuth (genuinely trending)

```bash
# Requires setup — see references/templates-trending.md
./scripts/reddit-trending.sh 20
```

## Project Structure

```
├── SKILL.md                     # Core knowledge file (include this in your agent)
├── humor-profiles.md            # 🎛️ Humor equalizer — darkness, dankness, style, geo
├── references/
│   ├── api.md                   # memegen.link API reference
│   ├── templates-classic.md     # 30 hardcoded fallback templates with URLs
│   ├── templates-trending.md    # How to fetch trending templates
│   └── research-improvements.md # Future improvement research
├── scripts/
│   ├── deep-fry.py              # 🔥 Deep fry image post-processor (Pillow)
│   ├── imgflip-trending.py      # Scrape Imgflip trending templates
│   ├── reddit-trending.sh       # Fetch from r/MemeTemplates (OAuth)
│   └── giphy-search.sh          # Search Giphy for reaction GIFs
└── integrations/
    ├── openclaw.md              # OpenClaw integration guide
    ├── langchain.md             # LangChain tool wrapper
    └── generic.md               # Any LLM / agent framework
```

## Integration Examples

### OpenClaw

```bash
# Clone into your skills directory
cd ~/.openclaw/workspace/skills/
git clone https://github.com/ArtemioPadilla/memegen-skill memegen
```

OpenClaw auto-discovers the skill via the YAML frontmatter in SKILL.md. See [integrations/openclaw.md](integrations/openclaw.md).

### LangChain

```python
from langchain.tools import Tool

meme_tool = Tool(
    name="meme_generator",
    description="Generate a meme. Input: 'template|top_text|bottom_text'",
    func=generate_meme,  # See integrations/langchain.md for full implementation
)
```

### OpenAI / Claude Function Calling

```python
tools = [{
    "type": "function",
    "function": {
        "name": "generate_meme",
        "description": "Generate a meme image from a template",
        "parameters": {
            "type": "object",
            "properties": {
                "template": {"type": "string", "description": "Template ID"},
                "top_text": {"type": "string", "description": "Top panel text"},
                "bottom_text": {"type": "string", "description": "Bottom panel text"}
            },
            "required": ["template", "top_text"]
        }
    }
}]
```

See [integrations/generic.md](integrations/generic.md) for complete examples.

## No API Key Required

The core functionality uses [memegen.link](https://api.memegen.link) which is completely free and requires no authentication. Optional features (Reddit trending, Giphy GIFs) need their own free API keys.

## Contributing

Contributions welcome! Some ideas:
- Add more template profiles to `SKILL.md`
- Improve the rhetorical pattern taxonomy
- Add integration guides for other frameworks (CrewAI, AutoGen, etc.)
- Expand regional humor profiles in `humor-profiles.md` (PRs for your country welcome!)
- Add more trending template scrapers
- Improve the deep fry script with new effects

## License

MIT — see [LICENSE](LICENSE).

---

Built with 🦅 by [ArtemIO](https://github.com/ArtemioPadilla)
