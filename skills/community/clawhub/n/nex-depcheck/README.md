# Nex DepCheck

Skill dependency checker. Scan Python skills to verify they only use stdlib and internal imports. Catch external dependencies before publishing.

**Built by [Nex AI](https://nex-ai.be)**

## Features

- Check individual skills or scan entire directories
- Classifies imports as stdlib, internal, or external
- Verbose mode shows per-file breakdown
- Check if any module is in Python stdlib
- No database needed, pure file scanner
- Python stdlib only, zero dependencies

## Setup

```bash
bash setup.sh
```

## Usage

```bash
# Check a single skill
nex-depcheck check /path/to/nex-timetrack

# Scan all skills
nex-depcheck scan /path/to/skills

# Check a single file
nex-depcheck file /path/to/script.py

# Is this stdlib?
nex-depcheck stdlib pathlib
```

## License

- **ClawHub:** MIT-0 (free for any use)
- **GitHub:** AGPL-3.0 (commercial licenses available via info@nex-ai.be)
