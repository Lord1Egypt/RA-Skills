#!/usr/bin/env python3
"""
lobster-novel: Mermaid diagram generator (inspired by novel-generator).
Generates text-based Mermaid diagrams for:
- Character relationship graph
- Plot timeline flow
- Arc structure overview
Output can be rendered by any Mermaid-compatible viewer.
"""
import re
from pathlib import Path
from typing import List, Dict, Optional


class MermaidGen:
    """Generate Mermaid.js diagram text from novel data."""

    @staticmethod
    def character_relations(chars: List[Dict]) -> str:
        """Generate a character relationship graph.
        Each char dict: {name, role, relation_to, relation_type, notes}
        """
        if not chars:
            return "%% no character data"

        lines = ["graph TD;"]
        # Style classes
        roles = {}
        for ch in chars:
            role = ch.get("role", "other")
            if role not in roles:
                roles[role] = []
            roles[role].append(ch["name"])

        # Define character nodes
        for ch in chars:
            name = ch["name"]
            role = ch.get("role", "")
            safe_id = re.sub(r'[^a-zA-Z0-9\u4e00-\u9fff]', '_', name)
            if role:
                lines.append(f"  {safe_id}[\"{name}\\n({role})\"];")
            else:
                lines.append(f"  {safe_id}[\"{name}\"];")

        # Relations
        for ch in chars:
            target = ch.get("relation_to", "")
            rel = ch.get("relation_type", "")
            if target:
                src_id = re.sub(r'[^a-zA-Z0-9\u4e00-\u9fff]', '_', ch["name"])
                tgt_id = re.sub(r'[^a-zA-Z0-9\u4e00-\u9fff]', '_', target)
                if rel:
                    lines.append(f"  {src_id} -- \"{rel}\" --> {tgt_id};")
                else:
                    lines.append(f"  {src_id} --- {tgt_id};")

        # Subgraphs by role
        for role, members in roles.items():
            safe_role = re.sub(r'[^a-zA-Z0-9\u4e00-\u9fff]', '_', role)
            lines.insert(lines.index("graph TD;") + 1,
                         f"  subgraph {safe_role}[\"{role}\"]")
            for m in members:
                safe_m = re.sub(r'[^a-zA-Z0-9\u4e00-\u9fff]', '_', m)
                lines.append(f"    {safe_m}")
            lines.append("  end")

        return "\n".join(lines)

    @staticmethod
    def plot_flow(chapters: List[Dict]) -> str:
        """Generate a timeline flow of key plot events.
        Each chapter: {number, title, summary, hook_type, emotional_type}
        """
        if not chapters:
            return "%% no chapter data"

        lines = ["flowchart LR;"]
        # Styles for emotional types
        lines.append("  classDef buildup fill:#ffe0b0,stroke:#d4a040;")
        lines.append("  classDef climax fill:#ffb0b0,stroke:#d04040;")
        lines.append("  classDef resolution fill:#b0d4b0,stroke:#40a040;")
        lines.append("  classDef twist fill:#d0b0ff,stroke:#8040d0;")

        for i, ch in enumerate(chapters):
            num = ch.get("number", i + 1)
            title = ch.get("title", f"Ch{num}")
            etype = ch.get("emotional_type", "normal")
            eid = f"ch{num:02d}"

            # Truncate long titles
            label = title if len(title) <= 15 else title[:12] + ".."
            lines.append(f"  {eid}[\"Ch{num}: {label}\"];")

            # Connect to next
            if i < len(chapters) - 1:
                next_num = chapters[i + 1].get("number", i + 2)
                next_id = f"ch{next_num:02d}"
                hook = ch.get("hook_type", "")
                if hook:
                    hook_labels = {
                        "question": "❓", "reveal": "🔍", "danger": "⚠️",
                        "cliffhanger": "🎯", "new_element": "🆕",
                    }
                    label = hook_labels.get(hook, "→")
                    lines.append(f"  {eid} -- \"{label}\" --> {next_id};")
                else:
                    lines.append(f"  {eid} --> {next_id};")

            # Apply class
            lines.append(f"  class {eid} {etype};")

        return "\n".join(lines)

    @staticmethod
    def arc_overview(arcs: List[Dict]) -> str:
        """Generate an arc structure overview.
        Each arc: {number, title, chapter_range, climax_chapter}
        """
        if not arcs:
            return "%% no arc data"

        lines = ["gantt"]
        lines.append("    title Arc Structure")
        lines.append("    dateFormat  X")
        lines.append("    axisFormat  %d")
        lines.append("")

        for arc in arcs:
            num = arc.get("number", 0)
            title = arc.get("title", f"Arc {num}")
            start = arc.get("chapter_range", [1, 10])[0]
            end = arc.get("chapter_range", [1, 10])[1]
            climax = arc.get("climax_chapter", start + (end - start) // 2)

            lines.append(f"    section Arc {num}: {title}")
            lines.append(f"    Setup     :{start}, {climax - start - 1}d")
            lines.append(f"    Buildup   :{start + 1}, {climax - start - 1}d")
            lines.append(f"    Climax    :milestone, {climax}, 0d")
            lines.append(f"    Resolution:{climax + 1}, {end - climax}d")
            lines.append("")

        return "\n".join(lines)

    @staticmethod
    def save_to_file(mermaid_text: str, path: Path):
        """Save mermaid text to a .mmd file."""
        path.write_text(mermaid_text, encoding="utf-8")

    @staticmethod
    def generate_all(chars: List[Dict], chapters: List[Dict],
                     arcs: List[Dict], output_dir: Path) -> Dict[str, Path]:
        """Generate all 3 diagrams and save to output_dir."""
        output_dir.mkdir(parents=True, exist_ok=True)
        files = {}

        rel_text = MermaidGen.character_relations(chars)
        if rel_text and "no data" not in rel_text:
            rel_path = output_dir / "character_relations.mmd"
            MermaidGen.save_to_file(rel_text, rel_path)
            files["characters"] = rel_path

        flow_text = MermaidGen.plot_flow(chapters)
        if flow_text and "no data" not in flow_text:
            flow_path = output_dir / "plot_flow.mmd"
            MermaidGen.save_to_file(flow_text, flow_path)
            files["plot"] = flow_path

        arc_text = MermaidGen.arc_overview(arcs)
        if arc_text and "no data" not in arc_text:
            arc_path = output_dir / "arc_structure.mmd"
            MermaidGen.save_to_file(arc_text, arc_path)
            files["arcs"] = arc_path

        return files


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="mermaid diagram generator")
    parser.add_argument("--dir", default="./my-novel")
    parser.add_argument("--output", default="./diagrams")
    args = parser.parse_args()

    project_dir = Path(args.dir)
    output_dir = Path(args.output)

    # Load bible for character data
    from bible import BibleManager
    bm = BibleManager(project_dir)
    chars = [{"name": c.name, "role": c.role, "relation_to": "", "relation_type": ""}
             for c in bm.bible.characters.values()]

    # Load chapters
    ch_dir = project_dir / "chapters"
    chapters = []
    if ch_dir.exists():
        for f in sorted(ch_dir.glob("ch*.md")):
            chapters.append({
                "number": int(re.search(r'ch(\d+)', f.name).group(1)) if re.search(r'ch(\d+)', f.name) else 0,
                "title": f.name,
                "summary": "",
                "emotional_type": "buildup",
            })

    # Load arcs
    plans_dir = project_dir / "plans"
    arcs = []
    if plans_dir.exists():
        for f in sorted(plans_dir.glob("arc_*_plan.json")):
            try:
                import json
                data = json.loads(f.read_text())
                arcs.append(data)
            except:
                pass

    files = MermaidGen.generate_all(chars, chapters, arcs, output_dir)
    if files:
        print("Generated:")
        for k, v in files.items():
            print(f"  {k}: {v}")
    else:
        print("No data to generate diagrams from.")
