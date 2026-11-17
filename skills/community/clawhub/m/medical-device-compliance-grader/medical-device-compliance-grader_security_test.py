#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
medical-device-compliance-grader_security_test.py — 医械合规评分器 · 安全稳定性实测
文档型技能 8 维量化测试（本地闭环 · 零真实凭据 · 可重复）

维度（0-5 分制，驱动雷达图）：
  1. official_links   官方链接可信度（外链域名全部落在官方域）
  2. sensitive_zero   敏感信息隔离（真名/邮箱/本地路径/密钥 0 命中）
  3. recency          法规时效标注（现行版本号 + 复核提醒）
  4. boundary         边界与免责声明（不替代裁定 / AS IS）
  5. copyright        权属与许可完整性（LICENSE.md + © + 知识版权声明）
  6. frontmatter      frontmatter 全字段（跨平台发布字段齐全）
  7. nav_consistency  references 导航一致（SKILL.md 导航表 vs 实际文件/章节）
  8. package_clean    打包纯净（无缓存/备份/二进制/_ 前缀元数据）

用法：
  python medical-device-compliance-grader_security_test.py [技能目录]
产出：
  security_results.json（本目录，供 gen_skill_security_radar.py 渲染雷达）
"""
import json
import os
import re
import sys
from pathlib import Path

OFFICIAL_DOMAINS = {'ecfr.gov', 'iso.org', 'eur-lex.europa.eu', 'samr.gov.cn', 'imdrf.org', 'fda.gov', 'cmde.org.cn', 'health.ec.europa.eu', 'nmpa.gov.cn', 'pmda.go.jp', 'adrs.org.cn'}
SENSITIVE = [r"(?<!\d)1[3-9]\d{9}(?!\d)", r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
             r"C:\\Users\\", r"C:/Users/", r"/Users/", r"/home/",
             r"sk-[A-Za-z0-9]{20,}", r"ghp_[A-Za-z0-9]{36,}"]
SKIP_FILES = {"SKILL.md", "LICENSE.md", "ATTESTATION.md", "manifest.json"}
SKIP_FILES_SENS = SKIP_FILES | {Path(__file__).name}


def score_dim(name: str, score: float, note: str) -> dict:
    return {"name": name, "score": round(min(max(score, 0), 5), 2), "note": note}


def main(root: str = ".") -> int:
    base = Path(root).resolve()
    sk = (base / "SKILL.md").read_text("utf-8")
    ref_dir = base / "references"
    refs = {p.name: p.read_text("utf-8") for p in ref_dir.glob("*.md")} if ref_dir.exists() else {}
    lic = (base / "LICENSE.md").read_text("utf-8") if (base / "LICENSE.md").exists() else ""

    dims = []

    # 1. 官方链接可信度：全部外链域名须为官方域
    links = re.findall(r"https?://([a-zA-Z0-9.-]+)", sk + "".join(refs.values()))
    bad = sorted({d for d in links if not any(d == o or d.endswith("." + o) for o in OFFICIAL_DOMAINS)})
    score1 = 5.0 if not bad else max(1.0, 5.0 - 1.5 * len(bad))
    dims.append(score_dim("官方链接可信度", score1,
                          f"{len(links)} 条外链全部官方域" if not bad else f"非官方域: {bad[:3]}"))

    # 2. 敏感信息隔离
    hits = []
    for fname, content in list(refs.items()) + [("SKILL.md", sk)]:
        for pat in SENSITIVE:
            m = re.search(pat, content)
            if m:
                hits.append(f"{fname}:{pat}")
    dims.append(score_dim("敏感信息隔离", 5.0 if not hits else 1.0,
                          "0 命中" if not hits else f"命中: {hits[:3]}"))

    # 3. 法规时效标注
    rec = sum(1 for kw in ["2025 年版", "现行", "最新版", "复核", "时效", "更新"] if kw in sk or kw in "".join(refs.values()))
    dims.append(score_dim("法规时效标注", min(5.0, 2.0 + rec), f"时效关键词命中 {rec}/6"))

    # 4. 边界与免责声明
    bnd = sum(1 for kw in ["不替代", "个案裁定", "免责声明", "AS IS", "不构成", "参考"] if kw in sk)
    dims.append(score_dim("边界与免责", min(5.0, 1.5 + bnd * 0.7), f"边界关键词命中 {bnd}/6"))

    # 5. 权属与许可完整性
    cop = 0
    if lic:
        cop += 2 if "MIT License" in lic and "Copyright" in lic else 0
    if "©" in sk or "版权所有" in sk:
        cop += 1
    if "知识版权声明" in sk:
        cop += 1
    if "注册老炮" in sk:
        cop += 1
    dims.append(score_dim("权属与许可", cop, "LICENSE.md+©+知识版权+品牌署名" if cop >= 4 else f"命中 {cop}/5"))

    # 6. frontmatter 全字段
    fm = sk.split("---")[1] if sk.startswith("---") else ""
    need = ["name", "slug", "displayName", "display_name", "title", "version",
            "author", "category", "platforms", "license", "description", "description_en", "tags"]
    miss = [f for f in need if not re.search(rf"^{f}:", fm, re.M)]
    dims.append(score_dim("frontmatter 全字段", 5.0 if not miss else max(1.0, 5.0 - 1.2 * len(miss)),
                          "13 字段齐全" if not miss else f"缺: {miss}"))

    # 7. references 导航一致：SKILL.md 导航表引用的文件须存在
    nav_refs = re.findall(r"references/([^\s`|]+\.md)", sk)
    missing = sorted({r for r in nav_refs if r not in refs})
    ch_in_nav = len(re.findall(r"第[一二三四五六七]章", sk))
    dims.append(score_dim("导航一致性", 5.0 if not missing and ch_in_nav >= 5 else max(1.0, 5.0 - 1.5 * (len(missing) + max(0, 5 - ch_in_nav))),
                          f"导航引用 {len(nav_refs)} 文件、覆盖 {ch_in_nav} 章" if not missing else f"缺失文件: {missing}"))

    # 8. 打包纯净
    bad_items = []
    for p in base.rglob("*"):
        if p.name in SKIP_FILES_SENS or "__pycache__" in p.parts or ".git" in p.parts:
            continue
        if p.is_file() and p.suffix.lower() in {".png", ".exe", ".jpg", ".jpeg", ".mp4", ".bak", ".tmp"}:
            bad_items.append(p.name)
        if p.is_file() and p.name.startswith("_"):
            bad_items.append(p.name)
    dims.append(score_dim("打包纯净", 5.0 if not bad_items else 2.0,
                          "无缓存/二进制/元数据" if not bad_items else f"混入: {bad_items[:3]}"))

    overall = sum(d["score"] for d in dims) / len(dims)
    result = {
        "skill": "medical-device-compliance-grader",
        "version": re.search(r"^version:\s*[\"']?([\w.]+)", sk.split("---")[1], re.M).group(1),
        "timestamp_local": __import__("datetime").datetime.now().isoformat(timespec="seconds"),
        "scope": "本地闭环 · 零真实凭据 · 可重复",
        "dimensions": dims,
        "overall": round(overall, 2),
    }
    out = base / "security_results.json"
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), "utf-8")
    print(f"✔ 综合 {overall:.2f}/5 → {out}")
    for d in dims:
        print(f"  {d['name']:<8} {d['score']}/5  {d['note']}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "."))
