# Journal Abbrev — Journal Name Abbreviation Lookup Skill

[中文](README_CN.md)

A Claude Code skill for looking up standard journal/magazine name abbreviations. Supports both ISO 4 and MEDLINE abbreviation standards, covering 25,000+ journals.

## Features

| Feature | Native Claude Code | Journal Abbrev |
|---------|-------------------|----------------|
| Journal abbreviation lookup | Manual guessing | Multi-source cascade, accurate results |
| Reverse lookup (abbrev → full) | Not supported | Bidirectional lookup |
| BibTeX batch processing | Not supported | Auto-replace journal fields |
| Fuzzy search | Not supported | Partial name matching |
| Offline lookup | Not supported | Local cache with 25K+ journals |

## Data Sources

1. **JabRef Database** — 25,000+ journals, CC0 licensed, auto-downloaded on first run
2. **AbbrevISO API** — Algorithmic ISO 4 abbreviation based on LTWA (forward only)
3. **NLM Catalog** — Bidirectional lookup for biomedical journals (MEDLINE standard)

## Installation

`journal-abbrev` is a skill distributed via `SKILL.md`. Install it into any
`SKILL.md`-aware platform:

| Platform | Install |
|---|---|
| **Claude Code** (global) | `git clone https://github.com/Agents365-ai/journal-abbrev.git ~/.claude/skills/journal-abbrev` |
| **Claude Code** (project) | `git clone https://github.com/Agents365-ai/journal-abbrev.git .claude/skills/journal-abbrev` |
| **OpenClaw** (global) | `git clone https://github.com/Agents365-ai/journal-abbrev.git ~/.openclaw/skills/journal-abbrev` |
| **OpenClaw** (project) | `git clone https://github.com/Agents365-ai/journal-abbrev.git skills/journal-abbrev` |
| **ClawHub** | `clawhub install journal-abbrev` |
| **SkillsMP** | Search for `journal-abbrev` on [skillsmp.com](https://skillsmp.com) |

Or clone it anywhere and run the CLI directly — it is pure Python 3.9+
standard library with no third-party dependencies, and works on macOS, Linux,
and Windows:

```bash
git clone https://github.com/Agents365-ai/journal-abbrev.git
cd journal-abbrev
python3 jabbrv.py lookup "Nature Medicine"
python3 jabbrv.py schema              # full machine-readable CLI contract
```

## Usage

### Natural Language

Ask Claude directly:

- "What's the abbreviation for Nature Medicine?"
- "What journal is J. Biol. Chem.?"
- "Abbreviate all journal names in refs.bib"
- "Search for journals related to biolog chem"

### Command Line

```bash
# Auto-detect direction
python3 jabbrv.py lookup "Nature Medicine"

# Full name → abbreviation
python3 jabbrv.py abbrev "Journal of Biological Chemistry"

# Abbreviation → full name
python3 jabbrv.py expand "Nat. Med."

# Fuzzy search (paginated)
python3 jabbrv.py search "biolog chem" --limit 10 --offset 0

# Process BibTeX file (preview without writing first)
python3 jabbrv.py bib refs.bib --dry-run
python3 jabbrv.py bib refs.bib --output refs_final.bib

# Batch lookup (one journal per line)
python3 jabbrv.py batch journals.txt
python3 jabbrv.py batch journals.txt --stream   # NDJSON, one result per line

# Cache management
python3 jabbrv.py cache status     # inspect local cache
python3 jabbrv.py cache update     # download missing files
python3 jabbrv.py cache rebuild    # delete + redownload everything

# Machine-readable CLI contract (for AI agents and automation)
python3 jabbrv.py schema
python3 jabbrv.py schema lookup
```

### Agent-native output contract

Stdout is a stable JSON envelope when not attached to a terminal (piped or
captured by an agent runtime), and a human table/indent view when run on a TTY.
Every response carries the same shape:

- Success: `{"ok": true, "data": ..., "meta": {"schema_version", "cli_version", "cache", "latency_ms"}}`
- Partial (batch): `{"ok": "partial", "data": {"succeeded": [...], "failed": [...]}}`
- Error: `{"ok": false, "error": {"code", "message", "retryable", ...}}`

Exit codes are distinct per failure class: `0` success, `1` runtime,
`2` validation, `3` not found. Force a format with `--format json|table|human`
(or the back-compat `--json`); flags may appear before or after the subcommand.

## Requirements

- Python 3.9+ (no third-party packages required)

## Support

If this project helps you, consider supporting the author:

<table>
  <tr>
    <td align="center">
      <img src="https://raw.githubusercontent.com/Agents365-ai/images_payment/main/qrcode/wechat-pay.png" width="180" alt="WeChat Pay">
      <br>
      <b>WeChat Pay</b>
    </td>
    <td align="center">
      <img src="https://raw.githubusercontent.com/Agents365-ai/images_payment/main/qrcode/alipay.png" width="180" alt="Alipay">
      <br>
      <b>Alipay</b>
    </td>
    <td align="center">
      <img src="https://raw.githubusercontent.com/Agents365-ai/images_payment/main/qrcode/buymeacoffee.png" width="180" alt="Buy Me a Coffee">
      <br>
      <b>Buy Me a Coffee</b>
    </td>
  </tr>
</table>

## Author

**Agents365-ai**

- Bilibili: https://space.bilibili.com/441831884
- GitHub: https://github.com/Agents365-ai

## License

MIT
