"""Bounded MusicXML/MXL loading helpers for untrusted user files."""

from __future__ import annotations

import xml.etree.ElementTree as ET
from pathlib import Path, PurePosixPath
from zipfile import BadZipFile, ZipFile


MAX_XML_BYTES = 32 * 1024 * 1024
MAX_ARCHIVE_ENTRIES = 256
MAX_COMPRESSION_RATIO = 200


def _parse_xml_bytes(data: bytes, label: str) -> ET.ElementTree:
    if len(data) > MAX_XML_BYTES:
        raise ValueError(f"XML exceeds 32 MiB safety limit: {label}")
    upper = data[: min(len(data), 1_000_000)].upper()
    if b"<!ENTITY" in upper:
        raise ValueError(f"ENTITY declarations are not allowed: {label}")
    if b"<!DOCTYPE" in upper:
        start = upper.find(b"<!DOCTYPE")
        end = upper.find(b">", start)
        if end < 0 or b"[" in upper[start:end + 1] or b"<!DOCTYPE" in upper[end + 1:]:
            raise ValueError(f"internal or repeated DOCTYPE is not allowed: {label}")
        data = data[:start] + data[end + 1:]
    return ET.ElementTree(ET.fromstring(data))


def _safe_member(name: str) -> bool:
    path = PurePosixPath(name)
    return bool(name) and not path.is_absolute() and ".." not in path.parts and "\\" not in name


def load_musicxml(path: Path, allow_mxl: bool = True) -> tuple[ET.ElementTree, str]:
    if not path.is_file():
        raise ValueError(f"input not found: {path}")
    if path.suffix.lower() != ".mxl":
        return _parse_xml_bytes(path.read_bytes(), path.name), path.name
    if not allow_mxl:
        raise ValueError("MXL input is not supported for this operation")
    if path.stat().st_size > MAX_XML_BYTES:
        raise ValueError("MXL exceeds 32 MiB safety limit")
    try:
        with ZipFile(path) as archive:
            infos = archive.infolist()
            if len(infos) > MAX_ARCHIVE_ENTRIES:
                raise ValueError("MXL contains too many archive entries")
            for info in infos:
                if not _safe_member(info.filename):
                    raise ValueError(f"unsafe MXL member path: {info.filename}")
                if info.file_size > MAX_XML_BYTES:
                    raise ValueError(f"MXL member exceeds 32 MiB limit: {info.filename}")
                compressed = max(info.compress_size, 1)
                if info.file_size / compressed > MAX_COMPRESSION_RATIO:
                    raise ValueError(f"MXL compression ratio exceeds safety limit: {info.filename}")
            names = {info.filename for info in infos}
            root_name = ""
            if "META-INF/container.xml" in names:
                container = _parse_xml_bytes(archive.read("META-INF/container.xml"), "META-INF/container.xml")
                for item in container.getroot().iter():
                    if item.tag.rsplit("}", 1)[-1] == "rootfile":
                        root_name = item.attrib.get("full-path", "")
                        if root_name:
                            break
            if not root_name:
                root_name = next((name for name in names if name.lower().endswith(".xml") and name != "META-INF/container.xml"), "")
            if not root_name or root_name not in names or not _safe_member(root_name):
                raise ValueError("MXL does not declare a safe MusicXML root file")
            return _parse_xml_bytes(archive.read(root_name), root_name), f"{path.name}:{root_name}"
    except BadZipFile as exc:
        raise ValueError("invalid MXL archive") from exc
