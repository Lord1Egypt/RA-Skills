#!/usr/bin/env python3
"""
JSON Processor mit Pydantic Validation und JSON-Repair.
Für robuste Verarbeitung von LLM-Outputs.
"""

import json
import sys
from typing import Any, Type, TypeVar, Optional
from pathlib import Path

try:
    from pydantic import BaseModel, ValidationError
except ImportError:
    print("Error: pydantic not installed. Run: pip install pydantic", file=sys.stderr)
    sys.exit(1)

try:
    from json_repair import repair_json
    HAS_JSON_REPAIR = True
except ImportError:
    HAS_JSON_REPAIR = False
    print("Warning: json_repair not installed. Run: pip install json-repair", file=sys.stderr)

T = TypeVar('T', bound=BaseModel)


class JSONProcessingError(Exception):
    """Base exception for JSON processing errors."""
    pass


class JSONValidationError(JSONProcessingError):
    """Raised when JSON validation fails."""
    pass


class JSONRepairError(JSONProcessingError):
    """Raised when JSON repair fails."""
    pass


def repair_json_string(raw_json: str) -> str:
    """
    Repariert häufige JSON-Fehler aus LLM-Outputs.
    
    Behebt:
    - Trailing commas
    - Einzelne statt doppelte Quotes
    - JavaScript-Style Kommentare
    - Unescaped Zeilenumbrüche in Strings
    """
    if HAS_JSON_REPAIR:
        try:
            repaired = repair_json(raw_json, return_objects=False)
            return repaired
        except Exception as e:
            raise JSONRepairError(f"JSON repair failed: {e}")
    else:
        # Fallback: Manuelle Reparaturen
        import re
        cleaned = raw_json.strip()
        
        # Entferne JavaScript-Kommentare
        cleaned = re.sub(r'//.*?\n', '\n', cleaned)
        cleaned = re.sub(r'/\*.*?\*/', '', cleaned, flags=re.DOTALL)
        
        # Entferne trailing commas vor ] oder }
        cleaned = re.sub(r',(\s*[}\]])', r'\1', cleaned)
        
        return cleaned


def parse_json(raw_input: str, repair: bool = True) -> Any:
    """
    Parst JSON-String mit optionaler automatischer Reparatur.
    
    Args:
        raw_input: Der zu parsende JSON-String
        repair: Ob JSON-Reparatur versucht werden soll (default: True)
    
    Returns:
        Geparstes Python-Objekt
    
    Raises:
        JSONProcessingError: Wenn Parsing fehlschlägt
    """
    raw_input = raw_input.strip()
    
    # Versuche zuerst direktes Parsing
    try:
        return json.loads(raw_input)
    except json.JSONDecodeError:
        pass
    
    # Extrahiere JSON aus Markdown-Code-Blöcken
    if "```" in raw_input:
        import re
        # Suche nach JSON in ```json ... ``` oder ``` ... ```
        patterns = [
            r'```json\s*(.*?)\s*```',
            r'```\s*(\{.*?\})\s*```',
            r'```\s*(\[.*?\])\s*```',
        ]
        for pattern in patterns:
            matches = re.findall(pattern, raw_input, re.DOTALL)
            for match in matches:
                try:
                    return json.loads(match)
                except json.JSONDecodeError:
                    continue
    
    # Versuche Reparatur
    if repair:
        try:
            repaired = repair_json_string(raw_input)
            return json.loads(repaired)
        except (json.JSONDecodeError, JSONRepairError) as e:
            raise JSONProcessingError(f"Could not parse JSON even after repair: {e}")
    
    raise JSONProcessingError("Could not parse JSON")


def parse_and_validate(
    raw_input: str,
    model_class: Type[T],
    repair: bool = True,
    strict: bool = False
) -> T:
    """
    Parst JSON und validiert gegen ein Pydantic-Modell.
    
    Args:
        raw_input: Der zu parsende JSON-String
        model_class: Pydantic-Modellklasse für Validierung
        repair: Ob JSON-Reparatur versucht werden soll
        strict: Ob strikte Validierung angewendet werden soll
    
    Returns:
        Validierte Instanz des Pydantic-Modells
    
    Raises:
        JSONValidationError: Wenn Validierung fehlschlägt
    """
    try:
        data = parse_json(raw_input, repair=repair)
    except JSONProcessingError as e:
        raise JSONValidationError(f"JSON parsing failed: {e}")
    
    try:
        if strict:
            return model_class.model_validate(data, strict=True)
        else:
            return model_class.model_validate(data)
    except ValidationError as e:
        raise JSONValidationError(f"Pydantic validation failed: {e}")


def validate_tool_call(
    raw_json: str,
    tool_name: Optional[str] = None
) -> dict:
    """
    Validiert einen OpenClaw/Tool-Call JSON.
    
    Args:
        raw_json: Der Tool-Call JSON-String
        tool_name: Optionaler erwarteter Tool-Name
    
    Returns:
        Validiertes Tool-Call Dict
    """
    from pydantic import Field
    
    class ToolCall(BaseModel):
        tool: str = Field(..., description="Name of the tool to call")
        arguments: dict = Field(default_factory=dict, description="Tool arguments")
        reasoning: Optional[str] = Field(None, description="Optional reasoning")
    
    tool_call = parse_and_validate(raw_json, ToolCall, repair=True)
    
    if tool_name and tool_call.tool != tool_name:
        raise JSONValidationError(
            f"Expected tool '{tool_name}', got '{tool_call.tool}'"
        )
    
    return {
        "tool": tool_call.tool,
        "arguments": tool_call.arguments,
        "reasoning": tool_call.reasoning
    }


def safe_json_loads(
    raw_input: str,
    default: Any = None,
    repair: bool = True
) -> Any:
    """
    Sicheres JSON-Parsing mit Fallback auf Default-Wert.
    
    Args:
        raw_input: Der zu parsende JSON-String
        default: Rückgabewert bei Fehlschlag (default: None)
        repair: Ob Reparatur versucht werden soll
    
    Returns:
        Geparstes Objekt oder Default-Wert
    """
    try:
        return parse_json(raw_input, repair=repair)
    except JSONProcessingError:
        return default


def extract_json_from_text(text: str) -> list:
    """
    Extrahiert alle JSON-Objekte aus einem Text.
    
    Args:
        text: Text, der JSON-Objekte enthalten könnte
    
    Returns:
        Liste aller gefundenen und geparsten JSON-Objekte
    """
    import re
    
    results = []
    
    # Pattern für JSON-Objekte und Arrays
    patterns = [
        r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}',  # Objekte
        r'\[[^\[\]]*(?:\[[^\[\]*\][^\[\]]*)*\]',  # Arrays
    ]
    
    for pattern in patterns:
        for match in re.finditer(pattern, text):
            try:
                parsed = parse_json(match.group(), repair=True)
                results.append(parsed)
            except JSONProcessingError:
                continue
    
    return results


if __name__ == "__main__":
    # CLI-Interface
    import argparse
    
    parser = argparse.ArgumentParser(description="JSON Processor with repair")
    parser.add_argument("input", help="JSON string or file path")
    parser.add_argument("--file", "-f", action="store_true", help="Input is a file path")
    parser.add_argument("--repair", "-r", action="store_true", default=True, help="Enable JSON repair")
    parser.add_argument("--no-repair", dest="repair", action="store_false", help="Disable JSON repair")
    parser.add_argument("--pretty", "-p", action="store_true", help="Pretty print output")
    
    args = parser.parse_args()
    
    try:
        if args.file:
            content = Path(args.input).read_text()
        else:
            content = args.input
        
        result = parse_json(content, repair=args.repair)
        
        output = json.dumps(result, indent=2 if args.pretty else None, ensure_ascii=False)
        print(output)
        
    except JSONProcessingError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)
