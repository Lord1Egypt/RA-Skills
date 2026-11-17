#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
avatars.py — 本体论智能体 · 头像选择 + 性别逻辑 + 写入专家包
本体论智能体 (Ontology Agent) · 天津市微数人工智能科技有限责任公司

职责：
  - select(code, gender)         : 按 (部门, 性别) 取技能包头像池路径；无则回退通用池
  - avatar_prompt(code, gender)  : 生成该部门头像的 ImageGen 提示词（供补图用）
  - map_instance(instance)        : 返回 {code: 头像路径}，按 instance 的性别覆盖
  - apply_to_expert_package(...)  : 把所选头像写入专家包 avatars/ 并更新 plugin.json

性别只影响头像与语感，绝不影响部门能力。所有头像存技能包 assets/avatars/（可分发），
用户私有 instance 仅记录性别选择，不改技能包文件。
"""
import os
import json
import shutil

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(BASE, "assets", "avatars")
# 头像二进制资产统一托管在 user-level 资源目录，不进 SkillHub 包（平台禁二进制）。
# 加载顺序：user-level 优先 -> 技能包自身 assets/avatars 兜底。两者任一存在即可用。
USER_ASSETS = os.path.expanduser("~/.workbuddy/skills/ontology-agent-assets/avatars")
GENERIC = ["generic_m_1.png", "generic_m_2.png", "generic_f_1.png", "generic_f_2.png"]


def _avatar_dirs(assets_dir=ASSETS):
    dirs = []
    if os.path.isdir(USER_ASSETS):
        dirs.append(USER_ASSETS)
    if assets_dir and os.path.isdir(assets_dir):
        dirs.append(assets_dir)
    return dirs

# 统一的扁平职业风（保证团队视觉一致）
STYLE = ("flat vector illustration of a corporate avatar, minimal modern style, "
         "solid muted background, friendly professional expression, simple clothing, "
         "no text, no logo, no watermark, centered head-and-shoulders, clean composition")

# 各部门视觉线索（让 24 个头像彼此可区分）
CUES = {
    "lead": "a leader with a confident posture, subtle tie",
    "admin": "holding a planner and pen",
    "hr": "warm approachable, handshake gesture",
    "finance": "beside a ledger and calculator",
    "legal": "with a document and scales motif",
    "rnd": "with a laptop and blueprint",
    "mkt_content": "with a camera and notebook",
    "mkt_dist": "with a megaphone and channels",
    "mkt_seo": "with a magnifier over a chart",
    "sales": "with a handshake and rising bar",
    "data": "with a dashboard and graphs",
    "strategy": "before a chessboard and roadmap",
    "customer_service": "wearing a headset, smiling",
    "product": "holding a prototype and roadmap",
    "design": "with a palette and pen",
    "operations": "with gears and checklist",
    "procurement": "with a shipping box and list",
    "quality": "with a magnifier over a sample",
    "it_security": "with a shield and lock",
    "pr": "at a podium with microphone",
    "investor": "with an upward arrow and briefcase",
    "csm": "with a heart and growth icon",
    "international": "with a globe and languages",
    "risk": "with a balance scale",
}


def avatar_prompt(code, gender, name_zh=""):
    g = "male" if gender == "male" else "female"
    cue = CUES.get(code, "professional at work")
    nm = f" representing the Chinese corporate role 「{name_zh}」" if name_zh else ""
    return (f"{STYLE}, a {g} professional{nm}, {cue}. "
            f"Distinct, recognizable, cohesive with a team of 24 department avatars.")


def select(code, gender="male", assets_dir=ASSETS):
    if gender not in ("male", "female"):
        gender = "male"
    g = "f" if gender == "female" else "m"   # 文件名约定 {code}_m.png / {code}_f.png
    for d in _avatar_dirs(assets_dir):
        for cand in (f"{code}_{g}.png", f"{code}.png"):
            p = os.path.join(d, cand)
            if os.path.isfile(p):
                return p
    for d in _avatar_dirs(assets_dir):     # 同性别通用备池
        for ge in GENERIC:
            if g in ge and os.path.isfile(os.path.join(d, ge)):
                return os.path.join(d, ge)
    for d in _avatar_dirs(assets_dir):     # 任意通用备池（最后兜底）
        for ge in GENERIC:
            if os.path.isfile(os.path.join(d, ge)):
                return os.path.join(d, ge)
    return None


def map_instance(instance, assets_dir=ASSETS):
    from init import resolve_departments
    out = {}
    for d in resolve_departments(instance or {}):
        out[d["code"]] = select(d["code"], d.get("gender", "male"), assets_dir)
    return out


def apply_to_expert_package(slug, pkg_dir, instance=None, assets_dir=ASSETS):
    """把所选头像复制到专家包 avatars/ 并更新 plugin.json 的 avatar 字段（用户部署层，零侵入技能包）。"""
    pkg_av = os.path.join(pkg_dir, "avatars")
    os.makedirs(pkg_av, exist_ok=True)
    gender_map = {}
    if instance:
        from init import resolve_departments
        for d in resolve_departments(instance):
            gender_map[d["code"]] = d.get("gender", "male")

    plugin_path = os.path.join(pkg_dir, ".codebuddy-plugin", "plugin.json")
    with open(plugin_path, encoding="utf-8") as fh:
        cfg = json.load(fh)

    # 团队图标（user-level 优先 -> 技能包自身兜底）
    team_src = None
    for d in _avatar_dirs(assets_dir):
        cand = os.path.join(d, "team.png")
        if os.path.isfile(cand):
            team_src = cand
            break
    if team_src:
        shutil.copy(team_src, os.path.join(pkg_av, "team.png"))

    for m in cfg.get("members", []):
        code = m.get("id") or ""
        gender = gender_map.get(code, "male")
        if m.get("role") == "lead":
            code = "lead"
        src = select(code, gender, assets_dir)
        if not src:
            continue
        if m.get("role") == "lead":
            dst_name = "weishu-ontology-digital-company-team-lead.png"
        else:
            dst_name = f"{code}.png"
        shutil.copy(src, os.path.join(pkg_av, dst_name))
        m["avatar"] = f"avatars/{dst_name}"

    with open(plugin_path, "w", encoding="utf-8") as fh:
        json.dump(cfg, fh, ensure_ascii=False, indent=2)
    return cfg


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="头像选择与写入专家包")
    ap.add_argument("--slug", help="公司简称 slug（读 company-data/<slug>/instance.yaml 决定性别）")
    ap.add_argument("--pkg", help="专家包目录（apply 时写入头像）")
    ap.add_argument("--map", action="store_true", help="打印 {code: 头像路径}")
    ap.add_argument("--prompt", nargs=2, metavar=("CODE", "GENDER"), help="打印某部门头像生成提示词")
    args = ap.parse_args()

    if args.prompt:
        print(avatar_prompt(args.prompt[0], args.prompt[1]))
    elif args.map and args.slug:
        from init import default_instance_path, load_instance
        p = default_instance_path(args.slug)
        inst = load_instance(p) if os.path.isfile(p) else {}
        for c, path in map_instance(inst).items():
            print(f"  {c:<16} -> {path}")
    elif args.pkg and args.slug:
        from init import default_instance_path, load_instance
        p = default_instance_path(args.slug)
        inst = load_instance(p) if os.path.isfile(p) else {}
        apply_to_expert_package(args.slug, args.pkg, inst)
        print(f"已写入专家包头像: {args.pkg}/avatars/")
    else:
        ap.print_help()
