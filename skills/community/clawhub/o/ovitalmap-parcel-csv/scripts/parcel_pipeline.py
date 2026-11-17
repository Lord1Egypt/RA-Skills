"""Orchestrate parcel validation, matching, export, and archiving."""

import argparse
import json
import sys
import uuid
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from archive_manager import (
    append_parcels,
    check_duplicate,
    scan_archive,
    update_cadastre,
)
from batch_rules import (
    annotate_parcels,
    duplicate_official_ids,
    find_prior_boundary_match,
    resolution_for,
)
from country_locator import locate_country
from csv_builder import build_parcel_exports, normalize_export_mode, prepare_parcels
from provider_matcher import fuzzy_match
from response_protocol import (
    blocked_response,
    build_response,
    input_error_response,
)
from utils import (
    build_boundary_string,
    get_workspace_root,
    read_csv,
    validate_country_code,
    validate_date_token,
    validate_identifier,
    write_json_stdout,
)


WORKSPACE_ROOT = get_workspace_root()
STATE_DIR = WORKSPACE_ROOT / "ovitalmap_archive" / ".pipeline_state"


class WorkflowInputError(ValueError):
    def __init__(self, code, required_input, message, next_action):
        super().__init__(message)
        self.code = code
        self.required_input = required_input
        self.message = message
        self.next_action = next_action


def _state_path(run_id):
    safe_run_id = validate_identifier(run_id, "run_id")
    return STATE_DIR / f"{safe_run_id}.json"


def save_state(run_id, state):
    path = _state_path(run_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".tmp")
    temporary.write_text(
        json.dumps(state, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    temporary.replace(path)


def load_state(run_id):
    path = _state_path(run_id)
    if not path.exists():
        raise ValueError(f"Unknown pipeline run_id: {run_id}")
    return json.loads(path.read_text(encoding="utf-8"))


def _master_providers():
    _, rows = read_csv(str(WORKSPACE_ROOT / "ovitalmap_archive" / "master.csv"))
    return {
        row.get("provider_name", "").strip()
        for row in rows
        if row.get("provider_name", "").strip().lower() not in {"", "unknown"}
    }


def step1_country_and_provider(parcels, country_code=None):
    """Validate coordinates and match each parcel's provider."""
    if not isinstance(parcels, list) or not parcels:
        raise ValueError("parcels must be a non-empty list")
    annotated, parcel_countries = annotate_parcels(parcels)
    country_code = validate_country_code(country_code) if country_code else None
    if len(parcel_countries) > 1:
        groups = "; ".join(
            f"{code}: {','.join(refs)}"
            for code, refs in sorted(parcel_countries.items())
        )
        raise WorkflowInputError(
            "mixed_country_batch",
            ["separate_runs_by_country"],
            f"The batch contains multiple countries or regions ({groups}). Split it into separate runs.",
            "split_by_country",
        )
    if parcel_countries:
        parcel_country = next(iter(parcel_countries))
        if country_code and country_code != parcel_country:
            refs = ",".join(parcel_countries[parcel_country])
            raise WorkflowInputError(
                "country_mismatch",
                ["country_code"],
                f"{refs} is marked {parcel_country}, which conflicts with batch country or region {country_code}.",
                "confirm_preflight",
            )
        country_code = country_code or parcel_country

    coordinate_results = []
    normalized_parcels = []
    all_errors = []
    for source in annotated:
        parcel = dict(source)
        result = locate_country(parcel.get("vertices", []))
        coordinate_results.append(result)
        if result["errors"]:
            all_errors.extend(
                f"{parcel['parcel_ref']}: {message}" for message in result["errors"]
            )
        parcel["vertices"] = result["normalized_vertices"]
        normalized_parcels.append(parcel)
    if all_errors:
        raise ValueError("; ".join(all_errors))

    existing_providers = set()
    archive_exists = False
    if country_code:
        archive_scan = scan_archive(country_code)
        existing_providers.update(archive_scan["all_providers"])
        archive_exists = archive_scan["archive_exists"]
    existing_providers.update(_master_providers())
    existing_providers = sorted(existing_providers)

    provider_results = []
    for parcel in normalized_parcels:
        provider = str(
            parcel.get("resolved_provider_name")
            or parcel.get("provider_name")
            or ""
        ).strip()
        provider_results.append(
            fuzzy_match(provider, existing_providers)
            if provider
            else {
                "input_name": "",
                "exact_match": None,
                "candidates": [],
                "ambiguous": False,
            }
        )

    return {
        "country_code": country_code,
        "country_name": None,
        "method": "confirmed_input" if country_code else "needs_confirmation",
        "coordinate_results": coordinate_results,
        "provider_results": provider_results,
        "archive_exists": archive_exists,
        "existing_providers": existing_providers,
        "parcels": normalized_parcels,
        "needs_country_confirmation": country_code is None,
    }


def _resolved_provider(parcel, batch_provider=None):
    provider = str(
        parcel.get("resolved_provider_name")
        or parcel.get("provider_name")
        or batch_provider
        or ""
    ).strip()
    if not provider:
        raise ValueError("Every parcel requires a confirmed provider_name")
    return provider


def _apply_provider_resolutions(parcels, data, state):
    resolutions = data.get("provider_resolutions", {})
    batch_provider = data.get("resolved_provider_name")
    provider_results = state.get("step1", {}).get("provider_results", [])
    resolved = []
    missing = []

    for index, source in enumerate(parcels):
        parcel = dict(source)
        provider_result = (
            provider_results[index] if index < len(provider_results) else {}
        )
        selected = (
            resolution_for(resolutions, parcel)[1]
            or provider_result.get("exact_match")
            or parcel.get("resolved_provider_name")
            or batch_provider
        )
        requires_resolution = (
            not provider_result.get("input_name")
            or (
                provider_result.get("candidates")
                and not provider_result.get("exact_match")
            )
        )
        if selected:
            parcel["resolved_provider_name"] = str(selected).strip()
        elif requires_resolution:
            missing.append(f"provider_resolutions.{parcel['parcel_ref']}")
        resolved.append(parcel)

    if missing:
        raise WorkflowInputError(
            "provider_confirmation_required",
            missing,
            "Confirm each missing provider before checking for duplicate parcels.",
            "confirm_preflight",
        )
    return resolved


def step2b_check_duplicates(
    parcels,
    country_code,
    resolved_provider_name=None,
    duplicate_resolutions=None,
):
    """Classify parcels without modifying archives."""
    country_code = validate_country_code(country_code)
    duplicate_results = []
    hits = []
    new = []
    ordered = []
    conflicts = []
    prior_parcels = []

    for index, source in enumerate(parcels):
        parcel = dict(source)
        parcel.setdefault("input_index", index)
        parcel.setdefault("parcel_ref", f"P{parcel['input_index'] + 1:02d}")
        provider = _resolved_provider(parcel, resolved_provider_name)
        prior = find_prior_boundary_match(parcel, prior_parcels)
        if prior:
            found, decision = resolution_for(duplicate_resolutions, parcel)
            decision = str(decision or "").strip().lower() if found else ""
            if decision not in {"same", "different"}:
                conflicts.append(
                    {
                        "index": parcel["input_index"],
                        "parcel_ref": parcel["parcel_ref"],
                        "matches_index": prior["input_index"],
                        "matches_ref": prior["parcel_ref"],
                    }
                )
                continue
            if decision == "same":
                duplicate_results.append(
                    {
                        "index": parcel["input_index"],
                        "parcel_ref": parcel["parcel_ref"],
                        "match_found": True,
                        "match_source": "batch",
                        "matches_ref": prior["parcel_ref"],
                        "resolution": "same",
                        "skipped": True,
                    }
                )
                continue
            parcel["allow_duplicate_coordinates"] = True
            note = (
                f"Coordinates identical to {prior['parcel_ref']}; "
                "user confirmed a different parcel."
            )
            parcel["provider_notes"] = " ".join(
                part for part in [parcel.get("provider_notes", ""), note] if part
            )
            result = {"match_found": False}
        else:
            result = check_duplicate(country_code, parcel.get("vertices", []))

        entry = {
            "index": parcel["input_index"],
            "parcel_ref": parcel["parcel_ref"],
            "match_found": result["match_found"],
        }

        if result["match_found"]:
            parcel.update(
                {
                    "parcel_code": result["matched_code"],
                    "resolved_provider_name": result["matched_provider"] or provider,
                    "archive_date": result["matched_archive_date"],
                    "cadastre_code": (
                        parcel.get("official_id")
                        or result["matched_cadastre_code"]
                    ),
                    "matched_cadastre_code": result["matched_cadastre_code"],
                    "is_archive_hit": True,
                }
            )
            needs_update = bool(
                parcel.get("official_id")
                and not result["matched_cadastre_code"]
            )
            entry.update(
                {
                    "matched_code": result["matched_code"],
                    "matched_provider": result["matched_provider"],
                    "matched_cadastre_code": result["matched_cadastre_code"],
                    "needs_cadastre_update": needs_update,
                }
            )
            hits.append(parcel)
        else:
            parcel.update(
                {
                    "resolved_provider_name": provider,
                    "archive_date": datetime.now().strftime("%Y-%m-%d"),
                    "cadastre_code": parcel.get("official_id", ""),
                    "is_archive_hit": False,
                }
            )
            new.append(parcel)
        duplicate_results.append(entry)
        ordered.append(parcel)
        prior_parcels.append(parcel)

    return {
        "duplicate_results": duplicate_results,
        "archive_hit_parcels": hits,
        "new_parcels": new,
        "all_parcels_ordered": ordered,
        "batch_duplicate_conflicts": conflicts,
    }


def step2_assign_codes(new_parcels, country_code, date_hint):
    country_code = validate_country_code(country_code)
    date_hint = validate_date_token(date_hint)
    if not new_parcels:
        return {
            "assigned_codes": [],
            "warnings": [],
            "message": "No new parcels to assign codes to.",
            "new_parcels": [],
        }

    archive_scan = scan_archive(country_code, date_hint)
    existing_codes = set(archive_scan["all_codes"])
    sequence = archive_scan["today_max_seq"]
    assigned = []
    prepared = []

    for index, source in enumerate(new_parcels):
        parcel = dict(source)
        official_id = parcel.get("official_id")
        if official_id:
            official_id = validate_identifier(official_id, "official_id")
            candidate = f"{country_code}-{official_id}"
            if candidate in existing_codes:
                raise ValueError(
                    f"Official parcel code already exists and requires review: {candidate}"
                )
            is_sequential = False
            parcel["cadastre_code"] = official_id
        else:
            sequence += 1
            candidate = f"{country_code}-{date_hint}-{sequence:03d}"
            while candidate in existing_codes:
                sequence += 1
                candidate = f"{country_code}-{date_hint}-{sequence:03d}"
            is_sequential = True

        existing_codes.add(candidate)
        parcel["parcel_code"] = candidate
        prepared.append(parcel)
        assigned.append(
            {
                "index": parcel.get("input_index", index),
                "parcel_ref": parcel.get("parcel_ref", f"P{index + 1:02d}"),
                "parcel_code": candidate,
                "is_sequential": is_sequential,
            }
        )

    return {
        "assigned_codes": assigned,
        "warnings": [],
        "today_max_seq": archive_scan["today_max_seq"],
        "new_max_seq": sequence,
        "new_parcels": prepared,
    }


def _merge_assigned(ordered, assigned):
    # State serialization loses object identity; preserve order by replacing
    # each non-hit parcel from the assigned queue.
    queue = iter(assigned)
    merged = []
    for parcel in ordered:
        merged.append(parcel if parcel.get("is_archive_hit") else next(queue))
    return merged


def _apply_official_id_resolutions(parcels, resolutions):
    resolved = []
    for source in parcels:
        parcel = dict(source)
        found, value = resolution_for(resolutions, parcel)
        if found:
            parcel["official_id"] = (
                validate_identifier(value, "official_id")
                if value not in {None, ""}
                else None
            )
        resolved.append(parcel)
    return resolved


def _replace_by_ref(parcels, replacements):
    by_ref = {parcel["parcel_ref"]: parcel for parcel in replacements}
    return [by_ref.get(parcel["parcel_ref"], parcel) for parcel in parcels]


def step3_build_and_archive(
    all_parcels,
    new_parcels,
    country_code,
    export_mode="boundary",
):
    country_code = validate_country_code(country_code)
    prepare_parcels(all_parcels)
    export_mode = normalize_export_mode(export_mode)

    cadastre_updates = []
    for parcel in all_parcels:
        if not parcel.get("is_archive_hit"):
            continue
        if parcel.get("official_id") and not parcel.get("matched_cadastre_code"):
            cadastre_updates.append(
                update_cadastre(
                    country_code,
                    parcel["parcel_code"],
                    parcel["official_id"],
                )
            )
    export_result = build_parcel_exports(all_parcels, country_code, export_mode)
    archive_result = None
    if new_parcels:
        archive_rows = [
            {
                "parcel_code": parcel["parcel_code"],
                "provider_name": _resolved_provider(parcel),
                "archive_date": datetime.now().strftime("%Y-%m-%d"),
                "boundary_coords": build_boundary_string(parcel["vertices"]),
                "provider_notes": parcel.get("provider_notes", ""),
                "cadastre_code": parcel.get("cadastre_code", ""),
                "allow_duplicate_coordinates": parcel.get(
                    "allow_duplicate_coordinates", False
                ),
            }
            for parcel in new_parcels
        ]
        archive_result = append_parcels(country_code, archive_rows)

    return {
        **export_result,
        "archive_result": archive_result,
        "cadastre_updates": cadastre_updates,
    }


def _run_step(step, data, state):
    parcels = (
        data.get("parcels", [])
        if step == "1"
        else state.get("parcels") or data.get("parcels", [])
    )
    country_code = data.get("country_code") or state.get("country_code")
    provider = data.get("resolved_provider_name") or state.get(
        "resolved_provider_name"
    )
    date_hint = data.get("date") or state.get(
        "date", datetime.now().strftime("%y%m%d")
    )
    if "export_mode" in data or "export_mode" not in state:
        state["export_mode"] = normalize_export_mode(data.get("export_mode"))
    export_mode = state["export_mode"]

    if step == "1":
        result = step1_country_and_provider(parcels, country_code)
        result["coordinates_confirmed"] = bool(
            data.get("confirmed_coordinates") or data.get("confirmed")
        )
        state.update(
            {
                "parcels": result["parcels"],
                "country_code": result["country_code"],
                "date": validate_date_token(date_hint),
                "resolved_provider_name": provider,
                "coordinates_confirmed": result["coordinates_confirmed"],
                "step1": result,
            }
        )
        return result

    if not country_code:
        raise WorkflowInputError(
            "country_required",
            ["country_code"],
            "Provide or confirm the parcel country or region before continuing.",
            "confirm_preflight",
        )

    if step == "2b":
        coordinates_confirmed = bool(
            data.get("confirmed_coordinates")
            or data.get("confirmed")
            or state.get("coordinates_confirmed")
        )
        if not coordinates_confirmed:
            raise WorkflowInputError(
                "coordinate_confirmation_required",
                ["confirmed_coordinates"],
                "Confirm the displayed WGS84 coordinates before checking for duplicates.",
                "confirm_preflight",
            )
        parcels = _apply_provider_resolutions(parcels, data, state)
        result = step2b_check_duplicates(
            parcels,
            country_code,
            provider,
            data.get("duplicate_resolutions"),
        )
        state.update(
            {
                "parcels": (
                    parcels
                    if result["batch_duplicate_conflicts"]
                    else result["all_parcels_ordered"]
                ),
                "country_code": country_code,
                "date": validate_date_token(date_hint),
                "resolved_provider_name": provider,
                "coordinates_confirmed": True,
                "step2b": result,
            }
        )
        return result

    if step == "2":
        if "step2b" not in state:
            raise ValueError("Run Step 2b before Step 2")
        conflicts = state["step2b"].get("batch_duplicate_conflicts", [])
        if conflicts:
            fields = [
                f"duplicate_resolutions.{item['parcel_ref']}"
                for item in conflicts
            ]
            raise WorkflowInputError(
                "batch_duplicate_resolution_required",
                fields,
                "Confirm whether identical boundaries in this batch are the same or different parcels.",
                "resolve_batch_duplicates",
            )
        new_parcels = _apply_official_id_resolutions(
            state["step2b"]["new_parcels"],
            data.get("official_id_resolutions", {}),
        )
        official_conflicts = duplicate_official_ids(new_parcels)
        if official_conflicts:
            lines = "; ".join(
                f"{item['parcel_ref']} and {item['first_ref']} both use {item['official_id']}"
                for item in official_conflicts
            )
            raise WorkflowInputError(
                "duplicate_official_ids",
                [
                    f"official_id_resolutions.{item['parcel_ref']}"
                    for item in official_conflicts
                ],
                f"Duplicate official identifiers found: {lines}. Correct or clear the later value.",
                "resolve_official_ids",
            )
        state["step2b"]["new_parcels"] = new_parcels
        state["step2b"]["all_parcels_ordered"] = _replace_by_ref(
            state["step2b"]["all_parcels_ordered"],
            new_parcels,
        )
        try:
            result = step2_assign_codes(
                new_parcels,
                country_code,
                date_hint,
            )
        except ValueError as exc:
            prefix = "Official parcel code already exists and requires review: "
            if not str(exc).startswith(prefix):
                raise
            candidate = str(exc)[len(prefix):]
            parcel = next(
                (
                    item
                    for item in new_parcels
                    if f"{country_code}-{item.get('official_id')}" == candidate
                ),
                None,
            )
            parcel_ref = parcel["parcel_ref"] if parcel else "the corresponding parcel"
            raise WorkflowInputError(
                "official_code_exists",
                [f"official_id_resolutions.{parcel_ref}"],
                f"Official code {candidate} for {parcel_ref} already exists. Verify, correct, or clear the identifier.",
                "resolve_official_ids",
            ) from exc
        ordered = _merge_assigned(
            state["step2b"]["all_parcels_ordered"],
            result["new_parcels"],
        )
        state["step2"] = result
        state["parcels"] = ordered
        return {
            key: value for key, value in result.items() if key != "new_parcels"
        }

    if step == "3":
        if "step2b" not in state:
            raise ValueError("Run Step 2b before Step 3")
        new_parcels = state.get("step2", {}).get("new_parcels", [])
        if state["step2b"]["new_parcels"] and not new_parcels:
            raise ValueError("Run Step 2 before Step 3")
        if new_parcels and not (
            data.get("confirmed_codes") or data.get("auto_accept_codes")
        ):
            raise WorkflowInputError(
                "code_confirmation_required",
                ["confirmed_codes"],
                "Confirm the proposed parcel codes before export and archiving.",
                "confirm_codes",
            )
        result = step3_build_and_archive(
            state["parcels"],
            new_parcels,
            country_code,
            export_mode,
        )
        state["step3"] = result
        return result

    raise ValueError(f"Unknown step: {step}")


def _public_result(step, result):
    """Keep tool output concise; full working data remains in per-run state."""
    if step == "1":
        return {
            "country_code": result["country_code"],
            "method": result["method"],
            "provider_results": result["provider_results"],
            "archive_exists": result["archive_exists"],
            "needs_country_confirmation": result["needs_country_confirmation"],
            "coordinates_confirmed": result["coordinates_confirmed"],
            "coordinate_preview": [
                item["normalized_vertices"]
                for item in result["coordinate_results"]
            ],
            "coordinate_warnings": [
                warning
                for item in result["coordinate_results"]
                for warning in item["warnings"]
            ],
            "parcel_refs": [
                parcel["parcel_ref"] for parcel in result["parcels"]
            ],
        }
    if step == "2b":
        return {
            "duplicate_results": result["duplicate_results"],
            "archive_hit_count": len(result["archive_hit_parcels"]),
            "new_parcel_count": len(result["new_parcels"]),
            "batch_duplicate_conflicts": result.get(
                "batch_duplicate_conflicts", []
            ),
        }
    if step == "2":
        return {
            key: value
            for key, value in result.items()
            if key != "new_parcels"
        }
    return result


def main():
    parser = argparse.ArgumentParser(description="Ovitalmap parcel pipeline")
    parser.add_argument("--step", choices=["1", "2b", "2", "3", "all"], default="all")
    args = parser.parse_args()

    run_id = None
    state = {}
    current_step = args.step
    try:
        data = json.load(sys.stdin)
        run_id = data.get("run_id") or uuid.uuid4().hex[:12]
        state = {} if args.step in {"1", "all"} else load_state(run_id)

        if args.step == "all":
            if not data.get("confirmed"):
                raise WorkflowInputError(
                    "preflight_confirmation_required",
                    ["confirmed"],
                    "Confirm the coordinates, country or region, and provider information before running the complete workflow.",
                    "confirm_preflight",
                )
            if not data.get("auto_accept_codes"):
                raise WorkflowInputError(
                    "automatic_code_acceptance_required",
                    ["auto_accept_codes"],
                    "The complete workflow accepts generated codes automatically. Set auto_accept_codes only after explicit approval.",
                    "confirm_codes",
                )
            outputs = {}
            for step in ("1", "2b", "2", "3"):
                current_step = step
                outputs[step] = _public_result(
                    step,
                    _run_step(step, data, state),
                )
            response = build_response(run_id, "3", outputs["3"])
            response["steps"] = outputs
        else:
            output = _run_step(args.step, data, state)
            response = build_response(
                run_id,
                args.step,
                _public_result(args.step, output),
            )

        save_state(run_id, state)
        write_json_stdout(response)
    except WorkflowInputError as exc:
        if run_id and state:
            save_state(run_id, state)
        write_json_stdout(input_error_response(run_id, current_step, exc))
        raise SystemExit(2)
    except (KeyError, TypeError, ValueError, OSError) as exc:
        write_json_stdout(blocked_response(run_id, current_step, exc))
        raise SystemExit(2)


if __name__ == "__main__":
    main()
