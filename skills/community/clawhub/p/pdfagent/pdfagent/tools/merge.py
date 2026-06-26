from __future__ import annotations

from pathlib import Path
from typing import Iterable

from pypdf import PdfReader, PdfWriter


def merge_pdfs(
    inputs: Iterable[Path],
    output: Path,
    password: str | None = None,
    passwords: dict[str, str] | None = None,
) -> None:
    writer = PdfWriter()
    for path in inputs:
        reader = PdfReader(str(path))
        if reader.is_encrypted:
            _decrypt_reader(reader, path, password=password, passwords=passwords)
        for page in reader.pages:
            writer.add_page(page)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("wb") as f:
        writer.write(f)


def _decrypt_reader(
    reader: PdfReader,
    path: Path,
    *,
    password: str | None,
    passwords: dict[str, str] | None,
) -> None:
    candidates: list[str] = []
    if passwords:
        pwd = passwords.get(str(path)) or passwords.get(path.name)
        if pwd:
            candidates.append(pwd)
    if password:
        candidates.append(password)
    candidates.append("")  # many PDFs are encrypted with an empty user password

    for pwd in candidates:
        try:
            if reader.decrypt(pwd):
                return
        except Exception:
            continue

    raise ValueError(
        f"Encrypted PDF requires password: {path}. "
        "Provide --password or --passwords (file=pass) to decrypt."
    )
