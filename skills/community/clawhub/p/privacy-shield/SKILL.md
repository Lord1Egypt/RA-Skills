# Privacy Shield

Privacy data marking system — unified sensitive resource management with pre-operation checks and audit logging.

## Design Principles

- **Conservative by default**: Unmarked data should be handled with caution
- **Check before act**: Verify privacy level before any data operation
- **Centralized control**: One registry file governs all privacy rules

## Privacy Levels

| Level | Meaning | Example |
|-------|---------|---------|
| `owner_only` | Owner can view/use only | Photos, personal info |
| `private` | No external disclosure, internal use OK | Model info, API keys |
| `no_export` | Must not leave the machine | Memory files, ontology |
| `public` | Free to use | Non-sensitive data |

## Quick Start

### Mark a resource

```bash
# Mark a file or directory
python scripts/registry.py mark media/images/people/ --level owner_only --reason "Family photos"

# Mark a rule category
python scripts/registry.py mark --type rule "model_info" --level private --reason "Infrastructure"
```

### Check permission

```bash
# Check if a resource can be shared
python scripts/registry.py check media/images/people/photo.jpg --action share

# Check privacy level only
python scripts/registry.py check media/images/people/photo.jpg
```

### List all marks

```bash
python scripts/registry.py list
python scripts/registry.py list --level owner_only
```

### Remove a mark

```bash
python scripts/registry.py unmark media/images/old-photo.jpg
```

### View audit log

```bash
python scripts/registry.py audit
python scripts/registry.py audit --deny-only
```

## Agent Integration

Before any data output operation:

1. **Check registry** → `python scripts/registry.py check <resource> --action <action>`
2. **Evaluate result**:
   - `owner_only` → Output only when owner requests
   - `private` → No external disclosure, internal processing OK
   - `no_export` → Never leave this machine
   - Unmarked → Default to caution, ask the owner

## Registry File

Location: `data/privacy-registry.json`

```json
{
  "version": "1.0.0",
  "rules": {
    "photos": {"level": "owner_only", "reason": "Family photos"},
    "model_info": {"level": "private", "reason": "Infrastructure"}
  },
  "resources": [
    {
      "path": "media/images/people/",
      "level": "owner_only",
      "reason": "Family photos",
      "marked_at": "2026-03-20T09:53:00+08:00"
    }
  ]
}
```

## Features

- ✅ Path prefix + glob pattern matching
- ✅ Automatic audit logging (JSONL)
- ✅ Integration with image-manager (`--privacy` flag)
- ✅ CLI for mark/check/list/unmark/audit
