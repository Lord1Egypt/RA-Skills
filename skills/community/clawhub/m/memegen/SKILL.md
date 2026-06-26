---
name: memegen
description: >
  Generate meme images using the memegen.link API. Use when the user asks to create,
  make, send, or generate a meme, funny image, reaction image, or similar request.
  Produces meme images via URL — no local image generation needed. Supports 100+ classic
  meme templates (Drake, Doge, Disaster Girl, Expanding Brain, etc.) and custom backgrounds.
---

# Memegen Skill

Generate memes via the memegen.link public API + Imgflip trending templates. No API key required.

## Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────┐
│  Template Source │────▶│  Caption Engine   │────▶│  Renderer   │
│                  │     │                  │     │             │
│ • Built-in IDs   │     │ • Manual text    │     │ • memegen   │
│ • Imgflip API    │     │ • Agent-picked   │     │   .link     │
│ • Custom URL     │     │                  │     │ • Pillow    │
│ • Top 30 fallback│     │                  │     │   (local)   │
└─────────────────┘     └──────────────────┘     └─────────────┘
```

## How It Works

Memes are generated entirely via URL — no POST requests needed. Build the URL and download the image.

### URL Format

```
https://api.memegen.link/images/{template}/{top_text}/{bottom_text}.png
```

### Downloading Memes

memegen.link returns HTTP 404 status but valid image body — many HTTP clients reject 404 URLs.

**Always download first, then verify:**

```bash
curl -s -o /tmp/meme.png "https://api.memegen.link/images/drake/top/bottom.png"
file /tmp/meme.png       # Should say "PNG image data"
ls -la /tmp/meme.png     # Should be >10KB for a real meme
```

If the file is empty or <1KB, the template ID is probably wrong.

### URL Encoding Rules

| Character | Encoding | Example |
|-----------|----------|---------|
| Space     | `_`      | `hello_world` |
| `?`       | `~q`     | `why~q` |
| `/`       | `~s`     | `yes~sno` |
| `#`       | `~h`     | `tag~h1` |
| `%`       | `~p`     | `100~p` |
| `"`       | `''`     | `he_said_''hi''` |
| `_` (literal) | `__` | `double__underscore` |
| Newline   | `~n`     | `line1~nline2` |
| Blank line | `_`     | Top only: `/top_text/_` |

### Query Parameters

| Param | Type | Description |
|-------|------|-------------|
| `background` | URL | Custom background image URL |
| `width` | int | Scale to width (px), use `800` for larger |
| `height` | int | Scale to height (px) |
| `font` | string | Font name (see `/api/fonts`) |
| `layout` | string | `default` or `top` (text positioning) |
| `color` | string | Text color: HTML name or hex (`FF80ED`) |

## 🎯 VARIETY RULE — Keep It Fresh

**Prefer variety over repetition.** Before picking a template:
1. Check what templates you've used recently (keep a history if possible)
2. Try to pick a different template from the last 5 memes
3. BUT — if a specific template is clearly the best fit for the joke, use it even if recent
4. After generating, log the template used for future reference

## Humor Configuration

This skill includes a **humor profile system** — an equalizer for meme tone, darkness, and cultural targeting. See [`humor-profiles.md`](humor-profiles.md) for the full reference.

### Default Profile

| Slider | Default | Range |
|--------|---------|-------|
| **Darkness** | Level 2 (Light) | 1: Clean → 5: Nuclear ☢️ |
| **Dank Meter** | Normie-Dank | Normie → Dank → Deep Fried → Surreal → Shitpost |
| **Style** | Contextual (auto-detect) | Sarcasm · Absurdist · Self-deprecating · Deadpan · Wholesome · Roast · Meta · Shitpost |
| **Geo** | Neutral | 🇲🇽 MX · 🇦🇷 AR · 🇪🇸 ES · 🇺🇸 US · 🇧🇷 BR · 🇨🇴 CO · 🌎 LATAM |

### How the Same Topic Hits Different

**Topic: "My code has bugs"**

**Level 1 + Wholesome + Normie:**
```
Template: success | "Found a bug / Fixed it on first try"
```

**Level 2 + Sarcasm + Dank:**
```
Template: fry | "Not sure if my code works / Or the tests are just broken too"
```

**Level 3 + Sarcasm + Dank:**
```
Template: fine | "Production is on fire / This is fine, it's a feature"
```

**Level 4 + Deadpan + Dank (🇲🇽):**
```
Template: harold | "Cuando dices 'ya casi queda' y llevas 3 horas / Pero sonríes porque el deploy es mañana"
```

**Level 5 + Shitpost + Deep Fried:**
```
Template: custom deep-fried | "BRUH THE CODE 💀💀💀 / IT COMPILES THO 😤🔥💯"
```

### Usage in Prompts

```
Generate a meme about [topic].
Humor profile: Level 3, Dank, Sarcasm, 🇲🇽
```

Or let the agent auto-detect from context (language used, group chat culture, conversation tone).

### Deep Fry Post-Processing

For Level 5 / Deep Fried memes, use the included script:

```bash
python3 scripts/deep-fry.py meme.png fried.png --level 4 --emojis --flare
```

Requires: `pip install pillow`

---

## Template Selection Guide

> **For ALL 207 templates with rhetorical patterns and examples, see [references/templates-complete.md](references/templates-complete.md)**
> **For a quick-reference index, see [references/template-index.md](references/template-index.md)**

Pick templates by **rhetorical pattern** first, then tone. Each entry includes:
- **Formula**: the semantic structure of the joke
- **Tone**: sarcastic, wholesome, self-deprecating, absurd, smug, panicked, etc.
- **Structure**: what goes in each panel/line
- **Best for**: situations where this template shines
- **Text length**: short (1-5 words), medium (5-15), long (15-30) per panel

---

### Binary Comparison (reject X / prefer Y)

**`drake`** — Drakeposting
- **Formula**: rejection of X / preference for Y
- **Tone**: casual, lighthearted, smug
- **Structure**: top=bad option (rejected), bottom=good option (approved)
- **Best for**: lazy shortcuts over proper solutions, guilty pleasures, obvious better choices
- **Text length**: medium / medium

**`pooh`** — Tuxedo Winnie the Pooh
- **Formula**: basic version of X / refined version of X
- **Tone**: smug, pretentious, self-aware
- **Structure**: top=normal/basic way, bottom=fancy/elevated way
- **Best for**: classy upgrades, pretending to be sophisticated, "we say it differently here"
- **Text length**: medium / medium

**`db`** — Distracted Boyfriend
- **Formula**: attracted to Z / neglecting Y / Z is the shiny new thing
- **Tone**: sarcastic, self-deprecating, relatable
- **Structure**: 3 lines — boyfriend=who's distracted, girlfriend=what's neglected, other=the temptation
- **Best for**: abandoning responsibilities for fun, shiny object syndrome, love triangles
- **Text length**: short / short / short

**`glasses`** — Peter Parker's Glasses
- **Formula**: blurry perception of X / clear perception of X
- **Tone**: revelatory, deadpan
- **Structure**: top=what it looks like at first, bottom=what it actually is
- **Best for**: seeing through BS, clarity moments, "oh that's what it really is"
- **Text length**: medium / medium

**`astronaut`** — Always Has Been
- **Formula**: discovery of X / it was always X
- **Tone**: ominous, deadpan, absurd
- **Structure**: 4 lines — astronaut1 sees something, asks question, astronaut2 reveals truth, "always has been"
- **Best for**: revelations that something was always true, conspiracies, hidden truths
- **Text length**: short / medium / short / short
- ⚠️ Built-in may be broken — use Imgflip URL with `custom` template as fallback

---

### Skepticism / Confusion

**`fry`** — Futurama Fry (Squinting)
- **Formula**: not sure if X or Y
- **Tone**: suspicious, paranoid, relatable
- **Structure**: top=not sure if X, bottom=or just Y
- **Best for**: ambiguous situations, "is this a compliment or insult", reading between the lines
- **Text length**: medium / medium

**`morpheus`** — Matrix Morpheus
- **Formula**: what if I told you X
- **Tone**: wise, smug, enlightening
- **Structure**: top=what if I told you, bottom=the revelation
- **Best for**: mind-blowing facts, uncomfortable truths, paradigm shifts
- **Text length**: short / long

**`philosoraptor`** — Philosoraptor
- **Formula**: if X then wouldn't Y
- **Tone**: absurd, pseudo-intellectual, shower-thought
- **Structure**: top=philosophical setup, bottom=absurd conclusion
- **Best for**: shower thoughts, wordplay, "technically correct" logic, paradoxes
- **Text length**: medium / medium

**`keanu`** — Conspiracy Keanu
- **Formula**: what if X is actually Y
- **Tone**: paranoid, conspiratorial, wide-eyed
- **Structure**: top=what if, bottom=wild conspiracy theory
- **Best for**: absurd theories, connecting unrelated dots, "everything is connected"
- **Text length**: short / long

---

### Clever Realization / Big Brain

**`rollsafe`** — Roll Safe (Thinking)
- **Formula**: can't have problem X if you do Y (terrible logic)
- **Tone**: smug, self-satisfied, terrible-advice
- **Structure**: top=can't X, bottom=if you Y (the "clever" workaround)
- **Best for**: life hacks that are actually terrible, loophole logic, galaxy-brain shortcuts
- **Text length**: medium / medium

**`gb`** — Galaxy Brain (Expanding Brain)
- **Formula**: level 1 normal → level 4 absurd/genius
- **Tone**: absurd, escalating, ironic
- **Structure**: 4 panels — each progressively more extreme/ridiculous take on same topic
- **Best for**: escalating absurdity, "big brain" solutions, tier lists of approaches
- **Text length**: medium / medium / medium / medium

**`scc`** — Sudden Clarity Clarence
- **Formula**: sudden realization that X
- **Tone**: shocked, enlightened, mind-blown
- **Structure**: top=setup, bottom=the realization
- **Best for**: epiphanies, "wait a minute" moments, obvious things nobody noticed
- **Text length**: medium / medium

---

### Sarcasm / Mockery

**`spongebob`** — Mocking SpongeBob
- **Formula**: mocking repetition of X
- **Tone**: sarcastic, mocking, petty
- **Structure**: top=the original statement, bottom=tHe MoCkInG vErSiOn
- **Best for**: mocking dumb takes, repeating someone's words back at them, "sure buddy"
- **Text length**: medium / medium (use alternating caps in bottom)

**`wonka`** — Condescending Wonka
- **Formula**: oh you X? you must be Y
- **Tone**: condescending, sarcastic, smug
- **Structure**: top=oh you [claim], bottom=you must [sarcastic conclusion]
- **Best for**: calling out fakes, "oh you're an expert now?", gatekeeping humor
- **Text length**: medium / medium

**`kermit`** — But That's None of My Business
- **Formula**: [controversial observation] but that's none of my business
- **Tone**: passive-aggressive, smug, "just saying"
- **Structure**: top=shady observation, bottom=but that's none of my business
- **Best for**: throwing shade, gossip, pointed observations you "didn't mean to make"
- **Text length**: long / short

**`khaby-lame`** — Khaby Lame Shrug
- **Formula**: the obvious solution was right there
- **Tone**: deadpan, "are you serious", exasperated
- **Structure**: top=the overcomplicated thing someone did, bottom=the obvious solution
- **Best for**: overengineering, when the answer was obvious, "just do X"
- **Text length**: medium / short

---

### Panic / Disaster / Pain

**`fine`** — This is Fine (Dog in Fire)
- **Formula**: everything is on fire / pretending it's okay
- **Tone**: denial, panicked-calm, self-deprecating
- **Structure**: top=the disaster happening, bottom=this is fine (or calm response)
- **Best for**: ignoring problems, deadlines, production outages, Monday mornings
- **Text length**: medium / short

**`harold`** — Hide the Pain Harold
- **Formula**: pain hidden behind a smile
- **Tone**: self-deprecating, pained, relatable
- **Structure**: top=the painful situation, bottom=the forced smile response
- **Best for**: putting on a brave face, "I'm fine" moments, internal screaming
- **Text length**: medium / medium

**`slap`** — Will Smith Slapping Chris Rock
- **Formula**: X attacks Y for Z
- **Tone**: aggressive, dramatic, sudden
- **Structure**: top=the trigger/joke, bottom=the violent response
- **Best for**: overreactions, defending something aggressively, sudden consequences
- **Text length**: medium / medium

**`gru`** — Gru's Plan
- **Formula**: plan → plan → consequence → wait what
- **Tone**: dramatic irony, panicked, backfire
- **Structure**: 4 panels — step 1, step 2, unexpected consequence, horrified reaction to step 3
- **Best for**: plans that backfire, unintended consequences, "I didn't think this through"
- **Text length**: medium / medium / medium / medium (panel 4 repeats panel 3)

**`chair`** — American Chopper Argument
- **Formula**: escalating argument between two people
- **Tone**: heated, dramatic, aggressive
- **Structure**: up to 6 panels — alternating arguments, escalating intensity
- **Best for**: heated debates, internal conflicts, "the duality of man", pros vs cons arguments
- **Text length**: medium per panel (up to 6 panels!)

---

### Wholesome / Positive

**`success`** — Success Kid
- **Formula**: attempted X / nailed it
- **Tone**: triumphant, wholesome, fist-pump
- **Structure**: top=the challenge or attempt, bottom=the win
- **Best for**: small victories, passing tests, things going right for once
- **Text length**: medium / short

**`stonks`** — Stonks (Meme Man)
- **Formula**: did X / stonks (profit/success)
- **Tone**: absurd, ironic-positive, surreal
- **Structure**: top=the questionable action, bottom=stonks (or "not stonks" for failures)
- **Best for**: questionable financial decisions, "business" moves, ironic success
- **Text length**: medium / short

**`handshake`** — Epic Handshake
- **Formula**: X and Y agree on Z
- **Tone**: wholesome, unifying, respectful
- **Structure**: 3 lines — left arm label, right arm label, handshake label (the shared thing)
- **Best for**: unlikely agreements, common ground between enemies, "we're not so different"
- **Text length**: short / short / medium

---

### Comparison / Identity

**`same`** — They're The Same Picture (Corporate)
- **Formula**: X and Y are identical / I see no difference
- **Tone**: deadpan, sarcastic, pointed
- **Structure**: top=thing 1, bottom=thing 2 (implying they're the same)
- **Best for**: calling out copycats, "these are literally the same thing", false distinctions
- **Text length**: short / short

**`pigeon`** — Is This a Pigeon?
- **Formula**: person misidentifies X as Y
- **Tone**: confused, absurd, oblivious
- **Structure**: 3 lines — the person (who), the butterfly (what it actually is), "is this a [wrong label]?"
- **Best for**: misidentifying things, clueless takes, "boomers calling everything WiFi"
- **Text length**: short / short / short

**`spiderman`** — Spider-Man Pointing
- **Formula**: X and Y are the same thing pointing at each other
- **Tone**: absurd, meta, accusatory
- **Structure**: top=first thing, bottom=second thing (both identical)
- **Best for**: two things that are secretly the same, hypocrisy, "you're one to talk"
- **Text length**: short / short

**`woman-cat`** — Woman Yelling at Cat
- **Formula**: angry accusation vs calm unbothered response
- **Tone**: chaotic, confrontational, deadpan
- **Structure**: top=the angry accusation (woman), bottom=the calm response (cat)
- **Best for**: arguments where one side is dramatic and the other is chill, overreaction vs facts
- **Text length**: long / short

---

### Reaction / Mood

**`kombucha`** — Kombucha Girl
- **Formula**: tries X / actually it's not bad
- **Tone**: surprised, conflicted, "huh okay"
- **Structure**: top=the thing you reluctantly tried, bottom=the unexpected reaction
- **Best for**: guilty pleasures, changing your mind, "okay this actually slaps"
- **Text length**: medium / short

**`right`** — Anakin Padmé ("Right?")
- **Formula**: states plan / partner assumes good intent / "right?" / silence
- **Tone**: dramatic irony, ominous, escalating dread
- **Structure**: 5 lines — Anakin states X, Padmé assumes benign reason, "right?", Anakin silent stare, "RIGHT?"
- **Best for**: someone revealing bad intentions, "wait you're joking right?", red flags
- **Text length**: medium / short / short / (blank) / short

**`cmm`** — Change My Mind
- **Formula**: hot take stated as fact, daring anyone to argue
- **Tone**: provocative, confident, debate-me
- **Structure**: 1 line only — the controversial opinion on the sign
- **Best for**: hot takes, unpopular opinions, starting arguments, confident declarations
- **Text length**: medium (single line, keep it punchy)

**`reveal`** — Scooby Doo Reveal (Unmasking)
- **Formula**: X was actually Y all along
- **Tone**: revelatory, dramatic, "I knew it"
- **Structure**: 4 lines — the villain, the mask being pulled, the reveal, reaction
- **Best for**: exposing the truth, "it was X all along", corporate rebranding, hidden motives
- **Text length**: short / short / short / short

---

## Rhetorical Pattern Quick Reference

Use this to identify the right template category before browsing individual templates:

| Pattern | Templates | When to Use |
|---------|-----------|-------------|
| **Binary comparison** (A vs B) | Drake, Pooh, Distracted Boyfriend | Rejecting one thing for another |
| **Escalation** (progressively more extreme) | Galaxy Brain, Expanding Brain | Ideas getting increasingly absurd |
| **Dramatic irony** (plan backfires) | Gru's Plan, Anakin/Padme ("Right?") | Confident plan with obvious flaw |
| **Denial / cope** | This Is Fine, Harold | Pretending everything's okay |
| **Obvious solution ignored** | Khaby Lame, Roll Safe | The answer was simple all along |
| **Mockery / sarcasm** | Spongebob, Wonka, Kermit | Making fun of a take |
| **Identity confusion** | Spider-Man Pointing, Same Picture, Pigeon | Things that are the same or misidentified |
| **Revelation / unmasking** | Scooby Doo Reveal, Peter Parker Glasses | Discovering the truth behind something |
| **Hot take / provocation** | Change My Mind | Stating a controversial opinion |
| **Shared agreement** | Epic Handshake | Two sides finding common ground |
| **Escalating argument** | American Chopper | Multi-party conflict |

## Trending Templates via Imgflip

When you want the freshest templates (not just built-in IDs):

```bash
curl -s "https://api.imgflip.com/get_memes" | python3 -c "
import sys, json
memes = json.load(sys.stdin)['data']['memes'][:20]
for m in memes:
    print(f\"{m['name']}: {m['url']}\")
"
```

Use with custom background:
```
https://api.memegen.link/images/custom/{top}/{bottom}.png?background={imgflip_url}&width=800
```

### Custom Background URL Encoding

```python
from urllib.parse import quote
bg = quote("https://i.imgflip.com/30b1gx.jpg", safe=":/")
url = f"https://api.memegen.link/images/custom/top/bottom.png?background={bg}&width=800"
```

For hardcoded fallback templates (when Imgflip is unreachable), see `references/templates-classic.md`.

For trending template sources (Reddit, Imgflip scraping, Giphy), see `references/templates-trending.md`.

## Local Render with Pillow (fallback, no network)

When memegen.link is down or you need full control:

```python
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import textwrap, requests

def render_meme(image_url, top, bottom="", output="/tmp/meme.png"):
    img = Image.open(BytesIO(requests.get(image_url).content)).convert("RGB")
    draw = ImageDraw.Draw(img)
    w, h = img.size
    font_size = max(w // 12, 20)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/msttcorefonts/Impact.ttf", font_size)
    except OSError:
        font = ImageFont.load_default()

    def draw_block(text, anchor="top"):
        if not text: return
        text = text.upper()
        lines = textwrap.wrap(text, width=max(int((w * 0.9) / (font_size * 0.6)), 10))
        line_h = [draw.textbbox((0,0), l, font=font)[3] - draw.textbbox((0,0), l, font=font)[1] for l in lines]
        total = sum(line_h) + (len(lines)-1) * 4
        y = 10 if anchor == "top" else h - total - 20
        for i, line in enumerate(lines):
            lw = draw.textbbox((0,0), line, font=font)[2]
            draw.text(((w-lw)/2, y), line, font=font, fill="white",
                      stroke_width=3, stroke_fill="black")
            y += line_h[i] + 4

    draw_block(top, "top")
    draw_block(bottom, "bottom")
    img.save(output, quality=95)
    return output
```

Requires: `pip install pillow requests` and optionally `sudo apt install ttf-mscorefonts-installer` for Impact font.

## ⚠️ Known Issues & Lessons

### Template names matter — use exact IDs
Common mistakes:
- ❌ `buzz-woody` → does not exist, grey placeholder
- ✅ `buzz` → "X, X Everywhere"
- ❌ `disaster-girl` → wrong
- ✅ `ds` → Disaster Girl
- ❌ `change-my-mind` → wrong
- ✅ `cmm` → Change My Mind

When unsure, fetch `https://api.memegen.link/templates/{id}` to verify.

### Broken/unreliable built-in templates
These render text-only on grey striped background (no image):
- ❌ `simply` — "One Does Not Simply" — background doesn't load
- ❌ `always` — "Always Has Been" — background doesn't load
- ❌ `panik` — "Panik Kalm Panik" — 3-panel doesn't render

**Workaround:** Use the Imgflip URL from the fallback list with `custom` template instead.

### Don't use formatting tags in meme text
- ❌ `~i~text~i~` — renders literally
- ✅ Just use plain text — memes don't need italics
- Only reliable special chars: `~n` (newline), `~q` (?), `~a` (&), `~h` (#), `~s` (/)

### Text encoding
- Accented characters (é, ñ, ó) work fine in URLs
- Keep text SHORT — max ~30 chars per line looks best
- Emojis don't render in memegen.link

## Tips

- Keep text short — long text gets tiny
- Use `?width=800` for larger images
- For custom backgrounds: `custom` template + `?background=<url>`
- For broken built-in templates, use Imgflip URL + `custom` as workaround
- `time.sleep(0.5)` between batch requests — be polite to memegen.link

For the full template list and special characters reference, see `references/api.md`.
