"""
config_validator.py - Configuration Validation for KWDB Data Migration

Validates all migration parameters before API calls. Ensures source type support,
required field presence, and compatibility between source and target configurations.

Key validations:
- Source type against 14 supported types
- Source capability against requested operation
- Required fields presence
- Target must be KAIWUDB
"""

from typing import Dict, List, Any, Optional
import re
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)


# Supported source types with their capabilities
# Based on KDTS SourceTypes.java implementation
SOURCE_TYPE_CAPABILITIES = {
    # (engine, supports_full_migration, supports_metadata, note)
    "MYSQL":         ("RELATIONAL", True, True, "Full migration supported"),
    "ORACLE":        ("RELATIONAL", True, True, "Full migration supported"),
    "POSTGRESQL":    ("RELATIONAL", True, True, "Full migration supported"),
    "SQLSERVER":     ("RELATIONAL", False, True, "Metadata + Data, no full migration"),
    "CLICKHOUSE":    ("RELATIONAL", True, False, "Full migration, no metadata"),
    "KAIWUDB":       (None, False, False, "Only supports data migration (as source)"),
    "TDENGINE3X":    ("TIMESERIES", True, True, "Full migration supported"),
    "TDENGINE2X":    ("TIMESERIES", False, False, "Only supports data migration"),
    "INFLUXDB1X":    ("TIMESERIES", False, True, "Metadata + Data, no full migration"),
    "INFLUXDB2X":    ("TIMESERIES", False, True, "Metadata + Data, no full migration"),
    "OPENTSDB":      ("TIMESERIES", False, False, "Only supports data migration"),
    "MONGODB":       ("TIMESERIES", False, False, "Only supports data migration"),
    "FTP":           ("TIMESERIES", False, False, "Only supports data migration"),
    "HDFS":          ("TIMESERIES", False, False, "Only supports data migration"),
}

# Target must be KAIWUDB
TARGET_ONLY_TYPES = {"KAIWUDB"}

# Required fields for source config (engine is REQUIRED per KDTS API)
SOURCE_REQUIRED_FIELDS = ["engine", "type", "host", "port", "username", "password"]
SOURCE_REQUIRED_FIELDS_WITH_DB = SOURCE_REQUIRED_FIELDS + ["dbName"]

# Required fields for target config (engine is required)
TARGET_REQUIRED_FIELDS = ["engine", "type", "host", "port", "username", "password"]
TARGET_REQUIRED_FIELDS_WITH_DB = TARGET_REQUIRED_FIELDS + ["dbName"]


class ConfigValidator:
    """
    Validates migration configurations before API calls.
    """

    @staticmethod
    def validate_source_type(source_type: str) -> Dict[str, Any]:
        """
        Check if source type is supported.

        Args:
            source_type: Source type string (e.g., MYSQL, ORACLE, KAIWUDB)

        Returns:
            Validation result dict: {valid, type, capabilities, message}
        """
        source_type_upper = source_type.upper()

        if source_type_upper not in SOURCE_TYPE_CAPABILITIES:
            supported = ", ".join(sorted(SOURCE_TYPE_CAPABILITIES.keys()))
            return {
                "valid": False,
                "type": source_type,
                "capabilities": None,
                "message": f"Unsupported source type '{source_type}'. Supported types: {supported}"
            }

        engine, supports_full, supports_meta, note = SOURCE_TYPE_CAPABILITIES[source_type_upper]
        return {
            "valid": True,
            "type": source_type_upper,
            "capabilities": {
                "engine": engine,
                "supports_full_migration": supports_full,
                "supports_metadata": supports_meta,
                "note": note
            },
            "message": f"Source type '{source_type_upper}' is supported. Engine: {engine}"
        }

    @staticmethod
    def validate_source_config(config: Dict, require_db: bool = True) -> Dict[str, Any]:
        """
        Validate complete source configuration.

        Note: engine is REQUIRED per KDTS API specification.
        Use SourceType.get_engine(source_type) to determine the correct engine value.

        Args:
            config: DataSource config dict (must include 'engine' field)
            require_db: If True, dbName is required

        Returns:
            Validation result dict: {valid, missing_fields, message}
        """
        errors = []
        missing = []

        # Check source type
        if "type" not in config:
            errors.append("Missing required field: type")
        else:
            type_result = ConfigValidator.validate_source_type(config["type"])
            if not type_result["valid"]:
                errors.append(type_result["message"])

        # Check engine
        if "engine" not in config:
            errors.append("Missing required field: engine (RELATIONAL or TIMESERIES)")
        elif config["engine"] not in ("RELATIONAL", "TIMESERIES"):
            errors.append(f"Invalid engine: {config['engine']}. Must be RELATIONAL or TIMESERIES")

        # Check required fields
        required = SOURCE_REQUIRED_FIELDS_WITH_DB if require_db else SOURCE_REQUIRED_FIELDS
        for field in required:
            if field not in config or config[field] is None or config[field] == "":
                missing.append(field)

        # Check URL or host:port
        if "url" not in config and ("host" in missing or "port" in missing):
            errors.append("Either 'url' or 'host'+'port' must be provided")

        if missing:
            errors.append(f"Missing fields: {', '.join(missing)}")

        return {
            "valid": len(errors) == 0,
            "missing_fields": missing,
            "errors": errors,
            "message": "Validation passed" if len(errors) == 0 else "; ".join(errors)
        }

    @staticmethod
    def validate_target_config(config: Dict) -> Dict[str, Any]:
        """
        Validate target configuration (must be KAIWUDB).

        Args:
            config: Target DataSource config dict

        Returns:
            Validation result dict
        """
        errors = []

        # Target type must be KAIWUDB
        if "type" not in config:
            errors.append("Missing required field: type (must be KAIWUDB)")
        elif config["type"].upper() != "KAIWUDB":
            errors.append(f"Target type must be KAIWUDB, got '{config['type']}'")

        # Check engine
        if "engine" not in config:
            errors.append("Missing required field: engine (RELATIONAL or TIMESERIES)")
        elif config["engine"] not in ("RELATIONAL", "TIMESERIES"):
            errors.append(f"Invalid engine: {config['engine']}. Must be RELATIONAL or TIMESERIES")

        # Check required fields
        required = TARGET_REQUIRED_FIELDS_WITH_DB
        missing = [f for f in required if f not in config or config[f] is None or config[f] == ""]
        if missing:
            errors.append(f"Missing fields: {', '.join(missing)}")

        return {
            "valid": len(errors) == 0,
            "missing_fields": missing,
            "errors": errors,
            "message": "Target validation passed" if len(errors) == 0 else "; ".join(errors)
        }

    @staticmethod
    def validate_table_mapping(source_type: str, table_mapping: Dict) -> Dict[str, Any]:
        """
        Validate table mapping configuration.

        Args:
            source_type: KDTS source type
            table_mapping: TableMapping dict with source/target keys

        Returns:
            Validation result dict
        """
        errors = []

        if "source" not in table_mapping:
            errors.append("Missing 'source' in table mapping")
        else:
            src = table_mapping["source"]
            if "table" not in src:
                errors.append("Missing 'table' in source mapping")
            if "sourceType" not in src:
                errors.append("Missing 'sourceType' in source mapping")

        if "target" not in table_mapping:
            errors.append("Missing 'target' in table mapping")
        else:
            tgt = table_mapping["target"]
            if "table" not in tgt:
                errors.append("Missing 'table' in target mapping")
            if tgt.get("sourceType", "").upper() != "KAIWUDB":
                errors.append("Target sourceType must be KAIWUDB")

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "message": "Table mapping valid" if len(errors) == 0 else "; ".join(errors)
        }

    @staticmethod
    def validate_full_migration_capable(source_type: str) -> Dict[str, Any]:
        """
        Check if source supports full migration (structure + data, all tables).

        Args:
            source_type: Source type string

        Returns:
            Result dict with capability info
        """
        result = ConfigValidator.validate_source_type(source_type)
        if not result["valid"]:
            return result

        if not result["capabilities"]["supports_full_migration"]:
            note = result["capabilities"]["note"]
            return {
                "valid": False,
                "type": source_type,
                "message": f"Source type '{source_type}' does NOT support full database migration. {note or 'Use table-level migration with explicit table mappings.'}"
            }

        return {
            "valid": True,
            "type": source_type,
            "message": f"Source type '{source_type}' supports full database migration."
        }

    @staticmethod
    def validate_metadata_capable(source_type: str) -> Dict[str, Any]:
        """
        Check if source supports metadata reading (for DDL preview).

        Args:
            source_type: Source type string

        Returns:
            Result dict with capability info
        """
        result = ConfigValidator.validate_source_type(source_type)
        if not result["valid"]:
            return result

        if not result["capabilities"]["supports_metadata"]:
            return {
                "valid": False,
                "type": source_type,
                "message": f"Source type '{source_type}' does NOT support metadata reading. DDL preview/auto-generate is not available."
            }

        return {
            "valid": True,
            "type": source_type,
            "message": f"Source type '{source_type}' supports metadata reading."
        }

    @staticmethod
    def get_supported_types() -> List[str]:
        """
        Get list of all supported source types.

        Returns:
            Sorted list of source type strings.
        """
        return sorted(SOURCE_TYPE_CAPABILITIES.keys())

    @staticmethod
    def get_type_capabilities_table() -> str:
        """
        Generate formatted capabilities table for display.

        Returns:
            Markdown-formatted table string.
        """
        lines = [
            "| Source Type | Engine | Full Migration | Metadata | Note |",
            "|-------------|--------|---------------|----------|------|"
        ]
        for stype, (engine, full, meta, note) in sorted(SOURCE_TYPE_CAPABILITIES.items()):
            full_str = "Yes" if full else "No"
            meta_str = "Yes" if meta else "No"
            note_str = note or "-"
            lines.append(f"| {stype} | {engine} | {full_str} | {meta_str} | {note_str} |")

        return "\n".join(lines)


# Convenience functions for common validation patterns

def quick_validate(source_config: Dict, target_config: Dict) -> Dict[str, Any]:
    """
    Quick validation of source and target configurations.

    Args:
        source_config: Source DataSource config
        target_config: Target DataSource config

    Returns:
        Combined validation result
    """
    source_result = ConfigValidator.validate_source_config(source_config)
    target_result = ConfigValidator.validate_target_config(target_config)

    all_errors = source_result.get("errors", []) + target_result.get("errors", [])

    return {
        "valid": len(all_errors) == 0,
        "source_valid": source_result["valid"],
        "target_valid": target_result["valid"],
        "errors": all_errors,
        "source_capabilities": ConfigValidator.validate_source_type(
            source_config.get("type", "")
        ).get("capabilities"),
        "message": "All validations passed" if len(all_errors) == 0 else "; ".join(all_errors)
    }


if __name__ == "__main__":
    # Quick test
    print("=== Supported Source Types ===")
    print(ConfigValidator.get_type_capabilities_table())
    print()

    test_configs = [
        {"engine": "RELATIONAL", "type": "MYSQL", "host": "127.0.0.1", "port": 3306,
         "username": "root", "password": "123456", "dbName": "test"},
        {"engine": "RELATIONAL", "type": "SQLSERVER", "host": "127.0.0.1", "port": 1433,
         "username": "sa", "password": "pass", "dbName": "test"},
        {"engine": "RELATIONAL", "type": "INVALID_DB", "host": "127.0.0.1", "port": 1234,
         "username": "u", "password": "p", "dbName": "test"},
    ]

    for i, config in enumerate(test_configs, 1):
        result = ConfigValidator.validate_source_config(config)
        print(f"\n=== Test {i}: {config.get('type', 'N/A')} ===")
        print(f"  Valid: {result['valid']}")
        print(f"  Message: {result['message']}")
