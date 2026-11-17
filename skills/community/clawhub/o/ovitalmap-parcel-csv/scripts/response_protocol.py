"""Build compact, language-neutral pipeline responses for agent use."""


def build_response(run_id, step, result):
    guidance = _guidance(step, result)
    return {
        "run_id": run_id,
        "step": step,
        "status": guidance["status"],
        "next_action": guidance["next_action"],
        "required_input": guidance["required_input"],
        "message": guidance["message"],
        "result": result,
    }


def input_error_response(run_id, step, error):
    return {
        "run_id": run_id,
        "step": step,
        "status": "needs_input",
        "next_action": error.next_action,
        "required_input": error.required_input,
        "message": error.message,
        "error_code": error.code,
    }


def blocked_response(run_id, step, error):
    return {
        "run_id": run_id,
        "step": step,
        "status": "blocked",
        "next_action": "correct_input_or_retry",
        "required_input": [],
        "message": f"Unable to continue: {error}",
        "error": str(error),
    }


def _guidance(step, result):
    if step == "1":
        return _step1_guidance(result)
    if step == "2b":
        return _step2b_guidance(result)
    if step == "2":
        return _step2_guidance(result)
    if step == "3":
        return _step3_guidance(result)
    raise ValueError(f"Unsupported response step: {step}")


def _step1_guidance(result):
    missing = []
    prompts = []
    coordinate_text = ""
    parcel_refs = result.get("parcel_refs", [])
    if not result.get("coordinates_confirmed"):
        missing.append("confirmed_coordinates")
        coordinate_text = "Recognized WGS84 coordinates:\n" + "\n".join(
            f"- {parcel_refs[index - 1] if index <= len(parcel_refs) else f'P{index:02d}'}: "
            + "; ".join(f"{lon},{lat}" for lon, lat in vertices)
            for index, vertices in enumerate(
                result.get("coordinate_preview", []),
                start=1,
            )
        )
        prompts.append("Confirm that these coordinates match the source")
    if result.get("needs_country_confirmation"):
        missing.append("country_code")
        prompts.append("Provide or confirm the country or region")

    for index, provider in enumerate(result.get("provider_results", []), start=1):
        parcel_ref = (
            parcel_refs[index - 1] if index <= len(parcel_refs) else f"P{index:02d}"
        )
        input_name = provider.get("input_name", "")
        if not input_name:
            missing.append(f"provider_resolutions.{parcel_ref}")
            prompts.append(f"Provide the provider name for {parcel_ref}")

    if missing:
        body = "\n".join(f"- {prompt}" for prompt in prompts)
        sections = [section for section in (coordinate_text, body) if section]
        return {
            "status": "needs_input",
            "next_action": "confirm_preflight",
            "required_input": missing,
            "message": "Required before continuing:\n" + "\n".join(sections),
        }
    return {
        "status": "ready",
        "next_action": "run_step_2b",
        "required_input": [],
        "message": "Coordinates, country or region, and provider information are confirmed.",
    }


def _step2b_guidance(result):
    conflicts = result.get("batch_duplicate_conflicts", [])
    if conflicts:
        fields = [
            f"duplicate_resolutions.{item['parcel_ref']}" for item in conflicts
        ]
        lines = "\n".join(
            f"- {item['parcel_ref']} has the same coordinates as "
            f"{item['matches_ref']}: choose same or different"
            for item in conflicts
        )
        return {
            "status": "needs_input",
            "next_action": "resolve_batch_duplicates",
            "required_input": fields,
            "message": f"Duplicate coordinates found:\n{lines}",
        }
    hit_count = result.get("archive_hit_count", 0)
    new_count = result.get("new_parcel_count", 0)
    return {
        "status": "ready",
        "next_action": "run_step_2" if new_count else "run_step_3",
        "required_input": [],
        "message": f"Duplicate check complete: {hit_count} archive hit(s), {new_count} new parcel(s).",
    }


def _step2_guidance(result):
    assigned = result.get("assigned_codes", [])
    if not assigned:
        return {
            "status": "ready",
            "next_action": "run_step_3",
            "required_input": [],
            "message": "No new parcel codes are required.",
        }
    code_lines = "\n".join(
        f"- {item.get('parcel_ref') or 'P%02d' % (item['index'] + 1)}: "
        f"{item['parcel_code']}"
        for item in assigned
    )
    return {
        "status": "needs_input",
        "next_action": "confirm_codes",
        "required_input": ["confirmed_codes"],
        "message": f"Proposed parcel codes:\n{code_lines}\nConfirm them before export and archiving.",
    }


def _step3_guidance(result):
    exports = result.get("exports", [])
    file_text = "\n".join(
        f"{index}. {item['path']}" for index, item in enumerate(exports, start=1)
    ) or "- No files generated"
    export_mode = result.get("export_mode", "boundary")
    instructions = {
        "boundary": "Import each CSV into OvitalMap as a track (轨迹).",
        "vertices": "Import each CSV into OvitalMap as labels (标签).",
        "both": "Import regular CSV files as tracks (轨迹) and _vertices files as labels (标签).",
    }
    return {
        "status": "completed",
        "next_action": "deliver_files",
        "required_input": [],
        "message": (
            f"Generated files:\n{file_text}\n"
            f"{instructions.get(export_mode, instructions['boundary'])}"
        ),
    }
