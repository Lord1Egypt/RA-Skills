#!/usr/bin/env python3
"""Extract *candidate-only* notehead centres from an Audiveris .omr project.

Audiveris stores detected notehead bounds in its project XML.  Those bounds
can make visual review much faster than estimating every x/y coordinate from a
full page, but they remain OMR evidence: this tool never changes a fingering
plan and never marks an anchor as verified.
"""

from __future__ import annotations

import argparse
import json
import struct
import sys
import xml.etree.ElementTree as ET
import zipfile
from collections import defaultdict
from pathlib import Path

from safe_xml import load_musicxml
from musicxml_parts import hand_for_part_staff, select_piano_parts


def local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def child(element: ET.Element, name: str) -> ET.Element | None:
    return next((item for item in element if local(item.tag) == name), None)


def png_dimensions(payload: bytes) -> tuple[int, int]:
    if payload[:8] != b"\x89PNG\r\n\x1a\n" or len(payload) < 24:
        raise ValueError("Audiveris page image is not a PNG")
    return struct.unpack(">II", payload[16:24])


def image_dimensions(path: Path) -> tuple[int, int]:
    if not path.is_file():
        raise ValueError(f"target image not found: {path}")
    return png_dimensions(path.read_bytes()[:24])


def parse_target(value: str) -> tuple[int, Path]:
    page_text, separator, image_text = value.partition(":")
    if not separator:
        raise argparse.ArgumentTypeError("--target-image must be PAGE:/absolute/or/local/page.png")
    try:
        page = int(page_text)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("target page must be a positive integer") from exc
    if page < 1 or not image_text:
        raise argparse.ArgumentTypeError("target page and image path are required")
    return page, Path(image_text).expanduser().resolve()


def candidate_note_count(path: Path) -> int:
    """Count sounding notes in the selected piano part(s), never a vocal part."""
    tree, _member = load_musicxml(path)
    parts, _modes = select_piano_parts(tree.getroot())
    return sum(
        1 for part in parts for element in part.iter()
        if local(element.tag) == "note" and child(element, "pitch") is not None
    )


def normalized_part_id(value: object) -> str:
    """Match Audiveris `3` with MusicXML `P3` without fuzzy name matching."""
    text_id = "".join(character for character in str(value).lower() if character.isalnum())
    return text_id[1:] if text_id.startswith("p") and text_id[1:].isdigit() else text_id


def selected_part_ids(path: Path) -> set[str]:
    tree, _member = load_musicxml(path)
    parts, _modes = select_piano_parts(tree.getroot())
    return {normalized_part_id(part.attrib.get("id", "")) for part in parts}


def omr_selected_staffs(root: ET.Element, wanted_parts: set[str] | None) -> set[int] | None:
    """Find OMR staff IDs belonging to selected MusicXML piano part IDs.

    Audiveris numbers staves afresh per system, so the filter is derived from
    each system's `part -> staff` structure rather than from odd/even staff
    numbers. If an engine's IDs cannot be matched at all, return ``None`` and
    let the later consistency gate block uncertainty instead of discarding all
    geometry silently.
    """
    if not wanted_parts:
        return None
    staffs: set[int] = set()
    for system in (item for item in root.iter() if local(item.tag) == "system"):
        for part in (item for item in system if local(item.tag) == "part"):
            if normalized_part_id(part.attrib.get("id", "")) not in wanted_parts:
                continue
            for staff in (item for item in part if local(item.tag) == "staff"):
                try:
                    staffs.add(int(staff.attrib["id"]))
                except (KeyError, TypeError, ValueError):
                    continue
    return staffs or None


def omr_notehead_count(path: Path, wanted_parts: set[str] | None = None) -> int:
    """Count selected piano head records without exporting anchors."""
    if not path.is_file():
        raise ValueError(f".omr archive not found: {path}")
    count = 0
    with zipfile.ZipFile(path) as archive:
        names = set(archive.namelist())
        page = 1
        while f"sheet#{page}/sheet#{page}.xml" in names:
            root = ET.fromstring(archive.read(f"sheet#{page}/sheet#{page}.xml"))
            by_id = {str(item.attrib.get("id", "")): item for item in root.iter() if item.attrib.get("id")}
            count += sum(
                1 for head_id in head_scopes(root, page, wanted_parts)
                if child(by_id.get(head_id, ET.Element("missing")), "bounds") is not None
            )
            page += 1
    return count


def _ids(element: ET.Element | None) -> list[str]:
    return [] if element is None or not (element.text or "").strip() else (element.text or "").split()


def _hand_for_omr_staff(staff: int) -> str:
    """Audiveris numbers the two piano staves in each system consecutively."""
    return "RH" if staff > 0 and staff % 2 else "LH"


def head_scopes(root: ET.Element, page: int, wanted_parts: set[str] | None = None) -> dict[str, dict[str, object]]:
    """Map every contained OMR head to its local measure and piano hand."""
    by_id = {str(item.attrib["id"]): item for item in root.iter() if "id" in item.attrib}
    chord_heads: dict[str, list[str]] = defaultdict(list)
    for relation in root.iter():
        if local(relation.tag) != "relation" or child(relation, "containment") is None:
            continue
        source, target = relation.attrib.get("source"), relation.attrib.get("target")
        if source and target and local(by_id.get(source, ET.Element("unknown")).tag) == "head-chord":
            if local(by_id.get(target, ET.Element("unknown")).tag) == "head":
                chord_heads[source].append(target)
    result: dict[str, dict[str, object]] = {}
    selected_staffs = omr_selected_staffs(root, wanted_parts)
    measures = [item for item in root.iter() if local(item.tag) == "measure"]
    for local_measure, measure in enumerate(measures, 1):
        for chord_id in _ids(child(measure, "head-chords")):
            for head_id in chord_heads.get(chord_id, []):
                head = by_id.get(head_id)
                if head is None:
                    continue
                try:
                    staff = int(head.attrib.get("staff", "0"))
                except ValueError:
                    staff = 0
                if selected_staffs is not None and staff not in selected_staffs:
                    continue
                result[head_id] = {
                    "page": page, "local_measure": local_measure,
                    "hand": _hand_for_omr_staff(staff),
                }
    return result


def omr_measure_head_counts(path: Path, wanted_parts: set[str] | None = None) -> tuple[dict[tuple[int, int, str], int], dict[int, int]]:
    """Return detected head counts by (page, local measure, hand).

    The counts use Audiveris containment links (head-chord -> head), rather
    than loose x/y buckets, so multi-note chords remain countable.
    """
    counts: dict[tuple[int, int, str], int] = defaultdict(int)
    page_measure_counts: dict[int, int] = {}
    with zipfile.ZipFile(path) as archive:
        names = set(archive.namelist())
        page = 1
        while f"sheet#{page}/sheet#{page}.xml" in names:
            root = ET.fromstring(archive.read(f"sheet#{page}/sheet#{page}.xml"))
            measures = [item for item in root.iter() if local(item.tag) == "measure"]
            page_measure_counts[page] = len(measures)
            for scope in head_scopes(root, page, wanted_parts).values():
                counts[(page, int(scope["local_measure"]), str(scope["hand"]))] += 1
            page += 1
    return dict(counts), page_measure_counts


def musicxml_measure_note_counts(path: Path) -> dict[tuple[int, str], int]:
    """Count candidate pitches by importer-equivalent measure/hand routing."""
    tree, _member = load_musicxml(path)
    parts, part_modes = select_piano_parts(tree.getroot())
    counts: dict[tuple[int, str], int] = defaultdict(int)
    for part_index, part in enumerate(parts):
        measures = [item for item in part if local(item.tag) == "measure"]
        for measure_index, measure in enumerate(measures, 1):
            for note in measure:
                if local(note.tag) != "note" or child(note, "pitch") is None:
                    continue
                try:
                    staff = int((child(note, "staff").text or "1") if child(note, "staff") is not None else "1")
                except (AttributeError, ValueError):
                    staff = 1
                part_id = str(part.attrib.get("id", f"P{part_index + 1}"))
                hand = hand_for_part_staff(part_id, staff, part_modes)
                counts[(measure_index, hand)] += 1
    return dict(counts)


def measure_consistency(omr: Path, musicxml: Path) -> list[dict]:
    omr_counts, page_measure_counts = omr_measure_head_counts(omr, selected_part_ids(musicxml))
    xml_counts = musicxml_measure_note_counts(musicxml)
    rows: list[dict] = []
    offset = 0
    for page in sorted(page_measure_counts):
        for local_measure in range(1, page_measure_counts[page] + 1):
            global_measure = offset + local_measure
            for hand in ("RH", "LH"):
                omr_count = omr_counts.get((page, local_measure, hand), 0)
                xml_count = xml_counts.get((global_measure, hand), 0)
                rows.append({
                    "page": page, "measure": local_measure, "global_measure": global_measure,
                    "hand": hand, "omr_noteheads": omr_count, "musicxml_notes": xml_count,
                    "consistent": omr_count == xml_count,
                })
        offset += page_measure_counts[page]
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("omr", type=Path, help="local .omr archive produced by Audiveris")
    parser.add_argument("-o", "--output", type=Path, required=True)
    parser.add_argument("--candidate-musicxml", type=Path,
                        help="optional paired candidate MXL/MusicXML; count mismatch blocks anchor proposal")
    parser.add_argument("--target-image", action="append", default=[], type=parse_target,
                        help="optional rendered original page, e.g. 1:source-page-001.png; repeat per page")
    args = parser.parse_args()
    if not args.omr.is_file():
        raise ValueError(f".omr archive not found: {args.omr}")
    if args.output.resolve() == args.omr.resolve():
        raise ValueError("output must not overwrite the .omr archive")
    if args.candidate_musicxml is not None and not args.candidate_musicxml.is_file():
        raise ValueError(f"candidate MusicXML not found: {args.candidate_musicxml}")
    wanted_parts = selected_part_ids(args.candidate_musicxml) if args.candidate_musicxml else None
    targets = dict(args.target_image)
    if len(targets) != len(args.target_image):
        raise ValueError("each --target-image page may appear only once")

    pages: list[dict] = []
    with zipfile.ZipFile(args.omr) as archive:
        names = set(archive.namelist())
        page = 1
        while f"sheet#{page}/sheet#{page}.xml" in names:
            xml_name = f"sheet#{page}/sheet#{page}.xml"
            image_name = f"sheet#{page}/BINARY.png"
            if image_name not in names:
                raise ValueError(f"{image_name} is missing from the .omr archive")
            width, height = png_dimensions(archive.read(image_name)[:24])
            root = ET.fromstring(archive.read(xml_name))
            scoped_heads = head_scopes(root, page, wanted_parts)
            # This is deliberately the number of <measure> elements rather
            # than the largest local_measure that happens to contain a head.
            # A page may finish with an all-rest measure.  Inferring the page
            # span from heads would then move every later page one measure
            # early, which is exactly the kind of global label drift this
            # candidate helper must prevent.
            measure_count = sum(1 for item in root.iter() if local(item.tag) == "measure")
            target = targets.get(page)
            target_width = target_height = None
            scale_x = scale_y = None
            if target is not None:
                target_width, target_height = image_dimensions(target)
                scale_x, scale_y = target_width / width, target_height / height
            heads: list[dict] = []
            for element in root.iter():
                if local(element.tag) != "head":
                    continue
                bounds = child(element, "bounds")
                if bounds is None:
                    continue
                try:
                    x, y = float(bounds.attrib["x"]), float(bounds.attrib["y"])
                    w, h = float(bounds.attrib["w"]), float(bounds.attrib["h"])
                    identifier = str(element.attrib["id"])
                except (KeyError, TypeError, ValueError):
                    continue
                record: dict[str, object] = {
                    "candidate_anchor_id": f"omr-p{page}-head{identifier}",
                    "omr_head_id": identifier,
                    "staff": int(element.attrib.get("staff", "0") or 0),
                    "shape": str(element.attrib.get("shape", "unknown")),
                    "pitch_position": float(element.attrib.get("pitch", "0") or 0),
                    "grade": float(element.attrib.get("grade", "0") or 0),
                    "context_grade": float(element.attrib.get("ctx-grade", "0") or 0),
                    "omr_bounds": [x, y, w, h],
                    "omr_center": [round(x + w / 2, 3), round(y + h / 2, 3)],
                    "candidate_only": True,
                    "anchor_verified": False,
                }
                scope = scoped_heads.get(identifier)
                if scope is None:
                    # Uncontained heads cannot be tied to a measure/event.
                    # Keeping them in the candidate total would create a
                    # misleading global mismatch and tempt a later x-order
                    # assignment to drift across the page.
                    continue
                record.update(scope)
                if scale_x is not None and scale_y is not None:
                    record["page_x"] = round((x + w / 2) * scale_x, 3)
                    record["page_y"] = round((y + h / 2) * scale_y, 3)
                heads.append(record)
            pages.append({
                "page": page,
                "measure_count": measure_count,
                "omr_image_width": width,
                "omr_image_height": height,
                "target_image": str(target) if target else None,
                "target_width": target_width,
                "target_height": target_height,
                "scale_x": scale_x,
                "scale_y": scale_y,
                "candidate_noteheads": heads,
            })
            page += 1
    if not pages:
        raise ValueError(".omr archive contains no sheet XML")
    anchor_count = sum(len(page["candidate_noteheads"]) for page in pages)
    xml_count = candidate_note_count(args.candidate_musicxml) if args.candidate_musicxml else None
    counts_match = xml_count is None or anchor_count == xml_count
    scoped_consistency = measure_consistency(args.omr, args.candidate_musicxml) if args.candidate_musicxml else []
    mismatched_scopes = [row for row in scoped_consistency if not row["consistent"]]
    payload = {
        "schema_version": "1.0",
        "purpose": "Audiveris candidate notehead geometry; review against the original page before any plan anchor is verified",
        "candidate_only": True,
        "source_omr": str(args.omr.resolve()),
        "candidate_musicxml": str(args.candidate_musicxml.resolve()) if args.candidate_musicxml else None,
        "candidate_notehead_count": anchor_count,
        "candidate_musicxml_note_count": xml_count,
        "count_consistent": counts_match,
        "proposal_gate": (
            "needs-original-page-review" if counts_match else "partial-needs-original-page-review"
        ),
        "warning": (
            "Candidate head count differs from candidate MusicXML note count; only scopes with matching local counts may be "
            "considered as review aids, and none may bypass original-page verification."
            if not counts_match else
            "Counts agree, but every anchor remains candidate-only until original-page and rendered-output audits pass."
        ),
        "measure_consistency": scoped_consistency,
        "mismatched_measure_scopes": mismatched_scopes,
        "pages": pages,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {anchor_count} candidate notehead anchor(s): {args.output}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, zipfile.BadZipFile, ET.ParseError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
