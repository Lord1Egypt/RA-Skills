from __future__ import annotations

from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
OUT = DIST / "openclaw-success-skill-publisher.zip"

INCLUDE = (
    "SKILL.md",
    "agents/openai.yaml",
    "scripts/",
    "references/",
    "examples/",
)


def should_include(path: Path) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    if "/__pycache__/" in f"/{rel}/":
        return False
    return any(rel == p or rel.startswith(p) for p in INCLUDE)


def main() -> int:
    DIST.mkdir(parents=True, exist_ok=True)
    with ZipFile(OUT, "w", ZIP_DEFLATED) as zf:
        for p in sorted(ROOT.rglob("*")):
            if p.is_file() and should_include(p):
                zf.write(p, arcname=p.relative_to(ROOT).as_posix())
    print(f"Wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
