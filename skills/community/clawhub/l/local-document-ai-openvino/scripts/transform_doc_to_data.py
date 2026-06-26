#!/usr/bin/env python3
"""
transform_doc_to_data.py

Turn canonical parsed document JSON into machine-readable extraction artifacts.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path

from data_enrichment import (
    build_entity_traceability,
    build_kv_traceability,
    build_record_summary,
    canonicalize_key,
    combine_entities,
    export_tables,
    extract_kv_pairs,
    summarize_document,
)
from utils import ensure_dir, load_json, validate_document_schema, write_error, write_json


SUPPORTED_EXTRACTS = {"tables", "entities", "kv_pairs"}


@dataclass
class Config:
    parsed_json: Path
    out: Path
    extracts: set[str]
    fields: list[str]
    debug: bool = False


def parse_args() -> Config:
    parser = argparse.ArgumentParser(description="Generate data-oriented artifacts from parsed document JSON.")
    parser.add_argument("--parsed-json", required=True, help="Path to parsed.json")
    parser.add_argument("--out", required=True, help="Output task directory")
    parser.add_argument(
        "--extract",
        default="tables,entities,kv_pairs",
        help="Comma-separated extracts: tables,entities,kv_pairs",
    )
    parser.add_argument(
        "--fields",
        default="",
        help="Comma-separated custom key fields to extract, such as invoice_number,total_amount,invoice_date",
    )
    parser.add_argument("--debug", action="store_true")
    ns = parser.parse_args()

    extracts = {item.strip() for item in ns.extract.split(",") if item.strip()}
    fields = [item.strip() for item in ns.fields.split(",") if item.strip()]
    invalid = extracts - SUPPORTED_EXTRACTS
    if invalid:
        raise SystemExit(f"Unsupported extract types: {sorted(invalid)}")

    return Config(
        parsed_json=Path(ns.parsed_json).expanduser().resolve(),
        out=Path(ns.out).expanduser().resolve(),
        extracts=extracts,
        fields=fields,
        debug=ns.debug,
    )


def build_requested_field_outputs(
    requested_fields: list[str],
    field_map: dict[str, list[dict[str, object]]],
) -> tuple[dict[str, object], dict[str, object]]:
    verbose: dict[str, object] = {
        "requested_fields": requested_fields,
        "results": [],
    }
    compact: dict[str, object] = {}

    for field_name in requested_fields:
        canonical_key, inferred_type = canonicalize_key(field_name)
        matches = list(field_map.get(canonical_key, []))
        primary = matches[0] if matches else None
        result = {
            "requested_field": field_name,
            "canonical_key": canonical_key,
            "inferred_value_type": inferred_type,
            "found": bool(matches),
            "match_count": len(matches),
            "primary": primary,
            "matches": matches,
        }
        cast_results = verbose["results"]
        assert isinstance(cast_results, list)
        cast_results.append(result)
        compact[field_name] = primary

    return verbose, compact


def main() -> int:
    config = parse_args()
    ensure_dir(config.out)

    try:
        if not config.parsed_json.exists():
            raise FileNotFoundError(f"parsed.json not found: {config.parsed_json}")

        document = load_json(config.parsed_json)
        problems = validate_document_schema(document)
        if problems:
            raise ValueError("Invalid parsed.json: " + "; ".join(problems))

        generated_files: list[str] = []
        traceability_rows: list[dict[str, object]] = []

        normalized: dict[str, object] = {
            "summary": summarize_document(document),
            "requested_extracts": sorted(config.extracts),
            "outputs": {},
        }

        kv_pairs, embedded_tables = extract_kv_pairs(document)
        entities = combine_entities(document, kv_pairs)
        table_index: list[dict[str, object]] = []

        if "entities" in config.extracts:
            write_json(config.out / "entities.json", entities)
            normalized["outputs"]["entities"] = {"count": len(entities), "path": "entities.json"}
            generated_files.append("entities.json")
            traceability_rows.extend(build_entity_traceability(entities))

        if "kv_pairs" in config.extracts:
            write_json(config.out / "kv_pairs.json", kv_pairs)
            normalized["outputs"]["kv_pairs"] = {"count": len(kv_pairs), "path": "kv_pairs.json"}
            generated_files.append("kv_pairs.json")
            traceability_rows.extend(build_kv_traceability(kv_pairs))

        if "tables" in config.extracts:
            table_index, table_trace = export_tables(document, embedded_tables, config.out)
            write_json(config.out / "table_index.json", table_index)
            normalized["outputs"]["tables"] = {
                "count": len(table_index),
                "index_path": "table_index.json",
                "combined_csv_path": "tables.csv",
                "directory": "tables/",
            }
            generated_files.extend(["table_index.json", "tables.csv"])
            traceability_rows.extend(table_trace)

        document_profile = build_record_summary(document, kv_pairs, entities, table_index, embedded_tables)
        structured_record = document_profile.get("structured_record", {})
        normalized["document_profile"] = document_profile
        normalized["structured_record"] = structured_record

        if config.fields:
            field_map = document_profile.get("field_map", {})
            if not isinstance(field_map, dict):
                field_map = {}
            requested_fields, requested_record = build_requested_field_outputs(config.fields, field_map)
            write_json(config.out / "requested_fields.json", requested_fields)
            write_json(config.out / "requested_fields_record.json", requested_record)
            normalized["requested_fields"] = {
                "requested": config.fields,
                "path": "requested_fields.json",
                "record_path": "requested_fields_record.json",
            }
            generated_files.extend(["requested_fields.json", "requested_fields_record.json"])

        write_json(config.out / "normalized.json", normalized)
        write_json(config.out / "structured_record.json", structured_record)
        write_json(
            config.out / "traceability.json",
            {
                "artifact": "task_output/normalized.json",
                "mappings": traceability_rows,
            },
        )

        generated_files.extend(["normalized.json", "structured_record.json", "traceability.json"])

        print(
            json.dumps(
                {
                    "ok": True,
                    "parsed_json": str(config.parsed_json),
                    "output_dir": str(config.out),
                    "generated_files": generated_files,
                    "requested_extracts": sorted(config.extracts),
                    "requested_fields": config.fields,
                    "traceability_count": len(traceability_rows),
                    "document_type": document_profile.get("document_type"),
                    "document_subtype": document_profile.get("document_subtype"),
                },
                ensure_ascii=False,
            )
        )
        return 0

    except Exception as exc:
        write_error(
            config.out,
            stage="transform_doc_to_data",
            message=str(exc),
            parsed_json=str(config.parsed_json),
            extracts=sorted(config.extracts),
            fields=config.fields,
        )
        print(
            json.dumps(
                {
                    "ok": False,
                    "stage": "transform_doc_to_data",
                    "message": str(exc),
                    "parsed_json": str(config.parsed_json),
                    "output_dir": str(config.out),
                },
                ensure_ascii=False,
            ),
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
