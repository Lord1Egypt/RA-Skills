"""Conservative piano-part selection shared by MusicXML and OMR helpers.

MusicXML files for vocal songs often contain Voice parts followed by a Piano
grand staff. Treating ``part[0]`` as the right hand turns the singer into a
pianist and corrupts every downstream fingering and anchor comparison.
"""

from __future__ import annotations

import xml.etree.ElementTree as ET


KEYBOARD_WORDS = ("piano", "keyboard", "klavier", "fortepiano", "grand piano")


def local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def children(element: ET.Element, name: str) -> list[ET.Element]:
    return [item for item in element if local(item.tag) == name]


def text(element: ET.Element | None, name: str, default: str = "") -> str:
    if element is None:
        return default
    item = next((child for child in element if local(child.tag) == name), None)
    return (item.text or default).strip() if item is not None else default


def part_metadata(root: ET.Element) -> dict[str, str]:
    labels: dict[str, str] = {}
    part_list = next((item for item in root if local(item.tag) == "part-list"), None)
    if part_list is None:
        return labels
    for item in children(part_list, "score-part"):
        part_id = str(item.attrib.get("id", ""))
        if not part_id:
            continue
        values = [text(item, "part-name"), text(item, "part-abbreviation")]
        for instrument in children(item, "score-instrument"):
            values.append(text(instrument, "instrument-name"))
        labels[part_id] = " ".join(value for value in values if value).lower()
    return labels


def part_staff_count(part: ET.Element) -> int:
    maximum = 1
    for measure in children(part, "measure"):
        attributes = next((item for item in measure if local(item.tag) == "attributes"), None)
        if attributes is not None:
            try:
                maximum = max(maximum, int(text(attributes, "staves")))
            except ValueError:
                pass
        for note in children(measure, "note"):
            try:
                maximum = max(maximum, int(text(note, "staff")))
            except ValueError:
                pass
    return maximum


def select_piano_parts(
    root: ET.Element,
    requested_part_id: str | None = None,
    rh_part_id: str | None = None,
    lh_part_id: str | None = None,
) -> tuple[list[ET.Element], dict[str, str]]:
    """Select keyboard parts and return their routing modes.

    ``staff`` means a normal grand staff; ``rh``/``lh`` are only used for an
    explicit pair of one-staff keyboard parts. Ambiguous sources fail closed.
    """
    parts = [item for item in root.iter() if local(item.tag) == "part"]
    indexed = {str(part.attrib.get("id", f"P{index + 1}")): part for index, part in enumerate(parts)}
    if (rh_part_id is None) != (lh_part_id is None):
        raise ValueError("explicit split-staff routing requires both --rh-part-id and --lh-part-id")
    if requested_part_id and rh_part_id:
        raise ValueError("use either --part-id or the --rh-part-id/--lh-part-id pair, not both")
    if rh_part_id and lh_part_id:
        if rh_part_id == lh_part_id:
            raise ValueError("--rh-part-id and --lh-part-id must identify different parts")
        rh_part, lh_part = indexed.get(rh_part_id), indexed.get(lh_part_id)
        missing = [part_id for part_id, part in ((rh_part_id, rh_part), (lh_part_id, lh_part)) if part is None]
        if missing:
            raise ValueError("requested keyboard part was not found: " + ", ".join(missing))
        if part_staff_count(rh_part) != 1 or part_staff_count(lh_part) != 1:
            raise ValueError("explicit RH/LH part routing only accepts one-staff parts; use --part-id for a grand staff")
        return [rh_part, lh_part], {rh_part_id: "rh", lh_part_id: "lh"}
    if requested_part_id:
        part = indexed.get(requested_part_id)
        if part is None:
            raise ValueError(f"requested MusicXML part {requested_part_id!r} was not found")
        return [part], {requested_part_id: "staff"}
    if len(parts) == 1:
        part_id = str(parts[0].attrib.get("id", "P1"))
        return parts, {part_id: "staff"}
    labels = part_metadata(root)
    keyboard = [part for part in parts if any(word in labels.get(str(part.attrib.get("id", "")), "") for word in KEYBOARD_WORDS)]
    if len(keyboard) == 1:
        part_id = str(keyboard[0].attrib.get("id", "P1"))
        return keyboard, {part_id: "staff"}
    if len(keyboard) == 2 and all(part_staff_count(part) == 1 for part in keyboard):
        first_id, second_id = (str(keyboard[0].attrib.get("id", "P1")), str(keyboard[1].attrib.get("id", "P2")))
        return keyboard, {first_id: "rh", second_id: "lh"}
    grand_staff = [part for part in parts if part_staff_count(part) >= 2]
    if len(grand_staff) == 1:
        part_id = str(grand_staff[0].attrib.get("id", "P1"))
        return grand_staff, {part_id: "staff"}
    available = ", ".join(f"{part_id} ({labels.get(part_id, 'unnamed') or 'unnamed'})" for part_id in indexed)
    raise ValueError("cannot identify one piano part safely; pass --part-id with the intended keyboard part. " + f"Available parts: {available}")


def hand_for_part_staff(part_id: str, staff: int, modes: dict[str, str]) -> str:
    mode = modes.get(part_id, "staff")
    if mode == "rh":
        return "RH"
    if mode == "lh":
        return "LH"
    return "LH" if staff >= 2 else "RH"
