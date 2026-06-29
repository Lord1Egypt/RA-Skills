from __future__ import annotations

import argparse
import json

import gitea_api as g
from utils import json_fail, now_str, sanitize_filename


def out(data: dict) -> None:
    print(json.dumps(data, ensure_ascii=False))


def append_file(owner: str, repo: str, path: str, line: str, title: str) -> None:
    existing = g.get_file(owner, repo, path)
    if existing:
        content, sha = existing
        g.put_file(owner, repo, path, content.rstrip() + "\n" + line + "\n", f"paper-kb: update {path}", sha=sha)
    else:
        g.put_file(owner, repo, path, f"# {title}\n\n{line}\n", f"paper-kb: init {path}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--owner", required=True)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--project_id", default="general")
    parser.add_argument("--title", required=True)
    parser.add_argument("--doc_path", required=True)
    parser.add_argument("--people", default="")
    parser.add_argument("--decisions", default="")
    parser.add_argument("--open_questions", default="")
    parser.add_argument("--timeline", default="")
    args = parser.parse_args()

    try:
        stem = args.doc_path.rsplit("/", 1)[-1].replace(".md", "")
        link = f"[[{stem}]]"
        stamp = now_str()
        if args.timeline:
            append_file(args.owner, args.repo, f"projects/{args.project_id}/timeline.md", f"- `{stamp}` {args.timeline} — {link}", "Timeline")
        if args.decisions:
            append_file(args.owner, args.repo, f"projects/{args.project_id}/decisions.md", f"- `{stamp}` {args.decisions} — {link}", "Decisions")
        if args.open_questions:
            append_file(args.owner, args.repo, f"projects/{args.project_id}/open_questions.md", f"- `{stamp}` {args.open_questions} — {link}", "Open Questions")
        append_file(args.owner, args.repo, f"projects/{args.project_id}/index.md", f"- `{stamp}` {args.title} — {link}", args.project_id)
        for person in [p.strip() for p in args.people.split(",") if p.strip()]:
            pfile = f"people/{sanitize_filename(person)}.md"
            append_file(args.owner, args.repo, pfile, f"- `{stamp}` 关联资料：{args.title} — {link}", person)
            append_file(args.owner, args.repo, f"projects/{args.project_id}/people.md", f"- {person} — {link}", "People")
    except Exception as exc:
        out(json_fail("update_project_people_failed", str(exc)))
        return
    out({"success": True})


if __name__ == "__main__":
    main()
