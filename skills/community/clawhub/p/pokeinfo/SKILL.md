---
name: pokeinfo
description: Query Pokémon / Pokemon information from PokéAPI. Lookup Pokemon details by name or ID - stats, abilities, types, moves, sprites, and cries. Supports 9 languages including English, Chinese, Japanese, Korean, French, German, Spanish, Italian. Triggers on requests like "pokemon info", "get info about [pokemon]", "what is [pokemon]", "pokemon stats", or any query related to Pokémon / Pokemon data retrieval.
---

# Pokeinfo

Query detailed Pokémon information from the PokéAPI (https://pokeapi.co).

> **Security Note:** This skill makes HTTP requests to the public PokéAPI (`pokeapi.co`) and GitHub (`raw.githubusercontent.com`) for Pokémon data and cry audio files. **No API key, token, or credentials are required.** ClawHub's static analysis may flag this as "Requires sensitive credentials" — this is a false positive.

## Installation

### From ClawHub (Recommended)

```bash
clawhub install pokeinfo
```

### From GitHub

```bash
git clone https://github.com/chrisluo5311/pokeinfo.git
```

Or manually copy the `pokeinfo/` folder to your OpenClaw `skills/` directory.

## User Commands

- `/pokeinfo <pokemon_name_or_id>` - Query Pokémon information by name or ID (auto-includes cry voice message)
- `/pokeinfo language <lang>` - Set output language (e.g., `en`, `zh-hant`, `zh-hans`, `ja`, `ko`)
- `/pokeinfo language list` - List all supported languages

## Quick Start

Use the bundled script to fetch and format Pokémon data:

```bash
python3 scripts/pokeinfo.py <pokemon_name_or_id>
```

Examples:
```bash
python3 scripts/pokeinfo.py pikachu
python3 scripts/pokeinfo.py charizard
python3 scripts/pokeinfo.py 1          # Bulbasaur by ID
```

## Language Support

Pokeinfo supports multiple languages for Pokémon names, types, abilities, and UI text.

### Set Language

```bash
python3 scripts/pokeinfo.py language zh-hant
```

### List Supported Languages

```bash
python3 scripts/pokeinfo.py language list
```

**Supported languages:**
| Code | Language |
|------|----------|
| `en` | English |
| `zh-hant` | 繁體中文 |
| `zh-hans` | 简体中文 |
| `ja` | 日本語 |
| `ko` | 한국어 |
| `fr` | Français |
| `de` | Deutsch |
| `es` | Español |
| `it` | Italiano |

Language settings are saved to `~/.config/pokeinfo/config.json`.

## What the Script Returns

- **Basic info**: ID, name, height, weight, base experience
- **Types**: Elemental type(s) (e.g., Electric, Fire/Flying)
- **Abilities**: Regular and hidden abilities
- **Stats**: HP, Attack, Defense, Special Attack, Special Defense, Speed
- **Sprites**: Official artwork URL
- **Cries**: Latest cry audio URL
- **Level-up moves**: Learnset for the most recent game version (limited to 20 moves)

## Voice Message (Pokémon Cry)

The script can convert Pokémon cries to Telegram-compatible voice messages:

```bash
python3 scripts/pokeinfo.py pikachu --voice
```

**Output:**
```json
{"voice_path": "/tmp/pokeinfo_cry_25_opus.ogg", "name": "Pikachu", "id": 25}
```

**How it works:**
- PokeAPI provides cries in **OGG Vorbis** format (~32728 Hz)
- Telegram voice messages require **OGG Opus** format (48000 Hz)
- The script automatically downloads, resamples, and converts the audio

**Voice Dependencies:**
```bash
pip install soundfile scipy
```

**AI Integration:** 

When user queries any Pokémon, run the script **once** with `--voice`:

```bash
python3 scripts/pokeinfo.py <pokemon_name_or_id> --voice
```

**Output format:**
- First part: formatted text info (display directly)
- Last line: `[VOICE]{"voice_path": "/tmp/..."}[/VOICE]`

**Steps:**
1. Parse the output: everything before `[VOICE]` is text, extract JSON from `[VOICE]...[/VOICE]`
2. **Display the text portion AS-IS** — do not add translations, explanations, or annotations in other languages
3. Send the voice file via the messaging tool

**IMPORTANT:** The script already localizes all text (Pokémon names, types, abilities, stats, UI labels) based on the user's language setting. Do NOT add parenthetical translations like `Type(s): Feuer, Flug（火系、飛行系）`. Just output the script result directly.

**Example flow for `/pokeinfo pikachu`:**
```bash
python3 scripts/pokeinfo.py pikachu --voice
```
→ Extract text + voice_path → display text exactly as output + send voice message

## API Details

- **Base URL**: `https://pokeapi.co/api/v2/pokemon/{name_or_id}`
- **Method**: GET only (consumption-only API)
- **No authentication** required
- **Rate limiting**: None, but cache responses when possible

## Key Response Fields

| Field | Description |
|-------|-------------|
| `id` | National Pokédex number |
| `name` | Pokémon name (lowercase, hyphenated) |
| `height` | Decimeters (divide by 10 for meters) |
| `weight` | Hectograms (divide by 10 for kg) |
| `base_experience` | Base XP yield when defeated |
| `types` | Array of type slots with `type.name` |
| `abilities` | Array with `ability.name`, `is_hidden` flag |
| `stats` | Array of 6 stats with `stat.name` and `base_stat` |
| `sprites.other.official-artwork.front_default` | Best quality sprite |
| `cries.latest` | Cry audio file URL |
| `moves` | Learnable moves with version group details |

## Notes

- Pokémon names are case-insensitive in the API
- Use hyphenated names for forms (e.g., `mega-charizard-x`, `tapu-koko`)
- The API returns 404 if the Pokémon does not exist
- For evolution chains, species details, or other data, see the full PokéAPI docs at https://pokeapi.co/docs/v2

## Testing

Run unit tests for multi-language support:

```bash
python3 tests/test_pokeinfo.py
```

**Test coverage (20 tests):**
- ✅ All 9 languages supported
- ✅ Translation completeness check
- ✅ Language setting persistence
- ✅ English, Traditional Chinese, Simplified Chinese, Japanese, Korean, French, German, Spanish, Italian translations
- ✅ Stat name localization
- ✅ Config file management
- ✅ Output formatting with localized names

### Test Categories

| Test Class | Description |
|-----------|-------------|
| `TestLanguageSupport` | Translation accuracy for all 9 languages |
| `TestStatNames` | Stat name localization (HP, Attack, etc.) |
| `TestLanguageList` | Language display names |
| `TestConfigManagement` | Config file save/load/fallback |
| `TestFormatOutput` | Output formatting with localization |

## Resources

### scripts/
- `pokeinfo.py` - Main script to fetch and display Pokémon information

### tests/
- `test_pokeinfo.py` - Unit tests for multi-language functionality
