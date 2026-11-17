#!/usr/bin/env python3
"""Create a fingering PDF from verified page images using only the standard library.

For PDF inputs, the host must first render each requested page to JPEG or PNG and
record the resulting local path in ``pages[].image``.  This script never parses an
arbitrary PDF, launches external programs, accesses the network, or deletes user files.
"""

from __future__ import annotations

import argparse
import struct
import sys
import zlib
from collections import defaultdict
from pathlib import Path

from plan_io import finite_number, load_plan, page_map
from source_provenance import file_digest


COLORS = {"RH": (0.09, 0.25, 0.42), "LH": (0.48, 0.14, 0.19)}
MAX_IMAGE_BYTES = 64 * 1024 * 1024


def pdf_number(value: float) -> str:
    return f"{value:.4f}".rstrip("0").rstrip(".")


def escape_text(value: str) -> str:
    return value.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def write_pdf(path: Path, objects: list[bytes]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0]
    for number, obj in enumerate(objects, 1):
        offsets.append(len(payload))
        payload.extend(f"{number} 0 obj\n".encode() + obj + b"\nendobj\n")
    xref = len(payload)
    payload.extend(f"xref\n0 {len(objects)+1}\n0000000000 65535 f \n".encode())
    for offset in offsets[1:]:
        payload.extend(f"{offset:010d} 00000 n \n".encode())
    payload.extend(f"trailer\n<< /Size {len(objects)+1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode())
    path.write_bytes(payload)


def jpeg_size(data: bytes) -> tuple[int, int, int]:
    if not data.startswith(b"\xff\xd8"):
        raise ValueError("invalid JPEG signature")
    index = 2
    while index + 9 < len(data):
        if data[index] != 0xFF:
            index += 1
            continue
        marker = data[index + 1]
        index += 2
        if marker in {0xD8, 0xD9}:
            continue
        length = struct.unpack(">H", data[index:index + 2])[0]
        if length < 2 or index + length > len(data):
            raise ValueError("invalid JPEG segment")
        if marker in range(0xC0, 0xC4):
            height, width, components = struct.unpack(">HHB", data[index + 3:index + 8])
            return width, height, components
        index += length
    raise ValueError("unable to determine JPEG dimensions")


def png_pixels(data: bytes) -> tuple[int, int, bytes, str]:
    if not data.startswith(b"\x89PNG\r\n\x1a\n"):
        raise ValueError("invalid PNG signature")
    pos, compressed = 8, bytearray()
    width = height = bit_depth = color_type = interlace = 0
    while pos + 12 <= len(data):
        length = struct.unpack(">I", data[pos:pos + 4])[0]
        kind = data[pos + 4:pos + 8]
        end = pos + 12 + length
        if end > len(data):
            raise ValueError("invalid PNG chunk length")
        payload = data[pos + 8:pos + 8 + length]
        pos = end
        if kind == b"IHDR":
            width, height, bit_depth, color_type, _, _, interlace = struct.unpack(">IIBBBBB", payload)
            if width <= 0 or height <= 0 or width * height > 100_000_000:
                raise ValueError("PNG dimensions exceed safety limit")
        elif kind == b"IDAT":
            compressed.extend(payload)
        elif kind == b"IEND":
            break
    if bit_depth != 8 or interlace != 0 or color_type not in {0, 2, 4, 6}:
        raise ValueError("PNG must be non-interlaced 8-bit grayscale, RGB, gray-alpha, or RGBA")
    channels = {0: 1, 2: 3, 4: 2, 6: 4}[color_type]
    expected_size = height * (width * channels + 1)
    decompressor = zlib.decompressobj()
    raw = decompressor.decompress(bytes(compressed), expected_size + 1)
    if decompressor.unconsumed_tail or len(raw) > expected_size:
        raise ValueError("PNG decompressed data exceeds safety limit")
    raw += decompressor.flush()
    stride = width * channels
    if len(raw) != height * (stride + 1):
        raise ValueError("unexpected PNG decompressed size")
    rows, offset, previous = [], 0, bytearray(stride)
    for _ in range(height):
        filter_type = raw[offset]
        scan = bytearray(raw[offset + 1:offset + 1 + stride])
        offset += stride + 1
        for x in range(stride):
            left = scan[x - channels] if x >= channels else 0
            up = previous[x]
            upper_left = previous[x - channels] if x >= channels else 0
            if filter_type == 1:
                scan[x] = (scan[x] + left) & 255
            elif filter_type == 2:
                scan[x] = (scan[x] + up) & 255
            elif filter_type == 3:
                scan[x] = (scan[x] + ((left + up) // 2)) & 255
            elif filter_type == 4:
                p = left + up - upper_left
                pa, pb, pc = abs(p - left), abs(p - up), abs(p - upper_left)
                predictor = left if pa <= pb and pa <= pc else up if pb <= pc else upper_left
                scan[x] = (scan[x] + predictor) & 255
            elif filter_type != 0:
                raise ValueError(f"unsupported PNG filter {filter_type}")
        rows.append(bytes(scan))
        previous = scan
    pixels = b"".join(rows)
    if color_type == 0:
        return width, height, pixels, "/DeviceGray"
    if color_type == 2:
        return width, height, pixels, "/DeviceRGB"
    color_channels = 1 if color_type == 4 else 3
    flattened = bytearray()
    for index in range(0, len(pixels), channels):
        alpha = pixels[index + color_channels]
        for component in pixels[index:index + color_channels]:
            flattened.append((component * alpha + 255 * (255 - alpha)) // 255)
    return width, height, bytes(flattened), "/DeviceGray" if color_channels == 1 else "/DeviceRGB"


def read_image(path: Path) -> tuple[int, int, bytes, str, str]:
    if not path.is_file():
        raise ValueError(f"page image not found: {path}")
    if path.stat().st_size > MAX_IMAGE_BYTES:
        raise ValueError(f"page image exceeds {MAX_IMAGE_BYTES // (1024*1024)} MiB limit: {path.name}")
    data = path.read_bytes()
    suffix = path.suffix.lower()
    if suffix in {".jpg", ".jpeg"}:
        width, height, components = jpeg_size(data)
        colorspace = "/DeviceGray" if components == 1 else "/DeviceRGB"
        if components not in {1, 3}:
            raise ValueError("only grayscale or RGB JPEG images are supported")
        return width, height, data, colorspace, "/DCTDecode"
    if suffix == ".png":
        width, height, pixels, colorspace = png_pixels(data)
        return width, height, zlib.compress(pixels), colorspace, "/FlateDecode"
    raise ValueError("page image must be JPEG or PNG")


def verified_external_page_asset(plan: dict, page_number: int, candidate: Path) -> bool:
    """Allow a source page outside the result directory only when bound to the plan.

    The pipeline deliberately writes generated plans into a fresh output
    directory, while visual source pages remain beside the user's original
    PDF.  The former directory-only check made every such successful run
    unrenderable.  Provenance gives us the safer boundary: exact path, size
    and SHA-256 must all match the page asset locked during recognition.
    """
    for asset in plan.get("recognition", {}).get("source_assets", []):
        if not isinstance(asset, dict) or asset.get("role") != "rendered_page":
            continue
        try:
            if int(asset.get("page", 0)) != page_number:
                continue
        except (TypeError, ValueError):
            continue
        if str(asset.get("path", "")) != str(candidate):
            continue
        if int(asset.get("bytes", -1)) != candidate.stat().st_size:
            continue
        expected = str(asset.get("sha256", "")).lower()
        if len(expected) == 64 and file_digest(candidate) == expected:
            return True
    return False


def resolve_page_image(plan_path: Path, plan: dict, page: dict, source: Path | None, page_count: int) -> Path:
    if source is not None and source.suffix.lower() in {".jpg", ".jpeg", ".png"}:
        if page_count != 1:
            raise ValueError("one source image can only be used with a one-page plan")
        candidate = source
    else:
        raw = page.get("image")
        if not raw:
            raise ValueError("PDF input requires a host-rendered local JPEG/PNG in pages[].image")
        candidate = Path(str(raw))
    if not candidate.is_absolute():
        candidate = plan_path.parent / candidate
    resolved = candidate.resolve()
    if source is None and not resolved.is_relative_to(plan_path.parent.resolve()):
        if not verified_external_page_asset(plan, int(page["page"]), resolved):
            raise ValueError(
                "pages[].image outside the plan directory must exactly match a SHA-256-bound rendered_page asset"
            )
    return resolved


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path)
    parser.add_argument("-o", "--output", type=Path, required=True)
    parser.add_argument("--source", type=Path, help="Optional JPEG/PNG source for a one-page plan")
    parser.add_argument("--dpi", type=float, default=144.0)
    parser.add_argument("--font-size", type=float, default=10.0)
    parser.add_argument("--offset", type=float, default=20.0)
    args = parser.parse_args()
    if args.dpi < 36 or args.dpi > 600:
        raise ValueError("dpi must be between 36 and 600")
    if args.output.suffix.lower() != ".pdf":
        raise ValueError("output must have a .pdf extension")
    if args.output.resolve() == args.plan.resolve():
        raise ValueError("output must not overwrite the input plan")
    plan = load_plan(args.plan)
    # A coloured digit on a copied score page looks finished even when its
    # source coordinate was merely guessed.  Do not create that misleading
    # artefact: PDF/image plans need a verified anchor for every labelled
    # note.  Structured MusicXML plans are intentionally outside this gate;
    # they may be exported as MusicXML without pretending to own page pixels.
    if str(plan.get("source", {}).get("type", "")).lower() in {"pdf", "image"}:
        unverified = [
            str(note.get("note_id", "unknown"))
            for note in plan.get("notes", [])
            if int(note.get("finger", 0) or 0) in {1, 2, 3, 4, 5}
            and note.get("anchor_verified") is not True
        ]
        if unverified:
            preview = ", ".join(unverified[:5])
            suffix = " …" if len(unverified) > 5 else ""
            raise ValueError(
                "PDF/image annotation requires verified source anchors for every labelled note; "
                f"missing: {preview}{suffix}"
            )
    declared = page_map(plan)
    source = args.source
    if source is not None and not source.is_absolute():
        source = (Path.cwd() / source).resolve()

    objects: list[bytes] = []
    objects.append(b"<< /Type /Catalog /Pages 2 0 R >>")
    declared_pages = [declared[number] for number in sorted(declared)]
    kids = " ".join(f"{4 + (index - 1) * 3} 0 R" for index in range(1, len(declared_pages) + 1))
    objects.append(f"<< /Type /Pages /Kids [{kids}] /Count {len(declared_pages)} >>".encode())
    objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>")

    total_labels = 0
    for render_index, page in enumerate(declared_pages, 1):
        source_page_number = int(page["page"])
        image_path = resolve_page_image(args.plan, plan, page, source, len(declared_pages))
        width_px, height_px, pixels, colorspace, image_filter = read_image(image_path)
        coordinate_width = finite_number(page["width"], f"page {source_page_number}.width")
        coordinate_height = finite_number(page["height"], f"page {source_page_number}.height")
        if abs(width_px / height_px - coordinate_width / coordinate_height) > 0.02:
            raise ValueError(f"page {source_page_number} image aspect ratio conflicts with plan")
        width, height = width_px * 72 / args.dpi, height_px * 72 / args.dpi
        sx, sy = width / coordinate_width, height / coordinate_height
        commands = [f"q {pdf_number(width)} 0 0 {pdf_number(height)} 0 0 cm /Im{render_index} Do Q"]
        notes = [n for n in plan["notes"] if int(n.get("page", 0)) == source_page_number and int(n.get("finger", 0))]
        groups: dict[tuple, list[dict]] = defaultdict(list)
        for note in notes:
            key = (note.get("part"), note.get("measure_index"), float(note.get("onset", 0)), note.get("event_index"), note.get("chord_id"), note.get("hand"))
            groups[key].append(note)
        for note in notes:
            hand = note["hand"]
            key = (note.get("part"), note.get("measure_index"), float(note.get("onset", 0)), note.get("event_index"), note.get("chord_id"), hand)
            chord = sorted(groups[key], key=lambda item: int(item.get("chord_row", 0)))
            stacked = len(chord) > 1 and note.get("chord_label_layout", "stacked") == "stacked"
            x = float(note.get("label_x", note["page_x"])) * sx
            if stacked:
                x = float(note.get("chord_label_x", sum(float(item["page_x"]) for item in chord) / len(chord))) * sx
            anchor_y = coordinate_height - float(note["page_y"])
            y = anchor_y * sy
            size = float(note.get("font_size", args.font_size))
            if stacked:
                anchors = [(coordinate_height - float(item["page_y"])) * sy for item in chord]
                offset = float(note.get("chord_label_offset", note.get("label_offset", args.offset))) * sy
                if note["placement"] == "above":
                    y = max(anchors) + offset + int(note.get("chord_row", 0)) * size * 1.15
                else:
                    y = min(anchors) - offset + int(note.get("chord_row", 0)) * size * 1.15
            else:
                offset = float(note.get("label_offset", args.offset)) * sy
                y += offset if note["placement"] == "above" else -offset
            red, green, blue = COLORS[hand]
            digit = escape_text(str(int(note["finger"])))
            commands.append(f"BT /F1 {pdf_number(size)} Tf {pdf_number(red)} {pdf_number(green)} {pdf_number(blue)} rg 1 0 0 1 {pdf_number(x-size*0.28)} {pdf_number(y-size*0.34)} Tm ({digit}) Tj ET")
        total_labels += len(notes)
        content = "\n".join(commands).encode()
        page_id = 4 + (render_index - 1) * 3
        content_id, image_id = page_id + 1, page_id + 2
        objects.append(f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {pdf_number(width)} {pdf_number(height)}] /Resources << /Font << /F1 3 0 R >> /XObject << /Im{render_index} {image_id} 0 R >> >> /Contents {content_id} 0 R >>".encode())
        objects.append(f"<< /Length {len(content)} >>\nstream\n".encode() + content + b"\nendstream")
        objects.append(f"<< /Type /XObject /Subtype /Image /Width {width_px} /Height {height_px} /ColorSpace {colorspace} /BitsPerComponent 8 /Filter {image_filter} /Length {len(pixels)} >>\nstream\n".encode() + pixels + b"\nendstream")

    write_pdf(args.output, objects)
    print(f"Rendered {len(declared_pages)} page(s), {total_labels} labels: {args.output}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
