---
name: config-manager
description: "Safe configuration file editing for JSON, YAML, TOML, and other config formats. Use when working with configuration files for: (1) Reading config values, (2) Updating/adding/removing keys, (3) Creating new config files, (4) Validating syntax, (5) Merging configs, (6) Converting between formats, or (7) Debugging config issues."
---

# Config Manager

Handles configuration files through safe, validated operations that preserve syntax and formatting.

## Core Workflows

### Format Detection
Identify config format by extension:
- `.json` → JSON
- `.yaml`, `.yml` → YAML
- `.toml` → TOML
- `.env` → Environment variables
- `.ini` → INI format
- `.xml` → XML
- `.cfg`, `.conf` → Generic config

### Safe Editing Rules

**Golden Rule:** Never manually edit structured configs unless trivial. Use tools:
- JSON: `jq` for CLI, JSON.parse/stringify for code
- YAML: `yq` for CLI, yaml libraries for code
- TOML: `toml` libraries (no standard CLI tool)

### Common Operations

#### Read Values
```bash
# JSON
jq '.key' config.json
jq '.nested.key' config.json

# YAML
yq '.key' config.yaml
yq '.nested.key' config.yaml

# TOML (requires python/toml)
python -c "import toml; print(toml.load('config.toml')['key'])"
```

#### Update Values
```bash
# JSON
jq '.key = "new value"' config.json > tmp && mv tmp config.json

# YAML
yq -i '.key = "new value"' config.yaml

# Always backup first
cp config.json config.json.bak
```

#### Add New Keys
```bash
# JSON
jq '.newKey = "value"' config.json > tmp && mv tmp config.json

# YAML
yq -i '.newKey = "value"' config.yaml
```

#### Remove Keys
```bash
# JSON
jq 'del(.unwantedKey)' config.json > tmp && mv tmp config.json

# YAML
yq -i 'del(.unwantedKey)' config.yaml
```

### Validation Before Save

**Always validate after edits:**
```bash
# JSON
jq empty config.json && echo "Valid JSON"

# YAML
yamllint config.yaml || python -c "import yaml; yaml.safe_load(open('config.yaml'))"

# TOML
python -c "import toml; toml.load('config.toml')"
```

### Formatting Preservation

- Use `yq -i` for in-place YAML edits (preserves comments)
- Use `jq` with `--indent` to control JSON spacing
- Never mix tabs/spaces in YAML
- Preserve trailing newlines

### Creating New Configs

**Use templates or generate programmatically:**
```bash
# JSON
echo '{"key": "value"}' | jq '.' > new-config.json

# YAML
cat > new-config.yaml << EOF
key: value
nested:
  key2: value2
EOF
```

## Safety Rules

1. **Validate syntax** before saving any changes
2. **Backup first** - Copy original before destructive edits
3. **Use tools, not manual edits** - `jq`/`yq` for JSON/YAML
4. **Test after changes** - Load config in application context
5. **Respect workspace boundaries** - Only touch ~/openclaw configs
6. **Never commit secrets** - Use .env for sensitive values, gitignore them

## When to Read references/formats.md

Load when:
- Need detailed format specifications (JSON schema, YAML anchors)
- Complex merge/conflict resolution needed
- Format conversion required (JSON↔YAML↔TOML)
- Validation schemas or type checking needed