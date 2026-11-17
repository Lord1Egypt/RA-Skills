# Meme Generator 🎨

> Create shareable SVG memes from text. Pure Python stdlib. Crisp at any resolution.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![No Dependencies](https://img.shields.io/badge/dependencies-zero-brightgreen.svg)

## Features

- ✅ **10 classic meme templates** — Drake, Distracted Boyfriend, Two Buttons, Change My Mind, Galaxy Brain, Stonks, This is Fine, Doge, Expanding Brain, Panik Kalm
- ✅ **Pure Python stdlib** — no pip install needed, no Pillow, no requests
- ✅ **SVG output** — crisp at any resolution, 3-5 KB per meme
- ✅ **Batch generation** — one quote → all templates instantly
- ✅ **Quote packs** — programming, startup, productivity, student life
- ✅ **Animated effects** — SVG-native animations
- ✅ **Custom templates** — use your own SVG with `{{TOP}}`/`{{BOTTOM}}` placeholders
- ✅ **Watermark-free**

## Quick Start

```bash
# Make a single meme
python scripts/meme_gen.py make 'Unit tests?' 'No tests.' --template drake --output meme.svg

# Batch: same text across ALL templates
python scripts/meme_gen.py batch 'Coffee is debug code' --all-templates --output-dir memes/

# Get random quotes
python scripts/meme_gen.py quote --category programming --count 5

# Pipe mode (stdin as top text)
echo 'When it works on production' | python scripts/meme_gen.py --template this_is_fine
```

## Templates

| Template | Key | Description |
|---|---|---|
| 🎤 Drake | `drake` | Reject / approve two-panel |
| 👀 Distracted Boyfriend | `distracted_boyfriend` | Three-character attention split |
| 🔘 Two Buttons | `two_buttons` | Impossible dilemma |
| 🪧 Change My Mind | `change_my_mind` | Guy at table with sign |
| 🧠 Galaxy Brain | `galaxy_brain` | Five ascending brain stages |
| 📈 Stonks | `stonks` | Suit guy + upward arrow |
| 🔥 This is Fine | `this_is_fine` | Dog in burning room |
| 🐕 Doge | `doge` | Shiba Inu + colorful text |
| ✨ Expanding Brain | `expanding_brain` | Four glowing brain levels |
| 😰 Panik Kalm | `panik_kalm` | Panic → calm → panic |

### Aliases

`cmm` → change_my_mind · `brain` → expanding_brain · `fine` → this_is_fine · `stocks` → stonks · `kalm`/`panik` → panik_kalm

## Quote Packs

```bash
python scripts/meme_gen.py quote --category programming --count 5 --generate --template drake
```

| Category | Count | Vibe |
|---|---|---|
| `programming` | 20 | Dev life struggles |
| `startup` | 15 | Hustle culture satire |
| `productivity` | 15 | Procrastination humor |
| `student` | 15 | Academic chaos |

## Output Formats

### SVG (default)
Standalone SVG file. Opens in any browser, scales infinitely.

```bash
python scripts/meme_gen.py make 'Top' 'Bottom' --template stonks --output meme.svg
```

### HTML (optional)
SVG wrapped in a styled HTML page for easy sharing/viewing.

```bash
python scripts/meme_gen.py make 'Top' 'Bottom' --template stonks --html
```

## Custom Templates

Create an SVG with `{{TOP}}` and `{{BOTTOM}}` placeholders:

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 800">
  <rect width="800" height="800" fill="#1a1a2a"/>
  {{TOP}}
  {{BOTTOM}}
</svg>
```

Then:

```bash
python scripts/meme_gen.py custom 'My text' 'Other text' --template-file my_template.svg
```

## Animation

Add `--animate` for SVG-native text fade-in effects:

```bash
python scripts/meme_gen.py make 'Hello' 'World' --template drake --animate --html
```

## Examples

```bash
# Programming memes
python scripts/meme_gen.py make 'WRITING TESTS' 'COPY-PASTING FROM SO' --template drake

# Productivity satire
python scripts/meme_gen.py make "5AM CLUB" "SNOOZE TO 9" --template stonks

# Student life
python scripts/meme_gen.py batch 'DUE TOMORROW' '3AM ENERGY' --all-templates --output-dir exam_memes/

# Generate 10 memes from quote pack
python scripts/meme_gen.py quote --category startup --count 10 --generate --output-dir startup_memes/
```

## Why SVG?

| Feature | SVG | Raster (PNG/JPG) |
|---|---|---|
| Resolution | ∞ (infinite) | Fixed pixels |
| File size | 3-5 KB | 100-500 KB |
| Editing | Text-based, easy | Pixel-level |
| Search | Text is selectable | Not searchable |
| Print | Perfect quality | Pixelated |

## File Structure

```
meme-generator/
├── SKILL.md              # Skill metadata
├── README.md             # This file
├── LICENSE               # MIT
├── scripts/
│   └── meme_gen.py       # Main generator script
└── references/
    ├── templates.md      # Template reference guide
    └── svg-text.md       # SVG text rendering guide
```

## License

MIT © Denis Voronin
