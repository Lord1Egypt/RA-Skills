"""Domain operations for Ovitalmap parcel archives."""

import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from archive_store import ArchiveStore, COUNTRY_HEADERS
from utils import (
    boundaries_equal,
    build_boundary_string,
    get_workspace_root,
    parse_boundary_coords,
    read_json_stdin,
    validate_coordinates,
    validate_country_code,
    validate_identifier,
    write_json_stdout,
)


STORE = ArchiveStore(get_workspace_root())


def scan_archive(country_code, date_hint=None):
    code = validate_country_code(country_code)
    date_token = str(date_hint or datetime.now().strftime("%y%m%d"))
    if len(date_token) != 6 or not date_token.isdigit():
        raise ValueError("date must use YYMMDD format")

    _, rows = STORE.read_country(code)
    codes = [row.get("parcel_code", "") for row in rows]
    prefix = f"{code}-{date_token}-"
    sequences = [
        int(parcel_code[len(prefix):])
        for parcel_code in codes
        if parcel_code.startswith(prefix)
        and parcel_code[len(prefix):].isdigit()
    ]
    providers = sorted(
        {
            row.get("provider_name", "").strip()
            for row in rows
            if row.get("provider_name", "").strip().lower() not in {"", "unknown"}
        }
    )
    return {
        "all_codes": codes,
        "today_max_seq": max(sequences, default=0),
        "all_providers": providers,
        "archive_exists": STORE.country_path(code).exists(),
    }


def _validate_archive_row(row):
    code = str(row.get("parcel_code", "")).strip()
    if not code or len(code) > 120 or any(char in code for char in "/\\\r\n,"):
        raise ValueError("Invalid parcel_code")
    provider = str(row.get("provider_name") or "").strip()
    if not provider:
        raise ValueError(f"{code}: provider_name is required")

    vertices = parse_boundary_coords(str(row.get("boundary_coords") or ""))
    errors = validate_coordinates(vertices, require_polygon=True)
    if errors:
        raise ValueError(f"{code}: {'; '.join(errors)}")

    validated = {header: row.get(header, "") for header in COUNTRY_HEADERS}
    validated.update(
        {
            "parcel_code": code,
            "provider_name": provider,
            "boundary_coords": build_boundary_string(vertices),
        }
    )
    return validated


def _same_code(rows, parcel_code):
    return next(
        (row for row in rows if row.get("parcel_code") == parcel_code),
        None,
    )


def _same_boundary(rows, boundary, excluded_code=None):
    return next(
        (
            row
            for row in rows
            if row.get("parcel_code") != excluded_code
            and boundaries_equal(row.get("boundary_coords", ""), boundary)
        ),
        None,
    )


def append_parcels(country_code, rows):
    """Append new rows once; reject conflicting codes or boundaries."""
    code = validate_country_code(country_code)
    if not isinstance(rows, list) or not rows:
        raise ValueError("rows must be a non-empty list")
    validated_rows = [_validate_archive_row(row) for row in rows]

    with STORE.locked():
        _, country_rows = STORE.read_country(code)
        _, master_rows = STORE.read_master()
        appended = []
        idempotent = []

        for source, row in zip(rows, validated_rows):
            existing_code = _same_code(country_rows, row["parcel_code"])
            if existing_code:
                if boundaries_equal(
                    existing_code.get("boundary_coords", ""),
                    row["boundary_coords"],
                ):
                    idempotent.append(row["parcel_code"])
                    continue
                raise ValueError(f"parcel_code already exists: {row['parcel_code']}")

            existing_boundary = _same_boundary(country_rows, row["boundary_coords"])
            if existing_boundary and not source.get("allow_duplicate_coordinates"):
                raise ValueError(
                    "Coordinates already archived as "
                    f"{existing_boundary.get('parcel_code', '')}"
                )

            country_rows.append(row)
            master_rows.append({"CC": code, **row})
            appended.append(row["parcel_code"])

        if appended:
            STORE.commit(code, country_rows, master_rows)

    return {
        "country_archive": str(STORE.country_path(code)),
        "master_archive": str(STORE.master_path),
        "rows_appended": len(appended),
        "appended_codes": appended,
        "idempotent_codes": idempotent,
    }


def check_duplicate(country_code, new_vertices):
    code = validate_country_code(country_code)
    errors = validate_coordinates(new_vertices, require_polygon=True)
    if errors:
        raise ValueError("; ".join(errors))

    _, rows = STORE.read_country(code)
    boundary = build_boundary_string(new_vertices)
    row = _same_boundary(rows, boundary)
    if not row:
        return {"match_found": False}
    return {
        "match_found": True,
        "matched_code": row.get("parcel_code", ""),
        "matched_provider": row.get("provider_name", ""),
        "matched_cadastre_code": row.get("cadastre_code", ""),
        "matched_archive_date": row.get("archive_date", ""),
        "matched_boundary": row.get("boundary_coords", ""),
    }


def _find_archive_row(country_code, parcel_code):
    _, rows = STORE.read_country(country_code)
    return _same_code(rows, parcel_code)


def extract_single(
    country_code,
    parcel_code,
    resolved_provider_name=None,
    archive_date=None,
    cadastre_code=None,
    export_mode="boundary",
):
    code = validate_country_code(country_code)
    row = _find_archive_row(code, parcel_code)
    if not row:
        return {"found": False, "error": f"Parcel not found: {parcel_code}"}

    from csv_builder import build_single_csvs

    parcel = {
        "parcel_code": row["parcel_code"],
        "vertices": parse_boundary_coords(row["boundary_coords"]),
        "resolved_provider_name": resolved_provider_name or row["provider_name"],
        "archive_date": archive_date or row["archive_date"],
        "cadastre_code": cadastre_code or row.get("cadastre_code", ""),
    }
    return {
        "found": True,
        "parcel_code": parcel_code,
        **build_single_csvs(parcel, code, export_mode),
    }


def _paired_rows(country_rows, master_rows, country_code, parcel_code):
    country_row = _same_code(country_rows, parcel_code)
    master_row = next(
        (
            row
            for row in master_rows
            if row.get("CC") == country_code
            and row.get("parcel_code") == parcel_code
        ),
        None,
    )
    if not country_row or not master_row:
        raise ValueError("Parcel must exist in both country and master archives")
    return country_row, master_row


def update_cadastre(
    country_code,
    parcel_code,
    cadastre_code,
    replace_existing=False,
):
    code = validate_country_code(country_code)
    cadastre_code = validate_identifier(cadastre_code, "cadastre_code")
    with STORE.locked():
        _, country_rows = STORE.read_country(code)
        _, master_rows = STORE.read_master()
        country_row, master_row = _paired_rows(
            country_rows,
            master_rows,
            code,
            parcel_code,
        )
        old_value = country_row.get("cadastre_code", "")
        if old_value == cadastre_code:
            return {
                "parcel_code": parcel_code,
                "cadastre_code": cadastre_code,
                "updated_country": False,
                "updated_master": False,
                "idempotent": True,
            }
        if old_value and not replace_existing:
            raise ValueError(
                f"cadastre_code is already {old_value}; confirmation is required to replace it"
            )

        note = f"Cadastre updated: {old_value or '(empty)'} → {cadastre_code}"
        for row in (country_row, master_row):
            row["cadastre_code"] = cadastre_code
            row["provider_notes"] = _append_note(row, note)
        STORE.commit(code, country_rows, master_rows)

    return {
        "parcel_code": parcel_code,
        "cadastre_code": cadastre_code,
        "updated_country": True,
        "updated_master": True,
        "idempotent": False,
    }


def _append_note(row, note):
    return "; ".join(
        part for part in [row.get("provider_notes", "").strip(), note] if part
    )


def backup_archive(country_code):
    return STORE.backup(country_code)


def correct_coordinates(
    country_code,
    parcel_code,
    new_vertices,
    export_mode="boundary",
):
    code = validate_country_code(country_code)
    errors = validate_coordinates(new_vertices, require_polygon=True)
    if errors:
        raise ValueError("; ".join(errors))
    new_boundary = build_boundary_string(new_vertices)

    with STORE.locked():
        _, country_rows = STORE.read_country(code)
        _, master_rows = STORE.read_master()
        country_row, master_row = _paired_rows(
            country_rows,
            master_rows,
            code,
            parcel_code,
        )
        duplicate = _same_boundary(country_rows, new_boundary, parcel_code)
        if duplicate:
            raise ValueError(
                f"Corrected coordinates already belong to {duplicate['parcel_code']}"
            )

        backup = STORE.backup(code)
        today = datetime.now().strftime("%Y-%m-%d")
        note = (
            f"[{today}] Coordinates corrected. Original backup: "
            f"{', '.join(backup['backup_paths'])}"
        )
        for row in (country_row, master_row):
            row["boundary_coords"] = new_boundary
            row["archive_date"] = today
            row["provider_notes"] = _append_note(row, note)
        STORE.commit(code, country_rows, master_rows)

    export = extract_single(code, parcel_code, export_mode=export_mode)
    return {
        "parcel_code": parcel_code,
        "country_code": code,
        "new_boundary": new_boundary,
        "updated_country": True,
        "updated_master": True,
        "backup_paths": backup["backup_paths"],
        "export_mode": export["export_mode"],
        "exports": export["exports"],
        **{
            key: export[key]
            for key in ("boundary_path", "vertices_path")
            if key in export
        },
    }


def dispatch(data):
    action = data.get("action", "")
    country_code = data["country_code"]
    handlers = {
        "scan": lambda: scan_archive(country_code, data.get("date")),
        "append": lambda: append_parcels(country_code, data["rows"]),
        "check_duplicate": lambda: check_duplicate(country_code, data["vertices"]),
        "extract_single": lambda: extract_single(
            country_code,
            data["parcel_code"],
            data.get("resolved_provider_name"),
            data.get("archive_date"),
            data.get("cadastre_code"),
            data.get("export_mode", "boundary"),
        ),
        "update_cadastre": lambda: update_cadastre(
            country_code,
            data["parcel_code"],
            data["cadastre_code"],
            data.get("replace_existing", False),
        ),
        "backup": lambda: backup_archive(country_code),
        "correct": lambda: correct_coordinates(
            country_code,
            data["parcel_code"],
            data["new_vertices"],
            data.get("export_mode", "boundary"),
        ),
    }
    if action not in handlers:
        raise ValueError(f"Unknown action: {action!r}")
    return handlers[action]()


def main():
    try:
        write_json_stdout(dispatch(read_json_stdin()))
    except (KeyError, TypeError, ValueError, OSError) as exc:
        write_json_stdout({"error": str(exc)})
        raise SystemExit(2)


if __name__ == "__main__":
    main()
