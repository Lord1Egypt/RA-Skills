#!/usr/bin/env python3
"""Rules Loader — configuration-driven rule engine for GKN-Phantom v3.0.

Replaces hardcoded DetectionRule lists in vuln_detector.py with loadable
YAML/JSON config files from the ../rules/ directory. Supports:

  - YAML loading via PyYAML (preferred) or a built-in minimal YAML subset parser
  - JSON fallback for .json rule files
  - Hot-reload: watches rules directory for file mtime changes
  - Schema validation on load (required fields checked)
  - Multi-file merging (all .yaml/.yml/.json in rules/)
  - RuleRegistry class with typed query methods
  - Backward-compatible export to vuln_detector.py's DetectionRule dataclass format
  - CLI: --validate (validate all rule files), --export (export rules as JSON)

Usage:
  from rules_loader import RuleRegistry, load_rules

  registry = load_rules()                     # auto-load from ../rules/
  low_rules = registry.get_rules_by_tier("low")
  sqli_rules = registry.get_rules_by_type("sqli")
  all_rules = registry.get_all_rules()
  registry.reload()                           # force hot-reload

CLI:
  python rules_loader.py --validate
  python rules_loader.py --export --tier medium
  python rules_loader.py --validate --verbose
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Optional

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

REQUIRED_RULE_FIELDS = [
    "id",
    "type",
    "severity",
    "tier",
    "risk_level",
    "probe_description",
    "detection_signal",
]

VALID_TIERS = {"low", "medium", "high", "critical"}
VALID_SEVERITIES = {"low", "medium", "high", "critical", "info", "warning"}
VALID_RISK_LEVELS = {"L1", "L2", "L3", "L4"}

_RULES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "rules")


# ---------------------------------------------------------------------------
# Minimal YAML subset parser (fallback when PyYAML is unavailable)
# ---------------------------------------------------------------------------

class _MiniYAMLError(Exception):
    """Error during minimal YAML parsing."""
    pass


def _parse_minimal_yaml(text: str) -> list[dict]:
    """Parse a minimal YAML subset sufficient for GKN-Phantom rule files.

    Supports:
      - Top-level list of mappings (each starting with ``- ``
      - Scalar values: unquoted strings, single/double-quoted strings, integers,
        floats, booleans (true/false/yes/no)
      - Nested lists (inline ``[...]`` and indented ``- item``)
      - Simple inline mappings ``{key: value, ...}`` (single line only)
      - Comments (``#`` to end of line)

    Does NOT support:
      - Anchors / aliases (&anchor, *alias)
      - Multi-line values (|, >)
      - Flow-style nested structures beyond single-line
      - Tags (!tag)
    """
    lines = text.splitlines()
    entries: list[dict] = []
    current_entry: Optional[dict] = None
    current_key: Optional[str] = None
    current_list_key: Optional[str] = None  # key whose value is being built as a list
    in_list_value: bool = False
    base_indent: Optional[int] = None

    def _parse_scalar(val: str) -> Any:
        val = val.strip()
        # Quoted string
        if (val.startswith('"') and val.endswith('"')) or \
           (val.startswith("'") and val.endswith("'")):
            return val[1:-1]
        # null / ~
        if val in ("null", "~", ""):
            return None
        # Booleans
        if val.lower() in ("true", "yes"):
            return True
        if val.lower() in ("false", "no"):
            return False
        # Integer
        try:
            return int(val)
        except (ValueError, OverflowError):
            pass
        # Float
        try:
            return float(val)
        except (ValueError, OverflowError):
            pass
        return val

    def _get_indent(line: str) -> int:
        return len(line) - len(line.lstrip(" "))

    for raw_line in lines:
        line = raw_line.rstrip()
        # Skip empty lines and comment-only lines
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        # Skip document separators
        if line.strip() in ("---", "..."):
            # --- can also delimit start of a new entry if not first
            if current_entry is not None and line.strip() == "---":
                # Could be a document separator; finalize if needed
                pass
            continue

        stripped = line.strip()
        indent = _get_indent(line)

        if base_indent is None and stripped:
            base_indent = indent

        # Detect new list entry: "- key: value" or "- key:" or "- value"
        if stripped.startswith("- "):
            after_dash = stripped[2:].strip()
            # Same indent level as previous entries or initial
            is_new_entry = (base_indent is not None and indent <= base_indent) or \
                           (current_entry is None)
            if is_new_entry and not in_list_value:
                # Finalize previous entry
                if current_entry is not None:
                    entries.append(current_entry)
                if ":" in after_dash and not after_dash.startswith(("{", "[", '"', "'")):
                    # Key: value on same line
                    key, _, val = after_dash.partition(":")
                    key = key.strip()
                    val = val.strip()
                    current_entry = {}
                    if val:
                        # Check for inline list or mapping
                        if val.startswith("[") and val.endswith("]"):
                            current_entry[key] = _parse_inline_list(val)
                        elif val.startswith("{") and val.endswith("}"):
                            current_entry[key] = _parse_inline_mapping(val)
                        else:
                            current_entry[key] = _parse_scalar(val)
                    else:
                        # Value may follow on next line(s)
                        current_entry[key] = None
                        current_key = key
                    current_list_key = None
                    in_list_value = False
                elif ":" in after_dash:
                    # Could be a URL like "http://..." — treat as scalar
                    current_entry = {}
                    current_entry["_inline_"] = _parse_scalar(after_dash)
                    current_key = None
                    current_list_key = None
                    in_list_value = False
                else:
                    current_entry = {}
                    current_entry["_inline_"] = _parse_scalar(after_dash)
                    current_key = None
                    current_list_key = None
                    in_list_value = False
            else:
                # Sub-list item (indented under a key)
                if current_list_key and current_entry is not None:
                    val = after_dash
                    if val.startswith("{") and val.endswith("}"):
                        item = _parse_inline_mapping(val)
                    elif val.startswith("[") and val.endswith("]"):
                        item = _parse_inline_list(val)
                    else:
                        item = _parse_scalar(val)
                    if isinstance(current_entry.get(current_list_key), list):
                        current_entry[current_list_key].append(item)
                    else:
                        current_entry[current_list_key] = [item]
                in_list_value = True
            continue

        # Key: value line
        if ":" in stripped and not stripped.startswith("#"):
            key, _, val = stripped.partition(":")
            key = key.strip()

            # Skip if key looks like a URL
            if key.startswith("http://") or key.startswith("https://"):
                if current_entry is not None and current_key is not None:
                    current_entry[current_key] = _parse_scalar(stripped)
                    current_key = None
                continue

            val = val.strip()
            in_list_value = False
            list_indicator = False

            if not val:
                # Value follows on next lines
                if current_entry is None:
                    current_entry = {}
                current_entry[key] = None  # placeholder
                current_key = key
                current_list_key = None
                continue

            # Inline list: key: [item1, item2]
            if val.startswith("[") and val.endswith("]"):
                parsed = _parse_inline_list(val)
                if current_entry is not None:
                    current_entry[key] = parsed
                    current_key = None
                elif key == "id":
                    # Corner case: key is at document root
                    current_entry = {}
                    current_entry[key] = parsed
                continue

            # Inline mapping: key: {k: v, ...}
            if val.startswith("{") and val.endswith("}"):
                parsed = _parse_inline_mapping(val)
                if current_entry is not None:
                    current_entry[key] = parsed
                continue

            # Multiline list indicator: key followed by nothing on same line but
            # next non-empty line starts with "- "
            if current_entry is not None:
                current_entry[key] = _parse_scalar(val)
                current_key = key
                current_list_key = None
            continue

    # End of file: finalize last entry
    if current_entry is not None:
        entries.append(current_entry)

    return entries


def _parse_inline_list(val: str) -> list:
    """Parse an inline JSON-like list: [item1, item2, "item3"]."""
    val = val.strip()
    if not (val.startswith("[") and val.endswith("]")):
        return [_parse_scalar(val)]
    inner = val[1:-1].strip()
    if not inner:
        return []
    items = _split_csv(inner)
    return [_parse_scalar(item.strip()) for item in items]


def _parse_inline_mapping(val: str) -> dict:
    """Parse an inline JSON-like mapping: {key: value, ...}."""
    val = val.strip()
    if not (val.startswith("{") and val.endswith("}")):
        return {}
    inner = val[1:-1].strip()
    if not inner:
        return {}
    result = {}
    for pair in _split_csv(inner):
        if ":" in pair:
            k, _, v = pair.partition(":")
            result[k.strip()] = _parse_scalar(v.strip())
    return result


def _split_csv(text: str) -> list[str]:
    """Split a comma-separated string respecting quoted strings and nested braces."""
    result = []
    current = []
    depth = 0
    in_quote = False
    quote_char = None
    for ch in text:
        if ch in ('"', "'") and not in_quote:
            in_quote = True
            quote_char = ch
            current.append(ch)
        elif ch == quote_char and in_quote:
            in_quote = False
            quote_char = None
            current.append(ch)
        elif ch in ("{", "[") and not in_quote:
            depth += 1
            current.append(ch)
        elif ch in ("}", "]") and not in_quote:
            depth -= 1
            current.append(ch)
        elif ch == "," and depth == 0 and not in_quote:
            result.append("".join(current))
            current = []
        else:
            current.append(ch)
    if current:
        result.append("".join(current))
    return result


# ---------------------------------------------------------------------------
# DetectionRule dataclass (backward-compatible with vuln_detector.py)
# ---------------------------------------------------------------------------

@dataclass
class DetectionRule:
    """Declarative description of one detection probe.

    Backward-compatible with vuln_detector.py's DetectionRule, plus v5 fields.
    """

    type: str
    severity: str
    tier: str
    risk_level: str
    target_param_hints: list
    probe_description: str
    detection_signal: str
    safe_poc: bool = True
    requires_credentials: bool = False
    requires_human_approval: bool = False
    blocked_in_safe_mode: bool = False
    id: str = ""
    # v5 extended fields
    remediation: str = ""
    cvss_vector: str = ""
    references: list = None
    tags: list = None

    def __post_init__(self):
        if self.references is None:
            self.references = []
        if self.tags is None:
            self.tags = []

    def to_dict(self) -> dict:
        """Export to plain dict (for JSON serialization)."""
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "DetectionRule":
        """Create a DetectionRule from a plain dict."""
        return cls(
            id=d.get("id", ""),
            type=d.get("type", ""),
            severity=d.get("severity", "low"),
            tier=d.get("tier", "low"),
            risk_level=d.get("risk_level", "L1"),
            target_param_hints=d.get("target_param_hints", []),
            probe_description=d.get("probe_description", ""),
            detection_signal=d.get("detection_signal", ""),
            safe_poc=d.get("safe_poc", True),
            requires_credentials=d.get("requires_credentials", False),
            requires_human_approval=d.get("requires_human_approval", False),
            blocked_in_safe_mode=d.get("blocked_in_safe_mode", False),
            remediation=d.get("remediation", ""),
            cvss_vector=d.get("cvss_vector", ""),
            references=d.get("references", []),
            tags=d.get("tags", []),
        )


# ---------------------------------------------------------------------------
# Schema validation
# ---------------------------------------------------------------------------

class RuleValidationError(Exception):
    """A rule failed schema validation."""

    def __init__(self, messages: list[str]):
        self.messages = messages
        super().__init__("\n".join(messages))


def _validate_rule(rule: dict, source_file: str, index: int) -> list[str]:
    """Validate a single rule dict. Returns list of error messages (empty = valid)."""
    errors = []

    # Required fields
    for field in REQUIRED_RULE_FIELDS:
        if field not in rule or rule[field] is None:
            errors.append(
                f"[{source_file}:rule #{index}] Missing required field: '{field}'"
            )

    if errors:
        return errors

    # Type checks
    if not isinstance(rule.get("type"), str) or not rule["type"]:
        errors.append(
            f"[{source_file}:rule #{index}] 'type' must be a non-empty string"
        )

    if rule.get("tier") not in VALID_TIERS:
        errors.append(
            f"[{source_file}:rule #{index}] 'tier' must be one of {VALID_TIERS}, "
            f"got: {rule.get('tier')}"
        )

    if rule.get("severity") not in VALID_SEVERITIES:
        errors.append(
            f"[{source_file}:rule #{index}] 'severity' must be one of "
            f"{VALID_SEVERITIES}, got: {rule.get('severity')}"
        )

    if rule.get("risk_level") not in VALID_RISK_LEVELS:
        errors.append(
            f"[{source_file}:rule #{index}] 'risk_level' must be one of "
            f"{VALID_RISK_LEVELS}, got: {rule.get('risk_level')}"
        )

    if not isinstance(rule.get("target_param_hints"), list):
        errors.append(
            f"[{source_file}:rule #{index}] 'target_param_hints' must be a list"
        )

    if not isinstance(rule.get("probe_description"), str) or not rule["probe_description"]:
        errors.append(
            f"[{source_file}:rule #{index}] 'probe_description' must be a non-empty string"
        )

    if not isinstance(rule.get("detection_signal"), str) or not rule["detection_signal"]:
        errors.append(
            f"[{source_file}:rule #{index}] 'detection_signal' must be a non-empty string"
        )

    # Optional field type checks
    for bool_field in ("safe_poc", "requires_credentials", "requires_human_approval",
                        "blocked_in_safe_mode"):
        if bool_field in rule and not isinstance(rule[bool_field], bool):
            errors.append(
                f"[{source_file}:rule #{index}] '{bool_field}' must be a boolean"
            )

    # ID uniqueness tracked at registry level, not here

    return errors


# ---------------------------------------------------------------------------
# YAML / JSON loading
# ---------------------------------------------------------------------------

def _try_import_pyyaml():
    """Attempt to import PyYAML. Returns the yaml module or None."""
    try:
        import yaml
        return yaml
    except ImportError:
        return None


def _load_yaml_pyyaml(filepath: str) -> list[dict]:
    """Load YAML using PyYAML."""
    yaml = _try_import_pyyaml()
    if yaml is None:
        raise ImportError("PyYAML not available")
    with open(filepath, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if data is None:
        return []
    if isinstance(data, dict):
        # Some YAML files might wrap rules under a key
        for key in ("rules", "entries", "items"):
            if key in data and isinstance(data[key], list):
                return data[key]
        return [data]
    if isinstance(data, list):
        return data
    return []


def _load_json_rules(filepath: str) -> list[dict]:
    """Load rules from a JSON file."""
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for key in ("rules", "entries", "items"):
            if key in data and isinstance(data[key], list):
                return data[key]
        return [data]
    return []


def _load_yaml_minimal(filepath: str) -> list[dict]:
    """Load YAML using the built-in minimal parser."""
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()
    data = _parse_minimal_yaml(text)
    return data


def load_rules_file(filepath: str) -> list[dict]:
    """Load rules from a single file (.yaml, .yml, or .json).

    Tries PyYAML first; falls back to the minimal parser for .yaml/.yml,
    and to json.loads for .json.
    """
    ext = os.path.splitext(filepath)[1].lower()

    if ext == ".json":
        return _load_json_rules(filepath)

    if ext in (".yaml", ".yml"):
        yaml = _try_import_pyyaml()
        if yaml is not None:
            try:
                return _load_yaml_pyyaml(filepath)
            except Exception:
                pass  # fall through to minimal parser
        return _load_yaml_minimal(filepath)

    # Unknown extension: try all
    yaml = _try_import_pyyaml()
    if yaml is not None:
        try:
            return _load_yaml_pyyaml(filepath)
        except Exception:
            pass
    try:
        return _load_yaml_minimal(filepath)
    except Exception:
        pass
    try:
        return _load_json_rules(filepath)
    except Exception:
        pass

    raise ValueError(f"Unsupported file format: {filepath}")


# ---------------------------------------------------------------------------
# RuleRegistry
# ---------------------------------------------------------------------------

class RuleRegistry:
    """Central rule registry with typed query methods and hot-reload support.

    Usage::

        registry = RuleRegistry()
        registry.load_directory("../rules/")
        low_rules = registry.get_rules_by_tier("low")
        sqli_rules = registry.get_rules_by_type("sqli")
    """

    def __init__(self):
        self._rules: list[DetectionRule] = []
        self._rules_dir: Optional[str] = None
        self._file_mtimes: dict[str, float] = {}
        self._last_load_time: float = 0.0
        self._errors: list[str] = []
        self._yaml_available: bool = _try_import_pyyaml() is not None

    # ---- Properties ----------------------------------------------------------

    @property
    def rule_count(self) -> int:
        """Total number of loaded rules."""
        return len(self._rules)

    @property
    def errors(self) -> list[str]:
        """Validation / loading errors from the last load."""
        return list(self._errors)

    @property
    def yaml_available(self) -> bool:
        """Whether PyYAML is installed."""
        return self._yaml_available

    @property
    def last_load_time(self) -> float:
        """Unix timestamp of the last successful load."""
        return self._last_load_time

    # ---- Loading -------------------------------------------------------------

    def load_directory(self, rules_dir: Optional[str] = None) -> int:
        """Load and merge all rule files (.yaml/.yml/.json) from a directory.

        Args:
            rules_dir: Path to rules directory. Defaults to ../rules/ relative
                       to this script's location.

        Returns:
            Number of rules successfully loaded.
        """
        if rules_dir is None:
            rules_dir = _RULES_DIR

        self._rules_dir = os.path.abspath(rules_dir)
        self._errors = []

        if not os.path.isdir(self._rules_dir):
            self._errors.append(f"Rules directory not found: {self._rules_dir}")
            return 0

        all_rules: list[DetectionRule] = []
        seen_ids: set[str] = set()
        loaded_files = 0

        # Collect all .yaml, .yml, .json files
        rule_files = []
        for fname in sorted(os.listdir(self._rules_dir)):
            if fname.startswith("."):
                continue
            ext = os.path.splitext(fname)[1].lower()
            if ext in (".yaml", ".yml", ".json"):
                rule_files.append(os.path.join(self._rules_dir, fname))

        if not rule_files:
            self._errors.append(f"No rule files found in {self._rules_dir}")
            return 0

        for filepath in rule_files:
            try:
                raw_rules = load_rules_file(filepath)
                for i, raw in enumerate(raw_rules):
                    if not isinstance(raw, dict):
                        self._errors.append(
                            f"[{filepath}:entry #{i}] Not a mapping, skipping"
                        )
                        continue

                    # Validate
                    errs = _validate_rule(raw, os.path.basename(filepath), i + 1)
                    if errs:
                        self._errors.extend(errs)
                        continue

                    # Check duplicate ID
                    rid = raw.get("id", "")
                    if rid and rid in seen_ids:
                        self._errors.append(
                            f"[{filepath}:rule #{i + 1}] Duplicate rule ID: '{rid}'"
                        )
                        continue
                    if rid:
                        seen_ids.add(rid)

                    rule = DetectionRule.from_dict(raw)
                    all_rules.append(rule)

                loaded_files += 1

                # Record mtime for hot-reload
                self._file_mtimes[filepath] = os.path.getmtime(filepath)

            except Exception as exc:
                self._errors.append(f"[{filepath}] Load error: {exc}")

        self._rules = all_rules
        self._last_load_time = time.time()
        return len(self._rules)

    def reload(self, force: bool = False) -> int:
        """Reload rules from the same directory if any file has changed.

        Args:
            force: If True, reload even if no mtime changes detected.

        Returns:
            Number of rules loaded, or -1 if no directory was previously loaded.
        """
        if not self._rules_dir:
            return -1

        if not force:
            # Check for mtime changes
            changed = False
            for filepath, old_mtime in self._file_mtimes.items():
                if not os.path.exists(filepath):
                    changed = True
                    break
                if os.path.getmtime(filepath) != old_mtime:
                    changed = True
                    break
            # Also check for new files
            for fname in os.listdir(self._rules_dir):
                ext = os.path.splitext(fname)[1].lower()
                if ext in (".yaml", ".yml", ".json"):
                    full = os.path.join(self._rules_dir, fname)
                    if full not in self._file_mtimes:
                        changed = True
                        break

            if not changed:
                return len(self._rules)

        return self.load_directory(self._rules_dir)

    def is_stale(self) -> bool:
        """Check whether any rule file has been modified since last load."""
        if not self._rules_dir:
            return False
        for filepath, old_mtime in self._file_mtimes.items():
            if not os.path.exists(filepath):
                return True
            if os.path.getmtime(filepath) != old_mtime:
                return True
        # Check for new files
        try:
            for fname in os.listdir(self._rules_dir):
                ext = os.path.splitext(fname)[1].lower()
                if ext in (".yaml", ".yml", ".json"):
                    full = os.path.join(self._rules_dir, fname)
                    if full not in self._file_mtimes:
                        return True
        except OSError:
            return True
        return False

    # ---- Query methods -------------------------------------------------------

    def get_all_rules(self) -> list[DetectionRule]:
        """Return all loaded rules."""
        return list(self._rules)

    def get_rules_by_tier(self, tier: str) -> list[DetectionRule]:
        """Return rules filtered by tier (low/medium/high/critical)."""
        tier = tier.lower()
        return [r for r in self._rules if r.tier == tier]

    def get_rules_by_type(self, vuln_type: str) -> list[DetectionRule]:
        """Return rules filtered by vulnerability type."""
        return [r for r in self._rules if r.type == vuln_type]

    def get_rules_by_severity(self, severity: str) -> list[DetectionRule]:
        """Return rules filtered by severity."""
        severity = severity.lower()
        return [r for r in self._rules if r.severity == severity]

    def get_rules_by_risk_level(self, risk_level: str) -> list[DetectionRule]:
        """Return rules filtered by risk level (L1-L4)."""
        return [r for r in self._rules if r.risk_level == risk_level]

    def get_rules_by_tag(self, tag: str) -> list[DetectionRule]:
        """Return rules that have the given tag."""
        return [r for r in self._rules if tag in (r.tags or [])]

    def get_rule_by_id(self, rule_id: str) -> Optional[DetectionRule]:
        """Return a single rule by its id, or None."""
        for r in self._rules:
            if r.id == rule_id:
                return r
        return None

    def get_vuln_types(self) -> list[str]:
        """Return sorted list of all unique vulnerability types loaded."""
        return sorted(set(r.type for r in self._rules))

    def get_tiers(self) -> list[str]:
        """Return sorted list of all tiers present."""
        return sorted(set(r.tier for r in self._rules))

    # ---- Export --------------------------------------------------------------

    def export_rules(self, tier: Optional[str] = None,
                     vuln_type: Optional[str] = None,
                     as_detection_rule: bool = False) -> list[dict]:
        """Export rules as dicts (or DetectionRule dataclass instances).

        Args:
            tier: Optional tier filter.
            vuln_type: Optional vulnerability type filter.
            as_detection_rule: If True, return DetectionRule instances.

        Returns:
            List of rule dicts or DetectionRule objects.
        """
        rules = self._rules
        if tier:
            rules = [r for r in rules if r.tier == tier]
        if vuln_type:
            rules = [r for r in rules if r.type == vuln_type]

        if as_detection_rule:
            return rules
        return [r.to_dict() for r in rules]

    def export_as_json(self, tier: Optional[str] = None,
                       vuln_type: Optional[str] = None,
                       indent: int = 2) -> str:
        """Export rules as a JSON string."""
        return json.dumps(self.export_rules(tier=tier, vuln_type=vuln_type),
                          ensure_ascii=False, indent=indent)

    def to_backward_compatible(self, tier: Optional[str] = None) -> list:
        """Export in the exact format used by vuln_detector.py's TIER_RULES.

        Returns a list of DetectionRule objects (compatible with the dataclass
        in vuln_detector.py), suitable for passing to build_plan() etc.
        """
        return self.export_rules(tier=tier, as_detection_rule=True)

    # ---- Stats ---------------------------------------------------------------

    def get_stats(self) -> dict:
        """Return a summary dict of the loaded rules."""
        tiers = {}
        types = {}
        severities = {}
        for r in self._rules:
            tiers[r.tier] = tiers.get(r.tier, 0) + 1
            types[r.type] = types.get(r.type, 0) + 1
            severities[r.severity] = severities.get(r.severity, 0) + 1
        return {
            "total_rules": len(self._rules),
            "rules_dir": self._rules_dir,
            "yaml_available": self._yaml_available,
            "last_load_time": self._last_load_time,
            "by_tier": tiers,
            "by_type": types,
            "by_severity": severities,
            "validation_errors": len(self._errors),
        }


# ---------------------------------------------------------------------------
# Convenience function
# ---------------------------------------------------------------------------

_registry: Optional[RuleRegistry] = None


def load_rules(rules_dir: Optional[str] = None, auto_reload: bool = False) -> RuleRegistry:
    """Load or return the cached RuleRegistry.

    Args:
        rules_dir: Optional override for the rules directory.
        auto_reload: If True, check for stale files and reload if needed.

    Returns:
        A RuleRegistry instance with rules loaded.
    """
    global _registry
    if _registry is None:
        _registry = RuleRegistry()
        _registry.load_directory(rules_dir)
    elif auto_reload and _registry.is_stale():
        _registry.reload()
    elif rules_dir is not None:
        _registry.load_directory(rules_dir)
    return _registry


def reset_registry():
    """Clear the cached registry (useful for testing)."""
    global _registry
    _registry = None


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(
        description="GKN-Phantom Rules Loader — validate, query, and export rules"
    )
    ap.add_argument(
        "--rules-dir",
        default=None,
        help="Path to rules directory (default: ../rules/ relative to this script)",
    )
    ap.add_argument(
        "--validate",
        action="store_true",
        help="Validate all rule files and report errors",
    )
    ap.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output",
    )
    ap.add_argument(
        "--export",
        action="store_true",
        help="Export rules as JSON to stdout",
    )
    ap.add_argument(
        "--tier",
        default=None,
        help="Filter by tier (low/medium/high/critical) for --export",
    )
    ap.add_argument(
        "--type",
        default=None,
        dest="vuln_type",
        help="Filter by vulnerability type for --export",
    )
    ap.add_argument(
        "--stats",
        action="store_true",
        help="Print rule statistics",
    )
    ap.add_argument(
        "--list-types",
        action="store_true",
        help="List all unique vulnerability types",
    )
    ap.add_argument(
        "--list-tiers",
        action="store_true",
        help="List all tiers",
    )

    args = ap.parse_args()

    registry = load_rules(args.rules_dir)

    exit_code = 0

    if args.validate:
        if registry.errors:
            print(f"VALIDATION FAILED — {len(registry.errors)} error(s):", file=sys.stderr)
            for err in registry.errors:
                print(f"  {err}", file=sys.stderr)
            exit_code = 1
        else:
            print(f"VALIDATION PASSED — {registry.rule_count} rules loaded successfully")
            if args.verbose:
                print(f"  Rules directory: {registry._rules_dir}")
                print(f"  PyYAML available: {registry.yaml_available}")

    if args.stats:
        stats = registry.get_stats()
        print(json.dumps(stats, indent=2, ensure_ascii=False))

    if args.list_types:
        print("\n".join(registry.get_vuln_types()))

    if args.list_tiers:
        print("\n".join(registry.get_tiers()))

    if args.export:
        print(registry.export_as_json(tier=args.tier, vuln_type=args.vuln_type))

    # Print errors if any occurred but --validate wasn't explicitly used
    if not args.validate and registry.errors:
        print(f"WARNING: {len(registry.errors)} validation error(s) during load:",
              file=sys.stderr)
        for err in registry.errors[:10]:
            print(f"  {err}", file=sys.stderr)

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
