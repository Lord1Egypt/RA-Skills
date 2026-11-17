#!/usr/bin/env python3
"""Robustness / boundary test harness for governance.py.

Runs the skill's CLI subcommands across many user scenarios (normal, edge,
destructive) and reports PASS/FAIL per case. Stdlib-only; run with:

    python tests/test_governance.py

Exit code is 0 when every case passes, 1 otherwise.
"""

from __future__ import annotations

import json
import shutil
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "governance.py"
sys.path.insert(0, str(SCRIPT.parent))

import governance  # noqa: E402

RESULTS: list[tuple[str, bool, str]] = []


def record(name: str, ok: bool, detail: str = "") -> None:
    RESULTS.append((name, ok, detail))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


def fresh(work: Path, name: str) -> Path:
    d = work / name
    if d.exists():
        shutil.rmtree(d)
    d.mkdir(parents=True)
    return d


def run(cmd: str, ns, **overrides):
    """Call a governance cmd_* function, returning (exit_code, exc)."""
    for k, v in overrides.items():
        setattr(ns, k, v)
    try:
        return getattr(governance, cmd)(ns), None
    except Exception as exc:  # noqa: BLE001
        return -1, exc


def _ns(project_dir, project_name, force):
    return type("NS", (), {"project_dir": str(project_dir), "project_name": project_name, "force": force, "max_depth": 4})()


def write_json(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False), encoding="utf-8")


def valid_blacklist() -> dict:
    return {
        "blacklist": [
            {
                "id": "b1",
                "reason": "test",
                "permanent_ban": True,
                "alternative": "use x",
                "test_ref": "t1",
                "judge": "human",
                "scope": "character",
                "status": "active",
            }
        ]
    }


def valid_whitelist() -> dict:
    return {
        "whitelist": [
            {
                "id": "w1",
                "score": 0.9,
                "config": {"base_model": "X"},
                "test_ref": "t1",
                "judge": "human",
                "last_verified": "2026-08-17",
                "scope": "character",
                "status": "active",
            }
        ]
    }


def test_init(work: Path) -> None:
    d = fresh(work, "init_fresh")
    code, exc = run("cmd_init", _ns(d, "Test Project", False))
    ok = code == 0 and all((d / f).exists() for f in governance.TEMPLATE_FILES)
    record(f"init: fresh empty dir creates {len(governance.TEMPLATE_FILES)} files", ok, f"exit={code}")

    d = fresh(work, "init_existing")
    (d / "AGENTS.md").write_text("ORIGINAL", encoding="utf-8")
    code, exc = run("cmd_init", _ns(d, "Test", False))
    ok = code == 0 and (d / "AGENTS.md").read_text(encoding="utf-8") == "ORIGINAL"
    record("init: existing file not overwritten without --force", ok)

    code, exc = run("cmd_init", _ns(d, "Test", True))
    ok = code == 0 and (d / "AGENTS.md").read_text(encoding="utf-8") != "ORIGINAL"
    record("init: --force overwrites existing files", ok)

    d = fresh(work, "init_dir_is_file")
    f = d / "blocker.txt"
    f.write_text("x", encoding="utf-8")
    code, exc = run("cmd_init", _ns(f, "Test", False))
    record("init: project-dir is a file fails gracefully", code != 0 and exc is None, f"exit={code} exc={type(exc).__name__ if exc else None}")

    d = work / "init_nested" / "a" / "b" / "c"
    if d.exists():
        shutil.rmtree(work / "init_nested")
    code, exc = run("cmd_init", _ns(d, "Test", False))
    ok = code == 0 and (d / "index.md").exists()
    record("init: nested non-existent dir auto-created", ok)

    d = fresh(work, "init_special_name")
    code, exc = run("cmd_init", _ns(d, '测试 "项目" & <demo>', False))
    record("init: project-name with special chars", code == 0, f"exit={code}")

    d = fresh(work, "init_dst_is_dir")
    (d / "AGENTS.md").mkdir()
    code, exc = run("cmd_init", _ns(d, "Test", False))
    record("init: dst is a directory fails gracefully", code != 0 and exc is None, f"exit={code} exc={type(exc).__name__ if exc else None}")

    d = fresh(work, "init_empty_name")
    code, exc = run("cmd_init", _ns(d, "", False))
    record("init: empty project-name falls back to default", code == 0)


def test_validate(work: Path) -> None:
    d = fresh(work, "val_valid")
    write_json(d / "blacklist.json", valid_blacklist())
    write_json(d / "whitelist.json", valid_whitelist())
    code, exc = run("cmd_validate", _ns(d, None, None))
    record("validate: valid registries pass", code == 0 and exc is None, f"exit={code}")

    d = fresh(work, "val_missing")
    write_json(d / "whitelist.json", valid_whitelist())
    code, exc = run("cmd_validate", _ns(d, None, None))
    record("validate: missing file fails gracefully", code != 0 and exc is None, f"exit={code}")

    d = fresh(work, "val_badjson")
    (d / "blacklist.json").write_text("{not json", encoding="utf-8")
    write_json(d / "whitelist.json", valid_whitelist())
    code, exc = run("cmd_validate", _ns(d, None, None))
    record("validate: invalid JSON syntax fails gracefully", code != 0 and exc is None, f"exit={code}")

    d = fresh(work, "val_notlist")
    write_json(d / "blacklist.json", {"blacklist": {"id": "x"}})
    write_json(d / "whitelist.json", valid_whitelist())
    code, exc = run("cmd_validate", _ns(d, None, None))
    record("validate: top-level not a list fails gracefully", code != 0 and exc is None, f"exit={code}")

    d = fresh(work, "val_entry_notobj")
    write_json(d / "blacklist.json", {"blacklist": ["string-entry"]})
    write_json(d / "whitelist.json", valid_whitelist())
    code, exc = run("cmd_validate", _ns(d, None, None))
    record("validate: non-object entry fails gracefully", code != 0 and exc is None, f"exit={code}")

    d = fresh(work, "val_missing_field")
    b = valid_blacklist()
    del b["blacklist"][0]["status"]
    write_json(d / "blacklist.json", b)
    write_json(d / "whitelist.json", valid_whitelist())
    code, exc = run("cmd_validate", _ns(d, None, None))
    record("validate: missing required field fails gracefully", code != 0 and exc is None, f"exit={code}")

    d = fresh(work, "val_dup_id")
    b = valid_blacklist()
    b["blacklist"].append(dict(b["blacklist"][0], id="b1"))
    write_json(d / "blacklist.json", b)
    write_json(d / "whitelist.json", valid_whitelist())
    code, exc = run("cmd_validate", _ns(d, None, None))
    record("validate: duplicate id fails gracefully", code != 0 and exc is None, f"exit={code}")

    d = fresh(work, "val_bad_status")
    b = valid_blacklist()
    b["blacklist"][0]["status"] = "bogus"
    write_json(d / "blacklist.json", b)
    write_json(d / "whitelist.json", valid_whitelist())
    code, exc = run("cmd_validate", _ns(d, None, None))
    record("validate: invalid status fails gracefully", code != 0 and exc is None, f"exit={code}")

    d = fresh(work, "val_bad_judge")
    b = valid_blacklist()
    b["blacklist"][0]["judge"] = "robot"
    write_json(d / "blacklist.json", b)
    write_json(d / "whitelist.json", valid_whitelist())
    code, exc = run("cmd_validate", _ns(d, None, None))
    record("validate: invalid judge fails gracefully", code != 0 and exc is None, f"exit={code}")

    d = fresh(work, "val_bad_score")
    w = valid_whitelist()
    w["whitelist"][0]["score"] = 1.5
    write_json(d / "blacklist.json", valid_blacklist())
    write_json(d / "whitelist.json", w)
    code, exc = run("cmd_validate", _ns(d, None, None))
    record("validate: score out of range fails gracefully", code != 0 and exc is None, f"exit={code}")

    d = fresh(work, "val_json_list")
    (d / "blacklist.json").write_text("[1,2,3]", encoding="utf-8")
    write_json(d / "whitelist.json", valid_whitelist())
    code, exc = run("cmd_validate", _ns(d, None, None))
    record("validate: top-level JSON list fails gracefully (no crash)", code != 0 and exc is None, f"exit={code} exc={type(exc).__name__ if exc else None}")

    d = fresh(work, "val_json_null")
    (d / "blacklist.json").write_text("null", encoding="utf-8")
    write_json(d / "whitelist.json", valid_whitelist())
    code, exc = run("cmd_validate", _ns(d, None, None))
    record("validate: top-level JSON null fails gracefully (no crash)", code != 0 and exc is None, f"exit={code} exc={type(exc).__name__ if exc else None}")

    d = fresh(work, "val_json_str")
    (d / "blacklist.json").write_text('"just a string"', encoding="utf-8")
    write_json(d / "whitelist.json", valid_whitelist())
    code, exc = run("cmd_validate", _ns(d, None, None))
    record("validate: top-level JSON string fails gracefully (no crash)", code != 0 and exc is None, f"exit={code} exc={type(exc).__name__ if exc else None}")

    d = fresh(work, "val_empty")
    (d / "blacklist.json").write_text("", encoding="utf-8")
    write_json(d / "whitelist.json", valid_whitelist())
    code, exc = run("cmd_validate", _ns(d, None, None))
    record("validate: empty file fails gracefully", code != 0 and exc is None, f"exit={code}")

    d = fresh(work, "val_score_bool")
    w = valid_whitelist()
    w["whitelist"][0]["score"] = True
    write_json(d / "blacklist.json", valid_blacklist())
    write_json(d / "whitelist.json", w)
    code, exc = run("cmd_validate", _ns(d, None, None))
    record("validate: boolean score is rejected (strict type)", code != 0 and exc is None, f"exit={code}")

    d = fresh(work, "val_id_nonstr")
    b = valid_blacklist()
    b["blacklist"][0]["id"] = 123
    write_json(d / "blacklist.json", b)
    write_json(d / "whitelist.json", valid_whitelist())
    code, exc = run("cmd_validate", _ns(d, None, None))
    record("validate: non-string id is rejected (strict type)", code != 0 and exc is None, f"exit={code}")


def make_index_md(d: Path, root_first: bool = True) -> None:
    d.mkdir(parents=True, exist_ok=True)
    if root_first:
        text = "# Index\n\n## Root layout\n```\n(placeholder)\n```\n\n## Change log\n- 2026-08-17 init\n"
    else:
        text = "# Index\n\n## Change log\n- 2026-08-17 init\n\n## Root layout\n```\n(placeholder)\n```\n"
    (d / "index.md").write_text(text, encoding="utf-8")


def test_index(work: Path) -> None:
    d = fresh(work, "idx_normal")
    make_index_md(d)
    (d / "src").mkdir()
    (d / "src" / "main.py").write_text("x", encoding="utf-8")
    code, exc = run("cmd_index", _ns(d, None, None))
    ok = code == 0 and "main.py" in (d / "index.md").read_text(encoding="utf-8")
    record("index: normal dir updated", ok, f"exit={code}")

    d = fresh(work, "idx_missing")
    code, exc = run("cmd_index", _ns(d, None, None))
    record("index: missing index.md fails gracefully", code != 0 and exc is None, f"exit={code}")

    d = fresh(work, "idx_no_root")
    (d / "index.md").write_text("# Index\n\n## Change log\n- x\n", encoding="utf-8")
    code, exc = run("cmd_index", _ns(d, None, None))
    record("index: missing Root layout section fails gracefully", code != 0 and exc is None, f"exit={code}")

    d = fresh(work, "idx_no_changelog")
    (d / "index.md").write_text("# Index\n\n## Root layout\n```\n```\n", encoding="utf-8")
    code, exc = run("cmd_index", _ns(d, None, None))
    record("index: missing Change log section fails gracefully", code != 0 and exc is None, f"exit={code}")

    d = fresh(work, "idx_reversed")
    make_index_md(d, root_first=False)
    code, exc = run("cmd_index", _ns(d, None, None))
    record("index: reversed sections fail gracefully", code != 0 and exc is None, f"exit={code}")

    d = fresh(work, "idx_empty")
    make_index_md(d)
    code, exc = run("cmd_index", _ns(d, None, None))
    record("index: empty dir updated", code == 0 and exc is None, f"exit={code}")

    d = fresh(work, "idx_unicode")
    make_index_md(d)
    (d / "测试 目录").mkdir()
    (d / "测试 目录" / "文件 一.md").write_text("x", encoding="utf-8")
    code, exc = run("cmd_index", _ns(d, None, None))
    ok = code == 0 and "文件 一.md" in (d / "index.md").read_text(encoding="utf-8")
    record("index: unicode/space filenames handled", ok, f"exit={code}")

    d = fresh(work, "idx_skip")
    make_index_md(d)
    for skip in (".git", "node_modules", "venv", "__pycache__"):
        (d / skip).mkdir()
        (d / skip / "junk.txt").write_text("x", encoding="utf-8")
    code, exc = run("cmd_index", _ns(d, None, None))
    text = (d / "index.md").read_text(encoding="utf-8")
    ok = code == 0 and ".git" not in text and "node_modules" not in text and "venv" not in text
    record("index: SKIP_DIRS excluded", ok, f"exit={code}")

    d = fresh(work, "idx_hidden")
    make_index_md(d)
    (d / ".hidden.txt").write_text("x", encoding="utf-8")
    (d / "visible.txt").write_text("x", encoding="utf-8")
    code, exc = run("cmd_index", _ns(d, None, None))
    text = (d / "index.md").read_text(encoding="utf-8")
    ok = code == 0 and ".hidden.txt" not in text and "visible.txt" in text
    record("index: dotfiles excluded", ok, f"exit={code}")

    d = fresh(work, "idx_depth0")
    make_index_md(d)
    (d / "a").mkdir()
    (d / "a" / "b").mkdir()
    code, exc = run("cmd_index", _ns(d, None, None), max_depth=0)
    text = (d / "index.md").read_text(encoding="utf-8")
    ok = code == 0 and "b/" not in text
    record("index: max-depth 0 shows root only", ok, f"exit={code}")

    d = fresh(work, "idx_depthneg")
    make_index_md(d)
    code, exc = run("cmd_index", _ns(d, None, None), max_depth=-5)
    record("index: negative max-depth no crash", code == 0 and exc is None, f"exit={code} exc={type(exc).__name__ if exc else None}")

    d = fresh(work, "idx_deep")
    make_index_md(d)
    cur = d
    for _ in range(60):
        cur = cur / "d"
        cur.mkdir(exist_ok=True)
    code, exc = run("cmd_index", _ns(d, None, None), max_depth=1000)
    record("index: 60-level nesting no crash", code == 0 and exc is None, f"exit={code} exc={type(exc).__name__ if exc else None}")

    d = fresh(work, "idx_is_dir")
    (d / "index.md").mkdir()
    code, exc = run("cmd_index", _ns(d, None, None))
    record("index: index.md is a directory fails gracefully", code != 0 and exc is None, f"exit={code} exc={type(exc).__name__ if exc else None}")


def test_destructive(work: Path) -> None:
    d = work / "破 坏 性 测 试"
    if d.exists():
        shutil.rmtree(d)
    code, exc = run("cmd_init", _ns(d, "T", False))
    record("destructive: unicode+space path init works", code == 0 and exc is None, f"exit={code}")

    long_dir = work / ("L" * 120)
    if long_dir.exists():
        shutil.rmtree(long_dir)
    code, exc = run("cmd_init", _ns(long_dir, "T", False))
    record("destructive: long path init works", code == 0 and exc is None, f"exit={code} exc={type(exc).__name__ if exc else None}")

    d = fresh(work, "destructive_special")
    make_index_md(d)
    for name in ("a&b.txt", "[x] y.txt", "comma,name.txt", "semi;colon.txt"):
        (d / name).write_text("x", encoding="utf-8")
    code, exc = run("cmd_index", _ns(d, None, None))
    text = (d / "index.md").read_text(encoding="utf-8")
    ok = code == 0 and all(n in text for n in ("a&b.txt", "[x] y.txt", "comma,name.txt", "semi;colon.txt"))
    record("destructive: special-char filenames in index", ok, f"exit={code}")

    d = fresh(work, "destructive_crlf")
    (d / "index.md").write_bytes(b"# Index\r\n\r\n## Root layout\r\n```\r\nx\r\n```\r\n\r\n## Change log\r\n- y\r\n")
    code, exc = run("cmd_index", _ns(d, None, None))
    record("destructive: CRLF index.md handled", code == 0 and exc is None, f"exit={code}")

    d = fresh(work, "destructive_bom")
    (d / "index.md").write_bytes(b"\xef\xbb\xbf# Index\n\n## Root layout\n```\nx\n```\n\n## Change log\n- y\n")
    code, exc = run("cmd_index", _ns(d, None, None))
    record("destructive: BOM index.md handled", code == 0 and exc is None, f"exit={code}")

    d = fresh(work, "destructive_placeholder")
    code, exc = run("cmd_init", _ns(d, "My Cool Project", False))
    arch = (d / "ARCHITECTURE.md").read_text(encoding="utf-8")
    ok = code == 0 and "My Cool Project" in arch
    record("destructive: project-name placeholder substituted", ok, f"exit={code}")


def test_adversarial(work: Path) -> None:
    """Adversarial / chaotic-user scenarios: wrong context, malicious file
    content, encoding chaos, state abuse. The 'ordering chow mein at a bar'
    cases."""
    # A1 blacklist.json is a directory -> graceful error, no crash
    d = fresh(work, "adv_dir_registry")
    (d / "blacklist.json").mkdir()
    write_json(d / "whitelist.json", valid_whitelist())
    code, exc = run("cmd_validate", _ns(d, None, None))
    record("adv: registry path is a directory fails gracefully", code != 0 and exc is None, f"exit={code} exc={type(exc).__name__ if exc else None}")

    # A2 GBK-encoded registry (non-ASCII) -> graceful error, no UnicodeDecodeError
    d = fresh(work, "adv_gbk")
    (d / "blacklist.json").write_bytes('{"blacklist": [{"id": "测试"}]}'.encode("gbk"))
    write_json(d / "whitelist.json", valid_whitelist())
    code, exc = run("cmd_validate", _ns(d, None, None))
    record("adv: GBK-encoded registry fails gracefully", code != 0 and exc is None, f"exit={code} exc={type(exc).__name__ if exc else None}")

    # A3 UTF-16 registry -> graceful error
    d = fresh(work, "adv_utf16")
    (d / "blacklist.json").write_bytes('{"blacklist": []}'.encode("utf-16"))
    write_json(d / "whitelist.json", valid_whitelist())
    code, exc = run("cmd_validate", _ns(d, None, None))
    record("adv: UTF-16 registry fails gracefully", code != 0 and exc is None, f"exit={code} exc={type(exc).__name__ if exc else None}")

    # A4 permanent_ban as string -> rejected
    d = fresh(work, "adv_permban_str")
    b = valid_blacklist()
    b["blacklist"][0]["permanent_ban"] = "true"
    write_json(d / "blacklist.json", b)
    write_json(d / "whitelist.json", valid_whitelist())
    code, exc = run("cmd_validate", _ns(d, None, None))
    record("adv: string permanent_ban rejected", code != 0 and exc is None, f"exit={code}")

    # A5 score as string -> rejected
    d = fresh(work, "adv_score_str")
    w = valid_whitelist()
    w["whitelist"][0]["score"] = "0.9"
    write_json(d / "blacklist.json", valid_blacklist())
    write_json(d / "whitelist.json", w)
    code, exc = run("cmd_validate", _ns(d, None, None))
    record("adv: string score rejected", code != 0 and exc is None, f"exit={code}")

    # A6 empty registry list -> passes (valid)
    d = fresh(work, "adv_empty_list")
    write_json(d / "blacklist.json", {"blacklist": []})
    write_json(d / "whitelist.json", {"whitelist": []})
    code, exc = run("cmd_validate", _ns(d, None, None))
    record("adv: empty registry list passes", code == 0 and exc is None, f"exit={code}")

    # A7 extra unknown fields -> passes (forward compatibility)
    d = fresh(work, "adv_extra_fields")
    b = valid_blacklist()
    b["blacklist"][0]["future_field"] = {"nested": [1, 2, 3]}
    write_json(d / "blacklist.json", b)
    write_json(d / "whitelist.json", valid_whitelist())
    code, exc = run("cmd_validate", _ns(d, None, None))
    record("adv: extra unknown fields pass (forward compat)", code == 0 and exc is None, f"exit={code}")

    # A8 duplicate keys in one JSON object -> no crash (last wins)
    d = fresh(work, "adv_dup_keys")
    (d / "blacklist.json").write_text('{"blacklist": [], "blacklist": []}', encoding="utf-8")
    write_json(d / "whitelist.json", valid_whitelist())
    code, exc = run("cmd_validate", _ns(d, None, None))
    record("adv: duplicate JSON keys no crash", code == 0 and exc is None, f"exit={code} exc={type(exc).__name__ if exc else None}")

    # A9 index run twice -> idempotent, no duplicated tree
    d = fresh(work, "adv_index_twice")
    make_index_md(d)
    (d / "src").mkdir()
    run("cmd_index", _ns(d, None, None))
    run("cmd_index", _ns(d, None, None))
    text = (d / "index.md").read_text(encoding="utf-8")
    ok = text.count("src/") == 1
    record("adv: index idempotent across runs", ok)

    # A10 multiple '## Root layout' sections -> no crash, first replaced
    d = fresh(work, "adv_multi_root")
    (d / "index.md").write_text(
        "# I\n\n## Root layout\n```\none\n```\n\n## Root layout\n```\ntwo\n```\n\n## Change log\n- x\n",
        encoding="utf-8",
    )
    code, exc = run("cmd_index", _ns(d, None, None))
    record("adv: multiple Root layout sections no crash", code == 0 and exc is None, f"exit={code} exc={type(exc).__name__ if exc else None}")

    # A11 '## Root layout' inside an earlier code block -> no crash
    d = fresh(work, "adv_false_match")
    (d / "index.md").write_text(
        "# I\n\n```\n## Root layout (this is inside a code fence)\n```\n\n## Root layout\n```\nreal\n```\n\n## Change log\n- x\n",
        encoding="utf-8",
    )
    code, exc = run("cmd_index", _ns(d, None, None))
    record("adv: Root layout inside code fence no crash", code == 0 and exc is None, f"exit={code} exc={type(exc).__name__ if exc else None}")

    # A12 index on the skill's own directory -> works
    d = fresh(work, "adv_self_scan")
    make_index_md(d)
    (d / "templates").mkdir()
    (d / "templates" / "AGENTS.md").write_text("x", encoding="utf-8")
    (d / "scripts").mkdir()
    (d / "scripts" / "governance.py").write_text("x", encoding="utf-8")
    code, exc = run("cmd_index", _ns(d, None, None))
    text = (d / "index.md").read_text(encoding="utf-8")
    ok = code == 0 and "templates/" in text and "scripts/" in text
    record("adv: index on nested project dir works", ok, f"exit={code}")

    # A13 GBK-encoded index.md -> graceful error
    d = fresh(work, "adv_index_gbk")
    (d / "index.md").write_bytes("# 索引\n\n## Root layout\n```\n```\n\n## Change log\n- x\n".encode("gbk"))
    code, exc = run("cmd_index", _ns(d, None, None))
    record("adv: GBK index.md fails gracefully", code != 0 and exc is None, f"exit={code} exc={type(exc).__name__ if exc else None}")

    # A14 huge max-depth -> no crash
    d = fresh(work, "adv_huge_depth")
    make_index_md(d)
    code, exc = run("cmd_index", _ns(d, None, None), max_depth=999999)
    record("adv: huge max-depth no crash", code == 0 and exc is None, f"exit={code} exc={type(exc).__name__ if exc else None}")

    # A15 project-dir with trailing backslash / mixed separators
    d = work / "adv_sep"
    if d.exists():
        shutil.rmtree(d)
    code, exc = run("cmd_init", _ns(str(d) + "\\", "T", False))
    record("adv: trailing-backslash project-dir works", code == 0 and exc is None, f"exit={code}")

    # A16 project-dir '.' via subprocess (scaffold into cwd) -> works
    import subprocess

    cwd = fresh(work, "adv_dot")
    r = subprocess.run(
        [sys.executable, str(SCRIPT), "init", "--project-dir", ".", "--project-name", "Dot Test"],
        cwd=str(cwd),
        capture_output=True,
        text=True,
    )
    record("adv: project-dir '.' scaffolds into cwd", r.returncode == 0 and (cwd / "index.md").exists(), f"exit={r.returncode}")

    # A17 registry with BOM -> graceful error (BOM is not valid JSON)
    d = fresh(work, "adv_bom_json")
    (d / "blacklist.json").write_bytes(b"\xef\xbb\xbf{\"blacklist\": []}")
    write_json(d / "whitelist.json", valid_whitelist())
    code, exc = run("cmd_validate", _ns(d, None, None))
    record("adv: BOM registry fails gracefully", code != 0 and exc is None, f"exit={code} exc={type(exc).__name__ if exc else None}")


def test_index_enhanced(work: Path) -> None:
    """New index features: clickable links, notes from index_notes.json,
    note truncation, custom section names, graceful degradation."""
    # E1 entries become clickable links
    d = fresh(work, "enh_links")
    make_index_md(d)
    (d / "src").mkdir()
    (d / "src" / "main.py").write_text("x", encoding="utf-8")
    code, exc = run("cmd_index", _ns(d, None, None))
    text = (d / "index.md").read_text(encoding="utf-8")
    ok = code == 0 and "[main.py](src/main.py)" in text
    record("enh: index entries are clickable links", ok, f"exit={code}")

    # E2 notes from index_notes.json appear
    d = fresh(work, "enh_notes")
    make_index_md(d)
    (d / "src").mkdir()
    (d / "src" / "main.py").write_text("x", encoding="utf-8")
    write_json(d / "index_notes.json", {"src/main.py": "entry point"})
    code, exc = run("cmd_index", _ns(d, None, None))
    text = (d / "index.md").read_text(encoding="utf-8")
    ok = code == 0 and "entry point" in text
    record("enh: notes from index_notes.json appear", ok, f"exit={code}")

    # E3 note truncation
    d = fresh(work, "enh_truncate")
    make_index_md(d)
    (d / "src").mkdir()
    (d / "src" / "main.py").write_text("x", encoding="utf-8")
    write_json(d / "index_notes.json", {"src/main.py": "x" * 200})
    code, exc = run("cmd_index", _ns(d, None, None), max_note_length=20)
    text = (d / "index.md").read_text(encoding="utf-8")
    ok = code == 0 and ("x" * 20 + "…") in text and ("x" * 21) not in text
    record("enh: notes truncated to max-note-length", ok, f"exit={code}")

    # E4 custom (Chinese) section names
    d = fresh(work, "enh_custom_sections")
    (d / "index.md").write_text(
        "# 索引\n\n## 根目录\n```\n(占位)\n```\n\n## 变更记录\n- init\n",
        encoding="utf-8",
    )
    (d / "src").mkdir()
    (d / "src" / "main.py").write_text("x", encoding="utf-8")
    code, exc = run("cmd_index", _ns(d, None, None),
                    root_section="## 根目录", changelog_section="## 变更记录")
    text = (d / "index.md").read_text(encoding="utf-8")
    ok = code == 0 and "[main.py](src/main.py)" in text and "## 变更记录" in text
    record("enh: custom (Chinese) section names work", ok, f"exit={code}")

    # E5 invalid index_notes.json degrades gracefully
    d = fresh(work, "enh_bad_notes")
    make_index_md(d)
    (d / "index_notes.json").write_text("{not json", encoding="utf-8")
    code, exc = run("cmd_index", _ns(d, None, None))
    record("enh: invalid index_notes.json no crash", code == 0 and exc is None, f"exit={code} exc={type(exc).__name__ if exc else None}")

    # E6 index_notes.json is a directory -> no crash
    d = fresh(work, "enh_notes_dir")
    make_index_md(d)
    (d / "index_notes.json").mkdir()
    code, exc = run("cmd_index", _ns(d, None, None))
    record("enh: index_notes.json as directory no crash", code == 0 and exc is None, f"exit={code} exc={type(exc).__name__ if exc else None}")

    # E7 trailing-slash note key matches a directory
    d = fresh(work, "enh_dir_note")
    make_index_md(d)
    (d / "src").mkdir()
    write_json(d / "index_notes.json", {"src/": "source code"})
    code, exc = run("cmd_index", _ns(d, None, None))
    text = (d / "index.md").read_text(encoding="utf-8")
    ok = code == 0 and "source code" in text
    record("enh: trailing-slash note key matches directory", ok, f"exit={code}")


def test_validate_relaxed(work: Path) -> None:
    d = fresh(work, "val_relaxed")
    b = valid_blacklist()
    del b["blacklist"][0]["scope"]
    del b["blacklist"][0]["status"]
    write_json(d / "blacklist.json", b)
    write_json(d / "whitelist.json", valid_whitelist())
    code, exc = run("cmd_validate", _ns(d, None, None))
    record("validate: strict mode rejects missing fields", code != 0 and exc is None, f"exit={code}")
    code, exc = run("cmd_validate", _ns(d, None, None), relaxed=True)
    record("validate: --relaxed accepts missing optional fields", code == 0 and exc is None, f"exit={code}")


def test_check(work: Path) -> None:
    """The 'check' subcommand: workspace health gate."""
    # C1 healthy workspace passes
    d = fresh(work, "chk_ok")
    run("cmd_init", _ns(d, "Test", False))
    run("cmd_index", _ns(d, None, None))
    code, exc = run("cmd_check", _ns(d, None, None))
    record("check: healthy workspace passes", code == 0 and exc is None, f"exit={code}")

    # C2 missing required file fails
    d = fresh(work, "chk_missing")
    run("cmd_init", _ns(d, "Test", False))
    (d / "LESSONS.md").unlink()
    code, exc = run("cmd_check", _ns(d, None, None))
    record("check: missing required file fails", code != 0 and exc is None, f"exit={code}")

    # C3 stale index (template placeholder never refreshed) fails
    d = fresh(work, "chk_stale")
    run("cmd_init", _ns(d, "Test", False))
    code, exc = run("cmd_check", _ns(d, None, None))
    record("check: stale index fails", code != 0 and exc is None, f"exit={code}")

    # C4 invalid registry fails
    d = fresh(work, "chk_bad_registry")
    run("cmd_init", _ns(d, "Test", False))
    (d / "blacklist.json").write_text("{bad", encoding="utf-8")
    code, exc = run("cmd_check", _ns(d, None, None))
    record("check: invalid registry fails", code != 0 and exc is None, f"exit={code}")

    # C5 adding a file makes the index stale -> fails
    d = fresh(work, "chk_new_file")
    run("cmd_init", _ns(d, "Test", False))
    run("cmd_index", _ns(d, None, None))
    (d / "new_file.txt").write_text("x", encoding="utf-8")
    code, exc = run("cmd_check", _ns(d, None, None))
    record("check: new file makes index stale", code != 0 and exc is None, f"exit={code}")

    # C6 invalid index_notes.json fails check
    d = fresh(work, "chk_bad_notes")
    run("cmd_init", _ns(d, "Test", False))
    run("cmd_index", _ns(d, None, None))
    (d / "index_notes.json").write_text("{bad", encoding="utf-8")
    code, exc = run("cmd_check", _ns(d, None, None))
    record("check: invalid index_notes.json fails", code != 0 and exc is None, f"exit={code}")

    # C7 custom section names honored by check
    d = fresh(work, "chk_custom")
    run("cmd_init", _ns(d, "Test", False))
    (d / "index.md").write_text(
        "# 索引\n\n## 根目录\n```\n(占位)\n```\n\n## 变更记录\n- init\n",
        encoding="utf-8",
    )
    run("cmd_index", _ns(d, None, None),
        root_section="## 根目录", changelog_section="## 变更记录")
    code, exc = run("cmd_check", _ns(d, None, None),
                    root_section="## 根目录", changelog_section="## 变更记录")
    record("check: custom section names honored", code == 0 and exc is None, f"exit={code}")


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="gov_test_") as tmp:
        work = Path(tmp)
        test_init(work)
        test_validate(work)
        test_index(work)
        test_index_enhanced(work)
        test_validate_relaxed(work)
        test_check(work)
        test_destructive(work)
        test_adversarial(work)

    fails = [r for r in RESULTS if not r[1]]
    print("\n" + "=" * 60)
    print(f"TOTAL: {len(RESULTS)}  PASS: {len(RESULTS) - len(fails)}  FAIL: {len(fails)}")
    if fails:
        print("FAILED CASES:")
        for name, _, detail in fails:
            print(f"  - {name}  {detail}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
