#!/usr/bin/env python3
import os
import re
import argparse
from typing import List, Dict, Optional


def find_used_citation_keys(project_dir: str) -> set:
    """Scan all .tex files under project_dir and collect used BibTeX keys."""
    pattern = re.compile(r"\\cite[t|p]?\{([^}]*)\}")
    used = set()
    for root, _dirs, files in os.walk(project_dir):
        for fn in files:
            if fn.endswith(".tex"):
                path = os.path.join(root, fn)
                with open(path, "r", encoding="utf-8") as f:
                    text = f.read()
                for match in pattern.finditer(text):
                    keys_str = match.group(1)
                    for key in keys_str.split(","):
                        key = key.strip()
                        if key:
                            used.add(key)
    return used


def find_all_bib_keys(bib_path: str) -> List[str]:
    """Parse custom.bib and return all entry keys (best-effort, lightweight parser)."""
    if not os.path.exists(bib_path):
        return []
    with open(bib_path, "r", encoding="utf-8") as f:
        text = f.read()
    keys: List[str] = []
    for match in re.finditer(r"@\w+\s*\{\s*([^,]+),", text):
        keys.append(match.group(1).strip())
    return keys


def choose_new_keys(all_keys: List[str], used_keys: set, limit: int) -> List[str]:
    """Pick up to `limit` keys that are present in custom.bib but not used in any \cite."""
    candidates = [k for k in all_keys if k not in used_keys]
    return candidates[: max(limit, 0)]


def insert_citation_sentence(
    tex_path: str,
    template: str,
    keys: List[str],
    anchor_substring: Optional[str] = None,
) -> Optional[Dict]:
    """Insert a new sentence with citations into a .tex file.

    The sentence is inserted right after the line containing `anchor_substring` if provided;
    otherwise it is appended to the end of the file.
    """
    if not os.path.exists(tex_path):
        print(f"[WARN] TeX file not found, skip: {tex_path}")
        return None

    with open(tex_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    cite_cmd = "\\cite{" + ",".join(keys) + "}"
    sentence = template.format(cites=cite_cmd)

    insert_idx = None
    if anchor_substring:
        for i, line in enumerate(lines):
            if anchor_substring in line:
                insert_idx = i + 1
                break
    if insert_idx is None:
        insert_idx = len(lines)

    new_lines: List[str] = []
    for idx, line in enumerate(lines):
        new_lines.append(line)
        if idx == insert_idx - 1:
            new_lines.append("% Added by oldglycine-paper-reference-adder\n")
            new_lines.append(sentence + "\n\n")

    with open(tex_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

    print(f"[INFO] Inserted citation sentence into {tex_path}")
    return {"file": tex_path, "sentence": sentence, "keys": keys}


def main() -> None:
    parser = argparse.ArgumentParser(description="oldglycine-paper-reference-adder runner")
    parser.add_argument("--project_dir", default="./", help="Overleaf-like project directory")
    parser.add_argument("--num_references", type=int, default=10, help="Maximum number of new references to use")
    parser.add_argument("--output_report", default="ADD.MD", help="Name of the ADD report file (relative to project_dir)")
    args = parser.parse_args()

    project_dir = os.path.abspath(args.project_dir)
    bib_path = os.path.join(project_dir, "custom.bib")
    report_path = os.path.join(project_dir, args.output_report)

    print(f"[INFO] Project directory: {project_dir}")
    print(f"[INFO] BibTeX file: {bib_path}")

    used_keys = find_used_citation_keys(project_dir)
    all_keys = find_all_bib_keys(bib_path)

    print(f"[INFO] Existing citation keys in .tex files: {len(used_keys)}")
    print(f"[INFO] Total keys in custom.bib: {len(all_keys)}")

    new_keys = choose_new_keys(all_keys, used_keys, args.num_references)
    print(f"[INFO] Unused keys available from custom.bib: {len(new_keys)}")

    modifications: List[Dict] = []

    if new_keys:
        # Allocate roughly half of them to Introduction and the rest to Related Work
        half = max(1, len(new_keys) // 2)
        intro_keys = new_keys[:half]
        related_keys = new_keys[half:]

        intro_path = os.path.join(project_dir, "section", "02_introduction.tex")
        related_path = os.path.join(project_dir, "section", "03_related_work.tex")

        if intro_keys:
            intro_template = (
                "Recent work on generative AI, music cognition, and human-centered evaluation "
                "further contextualizes this discussion {cites}."
            )
            m = insert_citation_sentence(
                intro_path,
                intro_template,
                intro_keys,
                anchor_substring="TODO:加引用",
            )
            if m:
                modifications.append(m)

        if related_keys:
            related_template = (
                "Complementary studies on generative models, aesthetic evaluation, and personalized "
                "recommendation highlight similar challenges in capturing subjective preferences {cites}."
            )
            m = insert_citation_sentence(
                related_path,
                related_template,
                related_keys,
                anchor_substring="\\subsection{Exploration of Musical Aesthetics and Personalization}",
            )
            if m:
                modifications.append(m)
    else:
        print("[WARN] No unused keys found in custom.bib; no new citation sentences will be inserted.")

    # Generate ADD.MD-style report
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# Added References Report (oldglycine-paper-reference-adder)\n\n")
        f.write(f"Project directory: {project_dir}\n\n")
        if not modifications:
            f.write("No new citation sentences were inserted.\n")
        else:
            for idx, m in enumerate(modifications, 1):
                rel_path = os.path.relpath(m["file"], project_dir)
                f.write(f"## {idx}. File: {rel_path}\n\n")
                f.write("Reference Position Sentence:\n\n")
                f.write(m["sentence"] + "\n\n")
                f.write("BibTeX Keys:\n\n")
                for key in m["keys"]:
                    f.write(f"- {key}\n")
                f.write("\n")

    print(f"[INFO] Report written to {report_path}")
    print(f"[INFO] Total modified files: {len(modifications)}")


if __name__ == "__main__":
    main()
