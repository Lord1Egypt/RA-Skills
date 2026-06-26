# JSON Utils API Reference

## json_processor.py

### parse_json(raw_input: str, repair: bool = True) → Any
Parst einen JSON-String mit automatischer Reparatur.

**Parameter:**
- `raw_input`: Der zu parsende JSON-String
- `repair`: Ob JSON-Reparatur versucht werden soll (default: True)

**Returns:** Geparstes Python-Objekt

**Raises:** `JSONProcessingError` wenn Parsing fehlschlägt

**Beispiel:**
```python
from json_processor import parse_json

result = parse_json('{"name": "test", "value": 123,}')
# Ergebnis: {"name": "test", "value": 123}
```

---

### parse_and_validate(raw_input: str, model_class: Type[T], repair: bool = True, strict: bool = False) → T
Parst JSON und validiert gegen ein Pydantic-Modell.

**Parameter:**
- `raw_input`: Der zu parsende JSON-String
- `model_class`: Pydantic-Modellklasse
- `repair`: Ob Reparatur versucht werden soll (default: True)
- `strict`: Ob strikte Validierung angewendet werden soll (default: False)

**Returns:** Validierte Instanz des Pydantic-Modells

---

### validate_tool_call(raw_json: str, tool_name: Optional[str] = None) → dict
Validiert einen OpenClaw/Tool-Call JSON.

**Returns:** `{"tool": str, "arguments": dict, "reasoning": Optional[str]}`

---

## json_schema_validator.py

### validate_with_jsonschema(data: Any, schema: Union[str, Path, dict], draft: str = "auto") → bool
Validiert Daten gegen ein JSON Schema.

**Parameter:**
- `data`: Zu validierende Daten
- `schema`: JSON Schema (Pfad, String oder Dict)
- `draft`: JSON Schema Draft Version ("auto", "draft7", "2020-12")

**Raises:** `SchemaValidationError` wenn Validierung fehlschlägt

**Beispiel:**
```python
from json_schema_validator import validate_with_jsonschema, SchemaBuilder

# Mit Schema-Datei
schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "integer", "minimum": 0}
    },
    "required": ["name"]
}
validate_with_jsonschema({"name": "Max"}, schema)

# Mit SchemaBuilder
schema = SchemaBuilder.object(
    properties={
        "email": SchemaBuilder.string(pattern=r"^[^@]+@[^@]+$"),
        "count": SchemaBuilder.integer(minimum=1)
    },
    required=["email"]
)
```

---

### SchemaBuilder
Hilfsklasse zum Erstellen von JSON Schemas.

**Methoden:**
- `object(properties: dict, required: Optional[list]) → dict`
- `string(enum=None, pattern=None, min_length=None) → dict`
- `integer(minimum=None, maximum=None) → dict`
- `array(items: dict, min_items=None) → dict`

---

## json_batch_processor.py

### process_file_batch(file_paths: list[Path], repair: bool = True, validate_model: Optional[type] = None, max_workers: int = 4) → list[BatchResult]
Verarbeitet mehrere JSON-Dateien parallel.

**Parameter:**
- `file_paths`: Liste der Datei-Pfade
- `repair`: Ob JSON-Reparatur angewendet werden soll
- `validate_model`: Optionales Pydantic-Modell für Validierung
- `max_workers`: Parallele Worker (default: 4)

**Returns:** Liste von `BatchResult` Objekten

**Beispiel:**
```python
from json_batch_processor import process_file_batch
from pathlib import Path

results = process_file_batch(
    [Path("a.json"), Path("b.json")],
    repair=True,
    max_workers=8
)

for result in results:
    if result.success:
        print(f"✓ {result.source}")
    else:
        print(f"✗ {result.source}: {result.error}")
```

---

### process_jsonl_file(file_path: Path, repair: bool = True, validate_model: Optional[type] = None) → list[BatchResult]
Verarbeitet eine JSON-Lines (NDJSON) Datei.

**Beispiel:**
```python
from json_batch_processor import process_jsonl_file

results = process_jsonl_file(Path("data.jsonl"))
successful = [r.data for r in results if r.success]
```

---

### BatchResult
Container für Batch-Verarbeitungsergebnisse.

**Attribute:**
- `index: int` - Position im Batch
- `source: str` - Quell-Identifier (Dateipfad oder Zeilennummer)
- `success: bool` - Ob Verarbeitung erfolgreich war
- `data: Any` - Geparste Daten (bei success=True)
- `error: Optional[str]` - Fehlermeldung (bei success=False)

**Methoden:**
- `to_dict() → dict` - Konvertiere zu Dictionary

---

## Exception-Hierarchie

```python
from json_processor import (
    JSONProcessingError,      # Base
    JSONValidationError,      # Validierungsfehler
    JSONRepairError          # Reparaturfehler
)
from json_schema_validator import SchemaValidationError

try:
    result = parse_json(llm_output)
except JSONValidationError as e:
    # Schema stimmt nicht
    pass
except JSONRepairError as e:
    # Reparatur nicht möglich
    pass
```
