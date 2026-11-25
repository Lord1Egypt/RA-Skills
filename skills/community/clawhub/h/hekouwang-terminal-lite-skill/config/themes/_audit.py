#!/usr/bin/env python3
# ============================================================
# hekouwang-terminal-skill — 色板视觉审计（只读）
#
# 读**生成出来的** <主题>.json（不是色板 .py），所以审的就是会装到机器上的东西。
# 判据与 palettes/_audit.py 同一份；这里只负责出表和退出码。
#
#   python3 _audit.py                 表格
#   python3 _audit.py --json          机器可读
#   python3 _audit.py --theme ember
#   python3 _audit.py --gate          不达标就 exit 1（release.sh --check 用）
# ============================================================
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), "lib"))

from palettes import _audit  # noqa: E402
from i18n import t  # noqa: E402


def _hex(c: dict) -> str:
    return "".join(
        f"{round(c[k] * 255):02x}"
        for k in ("Red Component", "Green Component", "Blue Component")
    )


def load_one(path: str) -> dict | None:
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    prof = data["Profiles"][0]
    if "Ansi 0 Color" not in prof or "Background Color" not in prof:
        return None
    p = {
        "bg": _hex(prof["Background Color"]),
        "fg": _hex(prof["Foreground Color"]),
        "ansi": [_hex(prof[f"Ansi {i} Color"]) for i in range(16)],
        "selbg": _hex(prof["Selection Color"]) if "Selection Color" in prof else None,
        "selfg": _hex(prof["Selected Text Color"]) if "Selected Text Color" in prof else None,
        "matchbg": _hex(prof["Match Background Color"]) if "Match Background Color" in prof else None,
        "cursor": _hex(prof["Cursor Color"]) if "Cursor Color" in prof else None,
        "faint_text_alpha": prof.get("Faint Text Alpha", 0.55),
    }
    p["light"] = _audit.luminance(p["bg"]) > 0.5
    name = os.path.basename(path)[:-5]
    syn_path = os.path.join(HERE, "ecosystem", name, "syntax.json")
    if os.path.isfile(syn_path):
        try:
            with open(syn_path, encoding="utf-8") as f:
                roles = json.load(f)["roles"]
            p["syntax"] = {
                role: (v["color"].lstrip("#"), v.get("style"))
                for role, v in roles.items()
            }
        except (OSError, ValueError, KeyError):
            pass
    return p


def load_all(only: str | None = None) -> list[dict]:
    out = []
    for fn in sorted(os.listdir(HERE)):
        if not fn.endswith(".json") or fn in ("names.json", "minimal.json"):
            continue
        name = fn[:-5]
        if only and name != only:
            continue
        try:
            p = load_one(os.path.join(HERE, fn))
        except (OSError, ValueError, KeyError):
            continue
        if p:
            r = _audit.evaluate(name, p)
            r["light"] = p["light"]
            out.append(r)
    return out


def detail(r: dict) -> str:
    bits = []
    for x in r["low"]:
        bits.append(f'{x["slot"]} {x["ratio"]:.2f}<{x["floor"]}')
    if r["duplicates"]:
        bits.append("bright=normal: " + ",".join(x["slot"] for x in r["duplicates"]))
    bits.extend(r.get("issues", []))
    if not r.get("hue_ok", True):
        bits.append(f"hue {r['hue_delta']:.3f}<0.06")
    if not r.get("diff", {}).get("ok", True):
        bits.append(f"diff ΔL {r['diff']['delta_l']:.3f}<0.025")
    if r.get("cvd", {}).get("warn"):
        bits.append(f"cvd {r['cvd']['min']:.3f}<0.045")
    return " · ".join(bits) if bits else "ok"


def main() -> int:
    args = sys.argv[1:]
    if "-h" in args or "--help" in args:
        print(t("AUDIT_USAGE"))
        return 0
    only = None
    if "--theme" in args:
        i = args.index("--theme")
        only = args[i + 1] if i + 1 < len(args) else None

    rows = load_all(only)
    if not rows:
        if "--brief" not in args:
            print(t("AUDIT_NONE"))
        return 1
    rows.sort(key=lambda r: (r["score"], r["name"]))

    if "--brief" in args:
        # 给 doctor / 脚本读的一行：平均分 未达标套数
        bad = sum(1 for r in rows if not r["ok"])
        avg = round(sum(r["score"] for r in rows) / len(rows))
        print(f"{avg} {bad} {len(rows)}")
        return 1 if (bad and "--gate" in args) else 0

    if "--json" in args:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
    else:
        print(t("AUDIT_HEAD"))
        print(f"  {'theme':<20}{'':>2}{'score':>5}  {'fg':>6}  {'dim':>6}"
              f"  {'sel':>5}  {'match':>5}  {'cur':>5}  {'hue':>5}  {'cvd':>5}  {'diff':>5}  {'surf':>5}  {'neu':>5}  {'syn':>5}  {'cli':>5}   detail")
        for r in rows:
            sel = r["selection"]["ratio"]
            match = r["match"]["fg_ratio"]
            cur = r["cursor"]
            syn = r.get("syntax", {}).get("min_contrast")
            surf = r.get("surfaces", {}).get("min_text")
            neu = r.get("neutral", {}).get("surface")
            print(f"  {r['name']:<20}{'':>2}{r['score']:>5}  {r['fg_contrast']:>6.2f}"
                  f"  {r['dim_contrast']:>6.2f}"
                  f"  {('—' if sel is None else f'{sel:.2f}'):>5}"
                  f"  {('—' if match is None else f'{match:.2f}'):>5}"
                  f"  {('—' if cur is None else f'{cur:.2f}'):>5}"
                  f"  {r['hue_delta']:>5.2f}"
                  f"  {r['cvd']['min']:>5.2f}"
                  f"  {r['diff']['delta_l']:>5.3f}"
                  f"  {('—' if surf is None else f'{surf:.2f}'):>5}"
                  f"  {('—' if neu is None else f'{neu:.2f}'):>5}"
                  f"  {('—' if syn is None else f'{syn:.2f}'):>5}"
                  f"  {r['cli_diff']:>5.2f}   {detail(r)}")
        bad = [r for r in rows if not r["ok"]]
        avg = round(sum(r["score"] for r in rows) / len(rows))
        print()
        print(t("AUDIT_PASS", len(rows)) if not bad else t("AUDIT_FAIL", len(bad)))
        print(t("AUDIT_SUM", avg, rows[0]["score"], rows[0]["name"]))

    if "--gate" in args and any(not r["ok"] for r in rows):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
