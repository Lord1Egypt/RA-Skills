#!/usr/bin/env python3
"""Write a unified fingering plan back to exact MusicXML note identities."""

from __future__ import annotations

import argparse
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path

from plan_io import load_plan
from safe_xml import load_musicxml


def local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def children(element: ET.Element, name: str) -> list[ET.Element]:
    return [item for item in element if local(item.tag) == name]


def child(element: ET.Element, name: str) -> ET.Element | None:
    return next((item for item in element if local(item.tag) == name), None)


def qualified(element: ET.Element, name: str) -> str:
    return element.tag.split("}", 1)[0] + "}" + name if element.tag.startswith("{") else name


def pitch_midi(note: ET.Element) -> int | None:
    pitch = child(note, "pitch")
    if pitch is None:
        return None
    step = (child(pitch, "step").text or "").strip()  # type: ignore[union-attr]
    octave = int((child(pitch, "octave").text or "0").strip())  # type: ignore[union-attr]
    alter_el = child(pitch, "alter")
    alter = int(float((alter_el.text or "0").strip())) if alter_el is not None else 0
    return (octave + 1) * 12 + {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}[step] + alter


def set_fingering(note: ET.Element, value: int, placement: str) -> None:
    notations = child(note, "notations")
    if notations is None:
        notations = ET.SubElement(note, qualified(note, "notations"))
    technical = child(notations, "technical")
    if technical is None:
        technical = ET.SubElement(notations, qualified(notations, "technical"))
    for item in list(technical):
        if local(item.tag) == "fingering":
            technical.remove(item)
    fingering = ET.SubElement(technical, qualified(technical, "fingering"))
    fingering.text = str(value)
    fingering.set("placement", placement)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("plan", type=Path)
    parser.add_argument("-o", "--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.resolve() in {args.input.resolve(), args.plan.resolve()}:
        raise ValueError("output must not overwrite the input score or plan")
    plan = load_plan(args.plan)
    by_key: dict[tuple, list[dict]] = defaultdict(list)
    by_id: dict[str, dict] = {}
    for record in plan["notes"]:
        if int(record.get("finger", 0)) not in {1, 2, 3, 4, 5}:
            continue
        by_id[str(record["note_id"])] = record
        key = (
            str(record["part"]), int(record["measure_index"]), int(record["staff"]),
            str(record["voice"]), round(float(record["onset"]), 8), int(record["pitch_midi"]),
        )
        by_key[key].append(record)
    # MXL is a normal accepted input for this Skill.  The output remains a
    # plain, portable MusicXML file so it can be opened without preserving or
    # modifying the input archive.
    tree, _ = load_musicxml(args.input, allow_mxl=True)
    root = tree.getroot()
    found: set[str] = set()
    divisions = 1.0
    for part in [item for item in root.iter() if local(item.tag) == "part"]:
        part_id = part.attrib.get("id", "")
        absolute_time = 0.0
        for measure_index, measure in enumerate(children(part, "measure"), 1):
            attrs = child(measure, "attributes")
            div_el = child(attrs, "divisions") if attrs is not None else None
            if div_el is not None:
                divisions = float((div_el.text or "1").strip())
            cursor = absolute_time
            furthest = cursor
            last_onset = cursor
            occurrence: dict[tuple, int] = defaultdict(int)
            for element in measure:
                kind = local(element.tag)
                if kind == "backup":
                    cursor -= float((child(element, "duration").text or "0")) / divisions  # type: ignore[union-attr]
                    continue
                if kind == "forward":
                    cursor += float((child(element, "duration").text or "0")) / divisions  # type: ignore[union-attr]
                    furthest = max(furthest, cursor)
                    continue
                if kind != "note":
                    continue
                duration_el = child(element, "duration")
                duration = float((duration_el.text or "0")) / divisions if duration_el is not None else 0
                chord = child(element, "chord") is not None
                onset = last_onset if chord else cursor
                if not chord:
                    last_onset = onset
                midi = pitch_midi(element)
                if midi is not None:
                    element_id = element.attrib.get("id", "")
                    record = by_id.get(element_id) if element_id else None
                    if record is None:
                        staff_el, voice_el = child(element, "staff"), child(element, "voice")
                        key = (part_id, measure_index, int((staff_el.text or "1") if staff_el is not None else 1), str((voice_el.text or "1") if voice_el is not None else "1"), round(onset, 8), midi)
                        index = occurrence[key]
                        occurrence[key] += 1
                        choices = sorted(by_key.get(key, []), key=lambda item: int(item["chord_row"]))
                        record = choices[index] if index < len(choices) else None
                    if record is not None:
                        set_fingering(element, int(record["finger"]), str(record["placement"]))
                        found.add(str(record["note_id"]))
                if not chord and child(element, "grace") is None:
                    cursor += duration
                    furthest = max(furthest, cursor)
            absolute_time = furthest
    missing = sorted(set(by_id) - found)
    if missing:
        raise ValueError(f"mapped notes not found ({len(missing)}): {missing[:8]}")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    ET.indent(tree, space="  ")
    tree.write(args.output, encoding="utf-8", xml_declaration=True)
    print(f"Wrote {args.output} with {len(found)} fingering marks.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, ET.ParseError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
