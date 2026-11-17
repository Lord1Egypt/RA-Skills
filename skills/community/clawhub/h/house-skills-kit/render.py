#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
house-skills-kit 渲染器 v2
  角色原型(archetype) + 挂载模块(modules) + 品牌配置(brand.yaml) → SKILL.md
用法:
  python3 render.py --config brand.yaml            # 按 yaml 里的 archetype+modules 渲染
  python3 render.py --config brand.yaml --out ./out
"""
import argparse
import datetime
import json
import os
import re
import sys

try:
    import yaml
except ImportError:
    sys.exit("需要 PyYAML: pip install pyyaml")

KIT_DIR = os.path.dirname(os.path.abspath(__file__))
TPL_DIR = os.path.join(KIT_DIR, "template")
ARCH_DIR = os.path.join(TPL_DIR, "archetypes")
MOD_DIR = os.path.join(TPL_DIR, "modules")


def build_vars(cfg):
    """brand.yaml → 模板变量(摊平)。"""
    brand = cfg.get("brand", {})
    skill = cfg.get("skill", {})
    adapter = cfg.get("adapter", {})
    content = cfg.get("content", {})

    city = (brand.get("cities") or ["本城"])[0]
    version = skill.get("version", "0.1.0")
    slug = brand.get("slug", "brand")

    vars_ = {}
    for k, v in content.items():
        vars_[k] = v if isinstance(v, str) else str(v)
    vars_.update({
        "brand_name": brand.get("name", "示例品牌"),
        "brand_company": brand.get("company", brand.get("name", "示例品牌")),
        "city": city,
        "version": version,
        "domain_id": skill.get("domain", "buy"),
        "skill_id": f"{slug}-{skill.get('domain', skill.get('archetype', 'skill'))}",
        "adapter_id": adapter.get("id", "mock"),
        "generated_at": datetime.date.today().isoformat(),
    })
    if "adapter_usage" in vars_:
        vars_["adapter_usage"] = (vars_["adapter_usage"]
                                  .replace("{cli}", vars_["adapter_id"])
                                  .replace("{city}", city))
    return vars_


def substitute(text, vars_):
    """{{var}} 替换；支持 {{var|默认值}} 语法；两者都缺则保留原样并记名。"""
    missing = set()

    def sub(m):
        key, default = m.group(1), m.group(2)
        if key in vars_:
            return str(vars_[key])
        if default is not None:
            return default
        missing.add(key)
        return m.group(0)

    return re.sub(r"\{\{(\w+)(?:\|([^}]*))?\}\}", sub, text), missing


def render(cfg, vars_override=None):
    """按 archetype+modules 组装渲染。返回 (text, manifest, missing)"""
    skill = cfg.get("skill", {})
    brand = cfg.get("brand", {})
    archetype = skill.get("archetype", "consumer-buy")
    modules = skill.get("modules", [])

    arch_path = os.path.join(ARCH_DIR, f"{archetype}.md.tmpl")
    if not os.path.exists(arch_path):
        avail = sorted(f.replace(".md.tmpl", "") for f in os.listdir(ARCH_DIR))
        sys.exit(f"[x] 未知 archetype: {archetype}（可选: {', '.join(avail)}）")

    text = open(arch_path, encoding="utf-8").read()
    for m in modules:
        mp = os.path.join(MOD_DIR, f"{m}.md.tmpl")
        if not os.path.exists(mp):
            avail = sorted(f.replace(".md.tmpl", "") for f in os.listdir(MOD_DIR))
            sys.exit(f"[x] 未知 module: {m}（可选: {', '.join(avail)}）")
        text += open(mp, encoding="utf-8").read()

    vars_ = build_vars(cfg)
    if vars_override:
        vars_.update(vars_override)
    out, missing = substitute(text, vars_)

    slug = brand.get("slug", "brand")
    skill_id = vars_["skill_id"]
    manifest = {
        "name": skill_id,
        "version": skill.get("version", "0.1.0"),
        "generated_by": "house-skills-kit v2",
        "brand": brand.get("name"),
        "city": (brand.get("cities") or [None])[0],
        "archetype": archetype,
        "modules": modules,
        "adapter": cfg.get("adapter", {}).get("id"),
        "entry": "SKILL.md",
        "generated_at": datetime.datetime.now().isoformat(timespec="seconds"),
    }
    return out, manifest, missing


def main():
    ap = argparse.ArgumentParser(description="house-skills-kit renderer v2")
    ap.add_argument("--config", required=True)
    ap.add_argument("--out", default=os.path.join(KIT_DIR, "output"))
    args = ap.parse_args()

    # 安全加固 1.4.1：输出一律收敛到仓库 output/ 内，杜绝写到包目录之外
    out_root = os.path.realpath(args.out)
    repo_root = os.path.realpath(KIT_DIR)
    if os.path.commonpath([out_root, repo_root]) != repo_root:
        ap.error(f"--out 必须位于仓库目录内: {out_root}")

    with open(args.config, encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    # 安全加固 1.4.1：--config 同样限定在仓库内读取
    cfg_real = os.path.realpath(args.config)
    if os.path.commonpath([cfg_real, repo_root]) != repo_root:
        ap.error(f"--config 必须位于仓库目录内: {cfg_real}")

    text, manifest, missing = render(cfg)
    outdir = os.path.join(args.out, manifest["name"])
    os.makedirs(outdir, exist_ok=True)

    skill_path = os.path.join(outdir, "SKILL.md")
    with open(skill_path, "w", encoding="utf-8") as f:
        f.write(text)
    with open(os.path.join(outdir, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    print(f"[ok] {skill_path}  (archetype={manifest['archetype']}, modules={manifest['modules']})")
    if missing:
        print(f"[warn] 未填充占位符: {sorted(missing)}")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
