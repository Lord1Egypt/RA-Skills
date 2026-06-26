#!/usr/bin/env python3
"""Project Memory Ledger.

Backend semantics (simplified):
- The **ledger is always written to local Markdown**.
- `backend` only decides where **project docs/assets** live when scaffolding a project:
  - local: local project directory + Markdown docs
  - drive: Drive folder structure + GDoc/GSheet (requires gws auth)

Config JSON (recommended path): <workspace>/config/project_memory_ledger.json
{
  "language": "zh" | "en",
  "backend": "local" | "drive",
  "default_project": "project-memory-ledger",

  // local backend
  "local_dir": "./ledgers",
  "projects_root_dir": "./projects",

  // drive backend (required when backend=drive)
  "projects_root_folder_id": "<Drive folder id where projects are created>",

  // optional / legacy
  "shared_folder_id": "<Drive folder id for Shared/>"
}

Commands:
  ledger.py init --config <path>
  ledger.py append --config <path> --doc <invariants|decisions|changes> --text <text> [--project <nameOrSlug>]
  ledger.py register-project --config <path> --name <display name> [--slug <slug>] --purpose <text> [--interfaces <a↔b>] [--notes <text>] [--scaffold <auto|off>]
  ledger.py update-prd --config <path> --project <nameOrSlug> [--mode propose|apply]

Project normalization:
- Input is case-insensitive.
- We normalize to slugs (examples):
  - "Hunter System" → hunter-system
  - "Keyword Engine" → keyword-engine
"""

import argparse
import json
import os
import re
import shlex
import subprocess
import sys
import shutil
from pathlib import Path
from datetime import datetime


def run(args: list[str]) -> str:
    """Run a command without using a shell (safer)."""
    p = subprocess.run(args, check=True, capture_output=True, text=True)
    return p.stdout.strip()


def require_bin(bin_name: str) -> None:
    if shutil.which(bin_name) is None:
        raise SystemExit(f"Missing required binary: {bin_name}. Please install it or switch backend=local.")


def run_gws(args: list[str]) -> str:
    require_bin('gws')
    return run(["gws", *args])


def normalize_project(p: str | None) -> str | None:
    if not p:
        return None
    s = p.strip().lower()
    # Known canonical names
    aliases = {
        'hunter system': 'hunter-system',
        'hunter-system': 'hunter-system',
        'hunter': 'hunter-system',
        'keyword engine': 'keyword-engine',
        'keyword-engine': 'keyword-engine',
        'ke': 'keyword-engine',
        'common': 'common',
        # deprecated: treat 'shared' as 'common' and require Interfaces field in the entry
        'shared': 'common',
    }
    if s in aliases:
        return aliases[s]
    # generic slugify
    s = s.replace('_', '-').replace(' ', '-')
    s = re.sub(r'[^a-z0-9\-]+', '-', s)
    s = re.sub(r'-{2,}', '-', s).strip('-')
    return s or None


def inject_project(text: str, project_slug: str | None) -> str:
    if not project_slug:
        return text
    # If user already included a Project field, do not override.
    if re.search(r'^-\s*\*\*Project\*\*\s*:', text, flags=re.IGNORECASE | re.MULTILINE):
        return text
    # Insert at the top of the entry.
    prefix = f"- **Project**: {project_slug}\n"
    return prefix + text


def jx(s: str):
    s = s.strip()
    i, j = s.find('{'), s.rfind('}')
    if i != -1 and j != -1 and j > i:
        s = s[i : j + 1]
    return json.loads(s)


def load_config(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save_config(path: str, cfg: dict) -> None:
    Path(path).write_text(json.dumps(cfg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def ensure_local_files(cfg: dict) -> dict:
    local_dir = cfg.get("local_dir") or "./ledgers"
    Path(local_dir).mkdir(parents=True, exist_ok=True)
    cfg["local_dir"] = local_dir
    return cfg


def local_path(cfg: dict, doc_key: str) -> Path:
    # Single-ledger but split into multiple files.
    name = {
        "invariants": "INVARIANTS.md",
        "decisions": "DECISIONS.md",
        "changes": "CHANGES.md",
        "projects": "PROJECTS.md",
    }[doc_key]
    return Path(cfg["local_dir"]) / name


def append_local(cfg: dict, doc_key: str, text: str) -> None:
    cfg = ensure_local_files(cfg)
    p = local_path(cfg, doc_key)
    if not p.exists():
        p.write_text(f"# {p.stem}\n", encoding="utf-8")
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    with p.open("a", encoding="utf-8") as f:
        f.write(f"\n\n<!-- appended {stamp} -->\n")
        f.write(text)
        if not text.endswith("\n"):
            f.write("\n")


def find_doc_in_folder(folder_id: str, title: str) -> str | None:
    q = f"'{folder_id}' in parents and name = '{title}' and mimeType='application/vnd.google-apps.document' and trashed=false"
    params = json.dumps({"q": q, "pageSize": 5, "fields": "files(id,name)"})
    out = run_gws(['drive','files','list','--params', params])
    files = jx(out).get("files", [])
    return files[0]["id"] if files else None


def create_doc(title: str) -> str:
    out = run_gws(['docs','documents','create','--json', json.dumps({'title': title})])
    return jx(out)["documentId"]


def move_to_folder(file_id: str, folder_id: str) -> None:
    meta = jx(run_gws(['drive','files','get','--params', json.dumps({'fileId': file_id, 'fields': 'parents'})]))
    parents = meta.get("parents", [])
    upd = {"fileId": file_id, "addParents": folder_id}
    if parents:
        upd["removeParents"] = ",".join(parents)
    run_gws(['drive','files','update','--params', json.dumps(upd), '--json', '{}'])


def ensure_drive_folder(parent_id: str, name: str) -> str:
    q = f"'{parent_id}' in parents and name='{name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    params = json.dumps({"q": q, "pageSize": 5, "fields": "files(id,name)"})
    out = run_gws(['drive','files','list','--params', params])
    files = jx(out).get('files', [])
    if files:
        return files[0]['id']
    body = json.dumps({"name": name, "mimeType": "application/vnd.google-apps.folder", "parents": [parent_id]})
    out = run_gws(['drive','files','create','--json', body])
    return jx(out)['id']


def create_gdoc_in_folder(folder_id: str, title: str, initial_text: str = "") -> str:
    out = run_gws(['docs','documents','create','--json', json.dumps({'title': title})])
    doc_id = jx(out)['documentId']
    move_to_folder(doc_id, folder_id)
    if initial_text:
        append_drive(doc_id, initial_text)
    return doc_id


def create_gsheet_in_folder(folder_id: str, title: str) -> str:
    out = run_gws(['sheets','spreadsheets','create','--json', json.dumps({'properties': {'title': title}})])
    sid = jx(out)['spreadsheetId']
    move_to_folder(sid, folder_id)
    return sid


def scaffold_drive_project(cfg: dict, slug: str, display_name: str, purpose: str) -> dict:
    # Create Drive folder structure under projects_root_folder_id (default: My Drive root)
    root_parent = cfg.get('projects_root_folder_id')
    if not root_parent:
        raise SystemExit("projects_root_folder_id missing (set it to a Drive folder id where projects should be created)")
    project_folder_id = ensure_drive_folder(root_parent, display_name)

    subfolders = {}
    for name in ['Docs','Specs','Data','Backlog','Evidence','Releases','Archive']:
        subfolders[name] = ensure_drive_folder(project_folder_id, name)

    # Create starter docs
    charter_id = create_gdoc_in_folder(subfolders['Docs'], '项目说明（Charter）', f"\n# 项目说明（Project Charter）\n- 项目名: {display_name}\n- Slug: {slug}\n- 目的: {purpose}\n")
    prd_id = create_gdoc_in_folder(subfolders['Docs'], 'PRD（需求文档）')
    # SDD is optional; create only if the user asks later
    backlog_sid = create_gsheet_in_folder(subfolders['Backlog'], 'Backlog（待办）')

    return {
        'backend': 'drive',
        'project_folder_id': project_folder_id,
        'charter_doc_id': charter_id,
        'prd_doc_id': prd_id,
        'backlog_sheet_id': backlog_sid,
    }


def scaffold_local_project(cfg: dict, slug: str, display_name: str, purpose: str) -> dict:
    root = Path(cfg.get('projects_root_dir') or './projects')
    project_dir = root / display_name
    sub = {}
    for name in ['Docs','Specs','Data','Backlog','Evidence','Releases','Archive']:
        p = project_dir / name
        p.mkdir(parents=True, exist_ok=True)
        sub[name] = p

    # starter markdown docs
    charter = sub['Docs'] / '项目说明（Charter）.md'
    prd = sub['Docs'] / 'PRD（需求文档）.md'
    backlog = sub['Backlog'] / 'Backlog（待办）.md'

    if not charter.exists():
        charter.write_text(f"# 项目说明（Project Charter）\n\n- 项目名: {display_name}\n- Slug: {slug}\n- 目的: {purpose}\n", encoding='utf-8')
    prd.touch(exist_ok=True)
    if not backlog.exists():
        backlog.write_text("# Backlog（待办）\n\n- [ ] P0: ...\n", encoding='utf-8')

    return {
        'backend': 'local',
        'project_dir': str(project_dir),
        'charter_path': str(charter),
        'prd_path': str(prd),
        'backlog_path': str(backlog),
    }


def append_drive(document_id: str, text: str) -> None:
    doc = jx(run_gws(['docs','documents','get','--params', json.dumps({'documentId': document_id})]))
    end = 1
    try:
        end = int(doc["body"]["content"][-1]["endIndex"])
    except Exception:
        end = 1
    insert_at = max(1, end - 1)
    req = [{"insertText": {"location": {"index": insert_at}, "text": text}}]
    run_gws(['docs','documents','batchUpdate','--params', json.dumps({'documentId': document_id}), '--json', json.dumps({'requests': req})])


def init_drive_docs(cfg: dict) -> dict:
    folder_id = cfg.get("shared_folder_id")
    if not folder_id:
        raise SystemExit("shared_folder_id missing for drive backend")

    mapping = {
        "invariants_doc_id": cfg["doc_titles"]["invariants"],
        "decision_log_doc_id": cfg["doc_titles"]["decisions"],
        "change_log_doc_id": cfg["doc_titles"]["changes"],
    }

    for key, title in mapping.items():
        doc_id = cfg["docs"].get(key) or ""
        if doc_id:
            continue
        existing = find_doc_in_folder(folder_id, title)
        if existing:
            cfg["docs"][key] = existing
            continue
        new_id = create_doc(title)
        move_to_folder(new_id, folder_id)
        cfg["docs"][key] = new_id

    return cfg


def init(cfg_path: str) -> dict:
    cfg = load_config(cfg_path)

    # language default + hint
    if not cfg.get('language'):
        cfg['language'] = 'en'
        print("[project-memory-ledger] config.language missing → defaulting to 'en' (set language=zh for Chinese)", file=sys.stderr)

    backend = (cfg.get("backend") or "local").lower()
    if backend not in ("local", "drive"):
        backend = "local"
    cfg["backend"] = backend

    # Ledger is always local
    cfg = ensure_local_files(cfg)
    cfg.setdefault('projects_root_dir', './projects')

    save_config(cfg_path, cfg)
    return cfg


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    ap_init = sub.add_parser("init")
    ap_init.add_argument("--config", required=True)

    ap_app = sub.add_parser("append")
    ap_app.add_argument("--config", required=True)
    ap_app.add_argument("--doc", choices=["invariants", "decisions", "changes"], required=True)
    ap_app.add_argument("--text", required=True)
    ap_app.add_argument("--project", required=False, help="Project name or slug (case-insensitive). Will be normalized.")

    ap_reg = sub.add_parser("register-project")
    ap_reg.add_argument("--config", required=True)
    ap_reg.add_argument("--name", required=True, help="Display name")
    ap_reg.add_argument("--slug", required=False, help="Optional slug; if omitted, derived from name")
    ap_reg.add_argument("--purpose", required=True, help="Why this project exists / success criteria")
    ap_reg.add_argument("--interfaces", required=False, help="Optional: A ↔ B")
    ap_reg.add_argument("--notes", required=False, default="")
    ap_reg.add_argument("--scaffold", required=False, default="auto", choices=["auto","off"], help="auto: create project scaffold based on backend; off: only register entry.")

    args = ap.parse_args()

    if args.cmd == "init":
        cfg = init(args.config)
        # Print doc ids (drive) and local dir
        out = {
            "backend": cfg.get("backend"),
            "local_dir": cfg.get("local_dir"),
            "docs": cfg.get("docs"),
        }
        print(json.dumps(out, ensure_ascii=False))
        return

    if args.cmd == "append":
        cfg = init(args.config)
        backend = cfg.get("backend")

        project_slug = normalize_project(getattr(args, 'project', None))
        if not project_slug:
            project_slug = normalize_project(cfg.get('default_project')) or 'project-memory-ledger'
        text = inject_project(args.text, project_slug)

        if backend in ("local", "both"):
            append_local(cfg, args.doc, text)

        if backend in ("drive", "both"):
            doc_map = {
                "invariants": cfg["docs"]["invariants_doc_id"],
                "decisions": cfg["docs"]["decision_log_doc_id"],
                "changes": cfg["docs"]["change_log_doc_id"],
            }
            doc_id = doc_map[args.doc]
            if not doc_id:
                raise SystemExit(f"Drive doc id missing for {args.doc}")
            append_drive(doc_id, text)
            print(doc_id)
        else:
            print(str(local_path(cfg, args.doc)))
        return

    if args.cmd == "update-prd":
        cfg = init(args.config)
        backend = cfg.get("backend")
        project_slug = normalize_project(args.project) or args.project

        if args.mode != 'propose':
            raise SystemExit('update-prd --mode apply is not implemented yet (propose-only)')

        # Minimal v1: generate a proposal skeleton and store it in local PRD_PATCHES.md (and optionally print).
        stamp = datetime.now().strftime('%Y-%m-%d %H:%M')
        proposal = (
            f"\n\n## PRD Patch Proposal ({stamp})\n"
            f"- **Project**: {project_slug}\n"
            f"- **Summary**: <what changed and why>\n"
            f"- **Evidence links**: <Decision/Change entries or logs>\n"
            f"- **PRD sections impacted**: <scope/non-goals/milestones/etc>\n"
            f"- **Proposed edits**:\n  - ...\n"
        )

        # Proposals are part of the ledger => always local
        append_local(cfg, 'prd_patches', proposal)
        print(proposal.strip())
        return

    if args.cmd == "register-project":
        cfg = init(args.config)
        backend = cfg.get("backend")

        slug = normalize_project(args.slug or args.name) or (args.slug or args.name)
        interfaces = (args.interfaces or '').strip()

        entry_lines = [
            f"## Project: {slug}",
            f"- **Name**: {args.name}",
            f"- **Purpose**: {args.purpose}",
        ]
        if interfaces:
            entry_lines.append(f"- **Interfaces**: {interfaces}")
        if args.notes:
            entry_lines.append(f"- **Notes**: {args.notes}")
        entry_text = "\n".join(entry_lines) + "\n"

        # Local registry (always)
        append_local(cfg, 'projects', entry_text)

        # Also record as a decision (for auditability)
        decision_text = (
            f"- **Project**: {slug}\n"
            + (f"- **Interfaces**: {interfaces}\n" if interfaces else "")
            + "- **Decision**: 立项（创建项目）\n"
            + f"- **Why**: {args.purpose}\n"
            + "- **Alternatives**: 不立项（作为现有项目的子任务/待办）\n"
            + "- **Scope**: 项目注册（Project Registry）\n"
            + f"- **Date**: {datetime.now().strftime('%Y-%m-%d')}\n"
            + "- **Status**: CONFIRMED\n"
        )

        scaffold_info = {}
        if args.scaffold == 'auto':
            if backend == 'drive':
                scaffold_info = scaffold_drive_project(cfg, slug, args.name, args.purpose)
            else:
                scaffold_info = scaffold_local_project(cfg, slug, args.name, args.purpose)

        # Append scaffold pointers into local registry entry
        if scaffold_info:
            if scaffold_info.get('backend') == 'drive':
                entry_text += (
                    f"- **Drive Folder**: https://drive.google.com/drive/folders/{scaffold_info['project_folder_id']}\n"
                    f"- **Charter**: https://docs.google.com/document/d/{scaffold_info['charter_doc_id']}/edit\n"
                    f"- **PRD**: https://docs.google.com/document/d/{scaffold_info['prd_doc_id']}/edit\n"
                    f"- **Backlog Sheet**: https://docs.google.com/spreadsheets/d/{scaffold_info['backlog_sheet_id']}/edit\n"
                )
            else:
                entry_text += (
                    f"- **Local Project Dir**: {scaffold_info['project_dir']}\n"
                    f"- **Charter**: {scaffold_info['charter_path']}\n"
                    f"- **PRD**: {scaffold_info['prd_path']}\n"
                    f"- **Backlog**: {scaffold_info['backlog_path']}\n"
                )
            append_local(cfg, 'projects', entry_text)

        print(str(local_path(cfg, 'projects')))
        return


if __name__ == "__main__":
    main()
