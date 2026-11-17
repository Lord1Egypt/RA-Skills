#!/usr/bin/env python3
"""rla_ledger.py — 从 ledger.yaml + indicators.yaml 生成账本（v3.6.0）

这是 report-ledger 台账能力的接管者：指标定义（含 SQL）在项目里，
本脚本按定义跑一遍、把结果写成 report-audit 的账本（`report-ledger/1.0`）。

与 rla_collect.py 的分工（两条路，产出同一本账本）：
    rla_collect  从「录像 trace」生成账本  ← 有脚本跑数的项目
    rla_ledger   从「指标定义」生成账本    ← 有模板/定义的项目（本脚本）

用法：
    python3 scripts/rla_ledger.py                        # 读 ./ledger.yaml → ./ledger.json
    python3 scripts/rla_ledger.py --config x.yaml --out y.json
    python3 scripts/rla_ledger.py --check                # 只校验（指纹/invariants），不重算
    python3 scripts/rla_ledger.py --list                 # 列出指标 id 与当前值

设计上的三条硬规矩（都是 report-ledger 那边踩出来的）：
  1. **先展开 {{pool}}，再替换 {{cap}}** —— 池条件里可能自带 {{cap}}
  2. **任何一条指标算不出来就整体失败**（退出码 2），不许静默跳过
  3. **替换后仍残留 {{...}} 直接报错**，绝不带着占位符去查库（会静默出错数）
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL_ROOT = HERE.parent
sys.path.insert(0, str(HERE))

try:
    import yaml
except ImportError:  # pragma: no cover
    print("❌ 需要 pyyaml：python3 -m pip install pyyaml", file=sys.stderr)
    raise SystemExit(2)


def now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def resolve_path(p: str, base: Path) -> Path:
    """相对路径按「配置文件所在目录」解析；{skills} 展开成技能根。"""
    s = str(p).replace("{skills}", str(SKILL_ROOT))
    q = Path(s)
    return q if q.is_absolute() else (base / q)


# ------------------------------------------------------------------ 配置加载
def load_yaml(path: Path) -> dict:
    if not path.exists():
        raise SystemExit(f"❌ 配置不存在：{path}")
    with open(path, encoding="utf-8-sig") as f:
        d = yaml.safe_load(f) or {}
    if not isinstance(d, dict):
        raise SystemExit(f"❌ {path.name} 顶层必须是映射")
    return d


def load_catalog(path: Path) -> tuple[list[dict], list[dict]]:
    """返回 (indicators, invariants)。"""
    d = load_yaml(path)
    items = d.get("indicators") or d.get("metrics") or []
    if not isinstance(items, list) or not items:
        raise SystemExit(f"❌ {path.name} 里没有 indicators（或为空）")
    bad = [i.get("id") for i in items
           if not i.get("id") or not (i.get("sql") or i.get("col")
                                      or i.get("num") or i.get("expr"))]
    if bad:
        raise SystemExit(f"❌ 这些指标既没有 id，也没有 sql / col / num 任一取值方式：{bad[:5]}")
    dup = {i["id"] for i in items if [x["id"] for x in items].count(i["id"]) > 1}
    if dup:
        raise SystemExit(f"❌ 指标 id 重复：{sorted(dup)}")
    return items, (d.get("invariants") or [])


# ------------------------------------------------------------------ 占位符
def expand_sql(sql: str, pool_where: str, cap: str, iid: str) -> str:
    """{{pool}} → pool.where；{{cap}} → meta.cap。顺序不能反（池条件可能自带 {{cap}}）。"""
    s = str(sql)
    if "{{pool}}" in s:
        if not pool_where:
            raise SystemExit(f"❌ {iid} 的 SQL 用了 {{{{pool}}}}，但 ledger.yaml 没定义 pool.where")
        s = s.replace("{{pool}}", pool_where)
    s = s.replace("{{cap}}", str(cap))
    left = [t for t in ("{{pool}}", "{{cap}}") if t in s]
    if left:
        raise SystemExit(f"❌ {iid} 替换后仍残留 {left}（绝不带着占位符去查库）")
    return s


# ------------------------------------------------------------------ 连接
def build_conn(source: dict, base: Path):
    """按 source.adapter 建连接。返回 (conn, meta)。"""
    import rla_collect as RC

    ad = str(source.get("adapter") or "duckdb").strip()

    if ad == "duckdb":
        cfg = source.get("duckdb") or {}
        p = resolve_path(cfg.get("path") or "", base)
        if not p.exists():
            raise SystemExit(f"❌ source.duckdb.path 不存在：{p}")
        conn, meta = RC.build_source({"": str(p)})
        return conn, meta

    if ad in ("command", "gateway"):
        cfg = source.get(ad) or {}
        argv = cfg.get("argv")
        if ad == "gateway":
            gw = cfg.get("gateway") or ""
            if not gw:
                raise SystemExit("❌ source.gateway.gateway 为空")
            argv = [sys.executable, str(resolve_path(gw, base))]
        if not isinstance(argv, list) or not argv:
            raise SystemExit(f"❌ source.{ad}.argv 必须是非空数组")
        argv = [str(resolve_path(a, base)) if a.startswith("scripts/") or "{" in str(a) else str(a)
                for a in argv]
        timeout = int(cfg.get("timeout") or 300)
        return RC.CommandConn(argv, timeout=timeout), {"id": "src1", "type": ad, "argv": argv}

    if ad == "module":
        cfg = source.get("module") or {}
        path = resolve_path(cfg.get("path") or "", base)
        fn = str(cfg.get("func") or "query")
        if not path.exists():
            raise SystemExit(f"❌ source.module.path 不存在：{path}")
        import importlib.util
        spec = importlib.util.spec_from_file_location("_rla_src", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        if not hasattr(mod, fn):
            raise SystemExit(f"❌ 模块 {path.name} 里没有函数 {fn}()")
        return _ModuleConn(getattr(mod, fn)), {"id": "src1", "type": "module", "path": str(path)}

    raise SystemExit(f"❌ 不认识的 source.adapter：{ad}（只支持 duckdb/command/gateway/module）")


class _ModuleConn:
    """把用户的 query(sql) -> list[dict] 包成 audit 认的连接。"""

    def __init__(self, fn):
        self.fn = fn

    def execute(self, sql):
        rows = self.fn(sql) or []
        return rows


# ------------------------------------------------------------------ 取值
PCT_UNITS = {"pct", "%", "％", "百分比", "percent"}


def to_value(raw, unit: str, is_ratio: bool = False) -> float:
    """按单位规则把原始比值/数值变成账本里的 value（与 report-ledger 的 fmt_value 同口径）。

    pct / % / 百分比：SQL 给的是 0~1 比值 → ×100，保留 1 位
    pct1：已经是百分数 → 原样
    元 / 金额：保留 2 位
    其他：最多 4 位
    """
    v = float(raw)
    u = str(unit or "").strip()
    ul = u.lower()
    # is_ratio=True 表示这个值**一定是比值**（num/den 或 ratio:true 算出来的）。
    # 比值不可能"已经是百分数"，所以 pct1 也要 ×100 —— 这条是与星仔那套
    # `round(n*100/d, 1)` 对齐的，避免同一个 pct1 在两种实现里差 100 倍。
    if is_ratio and (ul in PCT_UNITS or ul == "pct1"):
        return round(v * 100, 1)
    if ul == "pct1":
        return round(v, 1)
    if ul in PCT_UNITS:
        return round(v * 100, 1)
    if u in ("元", "金额"):
        return round(v, 2)
    return round(v, 4)


def get_one_sql(cfg: dict, base: Path) -> str | None:
    """取「一条 SQL 出所有列」的那条 SQL（col 模式用）。

    三种来源，按配置选一种：
        source.one_sql.module: scripts/wl_defs.py   + func: all_indicators_sql
        source.one_sql.file:   sql/all.sql
        source.one_sql.inline: "SELECT ..."
    """
    spec = ((cfg.get("source") or {}).get("one_sql")) or {}
    if not spec:
        return None
    if spec.get("inline"):
        return str(spec["inline"])
    if spec.get("file"):
        p = resolve_path(spec["file"], base)
        if not p.exists():
            raise SystemExit(f"❌ source.one_sql.file 不存在：{p}")
        return p.read_text(encoding="utf-8")
    if spec.get("module"):
        path = resolve_path(spec["module"], base)
        fn = str(spec.get("func") or "all_indicators_sql")
        if not path.exists():
            raise SystemExit(f"❌ source.one_sql.module 不存在：{path}")
        import importlib.util
        spec_obj = importlib.util.spec_from_file_location("_rla_onesql", path)
        mod = importlib.util.module_from_spec(spec_obj)
        # 模块里常会 import 同目录其它模块，把它的目录也放进 sys.path
        sys.path.insert(0, str(path.parent))
        try:
            spec_obj.loader.exec_module(mod)
        finally:
            sys.path.pop(0)
        if not hasattr(mod, fn):
            raise SystemExit(f"❌ 模块 {path.name} 里没有 {fn}()")
        return str(getattr(mod, fn)())
    raise SystemExit("❌ source.one_sql 必须给 module / file / inline 之一")


def fetch_one_row(conn, sql: str) -> dict:
    """跑一次大 SQL，返回第一行的 {列名: 值}。"""
    raw = conn.execute(sql)
    try:
        rows = raw.fetchall() if hasattr(raw, "fetchall") else list(raw)
    except Exception:  # noqa: BLE001
        rows = []
    if not rows:
        raise SystemExit("❌ source.one_sql 执行后没有返回行")
    row0 = rows[0]
    if isinstance(row0, dict):
        return {str(k): v for k, v in row0.items()}
    cols = [d[0] for d in (getattr(raw, "description", None) or [])]
    return dict(zip(cols or [f"c{i}" for i in range(len(row0))], row0))


def pick_cell(row: dict, iid: str):
    """从一行结果里取数值。ratio 时取 num/den 两列。"""
    low = {str(k).lower(): v for k, v in row.items()}
    if "num" in low and "den" in low:
        num, den = float(low["num"] or 0), float(low["den"] or 0)
        if not den:
            raise SystemExit(f"❌ {iid} 分母为 0")
        return num / den, num, den
    if not row:
        raise SystemExit(f"❌ {iid} SQL 无返回行")
    first = list(row.values())[0]
    return float(first), float(first), None


# ------------------------------------------------------------------ invariants
OPS = {
    "<=": lambda a, b: a <= b,
    "<": lambda a, b: a < b,
    ">=": lambda a, b: a >= b,
    ">": lambda a, b: a > b,
    "==": lambda a, b: a == b,
    "!=": lambda a, b: a != b,
}


def check_invariants(vals: dict, invariants: list) -> list[tuple[str, str]]:
    """返回违规列表 [(name, detail)]。违反属 FAIL 级（数据/口径本身错了）。"""
    bad = []
    for inv in invariants or []:
        left, op, right = inv.get("left"), str(inv.get("op") or "").strip(), inv.get("right")
        name = inv.get("name") or f"{left} {op} {right}"
        if op not in OPS:
            bad.append((name, f"不认识的操作符 {op!r}（只支持 {'/'.join(OPS)}）"))
            continue
        if left not in vals:
            bad.append((name, f"左边指标 {left} 不在本次计算范围内"))
            continue
        a = float(vals[left])
        if isinstance(right, str) and right in vals:
            b = float(vals[right])
        else:
            try:
                b = float(right)
            except (TypeError, ValueError):
                bad.append((name, f"右边 {right!r} 既不是数字也不是已算指标"))
                continue
        if not OPS[op](a, b):
            bad.append((name, f"{left}={a:g} 不满足 {op} {b:g}"))
    return bad


# ------------------------------------------------------------------ 主流程
def main() -> int:
    ap = argparse.ArgumentParser(description="从 ledger.yaml + indicators.yaml 生成账本")
    ap.add_argument("--config", default="ledger.yaml", help="配置文件（默认项目根 ledger.yaml）")
    ap.add_argument("--out", default=None, help="账本输出路径（默认与配置同目录 ledger.json）")
    ap.add_argument("--check", action="store_true", help="只校验指纹与不变式，不重算")
    ap.add_argument("--list", action="store_true", help="列出指标 id 与当前值（不写字）")
    args = ap.parse_args()

    cfg_path = Path(args.config).resolve()
    base = cfg_path.parent
    cfg = load_yaml(cfg_path)

    meta = cfg.get("meta") or {}
    cap = str(meta.get("cap") or "").strip()
    if not cap:
        raise SystemExit("❌ ledger.yaml 缺 meta.cap（数据截止日）。"
                         "没有 cap，数据和口径都可能随时长大")
    pool_where = str((cfg.get("pool") or {}).get("where") or "").strip()

    cat_rel = cfg.get("catalog") or "metrics/indicators.yaml"
    cat_path = resolve_path(cat_rel, base)
    items, invariants = load_catalog(cat_path)

    # 数据指纹（台账"出生证明"）：数据变了没重算，闸门 1 要能发现
    data_fp = None
    fp_cfg = (cfg.get("source") or {}).get("fingerprint") or {}
    fp_files = [resolve_path(f, base) for f in (fp_cfg.get("files") or [])]
    if fp_files:
        import rla_collect as RC
        data_fp = RC.fingerprint_files([str(p) for p in fp_files if Path(p).exists()])
    missing_fp = [str(p) for p in fp_files if not Path(p).exists()]

    print(f"[rla_ledger] 配置 {cfg_path.name}｜指标 {len(items)} 条｜cap {cap}")
    if pool_where:
        print(f"[rla_ledger] 池条件：{pool_where}")
    if data_fp:
        print(f"[rla_ledger] 数据指纹：{str(data_fp)[:16]}…")
    elif fp_files:
        print(f"[rla_ledger] ⚠️ 指纹文件缺失：{missing_fp[:3]}（闸门 1 将无法校验新鲜度）")

    if args.check:
        print("[rla_ledger] --check：只做了配置与指纹检查，未重算")
        return 0

    conn, src_meta = build_conn(cfg.get("source") or {}, base)

    numbers, vals, fails = [], {}, []
    facts: dict[str, tuple] = {}      # id -> (原始值, 分子, 分母)，供 num/den 二次计算

    # 「一条 SQL 出所有列」只跑一次（col 模式）
    one_row = None
    if any("col" in it for it in items):
        one_sql = get_one_sql(cfg, base)
        if not one_sql:
            # 配置缺失属"未就绪"（退出码 2），不是脚本崩溃
            print("❌ 未就绪：有指标用 col 取值，但 ledger.yaml 没配 source.one_sql"
                  "（module / file / inline 三选一）", file=sys.stderr)
            return 2
        one_row = fetch_one_row(conn, expand_sql(one_sql, pool_where, cap, "source.one_sql"))
        print(f"[rla_ledger] 大 SQL 已执行：{len(one_row)} 列")

    # ── 第一轮：sql（每条一句）或 col（从大 SQL 取列）
    # 只有 num/den 的指标跳过这里 —— 它们依赖第一轮的结果，留给第二轮
    for it in items:
        if not (it.get("sql") or it.get("col")):
            continue          # 只有 expr / num 的，留给第二轮
        iid = str(it["id"])
        unit = it.get("unit")
        try:
            if it.get("sql"):
                sql = expand_sql(it["sql"], pool_where, cap, iid)
                raw = conn.execute(sql)
                try:
                    rows = raw.fetchall() if hasattr(raw, "fetchall") else list(raw)
                except Exception:  # noqa: BLE001
                    rows = []
                if not rows:
                    fails.append(f"{iid}：SQL 无返回行")
                    continue
                row0 = rows[0]
                if not isinstance(row0, dict):
                    cols = [d[0] for d in (getattr(raw, "description", None) or [])]
                    row0 = dict(zip(cols or [f"c{i}" for i in range(len(row0))], row0))
                ratio, num, den = pick_cell(row0, iid)
                # ratio:true（SQL 返回 num/den 两列）→ 一定是比值
                is_ratio = den is not None
                val = to_value(ratio, unit, is_ratio=is_ratio)
            else:
                col = str(it.get("col"))
                if one_row is None:
                    fails.append(f"{iid}：用 col 取值但大 SQL 没跑起来")
                    continue
                if col not in one_row:
                    fails.append(f"{iid}：列 {col!r} 不在大 SQL 的结果里"
                                 f"（有 {len(one_row)} 列）")
                    continue
                num, den = one_row[col], None
                val = to_value(num, unit, is_ratio=False)
        except SystemExit as e:
            fails.append(str(e).replace("❌ ", ""))
            continue
        except Exception as e:  # noqa: BLE001
            fails.append(f"{iid}：{type(e).__name__}: {e}")
            continue
        vals[iid] = val
        facts[iid] = (num, den)

    # ── 第二轮：expr（指标之间加减，如「P6 - 无货场景」）
    # 复用 rla_audit 的 AST 白名单求值器：只认数字、引用、+ - * / 和括号，不用 eval
    import rla_audit as _AU
    for it in items:
        iid = str(it["id"])
        if not it.get("expr"):
            continue
        try:
            val = _AU._eval_expr(str(it["expr"]), {k: float(v) for k, v in vals.items()})
        except Exception as e:  # noqa: BLE001
            fails.append(f"{iid}：表达式 {it['expr']!r} 求值失败 —— {type(e).__name__}: {e}")
            continue
        vals[iid] = to_value(val, it.get("unit"), is_ratio=False)
        facts[iid] = (val, None)

    # ── 第三轮：num/den（两条指标相除）。结果一定是比值 → is_ratio=True
    for it in items:
        iid = str(it["id"])
        if not it.get("num"):
            continue
        nid, did = str(it["num"]), str(it.get("den"))
        if nid not in vals or did not in vals:
            fails.append(f"{iid}：依赖的 {nid} / {did} 未被解析")
            continue
        n, d = float(vals[nid]), float(vals[did])
        if not d:
            fails.append(f"{iid}：分母 {did}=0")
            continue
        val = to_value(n / d, it.get("unit"), is_ratio=True)
        vals[iid] = val
        facts[iid] = (n, d)

    # ── 组装账本条目（保持 items 原顺序）
    for it in items:
        iid = str(it["id"])
        if iid not in vals:
            continue
        num, den = facts.get(iid, (None, None))
        rec = {
            "id": iid,
            "label": it.get("name") or it.get("label") or iid,
            "value": vals[iid],
            "unit": it.get("unit") or "",
            "caliber": it.get("caliber") or "",
            "verifiable": bool(it.get("sql")),
            "role": it.get("role") or "indicator",
            "origin": (f"rla_ledger 按 {cat_path.name} 计算（cap {cap}）"),
        }
        if it.get("sql"):
            rec["sql"] = expand_sql(it["sql"], pool_where, cap, iid)
        elif it.get("col"):
            rec["col"] = it["col"]
            rec["origin"] = f"rla_ledger：从 source.one_sql 取列「{it['col']}」（cap {cap}）"
        elif it.get("num"):
            rec["origin"] = f"rla_ledger：{it['num']} ÷ {it.get('den')}（cap {cap}）"
        elif it.get("expr"):
            rec["expr"] = str(it["expr"])
            rec["origin"] = f"rla_ledger：表达式 {it['expr']}（cap {cap}）"
        if it.get("confidence"):
            rec["confidence"] = it["confidence"]
        if den is not None:
            rec["numerator"] = num
            rec["denominator"] = den
        numbers.append(rec)

    if fails:
        print("❌ 未就绪：以下指标没算出来（不许静默跳过）", file=sys.stderr)
        for f in fails:
            print("   " + f, file=sys.stderr)
        return 2

    bad_inv = check_invariants(vals, invariants)
    if bad_inv:
        print(f"❌ 不变式未通过 {len(bad_inv)} 条（属 FAIL 级：数据或口径本身有问题）", file=sys.stderr)
        for name, detail in bad_inv:
            print(f"   {name}：{detail}", file=sys.stderr)
        return 1

    report = {
        "name": meta.get("name") or cfg_path.stem,
        "files": [Path(f).name for f in (cfg.get("deliverables") or [])] or [],
        "data_as_of": cap,
        "generated_at": now_iso(),
        "agent": "rla_ledger",
    }
    if data_fp:
        report["data_fingerprint"] = data_fp

    ledger = {
        "schema": "report-ledger/1.0",
        "report": report,
        "sources": [src_meta] if src_meta else [],
        "numbers": numbers,
    }

    out = Path(args.out) if args.out else (base / "ledger.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(ledger, ensure_ascii=False, indent=2), encoding="utf-8")

    if args.list:
        for r in numbers:
            print(f"  {r['id']:<28}{r['value']:>16,.2f}  {r.get('unit', '')}")
    print(f"✅ 账本已生成：{out}｜{len(numbers)} 个指标"
          + (f"｜不变式 {len(invariants)} 条全过" if invariants else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
