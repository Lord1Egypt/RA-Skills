#!/usr/bin/env python
"""
batch_roster.py — 按花名册批量生成全班卷子（每个学生一份）。

输入：
    --roster PATH    学生花名册，CSV 或 JSON
                     CSV 必须含 `name` 列；JSON 是 list[{"name":"..."}]
                     name 可填空（空白姓名框）或具体姓名
    --level L1-L4    等级
    --count N        题量；0=按等级默认
    --seed N         全部学生使用同一 seed → 全班同一套题，便于横向比较
    --score          开启评分栏
    --no-name        姓名栏全部空白（推荐，老师批改后再写名字）
    --out-dir DIR    输出目录（默认 ./students/<日期>-<等级>-<seed>/）
    --topics T1,T2   可选，限定题型
    --csv-students   把花名册当成 CSV（自动识别 .csv 时也适用）

输出：
    DIR/<序号>_<safe_name>.html
    DIR/<序号>_<safe_name>_答案.json      （带 _blankname 后缀若 --no-name）
    DIR/_summary.json                     （本批任务的 manifest：seed、level、count、生成时间戳等）

典型用法：
    python batch_roster.py --roster class.csv --level L2 --seed 7 --no-name --score
"""
from __future__ import annotations
import argparse
import csv
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path


HERE = Path(__file__).resolve().parent
GENERATOR = HERE / "generate_worksheet.py"
PYTHON = sys.executable


def load_roster(path: str) -> list[dict]:
    p = Path(path)
    if not p.exists():
        raise SystemExit(f"找不到花名册文件: {path}")
    if p.suffix.lower() == ".csv":
        out = []
        with p.open("r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            if "name" not in reader.fieldnames:
                raise SystemExit("CSV 必须包含 `name` 列（首行表头）")
            for row in reader:
                out.append({
                    "name": (row.get("name") or "").strip(),
                    "id": (row.get("id") or row.get("student_id") or "").strip(),
                })
        return out
    # json
    data = json.loads(p.read_text(encoding="utf-8"))
    if isinstance(data, list):
        return [{"name": str(x.get("name", "") if isinstance(x, dict) else x), "id": ""} for x in data]
    raise SystemExit("JSON 必须是 list[object] 或 list[string]")


def safe_name(s: str, idx: int) -> str:
    """将学生姓名清洗为安全文件名。空名 → 学号无名。"""
    base = s.strip() if s else ""
    safe = re.sub(r"[\\/:*?\"<>|\s]", "_", base) if base else ""
    return f"{idx:02d}_{safe or 'unnamed'}"


def main() -> None:
    ap = argparse.ArgumentParser(description="批量生成全班卷子")
    ap.add_argument("--roster", required=True, help="花名册 CSV/JSON")
    ap.add_argument("--level", default="L2", help="等级 L1-L4")
    ap.add_argument("--count", type=int, default=0, help="题量；0=按等级默认")
    ap.add_argument("--seed", type=int, default=None, help="统一种子；不指定则随机")
    ap.add_argument("--topics", default="", help="限定题型，逗号分隔")
    ap.add_argument("--score", action="store_true", help="开启评分栏")
    ap.add_argument("--no-name", action="store_true", help="姓名栏全部空白（建议开启）")
    ap.add_argument("--lang", default="zh", choices=["zh", "en"])
    ap.add_argument("--out-dir", default="", help="输出目录；缺省 ./students/<时间>-<等级>-<seed>/")
    ap.add_argument("--columns", type=int, default=2, choices=[1, 2, 3])
    args = ap.parse_args()

    students = load_roster(args.roster)
    if not students:
        raise SystemExit("花名册为空")

    # 自动选种子以保证可复现
    import random as _r
    seed = args.seed if args.seed is not None else _r.randint(1, 999999)

    # 输出目录
    if args.out_dir:
        out_dir = Path(args.out_dir)
    else:
        stamp = time.strftime("%Y%m%d-%H%M%S")
        out_dir = Path("students") / f"{stamp}-{args.level}-seed{seed}"
    out_dir.mkdir(parents=True, exist_ok=True)

    summary = {
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "level": args.level,
        "count_arg": args.count,
        "seed": seed,
        "lang": args.lang,
        "score": args.score,
        "no_name": args.no_name,
        "topics_filter": args.topics,
        "out_dir": str(out_dir),
        "students": [],
    }

    print(f"=== 班级卷子批量生成：{len(students)} 人，seed={seed} ===")
    print(f"=== 输出目录: {out_dir} ===")
    for i, s in enumerate(students, 1):
        safe = safe_name(s["name"], i)
        html_path = out_dir / f"{safe}.html"
        json_path = out_dir / f"{safe}_答案.json"

        cmd = [
            PYTHON, str(GENERATOR),
            "--level", args.level,
            "--seed", str(seed),
            "--lang", args.lang,
            "--columns", str(args.columns),
            "--out", str(html_path),
            "--json", str(json_path),
        ]
        if args.count > 0:
            cmd += ["--count", str(args.count)]
        if args.topics:
            cmd += ["--topics", args.topics]
        if args.score:
            cmd.append("--score")
        # 姓名处理：--no-name 时完全不传 --name；否则传真实姓名
        if not args.no_name and s["name"]:
            cmd += ["--name", s["name"]]

        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0:
            print(f"  ✗ #{i} {s['name'] or '(unnamed)'} 生成失败: {r.stderr.strip()}")
            summary["students"].append({"index": i, "name": s["name"], "status": "failed", "error": r.stderr.strip()})
            continue
        size = html_path.stat().st_size if html_path.exists() else 0
        print(f"  ✓ #{i:02d} {s['name'] or '(blank)'}  →  {html_path.name}  ({size} bytes)")
        summary["students"].append({
            "index": i,
            "name": s["name"],
            "student_id": s["id"],
            "html": str(html_path),
            "json": str(json_path),
            "status": "ok",
        })

    (out_dir / "_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    (out_dir / "_summary.csv").write_text(
        "\n".join(["index,name,status,html"] + [
            f"{x['index']},{x['name']},{x['status']},{x['html']}" for x in summary["students"]
        ]), encoding="utf-8-sig")

    ok = sum(1 for s in summary["students"] if s["status"] == "ok")
    print(f"\n=== 完成 {ok}/{len(summary['students'])}；seed={seed}；seed 可复现整套班级卷子 ===")


if __name__ == "__main__":
    main()
