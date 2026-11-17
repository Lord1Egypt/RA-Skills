from __future__ import annotations

from dataclasses import dataclass
from importlib.abc import Traversable
from importlib.resources import files
from pathlib import Path
from typing import Iterable


STYLE_SKILLS = {
    "academic-paper",
    "argumentative",
    "fiction",
    "formal-document",
    "news-report",
    "self-media",
    "webnovel",
}


@dataclass(frozen=True)
class Skill:
    name: str
    path: Traversable
    content: str
    kind: str


def default_skills_dir() -> Traversable:
    source_skills = Path(__file__).resolve().parent.parent / "skills"
    if source_skills.is_dir():
        return source_skills
    try:
        return files("humanwriting_skill_data")
    except ModuleNotFoundError:
        return source_skills


def list_skills(skills_dir: Path | None = None) -> list[str]:
    root = skills_dir or default_skills_dir()
    return sorted(
        path.name.removesuffix(".md")
        for path in root.iterdir()
        if path.is_file() and path.name.endswith(".md")
    )


def list_style_skills(skills_dir: Path | None = None) -> list[str]:
    return [name for name in list_skills(skills_dir) if name in STYLE_SKILLS]


def list_module_skills(skills_dir: Path | None = None) -> list[str]:
    return [name for name in list_skills(skills_dir) if name not in STYLE_SKILLS]


def load_skill(name: str, skills_dir: Path | None = None) -> Skill:
    root = skills_dir or default_skills_dir()
    path = root / f"{name}.md"
    if not path.exists():
        available = ", ".join(list_skills(root)) or "none"
        raise FileNotFoundError(f"Unknown skill '{name}'. Available skills: {available}")
    kind = "style" if name in STYLE_SKILLS else "module"
    return Skill(name=name, path=path, content=path.read_text(encoding="utf-8").strip(), kind=kind)


def load_many(names: Iterable[str], skills_dir: Path | None = None) -> list[Skill]:
    loaded: list[Skill] = []
    seen: set[str] = set()
    for name in names:
        if name not in seen:
            loaded.append(load_skill(name, skills_dir))
            seen.add(name)
    return loaded
