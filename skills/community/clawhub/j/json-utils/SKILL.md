---
name: json-utils
description: Robust JSON parsing and validation with Pydantic schemas, JSON Schema validation, batch processing, and automatic JSON repair for LLM outputs. Use when Codex needs to (1) Parse JSON from unreliable LLM outputs with common errors like trailing commas or markdown code blocks, (2) Validate JSON against Pydantic models or JSON Schema, (3) Process multiple JSON files or JSON-Lines (NDJSON) in batch, (4) Extract JSON from mixed text content, (5) Safely parse tool call outputs with fallback handling, or for any JSON processing where robustness, batch processing, and error recovery are needed.
---

# JSON Utils

Robuste JSON-Verarbeitung mit Pydantic-Validierung, JSON Schema Support und automatischer JSON-Reparatur.

## Erweiterte Nutzung

Für **WebSearch-Integration** und **Multi-Environment** JSON-Verarbeitung siehe:
- **`../scripting-utils/`** - Kombiniert JSON-Utils mit WebSearch für API-Dokumentation und Response-Validierung

## Module

## Installation

```bash
pip install pydantic json-repair jsonschema
```

## Module

| Script | Zweck |
|--------|-------|
| `json_processor.py` | Kern-Funktionen: Parsing, Validierung, Tool-Calls |
| `json_schema_validator.py` | JSON Schema Draft 7/2020-12 Validierung |
| `json_batch_processor.py` | Batch-Verarbeitung & JSON-Lines (NDJSON) |
| `validate_tool_output.py` | CLI für Tool-Output Validierung |

## Quick Start

```python
from json_processor import parse_json, parse_and_validate, validate_tool_call
from pydantic import BaseModel

# Einfaches Parsing mit Auto-Reparatur
result = parse_json('{"name": "test", "value": 123,}')  # trailing comma OK

# Mit Pydantic-Validierung
class ToolCall(BaseModel):
    tool: str
    arguments: dict = {}

llm_output = '{"tool": "search", "arguments": {"q": "hello"},}'
validated = parse_and_validate(llm_output, ToolCall)
```

## Integration mit scripting-utils

```python
# Für erweiterte JSON-Verarbeitung mit WebSearch:
from scripting_utils.json_websearch import WebSearchJSON

# Sucht API-Doku, validiert Responses, generiert Schemas
ws = WebSearchJSON()
result = ws.search_and_validate(
    query="github api repos endpoint",
    schema_path="github_schema.json"
)
```

Siehe `../scripting-utils/scripts/json_websearch.py` für:
- API-Dokumentation via WebSearch
- Auto-Generierung von JSON-Schemas
- Batch-Validierung von API-Endpoints
- Cross-Platform JSON-Verarbeitung

## Szenarien

### 1. LLM-Output verarbeiten

```python
from json_processor import parse_json

# Verschiedene Input-Formate
parse_json('{"valid": true}')                              # Direkt OK
parse_json('```json\n{"valid": true}\n```')                # Aus Code-Block extrahiert
parse_json('{"valid": true,}')                             # Trailing comma repariert
parse_json('Some text {"tool": "x"} more text')           # JSON aus Text extrahiert
```

### 2. JSON Schema Validierung

```python
from json_schema_validator import validate_with_jsonschema, SchemaBuilder

# Gegen Datei validieren
validate_with_jsonschema(data, "/path/to/schema.json")

# Dynamisches Schema erstellen
schema = SchemaBuilder.object(
    properties={
        "name": SchemaBuilder.string(min_length=1),
        "age": SchemaBuilder.integer(minimum=0),
        "tags": SchemaBuilder.array(SchemaBuilder.string())
    },
    required=["name"]
)
```

### 3. Batch-Verarbeitung

```python
from json_batch_processor import process_file_batch, process_jsonl_file
from pathlib import Path

# Mehrere JSON-Dateien parallel
results = process_file_batch(
    [Path("a.json"), Path("b.json"), Path("c.json")],
    repair=True,
    max_workers=4
)

# JSON-Lines (NDJSON) verarbeiten
results = process_jsonl_file(Path("data.jsonl"))

for result in results:
    if result.success:
        print(f"[{result.source}] OK: {result.data}")
    else:
        print(f"[{result.source}] ERROR: {result.error}")
```

### 4. JSON-Lines verarbeiten

```bash
# Konvertiere JSON-Array zu JSON-Lines
python json_batch_processor.py data/*.json --output output.jsonl

# JSON-Lines validieren
python json_batch_processor.py data.jsonl --jsonl --repair
```

### 5. Tool-Call validieren

```python
from json_processor import validate_tool_call

result = validate_tool_call('{"tool": "weather", "arguments": {"city": "Berlin"}}')
# Mit Tool-Namensprüfung
try:
    result = validate_tool_call(raw_json, tool_name="weather")
except JSONValidationError:
    pass  # Falscher Tool-Name
```

## CLI-Nutzung

### Einzelnes JSON:
```bash
# Datei parsen
python scripts/json_processor.py -f output.json --pretty

# String parsen mit Reparatur
python scripts/json_processor.py '{"test": 123,}' --repair --pretty
```

### JSON Schema Validierung:
```bash
python scripts/json_schema_validator.py input.json -s schema.json
```

### Batch-Verarbeitung:
```bash
# Mehrere Dateien
python scripts/json_batch_processor.py *.json --workers 8

# JSON-Lines
python scripts/json_batch_processor.py data.jsonl --jsonl --output results.jsonl

# Nur Summary
python scripts/json_batch_processor.py *.json --summary
```

## API-Dokumentation

Siehe [references/api_reference.md](references/api_reference.md) für vollständige API-Dokumentation.

## Exception-Hierarchie

```
JSONProcessingError (Base)
├── JSONValidationError (Pydantic/Schema-Fehler)
│   └── SchemaValidationError (JSON Schema spezifisch)
└── JSONRepairError (Reparatur nicht möglich)
```

## Häufige Fehler repariert

- ✅ Trailing commas: `{"a": 1,}` → `{"a": 1}`
- ✅ Markdown-Blocks: `\`\`\`json\n{}\n\`\`\`` → `{}`
- ✅ JavaScript-Kommentare: `{"a": 1} // comment` → `{"a": 1}`
- ✅ Unescaped newlines in Strings
- ✅ Einzelne statt doppelte Anführungszeichen
