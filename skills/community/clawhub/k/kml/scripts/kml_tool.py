#!/usr/bin/env python3
"""Small helper for KML/KMZ summary, validation, and placemark extraction."""

from __future__ import annotations

import argparse
import json
import re
import sys
import xml.etree.ElementTree as ET
import zipfile
from collections import Counter
from dataclasses import dataclass
from pathlib import Path


KML_NS = "http://www.opengis.net/kml/2.2"
GX_NS = "http://www.google.com/kml/ext/2.2"
NS = {"kml": KML_NS, "gx": GX_NS}
GEOMETRY_TAGS = {
    "Point",
    "LineString",
    "LinearRing",
    "Polygon",
    "MultiGeometry",
    "Model",
    "Track",
    "MultiTrack",
}


@dataclass
class ParsedDocument:
    source_type: str
    root: ET.Element
    origin: str


def local_name(tag: str) -> str:
    if "}" in tag:
        return tag.rsplit("}", 1)[1]
    return tag


def text_of(element: ET.Element | None) -> str | None:
    if element is None or element.text is None:
        return None
    text = element.text.strip()
    return text or None


def load_document(path_text: str) -> ParsedDocument:
    path = Path(path_text)
    suffix = path.suffix.lower()

    if suffix == ".kmz":
        with zipfile.ZipFile(path) as archive:
            names = [name for name in archive.namelist() if name.lower().endswith(".kml")]
            if not names:
                raise ValueError("KMZ archive does not contain a .kml file.")
            preferred = "doc.kml"
            main_name = preferred if preferred in names else names[0]
            data = archive.read(main_name)
        try:
            root = ET.fromstring(data)
        except ET.ParseError as exc:
            raise ValueError(f"Invalid XML inside KMZ: {exc}") from exc
        return ParsedDocument(source_type="kmz", root=root, origin=main_name)

    if suffix != ".kml":
        raise ValueError("Input file must end with .kml or .kmz.")

    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as exc:
        raise ValueError(f"Invalid XML: {exc}") from exc
    return ParsedDocument(source_type="kml", root=root, origin=path.name)


def parse_coordinate_text(text: str) -> tuple[list[tuple[float, float, float | None]], list[str]]:
    coordinates: list[tuple[float, float, float | None]] = []
    errors: list[str] = []

    for raw_tuple in re.split(r"\s+", text.strip()):
        if not raw_tuple:
            continue
        parts = [part for part in raw_tuple.split(",") if part != ""]
        if len(parts) < 2:
            errors.append(f"Malformed coordinate tuple '{raw_tuple}'.")
            continue
        try:
            lon = float(parts[0])
            lat = float(parts[1])
            alt = float(parts[2]) if len(parts) >= 3 else None
        except ValueError:
            errors.append(f"Non-numeric coordinate tuple '{raw_tuple}'.")
            continue
        coordinates.append((lon, lat, alt))

    return coordinates, errors


def iter_coordinate_nodes(root: ET.Element) -> list[ET.Element]:
    return root.findall(".//kml:coordinates", NS)


def iter_placemarks(root: ET.Element) -> list[ET.Element]:
    return root.findall(".//kml:Placemark", NS)


def find_geometry_tags(placemark: ET.Element) -> list[str]:
    found: list[str] = []
    for element in placemark.iter():
        name = local_name(element.tag)
        if name in GEOMETRY_TAGS:
            found.append(name)
    return sorted(set(found))


def collect_coordinates(root: ET.Element) -> tuple[list[tuple[float, float, float | None]], list[str]]:
    coordinates: list[tuple[float, float, float | None]] = []
    errors: list[str] = []

    for node in iter_coordinate_nodes(root):
        text = text_of(node)
        if not text:
            continue
        parsed, parse_errors = parse_coordinate_text(text)
        coordinates.extend(parsed)
        errors.extend(parse_errors)

    for node in root.findall(".//gx:coord", NS):
        text = text_of(node)
        if not text:
            continue
        parts = text.split()
        if len(parts) < 2:
            errors.append(f"Malformed gx:coord '{text}'.")
            continue
        try:
            lon = float(parts[0])
            lat = float(parts[1])
            alt = float(parts[2]) if len(parts) >= 3 else None
        except ValueError:
            errors.append(f"Non-numeric gx:coord '{text}'.")
            continue
        coordinates.append((lon, lat, alt))

    return coordinates, errors


def compute_bbox(coordinates: list[tuple[float, float, float | None]]) -> list[float] | None:
    if not coordinates:
        return None
    longitudes = [item[0] for item in coordinates]
    latitudes = [item[1] for item in coordinates]
    return [min(longitudes), min(latitudes), max(longitudes), max(latitudes)]


def suspicious_notes(coordinates: list[tuple[float, float, float | None]]) -> list[str]:
    notes: list[str] = []
    if not coordinates:
        return notes

    out_of_range = sum(
        1
        for lon, lat, _alt in coordinates
        if not (-180.0 <= lon <= 180.0 and -90.0 <= lat <= 90.0)
    )
    maybe_swapped = sum(
        1
        for lon, lat, _alt in coordinates
        if -90.0 <= lon <= 90.0 and not (-90.0 <= lat <= 90.0)
    )

    if out_of_range:
        notes.append(f"{out_of_range} coordinate tuples fall outside lon/lat range.")
    if maybe_swapped:
        notes.append(f"{maybe_swapped} coordinate tuples may be swapped lat/lon.")

    return notes


def build_summary(document: ParsedDocument) -> dict[str, object]:
    root = document.root
    placemarks = iter_placemarks(root)
    folders = root.findall(".//kml:Folder", NS)
    overlays = root.findall(".//kml:GroundOverlay", NS)
    network_links = root.findall(".//kml:NetworkLink", NS)
    coordinates, parse_errors = collect_coordinates(root)

    geometry_counter: Counter[str] = Counter()
    placemark_summaries = []
    empty_placemarks = 0

    for placemark in placemarks:
        geometries = find_geometry_tags(placemark)
        if not geometries:
            empty_placemarks += 1
        for name in geometries:
            geometry_counter[name] += 1
        placemark_summaries.append(
            {
                "name": text_of(placemark.find("kml:name", NS)),
                "geometry_types": geometries,
            }
        )

    return {
        "source_type": document.source_type,
        "source_entry": document.origin,
        "document_name": text_of(root.find(".//kml:Document/kml:name", NS)) or text_of(root.find(".//kml:name", NS)),
        "placemark_count": len(placemarks),
        "empty_placemark_count": empty_placemarks,
        "geometry_types": dict(geometry_counter),
        "folder_count": len(folders),
        "ground_overlay_count": len(overlays),
        "network_link_count": len(network_links),
        "coordinate_count": len(coordinates),
        "bbox": compute_bbox(coordinates),
        "suspicious_notes": suspicious_notes(coordinates),
        "parse_errors": parse_errors,
        "sample_placemarks": placemark_summaries[:10],
    }


def validate_document(document: ParsedDocument) -> list[str]:
    errors: list[str] = []
    root = document.root

    if local_name(root.tag) != "kml":
        errors.append("Root element is not <kml>.")

    placemarks = iter_placemarks(root)
    if not placemarks:
        errors.append("No Placemark elements found.")

    coordinates, parse_errors = collect_coordinates(root)
    errors.extend(parse_errors)

    for index, placemark in enumerate(placemarks):
        geometries = find_geometry_tags(placemark)
        if not geometries:
            errors.append(f"Placemark at index {index} has no geometry.")

    if coordinates:
        for lon, lat, _alt in coordinates:
            if not (-180.0 <= lon <= 180.0):
                errors.append(f"Longitude {lon} is out of range.")
                break
        for lon, lat, _alt in coordinates:
            if not (-90.0 <= lat <= 90.0):
                errors.append(f"Latitude {lat} is out of range.")
                break
    else:
        errors.append("No coordinate tuples found.")

    return errors


def placemark_payload(document: ParsedDocument) -> list[dict[str, object]]:
    payload: list[dict[str, object]] = []

    for placemark in iter_placemarks(document.root):
        geometries = find_geometry_tags(placemark)
        coordinates, parse_errors = collect_coordinates(placemark)
        payload.append(
            {
                "name": text_of(placemark.find("kml:name", NS)),
                "geometry_types": geometries,
                "coordinate_count": len(coordinates),
                "bbox": compute_bbox(coordinates),
                "parse_errors": parse_errors,
            }
        )

    return payload


def cmd_summary(args: argparse.Namespace) -> int:
    document = load_document(args.file)
    print(json.dumps(build_summary(document), ensure_ascii=True, indent=2))
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    document = load_document(args.file)
    errors = validate_document(document)
    print(
        json.dumps(
            {
                "source_type": document.source_type,
                "source_entry": document.origin,
                "valid": not errors,
                "errors": errors,
            },
            ensure_ascii=True,
            indent=2,
        )
    )
    return 0 if not errors else 1


def cmd_placemarks(args: argparse.Namespace) -> int:
    document = load_document(args.file)
    print(json.dumps(placemark_payload(document), ensure_ascii=True, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="KML/KMZ summary and validation helper.")
    sub = parser.add_subparsers(dest="command", required=True)

    summary = sub.add_parser("summary", help="Summarize a KML or KMZ file.")
    summary.add_argument("--file", required=True)
    summary.set_defaults(func=cmd_summary)

    validate = sub.add_parser("validate", help="Validate a KML or KMZ file.")
    validate.add_argument("--file", required=True)
    validate.set_defaults(func=cmd_validate)

    placemarks = sub.add_parser("placemarks", help="List placemark-level summaries.")
    placemarks.add_argument("--file", required=True)
    placemarks.set_defaults(func=cmd_placemarks)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return args.func(args)
    except ValueError as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=True, indent=2))
        return 1


if __name__ == "__main__":
    sys.exit(main())
