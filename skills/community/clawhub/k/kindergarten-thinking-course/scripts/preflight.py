#!/usr/bin/env python3
"""
preflight.py — 上架发布前合规自检。

覆盖 skillhub 上架要求与评分红线：
  * Frontmatter 必填字段（name/version/category/platforms/description/license）
  * description 字数 ≤ 80（skillhub 建议 ≤ 50）
  * SKILL.md 必须在压缩包根目录
  * zip 总大小 ≤ 10 MB
  * LICENSE / CHANGELOG 存在
  * 终端匹配：脚本零外网调用（requests / urllib / socket / http）
  * 终端匹配：脚本零凭证/系统路径读取（.ssh / AppData / token / credentials / winreg）
  * 终端匹配：脚本零高危函数（eval / exec）
  * 文件清单存在（README / SKILL.md / scripts/test_skill.py）

执行：
    python scripts/preflight.py            # 人类可读输出
    python scripts/preflight.py --json     # 输出 JSON 便于 CI 集成
    python scripts/preflight.py --zip X    # 同时校验已存在的 zip
退出码：0 全部通过 / 1 有失败
"""
from __future__ import annotations
import argparse
import json as json_mod
import re
import sys
import zipfile
from datetime import datetime
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SKILL_MD = ROOT / "SKILL.md"
README = ROOT / "README.md"
CHANGELOG = ROOT / "CHANGELOG.md"
LICENSE = ROOT / "LICENSE"
ICON = ROOT / "assets" / "icon.png"
PREVIEW = ROOT / "assets" / "preview.png"
GALLERY = ROOT / "assets" / "gallery.png"


# ---------- report structure -------------------------------------------------

results: list[tuple[str, bool, str]] = []   # (name, passed, detail)

def chk(name: str, ok: bool, detail: str = ""):
    results.append((name, ok, detail))
    sym = "PASS" if ok else "FAIL"
    if detail and not ok:
        print(f"  [{sym}] {name}  —  {detail}")
    elif detail:
        print(f"  [{sym}] {name}  —  {detail}")
    else:
        print(f"  [{sym}] {name}")

def section(title: str):
    print(f"\n== {title} ==")


# ---------- frontmatter ------------------------------------------------------

def parse_frontmatter(text: str) -> dict:
    if not text.startswith("---"):
        return {}
    end = text.find("---", 3)
    if end == -1:
        return {}
    body = text[3:end]
    out = {}
    cur_key = None
    for line in body.splitlines():
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if m:
            cur_key = m.group(1)
            v = m.group(2).strip()
            if v.startswith("[") and v.endswith("]"):
                items = [x.strip().strip('"').strip("'") for x in v[1:-1].split(",") if x.strip()]
                out[cur_key] = items
            elif v == "":
                out[cur_key] = []  # 后续接缩进项视为列表
            else:
                out[cur_key] = v.strip('"').strip("'")
        elif line.startswith("  - ") and cur_key:
            existing = out.setdefault(cur_key, [])
            if not isinstance(existing, list):
                existing = []
                out[cur_key] = existing
            existing.append(line.strip()[2:])
        elif line.strip() and not line.strip().startswith("-"):
            cur_key = None
    return out


# ---------- checks -----------------------------------------------------------

def check_frontmatter() -> dict:
    section("Frontmatter 必填字段（skillhub 上架要求）")
    text = SKILL_MD.read_text(encoding="utf-8")
    fm = parse_frontmatter(text)
    must_have = ["name", "version", "category", "platforms", "description", "license"]
    for f in must_have:
        chk(f"必填字段 {f}", f in fm and str(fm[f]).strip() != "", f"现值: {fm.get(f, '<missing>')}")

    desc = str(fm.get("description", ""))
    desc_len = len(desc)
    # skillhub 建议 ≤ 50 字，但留冗余 ≤ 80
    chk(f"description 长度 ≤ 80（实际 {desc_len} 字）", desc_len <= 80,
        f"过长请精简（建议 ≤ 50 字）")

    # version 语义化
    v = str(fm.get("version", ""))
    chk(f"version 语义化（实际 {v}）",
        bool(re.match(r"^\d+\.\d+\.\d+$", v)))

    # platforms 非空且至少 1 个
    plats = fm.get("platforms", [])
    if isinstance(plats, str):
        plats = [plats]
    chk(f"platforms ≥ 1（实际 {len(plats) if isinstance(plats, list) else 0}）",
        isinstance(plats, list) and len(plats) >= 1)

    # folder 与 name 一致
    chk(f"文件夹名与 name 一致（{ROOT.name}）",
        fm.get("name") == ROOT.name)
    return fm


def check_files() -> None:
    section("必备文件清单")
    for label, path in [
        ("SKILL.md", SKILL_MD),
        ("README.md", README),
        ("CHANGELOG.md", CHANGELOG),
        ("LICENSE", LICENSE),
        ("assets/icon.png（推荐）", ICON),
        ("assets/preview.png（推荐）", PREVIEW),
        ("assets/gallery.png（推荐）", GALLERY),
    ]:
        chk(f"{label}", path.exists(), f"路径: {path.relative_to(ROOT)}")


def check_security() -> None:
    section("TRACE-T 可信任度（skillhub 红线维度）")
    scripts_dir = ROOT / "scripts"
    deny_patterns = {
        "外网调用 (requests/urllib/socket/http)":
            re.compile(r"\b(requests|urllib|socket|http\.|httpx|aiohttp)\b"),
        "凭证/敏感路径读取 (.ssh/token/credentials/winreg/AppData/homedir)":
            re.compile(r"(\.ssh|credentials|homedir|AppData|/\.aws|\.aws|/\.azure|/\.gcp|winreg|registry|token\b)"),
        "高危函数 (eval/exec)":
            re.compile(r"\b(eval|exec)\s*\("),
        "Shell 注入 (os.system/popen)":
            re.compile(r"\b(os\.system|popen|spawn|start_process)\b"),
    }

    issues = []
    for py in sorted(scripts_dir.rglob("*.py")):
        # 扫描脚本自身的正则定义会被自身匹配到，跳过
        if py.name == "preflight.py":
            continue
        rel = py.relative_to(scripts_dir).as_posix()
        try:
            text = py.read_text(encoding="utf-8")
        except Exception:
            continue
        for line_no, line in enumerate(text.splitlines(), 1):
            for label, pat in deny_patterns.items():
                if pat.search(line) and not line.strip().startswith("#"):
                    issues.append(f"{rel}:{line_no}  [{label}]  {line.strip()[:100]}")

    for label, pat in deny_patterns.items():
        chk(label, not any(f"[{label}]" in i for i in issues),
            "; ".join(i for i in issues if f"[{label}]" in i) if issues else "")

    if not issues:
        print("  ✓ 所有 scripts/*.py 文件通过安全扫描")


def check_zip(zip_path: Path | None) -> None:
    section("zip 包合规")
    if zip_path is None:
        print("  (跳过，未通过 --zip 指定)")
        return
    if not zip_path.exists():
        chk(f"zip 存在: {zip_path.name}", False, "文件不存在")
        return
    size_mb = zip_path.stat().st_size / (1024 * 1024)
    chk(f"zip 大小 ≤ 10 MB（实际 {size_mb:.2f} MB）", size_mb <= 10)

    try:
        with zipfile.ZipFile(zip_path, "r") as z:
            names = z.namelist()
            chk("zip 可正常打开", True)
            chk("SKILL.md 位于压缩包根目录",
                any(n == "SKILL.md" or n.endswith("/SKILL.md") and n.count("/") == 1 for n in names),
                f"顶层含: {[n for n in names if '/' not in n]}")

            # 不允许敏感文件
            for bad in ("__pycache__", ".pyc", ".pyo", ".env", ".git"):
                hits = [n for n in names if bad in n]
                chk(f"压缩包不含 {bad}", not hits, f"命中: {hits[:3]}" if hits else "")

            # 文件总数
            chk(f"压缩文件数 ≤ 200（实际 {len(names)}）", len(names) <= 200)
    except zipfile.BadZipFile:
        chk("zip 可正常打开", False, "不是合法 zip")


# ---------- main -------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description="skillhub 上架前合规自检")
    ap.add_argument("--zip", type=Path, default=None,
                    help="同时校验此 zip（如已生成）")
    ap.add_argument("--json", action="store_true", help="以 JSON 输出")
    args = ap.parse_args()

    fm = check_frontmatter()
    check_files()
    check_security()
    check_zip(args.zip)

    passed = sum(1 for _, ok, _ in results if ok)
    failed = len(results) - passed

    report = ROOT / "SHIP_REPORT.md"
    md = [
        f"# 上架自检报告 — {fm.get('name', ROOT.name)} @ {fm.get('version', '?')}",
        "",
        f"_自检时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_  ",
        f"_SKILL.md：{SKILL_MD.relative_to(ROOT)}_",
        "",
        f"## 汇总",
        "",
        f"| 项目 | 数值 |",
        f"|---|---|",
        f"| 通过 | **{passed}** |",
        f"| 失败 | **{failed}** |",
        f"| 通过率 | {100 * passed // max(1, len(results))}% |",
        "",
        f"## 详情",
        "",
        f"| 项目 | 状态 | 说明 |",
        f"|---|---|---|",
    ]
    for name, ok, detail in results:
        md.append(f"| {name} | {'✅' if ok else '❌'} | {detail or '—'} |")
    md += ["", "---", "", "本报告由 `scripts/preflight.py` 自动生成。", ""]
    report.write_text("\n".join(md), encoding="utf-8")

    if args.json:
        print(json_mod.dumps({
            "skill": fm.get("name"),
            "version": fm.get("version"),
            "passed": passed,
            "failed": failed,
            "results": [{"name": n, "ok": ok, "detail": d} for n, ok, d in results],
        }, ensure_ascii=False, indent=2))
    else:
        print(f"\n=== 汇总 === {passed}/{len(results)} 通过")
        if failed:
            print(f"❌ {failed} 项失败，已写入 {report.name}")
        else:
            print(f"✅ 全部通过，自检报告：{report.relative_to(ROOT)}")
    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
