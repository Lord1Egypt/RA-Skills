# Configuration Formats Reference

## JSON (JavaScript Object Notation)

### Syntax Rules
- Keys must be double-quoted strings: `"key"`
- Values: strings, numbers, booleans, null, arrays, objects
- No trailing commas
- No comments (standard JSON)
- UTF-8 encoding

### Tools
```bash
# Install jq (if not present)
sudo dnf install jq    # Fedora
sudo apt install jq    # Debian/Ubuntu
brew install jq        # macOS

# Validate
jq empty file.json

# Pretty print
jq '.' file.json

# Update value
jq '.key = "value"' file.json > tmp && mv tmp file.json

# Add nested key
jq '.parent.child = "value"' file.json > tmp && mv tmp file.json

# Delete key
jq 'del(.unwanted)' file.json > tmp && mv tmp file.json
```

### Common Patterns

**Merge two JSON files:**
```bash
jq -s '.[0] * .[1]' config.base.json config.override.json > merged.json
```

**Extract specific keys:**
```bash
jq '{key1: .key1, key2: .key2}' file.json
```

**Conditional updates:**
```bash
jq 'if .enabled == true then .timeout = 30 else .timeout = 60 end' file.json
```

### JSON Schema Validation
```bash
# Install ajv
npm install -g ajv-cli

# Validate against schema
ajv validate -s schema.json -d config.json
```

---

## YAML (YAML Ain't Markup Language)

### Syntax Rules
- Indentation: 2 spaces (never tabs)
- Keys: unquoted or quoted strings
- Values: strings, numbers, booleans, null, lists, mappings
- Lists: `- item` or `[item1, item2]`
- Comments: `# comment`
- Multi-line: `|` (preserve newlines) or `>` (fold newlines)
- Anchors: `&anchor` and aliases `*anchor`

### Tools
```bash
# Install yq
wget https://github.com/mikefarah/yq/releases/latest/download/yq_linux_amd64 -O yq
chmod +x yq
sudo mv yq /usr/local/bin/

# Or via pip
pip install yq

# Validate
yq '.' file.yaml > /dev/null
yamllint file.yaml

# Update value
yq -i '.key = "value"' file.yaml

# Preserve comments (yq v4)
yq eval '.key = "value"' -i file.yaml
```

### Common Patterns

**Nested updates:**
```yaml
# Original
database:
  host: localhost
  port: 5432

# Update nested
yq '.database.port = 5433' -i file.yaml
```

**Add to list:**
```yaml
yq '.items += ["new item"]' -i file.yaml
```

**Merge YAML files:**
```bash
yq eval-all '. as $item ireduce ({}; . * $item)' base.yaml override.yaml > merged.yaml
```

**Convert YAML to JSON:**
```bash
yq -o json '.' file.yaml > file.json
```

### YAML Linting
```bash
# Install yamllint
pip install yamllint

# Lint
yamllint file.yaml

# Strict mode
yamllint -d relaxed file.yaml
```

---

## TOML (Tom's Obvious, Minimal Language)

### Syntax Rules
- Keys: unquoted or quoted strings
- Values: strings (quoted), numbers, booleans, arrays, tables
- Sections: `[table]`
- Comments: `# comment`
- No indentation required (but allowed for readability)

### Tools
```bash
# Python toml library
pip install toml
# or
pip install tomli  # Python 3.11+ built-in

# Validate/read
python -c "import toml; toml.load('file.toml')"

# Edit (Python script)
python << EOF
import toml
with open('file.toml', 'r') as f:
    data = toml.load(f)
data['section']['key'] = 'value'
with open('file.toml', 'w') as f:
    toml.dump(data, f)
EOF
```

### Common Patterns

**Read value:**
```bash
python -c "import toml; print(toml.load('file.toml')['database']['port'])"
```

**Update value:**
```python
import toml

with open('config.toml', 'r') as f:
    data = toml.load(f)

data['server']['port'] = 8080

with open('config.toml', 'w') as f:
    toml.dump(data, f)
```

---

## Environment Files (.env)

### Syntax Rules
- KEY=VALUE pairs (no spaces around =)
- Comments: `# comment`
- Quotes optional: `KEY=value` or `KEY="value"`
- No nested structures
- Export format: `export KEY=value`

### Tools
```bash
# Read value
grep "^KEY=" .env | cut -d= -f2

# Update value
sed -i 's/^KEY=.*/KEY=newvalue/' .env

# Add new key
echo "NEW_KEY=value" >> .env

# Remove key
sed -i '/^OLD_KEY=/d' .env
```

### Safety
- Never commit .env files with secrets
- Use .env.example for template
- Gitignore: `*.env`

---

## INI Format

### Syntax Rules
- Sections: `[section]`
- Keys: `key = value`
- Comments: `;` or `#`

### Tools
```bash
# Python configparser
python -c "
import configparser
c = configparser.ConfigParser()
c.read('file.ini')
print(c['section']['key'])
"
```

---

## Format Conversion

### JSON ↔ YAML
```bash
# JSON to YAML
yq -o yaml '.' file.json > file.yaml

# YAML to JSON
yq -o json '.' file.yaml > file.json
```

### TOML ↔ JSON
```python
import toml
import json

# TOML to JSON
with open('file.toml') as f:
    data = toml.load(f)
with open('file.json', 'w') as f:
    json.dump(data, f, indent=2)
```

---

## Validation Strategies

### Syntax Validation
Always run before saving:
```bash
# JSON
jq empty file.json && echo "✓ Valid"

# YAML
yq '.' file.yaml > /dev/null && echo "✓ Valid"

# TOML
python -c "import toml; toml.load('file.toml')" && echo "✓ Valid"
```

### Schema Validation
For typed configs:
```bash
# JSON Schema
ajv validate -s schema.json -d config.json

# YAML (using JSON Schema)
yq -o json '.' file.yaml | ajv validate -s schema.json
```

### Semantic Validation
Check business logic:
```bash
# Port must be 1-65535
jq '.port | select(. >= 1 and . <= 65535)' config.json

# Required keys present
jq 'has("host") and has("port")' config.json
```

---

## Common Gotchas

### JSON
- ❌ Trailing commas: `[1, 2,]` → `[1, 2]`
- ❌ Comments: `// comment` → not allowed
- ❌ Single quotes: `'key'` → `"key"`

### YAML
- ❌ Tabs for indentation → use spaces
- ❌ Missing colons: `key value` → `key: value`
- ❌ Wrong indentation breaks nesting

### TOML
- ❌ Unquoted strings: `key = value` → `key = "value"`
- ❌ Missing section headers for nested tables

### .env
- ❌ Spaces around =: `KEY = value` → `KEY=value`
- ❌ Forgetting to export: `KEY=value` → `export KEY=value` (if sourcing)