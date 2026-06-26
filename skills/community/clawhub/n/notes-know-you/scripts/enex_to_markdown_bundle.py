from __future__ import annotations

import argparse
import html
import re
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

from bs4 import BeautifulSoup


INVALID_FILENAME_CHARS = r'[\\/:*?"<>|]'


def sanitize_filename(name: str) -> str:
    cleaned = re.sub(INVALID_FILENAME_CHARS, "_", name).strip()
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned[:180] or "untitled"


def strip_enml_wrappers(content: str) -> str:
    content = re.sub(r"<\?xml[^>]*\?>", "", content, flags=re.IGNORECASE).strip()
    content = re.sub(r"<!DOCTYPE[^>]*>", "", content, flags=re.IGNORECASE).strip()
    return content


def prepare_html(content: str) -> str:
    soup = BeautifulSoup(strip_enml_wrappers(content), "xml")
    note = soup.find("en-note")
    root = note if note is not None else soup

    for todo in root.find_all("en-todo"):
        checked = todo.get("checked", "").lower() == "true"
        todo.replace_with(soup.new_string("[x] " if checked else "[ ] "))

    for media in root.find_all("en-media"):
        media_type = media.get("type", "attachment")
        media.replace_with(soup.new_string(f"[Attachment: {media_type}]"))

    for br in root.find_all("br"):
        br.replace_with(soup.new_string("\n"))

    for tag in root.find_all(["span", "font"]):
        tag.unwrap()

    for a in root.find_all("a"):
        href = a.get("href")
        text = a.get_text(" ", strip=True)
        if href:
            a.replace_with(soup.new_string(f"[{text}]({href})"))
        else:
            a.replace_with(soup.new_string(text))

    for div in root.find_all("div"):
        div.insert_before(soup.new_string("\n"))
        div.insert_after(soup.new_string("\n"))
        div.unwrap()

    for tag in root.find_all(True):
        allowed = {}
        if tag.name == "img" and tag.get("src"):
            allowed["src"] = tag.get("src")
        if tag.name == "a" and tag.get("href"):
            allowed["href"] = tag.get("href")
        tag.attrs = allowed

    return "".join(str(child) for child in root.contents)


def html_to_markdown(html_content: str) -> str:
    result = subprocess.run(
        ["pandoc", "--from=html", "--to=gfm"],
        input=html_content,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=True,
    )
    return result.stdout.strip()


def clean_markdown(markdown: str) -> str:
    markdown = re.sub(r"(?m)^\\(#{1,6}\s)", r"\1", markdown)
    markdown = markdown.replace(r"\[", "[").replace(r"\]", "]")
    markdown = re.sub(r"(?m)^[ \t]*</?div>[ \t]*\n?", "", markdown)
    markdown = re.sub(r"(?m)^[ \t]*</?span[^>]*>[ \t]*\n?", "", markdown)
    markdown = re.sub(r"(?m)^[ \t]*<!--\s*-->[ \t]*\n?", "", markdown)
    markdown = re.sub(r"\n{3,}", "\n\n", markdown)
    return markdown.strip()


def note_to_markdown(note_el: ET.Element) -> str:
    title = note_el.findtext("title", default="Untitled")
    created = note_el.findtext("created", default="")
    updated = note_el.findtext("updated", default="")
    content = note_el.findtext("content", default="")
    source_url = note_el.findtext("note-attributes/source-url", default="")

    md_body = clean_markdown(html_to_markdown(prepare_html(content)))
    lines = [f"# {title}", ""]

    if created:
        lines.append(f"- Created: `{created}`")
    if updated:
        lines.append(f"- Updated: `{updated}`")
    if source_url:
        lines.append(f"- Source: `{html.unescape(source_url)}`")

    if len(lines) > 2:
        lines.append("")

    if md_body:
        lines.append(md_body)

    return "\n".join(lines).rstrip() + "\n"


def convert_enex_to_merged_markdown(enex_path: Path, output_file: Path) -> int:
    output_file.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    notes: list[tuple[str, str, str]] = []

    context = ET.iterparse(enex_path, events=("end",))
    for _event, elem in context:
        if elem.tag != "note":
            continue

        title = elem.findtext("title", default="Untitled")
        updated = elem.findtext("updated", default="")
        notes.append((updated, title, note_to_markdown(elem)))

        count += 1
        elem.clear()

    notes.sort(key=lambda item: (item[0], item[1]), reverse=True)

    with output_file.open("w", encoding="utf-8") as out:
        out.write(f"# {enex_path.stem}\n\n")
        for index, (_updated, _title, content) in enumerate(notes):
            if index > 0:
                out.write("\n\n---\n\n")
            out.write(content.rstrip())
            out.write("\n")

    return count


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert an ENEX file directly into one merged Markdown file."
    )
    parser.add_argument("input", type=Path, help="Path to the ENEX file")
    parser.add_argument("output_dir", type=Path, help="Directory for the final Markdown file")
    parser.add_argument("--output-file", type=Path, help="Optional explicit Markdown output path")
    args = parser.parse_args()

    output_file = args.output_file
    if output_file is None:
        output_file = args.output_dir / f"{sanitize_filename(args.input.stem)}.md"

    converted = convert_enex_to_merged_markdown(args.input, output_file)
    print(f"Converted {converted} notes to {output_file}")


if __name__ == "__main__":
    main()
