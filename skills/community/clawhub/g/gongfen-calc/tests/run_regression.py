"""回归入口：跑完 tests/ 下全部 fixture + 两份 --force-points 用例，打印退出码。

用法（在项目根目录）：
    python tests/run_regression.py [真实表路径]
不传真实表则只跑 fixture。退出码非 0 表示有 fixture 意外失败
（fixture_noheader.xlsx 预期 exit 1 —— 表头定位失败的故意失败用例）。
"""
from __future__ import annotations

import sys
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import run as RUN  # noqa: E402

EXPECT_FAIL = {"fixture_noheader.xlsx"}   # 故意失败用例


def run_one(path: Path, out_dir: Path, extra=None) -> int:
    argv = [str(path), "--out-dir", str(out_dir)] + (extra or [])
    try:
        code = RUN.main(argv)
    except SystemExit as e:
        code = e.code
    except Exception:
        traceback.print_exc()
        code = 9
    print(f"[exit {code}] {path.name} {' '.join(extra or [])}")
    return code


def main(argv=None) -> int:
    out_dir = ROOT / "tests" / "out"
    out_dir.mkdir(parents=True, exist_ok=True)
    bad = []

    fixtures = sorted((ROOT / "tests").glob("fixture_*.xlsx")) + \
        sorted((ROOT / "tests").glob("fixture_*.csv"))
    for f in fixtures:
        code = run_one(f, out_dir)
        want = 1 if f.name in EXPECT_FAIL else 0
        if code != want:
            bad.append(f.name)

    for name in ("fixture_no_dim.xlsx", "fixture_only_hours.xlsx"):
        if run_one(ROOT / "tests" / name, out_dir, ["--force-points"]) != 0:
            bad.append(name + " --force-points")

    if len(sys.argv) > 1:
        real = Path(sys.argv[1])
        if run_one(real, ROOT / "out") not in (0, 1):
            bad.append(real.name)

    print("\n回归结果：" + ("全部符合预期" if not bad else "异常 → " + "、".join(bad)))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
