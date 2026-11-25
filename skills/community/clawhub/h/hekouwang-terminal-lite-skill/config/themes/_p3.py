#!/usr/bin/env python3
# ============================================================
# P3 广色域转换
#
# iTerm2 的颜色字典支持 "Color Space": "Display P3"；Ghostty 用
# window-colorspace = display-p3 解释主题里的 hex。这里的做法：
#   1. sRGB 色 → OKLab（保 L / 色相）
#   2. 彩度乘一个系数，二分回缩到 Display P3 色域内
#   3. 转成 P3 分量（iTerm2 字典或 Ghostty hex）
#
# 背景 / 前景 / 中性色不扩彩度，只做 sRGB → P3 的等价表示，避免整体偏色。
#
#   python3 _p3.py <profile.json>      # 原地把 iTerm2 Profile 转成 Display P3
#   python3 _p3.py --hex <rrggbb>      # 打印 P3 分量 hex（给 Ghostty 用）
# ============================================================
from __future__ import annotations

import json
import math
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from palettes import _audit as A  # noqa: E402

# sRGB linear → XYZ D65
SRGB_TO_XYZ = (
    (0.4124564, 0.3575761, 0.1804375),
    (0.2126729, 0.7151522, 0.0721750),
    (0.0193339, 0.1191920, 0.9503041),
)
# XYZ D65 → Display P3 linear
XYZ_TO_P3 = (
    (2.493496911941425, -0.9313836179191239, -0.40271078445071684),
    (-0.8294889695615747, 1.7626640603183463, 0.023624685841943577),
    (0.03584583024378447, -0.07617238926804182, 0.9568845240076872),
)

CHROMATIC = {
    "Cursor Color", "Link Color", "Underline Color", "Badge Color",
} | {f"Ansi {i} Color" for i in (1, 2, 3, 4, 5, 6, 9, 10, 11, 12, 13, 14)}


def _p3_linear(L: float, A_: float, B_: float):
    """OKLab → linear Display P3；越界返回 None。"""
    rgb = A._oklab_to_linear(L, A_, B_)
    xyz = [sum(SRGB_TO_XYZ[i][j] * rgb[j] for j in range(3)) for i in range(3)]
    p3 = [sum(XYZ_TO_P3[i][j] * xyz[j] for j in range(3)) for i in range(3)]
    if any(c < -1e-6 or c > 1 + 1e-6 for c in p3):
        return None
    return tuple(min(1.0, max(0.0, c)) for c in p3)


def _encode(c: float) -> float:
    return A._delinear(min(1.0, max(0.0, c)))


def p3_components(hex_color: str, factor: float = 1.0) -> tuple[float, float, float]:
    """sRGB hex → Display P3 分量（0–1）。彩度超出 P3 时二分回缩。"""
    L, A_, B_ = A.srgb_to_oklab(hex_color.lstrip("#"))
    C = math.hypot(A_, B_)
    h = math.atan2(B_, A_)
    if C < 1e-6 or factor == 1.0:
        out = _p3_linear(L, A_, B_)
        if out:
            return out
    lo, hi = 0.0, 1.0
    best = None
    for _ in range(28):
        mid = (lo + hi) / 2
        scale = mid * factor
        out = _p3_linear(L, C * scale * math.cos(h), C * scale * math.sin(h))
        if out:
            best = out
            lo = mid
        else:
            hi = mid
    if best is None:
        out = _p3_linear(L, A_, B_)
        return out or (0.0, 0.0, 0.0)
    return best


def p3_hex(hex_color: str, factor: float = 1.0) -> str:
    r, g, b = p3_components(hex_color, factor)
    return "".join(f"{round(_encode(c) * 255):02x}" for c in (r, g, b))


def _color_hex(c: dict) -> str:
    return "".join(
        f"{round(c[k] * 255):02x}"
        for k in ("Red Component", "Green Component", "Blue Component")
    )


def _convert_dict(c: dict, factor: float) -> None:
    if c.get("Color Space") == "Display P3":
        return
    rgb = p3_components(_color_hex(c), factor)
    c["Red Component"], c["Green Component"], c["Blue Component"] = (
        _encode(v) for v in rgb
    )
    c["Color Space"] = "Display P3"


def _walk_color(obj, factor: float) -> None:
    """递归转换嵌套里的颜色字典（Status Bar Layout 这类）。"""
    if isinstance(obj, dict):
        if "Red Component" in obj:
            _convert_dict(obj, factor)
            return
        for val in obj.values():
            _walk_color(val, factor)
    elif isinstance(obj, list):
        for val in obj:
            _walk_color(val, factor)


def convert_profile(path: Path, factor: float = 1.15) -> bool:
    data = json.loads(path.read_text(encoding="utf-8"))
    changed = False
    for prof in data.get("Profiles", []):
        for key, val in prof.items():
            if not isinstance(val, dict) or "Red Component" not in val:
                if isinstance(val, (dict, list)):
                    before = json.dumps(val, sort_keys=True)
                    _walk_color(val, 1.0)
                    changed = changed or before != json.dumps(val, sort_keys=True)
                continue
            f = factor if key in CHROMATIC else 1.0
            before = val.get("Color Space")
            _convert_dict(val, f)
            changed = changed or before != "Display P3"
    if changed:
        path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    return changed


def main() -> int:
    args = sys.argv[1:]
    if not args:
        print("usage: _p3.py <profile.json> | --hex <rrggbb> [factor]", file=sys.stderr)
        return 2
    if args[0] == "--hex":
        if len(args) < 2:
            return 2
        factor = float(args[2]) if len(args) > 2 else 1.15
        print(p3_hex(args[1], factor))
        return 0
    factor = float(os.environ.get("HKW_P3_FACTOR", "1.15"))
    path = Path(args[0])
    convert_profile(path, factor)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
