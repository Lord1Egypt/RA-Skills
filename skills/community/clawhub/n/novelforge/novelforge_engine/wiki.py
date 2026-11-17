"""Native Markdown Wiki engine and deterministic integrity manifest."""

from pathlib import Path

from .io import (
    format_frontmatter,
    parse_frontmatter,
    read_frontmatter,
    read_json,
    safe_id,
    sha256_file,
    write_bytes_atomic,
    write_frontmatter_atomic,
    write_json_atomic,
)


def _safe_id(value):
    return safe_id(value)


WIKI_FOLDERS = (
    "characters",
    "locations",
    "items",
    "factions",
    "hooks",
    "relations",
    "timeline",
    "entities",
    "blueprints",
    "chapters",
)

FOLDER_BY_TYPE = {
    "character": "characters",
    "location": "locations",
    "item": "items",
    "faction": "factions",
    "hook": "hooks",
    "relation": "relations",
    "event": "timeline",
    "entity": "entities",
}


def collection_for_type(entity_type):
    return FOLDER_BY_TYPE.get(entity_type, "entities")


def format_entity_markdown(value, body=""):
    metadata = dict(value)
    name = metadata.get("name", metadata.get("id", "Untitled"))
    if not body:
        lines = [f"# {name}\n"]
        for key in sorted(metadata):
            if key in ("id", "name", "type", "_source_chapter", "_source_body_hash", "personality"):
                continue
            lines.append(f"\n## {key.replace('_', ' ').title()}\n\n{metadata[key]}")
        body = "\n".join(lines).rstrip() + "\n"
    return format_frontmatter(metadata, body)


def read_wiki_page(path):
    return read_frontmatter(path)


def write_wiki_page_atomic(path, metadata, body=""):
    write_frontmatter_atomic(path, metadata, body)


def _scan_wiki_files(root):
    """Scan all markdown files in the project returning (relative_path, full_path, metadata, body)."""
    root = Path(root).resolve()
    entries = []
    seen = set()

    # Scan standard root creation folders
    for folder in WIKI_FOLDERS:
        folder_path = root / folder
        if folder_path.is_dir():
            for path in sorted(folder_path.rglob("*.md")):
                try:
                    rel = str(path.relative_to(root))
                except ValueError:
                    continue
                parts = Path(rel).parts
                if any(not safe_id(part) and not (part.endswith(".md") and safe_id(part[:-3])) for part in parts):
                    continue
                try:
                    metadata, body = read_frontmatter(path)
                except Exception:
                    metadata, body = {}, ""
                entries.append((rel, path, metadata, body))
                seen.add(rel)

    # Legacy fallback: scan wiki/ subdirectory if present
    wiki = root / "wiki"
    if wiki.is_dir():
        for path in sorted(wiki.rglob("*.md")):
            if path.name == "index.md":
                continue
            try:
                rel = str(path.relative_to(root))
            except ValueError:
                continue
            if rel in seen:
                continue
            parts = Path(rel).parts
            if any(not safe_id(part) and not (part.endswith(".md") and safe_id(part[:-3])) for part in parts):
                continue
            try:
                metadata, body = read_frontmatter(path)
            except Exception:
                metadata, body = {}, ""
            entries.append((rel, path, metadata, body))
            seen.add(rel)

    # Scan outline.md (root or legacy wiki/)
    for outline_path in (root / "outline.md", root / "wiki" / "outline.md"):
        if outline_path.is_file():
            rel = str(outline_path.relative_to(root))
            if rel not in seen:
                try:
                    meta, body = read_frontmatter(outline_path)
                except Exception:
                    meta, body = {}, ""
                entries.append((rel, outline_path, meta, body))
                seen.add(rel)
            break

    return entries


def rebuild_wiki(root):
    """Rebuild index.md and .novelforge/wiki-manifest.json based on markdown files."""
    root = Path(root).resolve()
    for folder in WIKI_FOLDERS:
        (root / folder).mkdir(parents=True, exist_ok=True)

    entries = _scan_wiki_files(root)

    # Group pages
    chapters = []
    blueprints = []
    characters = []
    locations = []
    items = []
    factions = []
    hooks = []
    timeline = []
    others = []

    generated = []
    hashes = {}

    for rel, path, meta, _body in entries:
        generated.append(rel)
        hashes[rel] = sha256_file(path)
        stem = rel[:-3] if rel.endswith(".md") else rel
        link_title = meta.get("name") or meta.get("title") or Path(rel).stem

        # strip legacy "wiki/" prefix for grouping
        norm_rel = rel[5:] if rel.startswith("wiki/") else rel
        if norm_rel.startswith("chapters/"):
            chapters.append((stem, link_title))
        elif norm_rel.startswith("blueprints/"):
            blueprints.append((stem, link_title))
        elif norm_rel.startswith("characters/"):
            characters.append((stem, link_title))
        elif norm_rel.startswith("locations/"):
            locations.append((stem, link_title))
        elif norm_rel.startswith("items/"):
            items.append((stem, link_title))
        elif norm_rel.startswith("factions/"):
            factions.append((stem, link_title))
        elif norm_rel.startswith("hooks/"):
            hooks.append((stem, link_title))
        elif norm_rel.startswith("timeline/"):
            timeline.append((stem, link_title))
        elif norm_rel != "outline.md":
            others.append((stem, link_title))

    sections = ["# Story Index\n"]
    if (root / "outline.md").is_file() or (root / "wiki" / "outline.md").is_file():
        outline_link = "outline" if (root / "outline.md").is_file() else "wiki/outline"
        sections.append(f"## 故事大纲与主线\n\n- [[{outline_link}]]\n")

    if chapters or blueprints:
        sections.append("## 章节与蓝图 (Chapters & Blueprints)\n")
        all_ch_ids = sorted(set([s.split("/")[-1] for s, _ in chapters] + [s.split("/")[-1] for s, _ in blueprints]))
        ch_dict = {s.split("/")[-1]: title for s, title in chapters}
        bp_set = {s.split("/")[-1] for s, _ in blueprints}
        for ch_id in all_ch_ids:
            line_parts = []
            if ch_id in ch_dict:
                line_parts.append(f"[[chapters/{ch_id}]] ({ch_dict[ch_id]})")
            if ch_id in bp_set:
                line_parts.append(f"[[blueprints/{ch_id}]] (蓝图)")
            sections.append("- " + " | ".join(line_parts))
        sections.append("")

    if characters:
        sections.append("## 人物志 (Characters)\n")
        for stem, name in characters:
            sections.append(f"- [[{stem}]] - {name}")
        sections.append("")

    if locations:
        sections.append("## 世界与场景 (Locations)\n")
        for stem, name in locations:
            sections.append(f"- [[{stem}]] - {name}")
        sections.append("")

    if items:
        sections.append("## 功法与道具 (Items)\n")
        for stem, name in items:
            sections.append(f"- [[{stem}]] - {name}")
        sections.append("")

    if factions:
        sections.append("## 阵营与势力 (Factions)\n")
        for stem, name in factions:
            sections.append(f"- [[{stem}]] - {name}")
        sections.append("")

    if hooks:
        sections.append("## 伏笔与线索 (Hooks)\n")
        for stem, name in hooks:
            sections.append(f"- [[{stem}]] - {name}")
        sections.append("")

    if timeline:
        sections.append("## 纪事与时间线 (Timeline)\n")
        for stem, name in timeline:
            sections.append(f"- [[{stem}]] - {name}")
        sections.append("")

    if others:
        sections.append("## 其他设定 (Entities)\n")
        for stem, name in others:
            sections.append(f"- [[{stem}]] - {name}")
        sections.append("")

    if len(sections) == 1:
        sections.append("No entries yet.\n")

    index_text = "\n".join(sections).rstrip() + "\n"
    index_file = root / "index.md"
    write_bytes_atomic(index_file, index_text.encode("utf-8"))

    # Also keep wiki/index.md in sync if legacy wiki/ folder exists
    if (root / "wiki").is_dir():
        write_bytes_atomic(root / "wiki" / "index.md", index_text.encode("utf-8"))

    generated.append("index.md")
    hashes["index.md"] = sha256_file(index_file)

    manifest_path = root / ".novelforge" / "wiki-manifest.json"
    files = sorted(generated)
    manifest = {
        "schema": 1,
        "files": files,
        "hashes": {rel: hashes[rel] for rel in files},
    }
    write_json_atomic(manifest_path, manifest)

    total_pages = len(files) - 1  # exclude index.md
    return {"pages": total_pages, "index": str(index_file)}


def validate_wiki(root):
    """Validate story markdown files and their integrity manifest."""
    root = Path(root).resolve()
    manifest_path = root / ".novelforge" / "wiki-manifest.json"
    if not manifest_path.is_file():
        raise ValueError("wiki manifest is missing")

    index_file = root / "index.md"
    if not index_file.is_file():
        if (root / "wiki" / "index.md").is_file():
            index_file = root / "wiki" / "index.md"
        else:
            raise ValueError("index.md is missing")

    manifest = read_json(manifest_path)
    if not isinstance(manifest, dict) or manifest.get("schema") != 1:
        raise ValueError("invalid wiki manifest")

    files = manifest.get("files")
    hashes = manifest.get("hashes")
    if (
        not isinstance(files, list)
        or len(files) != len(set(files))
        or "index.md" not in files
        or not isinstance(hashes, dict)
        or set(files) != set(hashes)
    ):
        raise ValueError("invalid wiki manifest")

    for relative in files:
        if not isinstance(relative, str) or not relative or Path(relative).is_absolute():
            raise ValueError("wiki manifest contains an unsafe path")
        candidate = root / relative
        if not candidate.is_file() and (root / "wiki" / relative).is_file():
            candidate = root / "wiki" / relative
        try:
            candidate.resolve().relative_to(root.resolve())
        except (ValueError, OSError, TypeError):
            raise ValueError("wiki manifest contains an unsafe path")
        if not candidate.is_file() or hashes.get(relative) != sha256_file(candidate):
            raise ValueError("wiki page is missing or stale: {}".format(relative))

    # Check that no unmanifested markdown files exist
    actual_files = set()
    if (root / "index.md").is_file():
        actual_files.add("index.md")
    if (root / "outline.md").is_file():
        actual_files.add("outline.md")
    for folder in WIKI_FOLDERS:
        folder_path = root / folder
        if folder_path.is_dir():
            for path in folder_path.rglob("*.md"):
                try:
                    actual_files.add(str(path.relative_to(root)))
                except ValueError:
                    pass
    if (root / "wiki").is_dir():
        for path in (root / "wiki").rglob("*.md"):
            if path.name == "index.md":
                continue
            try:
                rel = str(path.relative_to(root))
                if rel in files:
                    actual_files.add(rel)
            except ValueError:
                pass

    if set(files) != actual_files:
        raise ValueError("wiki page set is stale")

    return manifest
