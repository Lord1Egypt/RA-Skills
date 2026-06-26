#!/usr/bin/env python3
"""
JSON Schema Validator - Validiert JSON gegen JSON Schema Draft 7/2020-12.
Erweitert Pydantic mit externen Schema-Dateien.
"""

import json
import sys
from pathlib import Path
from typing import Any, Optional, Union

try:
    from jsonschema import validate, ValidationError as JSONSchemaValidationError
    from jsonschema.protocols import Validator
    HAS_JSONSCHEMA = True
except ImportError:
    HAS_JSONSCHEMA = False

try:
    from pydantic import BaseModel, ValidationError as PydanticValidationError
    from pydantic.json_schema import model_json_schema
except ImportError:
    pass

from json_processor import parse_json, JSONProcessingError, JSONValidationError


class SchemaValidationError(JSONValidationError):
    """Raised when JSON Schema validation fails."""
    pass


def load_schema(schema_source: Union[str, Path, dict]) -> dict:
    """
    Lädt ein JSON Schema aus verschiedenen Quellen.
    
    Args:
        schema_source: Pfad zur Schema-Datei oder Schema-Dict oder JSON String
    
    Returns:
        Schema als Dictionary
    """
    if isinstance(schema_source, dict):
        return schema_source
    
    schema_path = Path(schema_source)
    if schema_path.exists():
        try:
            return json.loads(schema_path.read_text())
        except json.JSONDecodeError as e:
            raise SchemaValidationError(f"Invalid JSON in schema file: {e}")
    
    # Versuche als JSON String zu parsen
    try:
        return json.loads(schema_source)
    except json.JSONDecodeError:
        raise SchemaValidationError(f"Schema not found or invalid: {schema_source}")


def validate_with_jsonschema(
    data: Any,
    schema: Union[str, Path, dict],
    draft: str = "auto"
) -> bool:
    """
    Validiert Daten gegen ein JSON Schema.
    
    Args:
        data: Zu validierende Daten
        schema: JSON Schema (Pfad, String oder Dict)
        draft: JSON Schema Draft Version ("auto", "draft7", "2020-12")
    
    Returns:
        True wenn valid
    
    Raises:
        SchemaValidationError: Wenn Validierung fehlschlägt
    """
    if not HAS_JSONSCHEMA:
        raise SchemaValidationError("jsonschema not installed. Run: pip install jsonschema")
    
    schema_dict = load_schema(schema)
    
    try:
        validate(instance=data, schema=schema_dict)
        return True
    except JSONSchemaValidationError as e:
        raise SchemaValidationError(f"Schema validation failed: {e.message} at {list(e.path)}")


def pydantic_to_jsonschema(model_class: type) -> dict:
    """
    Konvertiert ein Pydantic-Modell zu JSON Schema.
    
    Args:
        model_class: Pydantic-Modellklasse
    
    Returns:
        JSON Schema als Dictionary
    """
    return model_json_schema(model_class)


def validate_and_convert(
    raw_input: str,
    schema: Union[str, Path, dict],
    repair: bool = True
) -> Any:
    """
    Parst, repariert und validiert JSON gegen Schema.
    
    Args:
        raw_input: JSON-String
        schema: JSON Schema
        repair: Ob Reparatur versucht werden soll
    
    Returns:
        Validierte Daten
    """
    data = parse_json(raw_input, repair=repair)
    validate_with_jsonschema(data, schema)
    return data


class SchemaBuilder:
    """Hilfsklasse zum Erstellen von JSON Schemas."""
    
    @staticmethod
    def object(properties: dict, required: Optional[list] = None) -> dict:
        """Erstellt ein Object-Schema."""
        schema = {
            "type": "object",
            "properties": properties
        }
        if required:
            schema["required"] = required
        return schema
    
    @staticmethod
    def string(enum: Optional[list] = None, pattern: Optional[str] = None, min_length: Optional[int] = None) -> dict:
        """Erstellt ein String-Schema."""
        schema = {"type": "string"}
        if enum:
            schema["enum"] = enum
        if pattern:
            schema["pattern"] = pattern
        if min_length is not None:
            schema["minLength"] = min_length
        return schema
    
    @staticmethod
    def integer(minimum: Optional[int] = None, maximum: Optional[int] = None) -> dict:
        """Erstellt ein Integer-Schema."""
        schema = {"type": "integer"}
        if minimum is not None:
            schema["minimum"] = minimum
        if maximum is not None:
            schema["maximum"] = maximum
        return schema
    
    @staticmethod
    def array(items: dict, min_items: Optional[int] = None) -> dict:
        """Erstellt ein Array-Schema."""
        schema = {"type": "array", "items": items}
        if min_items is not None:
            schema["minItems"] = min_items
        return schema


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="JSON Schema Validator")
    parser.add_argument("input", help="JSON file or string")
    parser.add_argument("--schema", "-s", required=True, help="Schema file")
    parser.add_argument("--file", "-f", action="store_true", help="Input is file")
    parser.add_argument("--repair", "-r", action="store_true", default=True)
    
    args = parser.parse_args()
    
    # Lade Input (Auto-detect file vs string)
    input_path = Path(args.input)
    if args.file or (input_path.exists() and input_path.is_file()):
        raw_input = input_path.read_text()
    else:
        raw_input = args.input
    
    try:
        result = validate_and_convert(raw_input, args.schema, repair=args.repair)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        print("\n✓ Validation passed", file=sys.stderr)
    except (JSONProcessingError, SchemaValidationError) as e:
        print(f"✗ Validation failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
