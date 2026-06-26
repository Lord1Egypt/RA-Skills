# Emblem Persona Marketplace API

All endpoints are public. No authentication required.

## Endpoints

| Action | URL |
|--------|-----|
| Full marketplace index | `https://raw.githubusercontent.com/decentraliser/personas/main/index.json` |
| Persona metadata | `https://raw.githubusercontent.com/decentraliser/personas/main/personas/{handle}/persona.json` |
| SOUL.md | `https://raw.githubusercontent.com/decentraliser/personas/main/personas/{handle}/SOUL.md` |
| IDENTITY.md | `https://raw.githubusercontent.com/decentraliser/personas/main/personas/{handle}/IDENTITY.md` |
| Avatar image | `https://raw.githubusercontent.com/decentraliser/personas/main/personas/{handle}/avatar.png` |
| Repository docs | `https://raw.githubusercontent.com/decentraliser/personas/main/AGENTS.md` |

## Local workspace layout

```text
<workspace>/personas/
├── config.json
├── index.json
└── <handle>/
    ├── persona.json
    ├── SOUL.md
    ├── IDENTITY.md
    └── avatar.png
```

## Shared context config schema

`<workspace>/personas/config.json`

```json
{
  "context_files": [
    "../_System/Motoko-Kru-Foundation.md",
    "../Resources/Coding-Subagent-Contract.md"
  ]
}
```

Notes:
- `context_files` may be either an array or a comma-separated string.
- Relative paths resolve from the directory containing `config.json`.
- Use this for shared org doctrine that every persona spawn should inherit.

## Remote marketplace index schema

```json
{
  "total": 1,
  "personas": [
    {
      "name": "The Mandalorian",
      "handle": "the-mandalorian",
      "tagline": "This is the Way.",
      "avatar": "avatar.png",
      "inspired_by": "Din Djarin (Star Wars: The Mandalorian)",
      "expertise": ["security operations", "tactical problem-solving"],
      "catchphrase": "I can bring you in warm, or I can bring you in cold.",
      "compatibility": ["openclaw", "claude-code", "cursor"],
      "version": "2.0.0",
      "files": ["SOUL.md", "IDENTITY.md"]
    }
  ]
}
```

## Local rebuilt index schema

After import, `rebuild-index.py` writes a local index with remote metadata plus local availability fields:

```json
{
  "total": 1,
  "personas": [
    {
      "name": "The Mandalorian",
      "handle": "the-mandalorian",
      "expertise": ["security operations", "tactical problem-solving"],
      "version": "2.0.0",
      "local": true,
      "files_present": {
        "soul": "SOUL.md",
        "identity": "IDENTITY.md",
        "avatar": "avatar.png"
      }
    }
  ]
}
```

## Rate-limit guidance

- Prefer the raw GitHub index over directory listing APIs.
- Cache locally after import.
- Re-fetch only on explicit refresh or import.
- Use `--no-index` during batch imports, then rebuild once.
