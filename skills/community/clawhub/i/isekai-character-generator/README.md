# Isekai Character Generator

Generate isekai anime characters and light novel protagonists from text descriptions — design transported-to-another-world heroes, JRPG main characters, fantasy adventurers, magical girls, demon lords, and reincarnated MCs in the Niji-style anime aesthetic popular in shows like *Sword Art Online*, *Re:Zero*, *Mushoku Tensei*, and *That Time I Got Reincarnated as a Slime*. Perfect for fanart, OC design, light novel covers, manga concept art, and character sheets.

Powered by the Neta AI image generation API (api.talesofai.com) — the same service as neta.art/open.

## Install

```bash
npx skills add blammectrappora/isekai-character-generator
```

Or with ClawHub:

```bash
clawhub install isekai-character-generator
```

## Usage

```bash
node isekaicharactergenerator.js "your description here" --token YOUR_TOKEN
```

### Examples

Generate a default isekai protagonist:

```bash
node isekaicharactergenerator.js "anime style isekai protagonist character, transported to a fantasy other-world, magical sword and ornate armor, vibrant Niji-style colors, dramatic cinematic lighting, light novel cover art composition, detailed face and outfit, full body character design sheet" --token YOUR_TOKEN
```

A magical girl reincarnated as a demon lord:

```bash
node isekaicharactergenerator.js "magical girl reincarnated as a demon lord, dark ornate dress, glowing crimson eyes, floating magical runes, dramatic backlighting, Niji-style anime art" --token YOUR_TOKEN
```

A reluctant shounen hero in a JRPG party:

```bash
node isekaicharactergenerator.js "teenage shounen isekai hero, brown spiky hair, leather armor over school uniform, holding an ancient tome, flanked by elf and beastkin companions, light novel cover composition" --size landscape --token YOUR_TOKEN
```

Use a reference image for style inheritance:

```bash
node isekaicharactergenerator.js "demon lord sitting on a throne, ornate horns, regal robes" --ref UUID_HERE --token YOUR_TOKEN
```

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `<prompt>` | Positional argument — text description of the character | (built-in isekai protagonist prompt) |
| `--token` | Your Neta API token (required) | — |
| `--size` | Output aspect ratio: `portrait` (832×1216), `landscape` (1216×832), `square` (1024×1024), `tall` (704×1408) | `portrait` |
| `--ref` | Reference image UUID for style inheritance | — |

## Output

Returns a direct image URL.

## Token setup

This skill requires a Neta API token. Pass it via the `--token` flag on every invocation:

```bash
node isekaicharactergenerator.js "your prompt" --token YOUR_TOKEN
```

You can store your token in a shell variable and expand it at call time:

```bash
node isekaicharactergenerator.js "your prompt" --token "$NETA_TOKEN"
```

Get a free trial token at <https://www.neta.art/open/>.

