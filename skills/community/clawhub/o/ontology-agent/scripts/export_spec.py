#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
export_spec.py —— 本体论规范可移植导出器（Phase 11 · 落地件）

作用：把「厂商中立的本体论规范层」打包成一个自包含、可移植的 bundle，
      让同一套规范能换壳到三种运行时（技能包 / 云端协同 / 纯私有化）。

导出内容：
  - source 规范：ontology-agent/references/*（含 packs/）+ experts-template/department_experts.yaml
  - instance 规范：~/.workbuddy/company-data/<slug>/instance.yaml + company-memory.md（+ 若存在 experts.yaml）
  - manifest.json：可移植契约（schema 版本 / 同步边界 / 红线 / 可移植目标）

设计红线：
  - 只读现有 references / 实例，绝不修改其核心；
  - 不依赖 init.py 等核心脚本，自包含；
  - 产出纯新增 artifact，不动 24 部门模板 / 141 动作库 / decision / semantic / logic。

用法：
  python export_spec.py --bundle all --slug weishu
  python export_spec.py --bundle source
  python export_spec.py --bundle instance --slug weishu --out exports/
  python export_spec.py --bundle all --slug weishu --zip
"""
import argparse
import json
import os
import shutil
import sys
from datetime import datetime, timezone

try:
    import yaml
except ImportError:
    yaml = None

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ONTOLOGY_ROOT = os.path.dirname(SCRIPT_DIR)            # ontology-agent/
REF_DIR = os.path.join(ONTOLOGY_ROOT, "references")
TPL_DIR = os.path.join(ONTOLOGY_ROOT, "experts-template")
HOME = os.path.expanduser("~")
COMPANY_DATA = os.path.join(HOME, ".workbuddy", "company-data")

SCHEMA_VERSION = "1.0"
PACKS = ["opc", "ecommerce", "sme", "manufacturing", "public_institution", "finance", "biomed", "edu_research"]
INVARIANTS = [
    "PII 不写明文（贯穿 A/B/C 三模式）",
    "越权动作一律草拟 + 等确认（proactive.yaml L2 默认档）",
    "语义/逻辑/决策规范一致，不重写",
]


def _log(msg):
    print(msg, file=sys.stderr)


def _ref_files():
    out = []
    for root, _, files in os.walk(REF_DIR):
        for f in files:
            # contact.yaml 为厂商联系方式 metadata，不属登记客体"数据集"，导出 bundle 时排除
            if f in (".gitkeep", "contact.yaml"):
                continue
            full = os.path.join(root, f)
            rel = os.path.relpath(full, ONTOLOGY_ROOT).replace(os.sep, "/")
            out.append(rel)
    out.sort()
    return out


def _count_actions():
    p = os.path.join(REF_DIR, "action_specs.yaml")
    if not yaml or not os.path.exists(p):
        return None
    try:
        d = yaml.safe_load(open(p, encoding="utf-8")) or {}
        return len(d.get("actions", d)) if isinstance(d, dict) else None
    except Exception:
        return None


def _count_depts():
    p = os.path.join(TPL_DIR, "department_experts.yaml")
    if not yaml or not os.path.exists(p):
        return None
    try:
        d = yaml.safe_load(open(p, encoding="utf-8")) or {}
        depts = d.get("departments")
        if isinstance(depts, list):
            return len(depts)
        if isinstance(depts, dict):
            return len(depts)
        return None
    except Exception:
        return None


def _load_instance(slug):
    p = os.path.join(COMPANY_DATA, slug, "instance.yaml")
    if not os.path.exists(p) or not yaml:
        return None
    try:
        return yaml.safe_load(open(p, encoding="utf-8")) or {}
    except Exception:
        return None


def _instance_meta(slug):
    inst = _load_instance(slug)
    if not inst:
        return None
    profile = inst.get("profile", {}) or {}
    meta = inst.get("meta", {}) or {}
    priv = {}
    for k in ("department_aliases", "department_genders", "disabled_departments", "custom_departments"):
        if k in inst and inst[k]:
            priv[k] = inst[k]
    return {
        "slug": slug,
        "company": profile.get("company"),
        "pack_id": meta.get("pack_id"),
        "pack_display": meta.get("pack_display"),
        "departments": profile.get("departments", []),
        "owner": (profile.get("owner_profile", {}) or {}).get("name"),
        "private_customizations": priv,
    }


def build_bundle(kind, slug, out_root, make_zip):
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    if kind == "source":
        bundle_dir = os.path.join(out_root, "ontology_source_bundle")
        title = "本体论源规范 bundle（厂商中立，无实例）"
    elif kind == "instance":
        bundle_dir = os.path.join(out_root, f"{slug}_digital_twin")
        title = f"数字孪生实例 bundle（{slug}）"
    else:
        bundle_dir = os.path.join(out_root, f"{slug}_ontology_bundle")
        title = f"完整本体论 bundle（源规范 + 实例 {slug}）"

    if os.path.exists(bundle_dir):
        shutil.rmtree(bundle_dir)
    os.makedirs(bundle_dir, exist_ok=True)

    manifest = {
        "ontology_bundle": {
            "schema_version": SCHEMA_VERSION,
            "generated_at": ts,
            "generator": "ontology-agent/scripts/export_spec.py",
            "bundle_kind": kind,
            "title": title,
            "portable_to": ["skill_package", "cloud_edge", "pure_private"],
            "source": None,
            "instance": None,
            "governance": {
                "compliance_redlines_ref": "references/decision.yaml",
                "sync_boundary_ref": "references/deployment.yaml#sync_boundary",
                "invariants": INVARIANTS,
            },
        }
    }

    # ── source 规范 ──
    if kind in ("all", "source"):
        dest_ref = os.path.join(bundle_dir, "references")
        # contact.yaml 为厂商联系方式 metadata，不属登记客体"数据集"，导出时排除
        shutil.copytree(REF_DIR, dest_ref, ignore=shutil.ignore_patterns("contact.yaml", ".gitkeep"))
        dest_tpl = os.path.join(bundle_dir, "experts-template")
        os.makedirs(dest_tpl, exist_ok=True)
        shutil.copy(os.path.join(TPL_DIR, "department_experts.yaml"), dest_tpl)
        # 运行内核脚本（模块 7：微数自创代码，纳入 bundle 以保证 7 模块完全覆盖）
        SCRIPT_DIR = os.path.join(os.path.dirname(REF_DIR), "scripts")
        dest_scripts = os.path.join(bundle_dir, "scripts")
        os.makedirs(dest_scripts, exist_ok=True)
        script_files = [f for f in os.listdir(SCRIPT_DIR) if f.endswith(".py") and not f.startswith("_")]
        for fn in script_files:
            shutil.copy(os.path.join(SCRIPT_DIR, fn), dest_scripts)
        manifest["ontology_bundle"]["source"] = {
            "files": _ref_files(),
            "packs": PACKS,
            "department_library_count": _count_depts(),
            "action_specs_total": _count_actions(),
            "scripts_files": script_files,
        }

    # ── instance 规范 ──
    if kind in ("all", "instance"):
        if not slug:
            _log("ERROR: --bundle instance/all 需要 --slug <公司简称>")
            sys.exit(2)
        inst_src = os.path.join(COMPANY_DATA, slug)
        if not os.path.isdir(inst_src):
            _log(f"ERROR: 找不到实例目录 {inst_src}")
            sys.exit(2)
        dest_inst = os.path.join(bundle_dir, "instance")
        os.makedirs(dest_inst, exist_ok=True)
        copied = []
        for fn in ("instance.yaml", "company-memory.md", "experts.yaml"):
            sp = os.path.join(inst_src, fn)
            if os.path.exists(sp):
                shutil.copy(sp, os.path.join(dest_inst, fn))
                copied.append(f"instance/{fn}")
        manifest["ontology_bundle"]["instance"] = _instance_meta(slug)
        if manifest["ontology_bundle"]["instance"] is None:
            manifest["ontology_bundle"]["instance"] = {"slug": slug, "files": copied}
        else:
            manifest["ontology_bundle"]["instance"]["files"] = copied

    # ── 写 manifest ──
    with open(os.path.join(bundle_dir, "manifest.json"), "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, ensure_ascii=False, indent=2)

    _log(f"[export] 已生成 bundle: {bundle_dir}")
    _log(f"[export] bundle_kind={kind} | files={len(_ref_files()) if kind in ('all','source') else 0} refs + instance")

    if make_zip:
        zip_path = shutil.make_archive(bundle_dir, "zip", bundle_dir)
        _log(f"[export] 已压缩: {zip_path}")

    return bundle_dir


def main():
    ap = argparse.ArgumentParser(description="本体论规范可移植导出器")
    ap.add_argument("--bundle", choices=["all", "source", "instance"], default="all")
    ap.add_argument("--slug", help="公司简称（instance/all 需要）")
    ap.add_argument("--out", default=os.path.join(ONTOLOGY_ROOT, "exports"))
    ap.add_argument("--zip", action="store_true", help="同时生成 .zip")
    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)
    build_bundle(args.bundle, args.slug, args.out, args.zip)


if __name__ == "__main__":
    main()
