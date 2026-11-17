"""Build deterministic, bounded static ZIPs without executing project code."""

import hashlib
import stat
import unicodedata
import zipfile
from io import BytesIO
from pathlib import Path, PurePosixPath

from echo_cli.litepage_review import review

MAX_BYTES = 50 * 1024 * 1024
EXTENSIONS = {
    ".md",
    ".html",
    ".htm",
    ".css",
    ".js",
    ".mjs",
    ".json",
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".webp",
    ".svg",
    ".ico",
    ".woff",
    ".woff2",
    ".ttf",
    ".txt",
    ".mp3",
    ".ogg",
    ".wav",
    ".mp4",
    ".webm",
    ".wasm",
}
IGNORED = {
    "node_modules",
    "__pycache__",
    "package.json",
    "package-lock.json",
    "pnpm-lock.yaml",
    "yarn.lock",
}


def bundle(source, preview=None):
    source = Path(source).expanduser().absolute()
    if source.is_symlink():
        raise RuntimeError("Publish a regular file or directory, not a symlink")
    if not source.exists():
        raise RuntimeError("Publish source does not exist")
    candidates = []
    if source.is_file():
        if source.suffix.lower() not in {".html", ".htm", ".md", ".txt"}:
            raise RuntimeError("Single-file publishing requires HTML, Markdown or TXT")
        suffix = source.suffix.lower()
        candidates = [("index" + (".html" if suffix == ".htm" else suffix), source)]
    else:
        # Traverse explicitly so excluded directories are never entered.
        pending = [source]
        visited = 0
        while pending:
            parent = pending.pop()
            for path in parent.iterdir():
                visited += 1
                if visited > 1000:
                    raise RuntimeError(
                        "Too many entries; publish a dedicated static output directory"
                    )
                if (
                    path.name.startswith(".")
                    or path.name in IGNORED
                    or path.suffix.lower() == ".map"
                ):
                    continue
                if path.is_symlink():
                    raise RuntimeError(
                        "Symlinks are not included; copy public assets into the output directory"
                    )
                if path.is_dir():
                    pending.append(path)
                else:
                    candidates.append((path.relative_to(source).as_posix(), path))
    if not candidates or len(candidates) > 100:
        raise RuntimeError("Publish between 1 and 100 static files")
    files, total = {}, 0
    canonical_names = set()
    for name, path in sorted(candidates):
        if (
            len(name) > 240
            or any(c in name for c in "\\%?#:")
            or any(unicodedata.category(c).startswith("C") for c in name)
            or PurePosixPath(name).suffix.lower() not in EXTENSIONS
        ):
            raise RuntimeError(f"Unsupported static asset: {name[:160]}")
        canonical = unicodedata.normalize("NFC", name).casefold()
        if canonical in canonical_names:
            raise RuntimeError("Asset names must not differ only by case or Unicode normalization")
        canonical_names.add(canonical)
        mode = path.lstat().st_mode
        if not stat.S_ISREG(mode):
            raise RuntimeError("Only regular static files can be uploaded")
        total += path.stat().st_size
        if total > MAX_BYTES:
            raise RuntimeError("Expanded assets exceed 50 MiB")
        with path.open("rb") as stream:
            value = stream.read(MAX_BYTES + 1)
        if len(value) > MAX_BYTES or sum(map(len, files.values())) + len(value) > MAX_BYTES:
            raise RuntimeError("Assets changed or exceed 50 MiB")
        if b"-----BEGIN " in value and b"PRIVATE KEY-----" in value:
            raise RuntimeError(f"Private key detected in {name[:160]}; remove it before publishing")
        files[name] = value
    entry = next((name for name in ("index.html", "index.md", "index.txt") if name in files), None)
    if entry is None or not files[entry]:
        raise RuntimeError(
            "Provide a nonempty index.html, index.md or index.txt at the output root"
        )
    if entry != "index.html":
        if len(files[entry]) > 2 * 1024 * 1024:
            raise RuntimeError("Markdown/TXT documents must not exceed 2 MiB")
        try:
            text = files[entry].decode("utf-8")
        except UnicodeDecodeError:
            raise RuntimeError("Use UTF-8 for Markdown/TXT documents") from None
        if "\x00" in text:
            raise RuntimeError("Markdown/TXT documents must not contain NUL")
    if preview is not None:
        from echo_cli.litepage_cover import cover

        name = "litepage-preview.webp"
        if name.casefold() in canonical_names:
            raise RuntimeError("litepage-preview.webp is reserved when using --preview")
        files[name] = cover(preview)
        if len(files) > 100 or sum(map(len, files.values())) > MAX_BYTES:
            raise RuntimeError("Preview and assets exceed the bundle limits")
    inspection = review(files)
    output = BytesIO()
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, value in sorted(files.items()):
            info = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (stat.S_IFREG | 0o644) << 16
            archive.writestr(info, value)
    data = output.getvalue()
    if len(data) > MAX_BYTES:
        raise RuntimeError("ZIP upload exceeds 50 MiB")
    return data, {
        "file_count": len(files),
        "size": sum(map(len, files.values())),
        "sha256": hashlib.sha256(data).hexdigest(),
        "entry_sha256": hashlib.sha256(files[entry]).hexdigest(),
        "entrypoint": entry,
        **inspection,
    }
