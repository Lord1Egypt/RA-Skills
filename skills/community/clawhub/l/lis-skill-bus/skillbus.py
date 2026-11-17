#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""lis-skill-bus v0.1.12 —— 本地 Skill 联动总线（纯 stdlib，无网络，跨平台）。

职责：
  1) 统一存取项目状态（断点续上）
  2) 解析 skill 契约 schema（resolve_contract）
  3) 枚举本机已安装 skill 与版本（list_skills）

双模式：
  python3 skillbus.py serve            # MCP stdio server（新行分隔 JSON-RPC）
  python3 skillbus.py <CLI 子命令>     # 未注册 MCP 时可直接使用命令行模式

红线：不访问网络；公司数据只落本机 SKILLBUS_STATE_DIR。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path

VERSION = "0.1.12"
# scripts/ 缺省时按根目录(SKILL.md/manifest)探测；加缓存(同图只解析一次)与溯源。
SKILL_SIGNS = ("SKILL.md", "manifest.json", "deps.py")

CODEX_HOME = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
DEFAULT_SKILLS_DIR = CODEX_HOME / "skills"
STATE_DIR = Path(os.environ.get("SKILLBUS_STATE_DIR", CODEX_HOME / "skills" / ".skillbus"))
STATE_FILE = STATE_DIR / "state.json"
REGISTRY = {
    "cad-file-reader": "cad-file-reader/v0",
    "tujian-suanliang": "qto-project/v1",
    "anzhuang-suanliang": "qto-project/v1",
    "zhuangshi-suanliang": "qto-project/v1",
    "yuanlin-suanliang": "qto-project/v1",
}
CONTRACT_SCHEMA_CATALOG = {
    "cad-file-reader/v0": {
        "spec": "cad-file-reader/v0",
        "description": "识图候选契约：置信分层 + 复核原因 + 证据坐标 + 来源文件；不含最终工程量。",
        "required_top": ["schema", "producer", "source"],
        "note": "详见 cad-file-reader/scripts/cad_contract.py 的 CONTRACT_SCHEMA；详细字段以完整包为准。",
    },
    "qto-project/v1": {
        "spec": "qto-project/v1",
        "description": "算量五件套联动契约：项目主键/草稿类型/专业 + cad-file-reader 候选。",
        "required_top": ["qto_spec", "project_key", "draft_type", "specialty"],
        "note": "详见 cad-file-reader/schemas/qto-project-v1.schema.json。",
    },
}


# --------------------------------------------------------------------------- #
# 状态文件（原子写，简单可靠）
# --------------------------------------------------------------------------- #
def _atomic_write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, path)


def _load_state() -> dict:
    if not STATE_FILE.exists():
        return {"state_version": 1, "projects": {}}
    try:
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        # 状态损坏时降级为空库，不覆盖原文件；调用方自行决定是否重写。
        return {"state_version": 1, "projects": {}, "_corrupted": str(STATE_FILE)}


def _project_key(state: dict, project: str, building: str = "", floor: str = "") -> str:
    parts = [p for p in (project, building, floor) if p]
    return "__slash__".join(parts) if parts else "__project__"


def get_project_state(project: str, building: str = "", floor: str = "") -> dict:
    state = _load_state()
    key = _project_key(state, project, building, floor)
    return {"project_key": key, "entries": state["projects"].get(key, {})}


def push_project_state(project: str, entry: dict, building: str = "", floor: str = "",
                       source_skill: str = "unknown", replace: bool = False) -> dict:
    state = _load_state()
    key = _project_key(state, project, building, floor)
    bucket = state["projects"].setdefault(key, {})
    entry = dict(entry or {})
    entry.setdefault("_provenance", {})
    entry["_provenance"].update({
        "source_skill": source_skill,
        "schema": entry.get("schema") or REGISTRY.get(source_skill, "unknown"),
        "pushed_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
    })
    # 溯源增强：契约自带 source 字段时把图纸指纹搬进 provenance，供同图判重/溯源。
    src = entry.get("source") or {}
    if src.get("sha256"):
        entry["_provenance"].setdefault("source_sha256", str(src["sha256"]))
    if src.get("file"):
        entry["_provenance"].setdefault("source_file", str(src["file"]))
    if entry.get("source_file"):
        entry["_provenance"].setdefault("source_file", str(entry["source_file"]))
    if not entry["_provenance"].get("source_sha256") and entry.get("_source_sha256"):
        entry["_provenance"]["source_sha256"] = str(entry["_source_sha256"])
    # 以 entry._id 为粒度；没有 _id 时整条替换/合并。
    eid = entry.get("_id")
    if eid:
        old = bucket.get(eid)
        bucket[eid] = entry if replace else {**(old or {}), **entry}
        entry = bucket[eid]
    elif replace:
        bucket["_last"] = entry
    else:
        latest = bucket.get("_last", {})
        entry = {**latest, **entry}
        bucket["_last"] = entry
    _atomic_write_text(STATE_FILE, json.dumps(state, ensure_ascii=False, indent=2))
    return {"project_key": key, "saved": True, "entry_id": eid or "_last", "count": len(bucket)}


def list_skills(skills_dir: Path = DEFAULT_SKILLS_DIR) -> list:
    out = []
    if not skills_dir.exists():
        return out
    for child in sorted(p for p in skills_dir.iterdir() if p.is_dir()):
        info = detect_skill(child)
        if info is None:
            continue
        out.append({"name": info["name"], "slug": info["slug"], "version": info["version"],
                    "path": info["path"], "contract": info["contract"],
                    "has_scripts": info["has_scripts"], "marker": info["marker"]})
    return out


def resolve_contract(name: str, version: str = "") -> dict:
    key = name
    if version and version not in name:
        key = f"{name}/{version}"
    cat = CONTRACT_SCHEMA_CATALOG.get(name) or CONTRACT_SCHEMA_CATALOG.get(key)
    if cat is None:
        return {"resolved": False, "name": name, "version": version,
                "reason": "未登记契约；可在平台完整包 schemas/ cad-contract-catalog.json 查询"}
    return {"resolved": True, "name": name, "version": version, "spec": cat.get("spec"),
            "description": cat.get("description"), "required_top": cat.get("required_top"),
            "note": cat.get("note")}


# --------------------------------------------------------------------------- #
# 目录探测（scripts/ 缺失也能探测；deps.py 仅作可选的强 marker）
# --------------------------------------------------------------------------- #
def _read_meta(root: Path) -> tuple[str, str]:
    """从 manifest.json / SKILL.md / _meta.json 读取 skill 名与版本。"""
    name = root.name
    ver = ""
    for cand, name_key, ver_key in (
        (root / "manifest.json", "name", "version"),
        (root / "_meta.json", "slug", "version"),
    ):
        try:
            if cand.is_file():
                data = json.loads(cand.read_text(encoding="utf-8"))
                name = str(data.get(name_key) or name)
                ver = str(data.get(ver_key) or "")
                break
        except (json.JSONDecodeError, OSError):
            continue
    return name, ver


def detect_skill(root) -> dict | None:
    """探测一个 skill 目录是否有效。

    兼容历史行为（scripts 下的 deps.py 默认 marker=scripts），但**不再强依赖 scripts/**：
    lis-skill-bus 本身没有 scripts/ 目录，遇到这类 skill 用根目录 SKILL.md /
    manifest.json 兜底即可命中。
    """
    root = Path(root)
    if not root.is_dir():
        return None
    scripts = root / "scripts"
    name, ver = _read_meta(root)
    has_scripts = scripts.is_dir()
    if has_scripts:
        scripts_py = sorted(scripts.glob("*.py")) if scripts.is_dir() else []
        if (scripts / "deps.py").is_file():
            marker = "scripts" + "/" + "deps.py"
        elif scripts_py:
            marker = f"scripts/{scripts_py[0].name}"
        else:
            marker = "scripts/"
    elif (root / "SKILL.md").is_file():
        marker = "SKILL.md"
    elif (root / "manifest.json").is_file():
        marker = "manifest.json"
    else:
        return None
    return {
        "name": name,
        "slug": root.name,
        "version": ver,
        "path": str(root),
        "scripts": str(scripts) if has_scripts else None,
        "has_scripts": has_scripts,
        "marker": marker,
        "contract": REGISTRY.get(root.name, ""),
    }


def find_skill(name: str, roots=()) -> dict | None:
    """在多处 skills 根目录里探测 name（无 scripts/ 也能探测）。"""
    bases = [Path(b) for b in roots if b]
    bases += [
        DEFAULT_SKILLS_DIR,
        Path.home() / ".workbuddy" / "skills",
        CODEX_HOME / "mcp_servers",
        CODEX_HOME / "skills" / "cad-suite" / "modules",
        CODEX_HOME / "skills" / ".skillbus",
    ]
    seen: set[str] = set()
    for base in bases:
        for cand in (base, base / name):
            try:
                r = cand.resolve()
            except OSError:
                continue
            key = str(r)
            if key in seen:
                continue
            seen.add(key)
            info = detect_skill(r)
            if info and info["slug"] == name:
                if info.get("has_scripts") or info.get("marker"):
                    return info
    return None


def _source_signature(source_file) -> tuple[str, str]:
    """图纸/原始文件指纹：优先 sha256，退化用 大小+mtime。"""
    p = Path(source_file) if source_file else None
    if p and p.is_file():
        try:
            import hashlib
            h = hashlib.sha256()
            with p.open("rb") as fh:
                for chunk in iter(lambda: fh.read(1024 * 1024), b""):
                    h.update(chunk)
            return h.hexdigest(), str(source_file)
        except OSError:
            pass
        try:
            st = p.stat()
            return f"size={st.st_size},mtime={int(st.st_mtime)}", str(source_file)
        except OSError:
            pass
    return "", str(source_file or "")


def find_contract(project: str, building: str = "", floor: str = "",
                  source_file: str = "", source_sha256: str = "") -> dict:
    """按来源图纸在 bus 里找已解析契约：同图只解析一次的判据。"""
    state = _load_state()
    key = _project_key(state, project, building, floor)
    bucket = state.get("projects", {}).get(key, {})
    sha, fname = _source_signature(source_file)
    want_sha = (source_sha256 or sha or "").lower()
    want_name = Path(fname).name if fname else ""
    for eid, entry in bucket.items():
        if eid == "_last" or not isinstance(entry, dict):
            continue
        prov = entry.get("_provenance") or {}
        src = entry.get("source") or {}
        cand_shas = [str(prov.get("source_sha256") or ""), str(src.get("sha256") or "")]
        cand_names = [str(prov.get("source_file") or ""), str(src.get("file") or ""),
                      str(entry.get("source_file") or "")]
        if want_sha and any(want_sha == c.lower() for c in cand_shas if c):
            return {"hit": True, "entry": entry, "entry_id": eid,
                    "reason": "source_sha256 命中", "source_sha256": want_sha}
        if want_name and any(want_name == Path(c).name for c in cand_names if c):
            return {"hit": True, "entry": entry, "entry_id": eid,
                    "reason": "source_file 同名命中（建议同时给文件以获得 sha256 判据）",
                    "source_sha256": want_sha}
    total = len([e for e in bucket.values() if isinstance(e, dict) and e.get("_id")])
    return {"hit": False, "entry": None, "entry_id": None, "reason": "未命中",
            "source_sha256": want_sha, "count": total}


# --------------------------------------------------------------------------- #
# 简易 stdio MCP server（行分隔 JSON-RPC，兼容当前 MCP stdio 传输）
# --------------------------------------------------------------------------- #
def _reply(req: dict, result: dict = None, error: dict = None) -> str:
    body = {"jsonrpc": "2.0", "id": req.get("id")}
    if error is not None:
        body["error"] = error
    else:
        body["result"] = result
    return json.dumps(body, ensure_ascii=False)


def _tool_router(name: str, args: dict) -> dict:
    if name == "list_skills":
        return {"skills": list_skills()}
    if name == "get_project_state":
        return get_project_state(str(args.get("project", "")),
                                 str(args.get("building", "")),
                                 str(args.get("floor", "")))
    if name == "push_project_state":
        return push_project_state(
            str(args.get("project", "")),
            args.get("entry") or {},
            building=str(args.get("building", "")),
            floor=str(args.get("floor", "")),
            source_skill=str(args.get("source_skill", "unknown")),
            replace=bool(args.get("replace", False)),
        )
    if name == "resolve_contract":
        return resolve_contract(str(args.get("name", "")), str(args.get("version", "") or ""))
    if name == "detect_skill":
        return {"skill": detect_skill(args.get("path", ""))}
    if name == "find_contract":
        return find_contract(
            str(args.get("project", "")), str(args.get("building", "")),
            str(args.get("floor", "")), str(args.get("source_file", "")),
            str(args.get("source_sha256", "") or ""))
    raise ValueError(f"unknown tool: {name}")


def serve() -> int:
    tools = [
        {"name": "list_skills", "description": "枚举本机已安装 Skill 与版本", "inputSchema": {"type": "object"}},
        {"name": "get_project_state", "description": "读取指定项目的共享状态", "inputSchema": {
            "type": "object", "properties": {
                "project": {"type": "string"}, "building": {"type": "string"}, "floor": {"type": "string"}}}},
        {"name": "push_project_state", "description": "写入指定项目的共享状态（原子写）", "inputSchema": {
            "type": "object", "properties": {
                "project": {"type": "string"}, "building": {"type": "string"}, "floor": {"type": "string"},
                "source_skill": {"type": "string"}, "replace": {"type": "boolean"}, "entry": {"type": "object"}}}},
        {"name": "resolve_contract", "description": "解析 skill 契约 schema 元数据", "inputSchema": {
            "type": "object", "properties": {"name": {"type": "string"}, "version": {"type": "string"}}}},
        {"name": "detect_skill", "description": "探测 skill 目录（scripts/ 缺失也能命中）", "inputSchema": {
            "type": "object", "properties": {"path": {"type": "string"}}}},
        {"name": "find_contract", "description": "按来源图纸找已解析契约（同图只解析一次）", "inputSchema": {
            "type": "object", "properties": {
                "project": {"type": "string"}, "building": {"type": "string"}, "floor": {"type": "string"},
                "source_file": {"type": "string"}, "source_sha256": {"type": "string"}}}},
    ]
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except json.JSONDecodeError:
            continue
        method = req.get("method")
        if method == "initialize":
            sys.stdout.write(_reply(req, {"protocolVersion": "2024-11-05",
                                          "capabilities": {"tools": {}},
                                          "serverInfo": {"name": "lis-skill-bus", "version": VERSION}}))
        elif method == "notifications/initialized":
            continue
        elif method == "tools/list":
            sys.stdout.write(_reply(req, {"tools": tools}))
        elif method == "tools/call":
            try:
                r = _tool_router(req.get("params", {}).get("name", ""),
                                 req.get("params", {}).get("arguments") or {})
                sys.stdout.write(_reply(req, {"content": [{"type": "text",
                                                           "text": json.dumps(r, ensure_ascii=False, indent=2)}],
                                             "isError": False}))
            except Exception as exc:  # noqa: BLE001
                sys.stdout.write(_reply(req, error={"code": -32000, "message": str(exc)}))
        sys.stdout.flush()
    return 0


# --------------------------------------------------------------------------- #
# CLI 模式
# --------------------------------------------------------------------------- #
def main() -> int:
    ap = argparse.ArgumentParser(description="lis-skill-bus CLI 入口")
    ap.add_argument("command", choices=["serve", "list-skills", "get-project-state",
                                        "push-project-state", "resolve-contract",
                                        "detect-skill", "find-contract"])
    ap.add_argument("--project", default="", help="项目标识")
    ap.add_argument("--building", default="", help="楼栋（可选）")
    ap.add_argument("--floor", default="", help="楼层（可选）")
    ap.add_argument("--skill", default="", help="skill 名称")
    ap.add_argument("--contract", default="", help="契约名，如 cad-file-reader/v0")
    ap.add_argument("--entry-file", default="", help="push 模式的状态 JSON 文件")
    ap.add_argument("--skill-dir", default="", help="detect-skill 的目录")
    ap.add_argument("--source-file", default="", help="find-contract 的原始图纸路径")
    ap.add_argument("--source-sha256", default="", help="find-contract 的 sha256（可选）")
    args = ap.parse_args()

    if args.command == "serve":
        return serve()
    if args.command == "list-skills":
        print(json.dumps(list_skills(), ensure_ascii=False, indent=2))
        return 0
    if args.command == "get-project-state":
        print(json.dumps(get_project_state(args.project, args.building, args.floor),
                         ensure_ascii=False, indent=2))
        return 0
    if args.command == "resolve-contract":
        print(json.dumps(resolve_contract(args.contract), ensure_ascii=False, indent=2))
        return 0
    if args.command == "detect-skill":
        print(json.dumps(detect_skill(args.skill_dir or DEFAULT_SKILLS_DIR),
                         ensure_ascii=False, indent=2))
        return 0
    if args.command == "find-contract":
        print(json.dumps(find_contract(args.project, args.building, args.floor,
                                       args.source_file, args.source_sha256),
                         ensure_ascii=False, indent=2))
        return 0
    if args.command == "push-project-state":
        if not args.entry_file:
            print(json.dumps({"error": "需要 --entry-file"}, ensure_ascii=False), file=sys.stderr)
            return 2
        entry = json.loads(Path(args.entry_file).read_text(encoding="utf-8"))
        print(json.dumps(push_project_state(args.project, entry, args.building, args.floor,
                                            source_skill=args.skill), ensure_ascii=False, indent=2))
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
