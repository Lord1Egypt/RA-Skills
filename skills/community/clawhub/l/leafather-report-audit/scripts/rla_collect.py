#!/usr/bin/env python3
"""rla_collect.py — 把 SQL 录像变成账本（每个数字带出生证明）。

它做的事：
    读 .trace.jsonl（rla_track 录的）→ 去重 → 逐条复算 → 展开成账本 numbers

用法：
    python3 scripts/rla_collect.py --trace run.trace.jsonl --ledger ledger.json \
        --mount "data=/path/your.parquet" \
        --report-name "减肥场景报告" --data-as-of 2026-10-19

    # 不复算（只把 SQL 记进账本，值标记为未验证）
    python3 scripts/rla_collect.py --trace run.trace.jsonl --ledger l.json --no-recompute

设计要点：
    * **一条 SQL 出多列 → 展开成多个数字**（兼容"一条大 SQL 算几百个指标"的老做法）
    * 复算失败 = 退出码 2（未就绪），绝不"跳过即通过"
    * 只认 SELECT / WITH，其它语句只记不账
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shlex
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

READ_ONLY_RE = re.compile(r"^\s*(select|with)\b", re.I)
HARMLESS_RE = re.compile(r"^\s*(create\s+(or\s+replace\s+)?(temp\s+)?view|set\s|pragma\s|explain\s|describe\s)", re.I)


def now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def load_trace(path: Path, allow_missing: bool = False) -> list[dict]:
    if not path.exists():
        if allow_missing:
            # 纯 pandas / 纯 Python 项目：没有 SQL 可录，但有 rla_note 登记的数字。
            # 这时 trace 不存在是正常的，不该当失败。
            return []
        raise SystemExit(f"❌ trace 文件不存在：{path}")
    out, seen = [], set()
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue
        sql = (rec.get("sql") or "").strip()
        if not sql or sql in seen:
            continue
        seen.add(sql)
        rec["sql"] = sql
        out.append(rec)
    return out


def is_queryable(sql: str) -> bool:
    return bool(READ_ONLY_RE.match(sql)) and "?" not in sql


def fingerprint_files(paths: list[str]) -> str:
    h = hashlib.sha256()
    for p in paths:
        fp = Path(p)
        if not fp.exists():
            continue
        size = fp.stat().st_size
        with fp.open("rb") as f:
            h.update(f.read(4 * 1024 * 1024))
            if size > 8 * 1024 * 1024:
                f.seek(-4 * 1024 * 1024, 2)
                h.update(f.read())
        h.update(str(size).encode())
    return h.hexdigest()[:16]



# ---------------------------------------------------------------- 通用取数适配器
class _Cur:
    """模拟 duckdb cursor 的最小接口（description / fetchone / fetchall）。"""
    def __init__(self, cols, rows):
        self.description = [(c,) for c in cols]
        self._rows = rows

    def fetchone(self):
        return self._rows[0] if self._rows else None

    def fetchall(self):
        return self._rows


def _norm_rows(rows: list[dict]) -> _Cur:
    if not rows:
        return _Cur([], [])
    cols = list(rows[0].keys())
    return _Cur(cols, [[r.get(c) for c in cols] for r in rows])


def _num_or_str(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return v


def split_command(cmd: str, windows: bool | None = None) -> list[str]:
    """把用户给的命令行字符串拆成 argv。

    ⚠️ Windows 上必须 posix=False（2026-10-26 WorkBuddy 实机验收报的必修 bug）：
        shlex 的 posix 模式把反斜杠当转义符，C:\\Users\\x 会被啃成 C:Usersx
        （\\U \\A \\L \\T 全被吃掉）→ 路径彻底失效 → 所有 --command 复算静默全废。
        而"复算失败"会让所有用例都判 FAIL，恰好等于"期望被拦"，于是假阳性通过。
    posix=False 时引号会留在 token 里，所以要剥掉（兼容带空格的路径写法）。

    windows 参数仅供测试显式指定（None = 跟随当前系统）。
    """
    is_win = (os.name == "nt") if windows is None else windows
    if is_win:
        return [tok.strip('"') for tok in shlex.split(cmd, posix=False)]
    return shlex.split(cmd)


class CommandConn:
    """--command：SQL 从 stdin 进，CSV 从 stdout 出。

    这是**通用接法**：MySQL / PG / SQL Server / HTTP API 都行，
    只要写一个把 SQL 变成 CSV 的脚本。技能不关心背后是什么库。
    """
    def __init__(self, argv: list[str], timeout: int = 300):
        self.argv, self.timeout = argv, timeout

    def execute(self, sql):
        import csv as _csv
        import io as _io
        p = subprocess.run(self.argv, input=str(sql), capture_output=True,
                           text=True, timeout=self.timeout)
        if p.returncode != 0:
            raise RuntimeError(f"取数命令退出码 {p.returncode}：{p.stderr[-300:]}")
        rows = list(_csv.DictReader(_io.StringIO(p.stdout)))
        return _norm_rows(rows)


class GatewayConn(CommandConn):
    """--gateway：调 --sql / --out 协议的网关脚本（某 agent那套 xingbao_query.py 就是）。"""
    def __init__(self, script: str, timeout: int = 300):
        self.script, self.timeout = script, timeout

    def execute(self, sql):
        import csv as _csv
        import tempfile
        fd, out = tempfile.mkstemp(suffix=".csv")
        os.close(fd)
        try:
            p = subprocess.run([sys.executable, self.script, "--sql", str(sql),
                                "--out", out, "--limit", "100000",
                                "--timeout", str(self.timeout)],
                               capture_output=True, text=True)
            if p.returncode != 0:
                raise RuntimeError(f"网关退出码 {p.returncode}：{p.stderr[-300:]}")
            with open(out, encoding="utf-8-sig") as f:
                rows = list(_csv.DictReader(f))
            return _norm_rows(rows)
        finally:
            try:
                os.unlink(out)
            except OSError:
                pass


def build_source(mounts: dict[str, str]):
    """返回 (conn, source_meta)。

    支持两种挂法（2026-10-25 加第二种，某客户场景）：
      --mount "data=/path/xx.parquet"   把文件挂成一个叫 data 的视图（星宝）
      --mount "=/path/xx.duckdb"        视图名留空 = 直接把库当主库打开（某客户）
                                        这样 SQL 里可以直接写表名 raw_shipment_detail
    """
    import deps_check as DC
    duckdb = DC.duckdb_or_hint()      # 缺 duckdb / DLL 被拦时给可操作指引，而不是裸 traceback

    # 视图名留空 → 用它当主库，而不是 ATTACH 进来（否则 SQL 得写 data.表名）
    # 注意：必须用副本，不能 pop 调用方的字典（否则上层会误判"未挂载"→ 谎报未复算）
    mounts = dict(mounts)
    primary = mounts.pop("", None) if "" in mounts else None
    if primary is None:
        for k in list(mounts):
            if k.strip() == "":
                primary = mounts.pop(k)
                break

    if primary:
        p = Path(primary)
        if not p.exists():
            raise SystemExit(f"❌ 主库文件不存在：{primary}")
        conn = duckdb.connect(str(p), read_only=True)
        meta = {"id": "src1", "type": "duckdb", "primary": str(p),
                "fingerprint": fingerprint_files([str(p)])}
        return conn, meta

    conn = duckdb.connect(":memory:")
    conn.execute("SET threads=2")
    conn.execute("SET memory_limit='2GB'")
    for view, path in mounts.items():
        p = Path(path)
        if not p.exists():
            raise SystemExit(f"❌ 挂载文件不存在：{path}")
        suffix = p.suffix.lower()
        if suffix in (".parquet", ".pq"):
            reader = f"read_parquet('{path}')"
        elif suffix in (".csv", ".gz"):
            reader = f"read_csv_auto('{path}', header=true)"
        elif suffix == ".duckdb":
            conn.execute(f"ATTACH '{path}' AS {view} (READ_ONLY)")
            continue
        else:
            conn.execute(f"CREATE OR REPLACE TEMP VIEW {view} AS SELECT * FROM read_auto('{path}')")
            continue
        conn.execute(f"CREATE OR REPLACE TEMP VIEW {view} AS SELECT * FROM {reader}")
    meta = {"id": "src1", "type": "duckdb", "mounts": mounts,
            "fingerprint": fingerprint_files(list(mounts.values())) if mounts else None}
    return conn, meta


def human_label(sql: str, col: str) -> str:
    """从 SQL 猜一个能看懂的名字（自动采集时拿不到业务命名，只能启发式）。"""
    s = sql.lower()
    if "count(distinct" in s:
        # 先处理"场景ID 计数 + 单值维度过滤"这一常见形态：
        #   COUNT(DISTINCT "场景ID") WHERE "省份" = '山东省'
        # 正确的名字是「山东省场景数」，但下面的关键词表会先命中 `"省份"` → 说成「省份数」，
        # 上下文就锚不上了（实测：报告写"山东省场景"，账本说"省份数" → 判弱锚定）。
        if re.search(r'count\s*\(\s*distinct\s+["\'`]?场景id', s):
            for dim in ("省份", "城市", "连锁"):
                mm = re.search(r'["\'`]?' + dim + r'["\'`]?\s*=\s*\'([^\']+)\'', sql)
                if mm:
                    return mm.group(1) + "场景数"
        for key, name in (
            ('"门店id"', "门店数"), ('"店员id"', "店员数"), ('"省份"', "省份数"),
            ('"城市"', "城市数"), ('"连锁"', "连锁数"), ("门店id", "门店数"),
            ("店员id", "店员数"), ("省份", "省份数"), ("城市", "城市数"),
        ):
            if key in s:
                return name
        if "是否问症" in sql:
            return "问症场景数"
        if "交易是否达成" in sql:
            return "成交场景数"
        if "是否联合用药" in sql:
            return "联合用药场景数"
        return "场景数"
    if "sum(" in s:
        return "合计"
    if "avg(" in s:
        return "均值"
    return col if col and not col.startswith("count") else "查询结果"


def scalar_of(v):
    try:
        f = float(v)
        return f
    except (TypeError, ValueError):
        return v


def main() -> int:
    ap = argparse.ArgumentParser(description="SQL 录像 → 账本")
    ap.add_argument("--trace", required=True)
    ap.add_argument("--ledger", required=True)
    ap.add_argument("--mount", action="append", default=[],
                    help='挂载视图，格式 "视图名=文件路径"，可重复')
    ap.add_argument("--report-name", default="未命名报告")
    ap.add_argument("--report-files", default="", help="报告文件，逗号分隔")
    ap.add_argument("--data-as-of", default="")
    ap.add_argument("--agent", default="")
    ap.add_argument("--no-recompute", action="store_true", help="不复算，值标记为未验证")
    ap.add_argument("--command", default=None,
                    help='通用取数：SQL 从 stdin 进、CSV 从 stdout 出。'
                         '例：--command "python3 mysql_query.py"（MySQL/PG/HTTP 都行）')
    ap.add_argument("--gateway", default=None,
                    help="取数网关脚本（--sql/--out 协议）")
    ap.add_argument("--metrics", default=None,
                    help="可选：metrics.yaml（给数字贴稳定身份 metric_id）")
    args = ap.parse_args()

    trace_path = Path(args.trace)
    _notes_peek = Path(args.ledger).with_suffix(".notes.jsonl")
    records = load_trace(trace_path, allow_missing=_notes_peek.exists())
    if not records and not _notes_peek.exists():
        print("❌ 未就绪：trace 里没有任何查询记录（业务可能没跑 SQL，或钩子没挂上）", file=sys.stderr)
        print("   纯 pandas 项目请在脚本里用 from rla_note import note 登记数字", file=sys.stderr)
        return 2
    if not records:
        print("[rla_collect] 没有 SQL 记录，仅用 rla_note 登记的数字生成账本")

    mounts = {}
    for m in args.mount:
        if "=" not in m:
            print(f'❌ --mount 格式应为 "视图名=路径"，收到：{m}', file=sys.stderr)
            return 2
        k, v = m.split("=", 1)
        mounts[k.strip()] = v.strip()

    conn, src_meta = (None, None)
    if args.command:
        conn = CommandConn(split_command(args.command))
        src_meta = {"id": "src1", "type": "command", "argv": args.command}
    elif args.gateway:
        gp = Path(args.gateway)
        if not gp.exists():
            print(f"❌ 未就绪：网关脚本不存在 {args.gateway}", file=sys.stderr)
            return 2
        conn = GatewayConn(str(gp))
        src_meta = {"id": "src1", "type": "gateway", "gateway": str(gp)}

    # 没有 SQL 记录时（纯 note 场景）本来就没有东西复算，不该要求挂数据源
    _effective_no_recompute = args.no_recompute or not records
    if not _effective_no_recompute and conn is None:
        if not mounts:
            print("❌ 未就绪：要复算必须给 --mount（否则不知道 SQL 跑在哪个数据上）；"
                  "只想记账不过数请加 --no-recompute", file=sys.stderr)
            return 2
        conn, src_meta = build_source(mounts)

    numbers, problems, skipped = [], [], []
    for i, rec in enumerate(records, 1):
        sql = rec["sql"]
        where = f'{Path(rec.get("file", "")).name}:{rec.get("line", "")}'.strip(":")
        # Node 侧会带上调用者（业务常把查询封在 scalar() 里，只有行内那一帧分不清是哪一句）
        if rec.get("caller"):
            where += f'（调用自 {rec["caller"]}）'
        # Node 侧钩子若没能把绑定参数内联（遇到无法安全转成字面量的类型），
        # 会留下 bound_unresolved 标记。这种 SQL 带 `?`，表面上会被当成"参数化语句跳过"，
        # 静默消失——等于账本悄悄少一个数。要复算时必须明确报出来，不许静默跳过。
        if rec.get("bound_unresolved"):
            if conn is not None:
                problems.append(f"参数无法内联，这条查询没法复算（{where}）：{sql[:80]}")
                continue
            numbers.append({
                "id": f"n{i}", "label": (rec.get("label") or f"查询{i}").strip(),
                "value": None, "unit": "",
                "caliber": f"来自 {where} 的查询（参数未能内联，未复算）",
                "sql": sql, "verifiable": False, "origin": "参数未内联",
            })
            continue
        if not is_queryable(sql):
            skipped.append({"type": "non_select", "sql_head": sql[:80], "where": where})
            continue
        if conn is None:
            numbers.append({
                "id": f"n{i}", "label": (rec.get("label") or f"查询{i}").strip(),
                "value": None, "unit": "", "caliber": f"来自 {where} 的查询（未复算）",
                "sql": sql, "verifiable": False, "origin": "录像未复算",
            })
            continue
        try:
            cur = conn.execute(sql)
            cols = [d[0] for d in cur.description] if cur.description else []
            rows = cur.fetchall()
        except Exception as e:  # noqa: BLE001
            problems.append(f"复算失败（{where}）：{type(e).__name__}: {e}")
            continue
        if not rows:
            problems.append(f"查询无返回行（{where}）：{sql[:100]}")
            continue
        row = rows[0]
        for cname, raw in zip(cols, row):
            val = scalar_of(raw)
            if not isinstance(val, (int, float)):
                continue
            nid = f"n{i}" if len(cols) == 1 else f"n{i}.{cname}"
            numbers.append({
                "id": nid, "label": human_label(sql, str(cname)), "value": val, "unit": "",
                "caliber": f"来自 {where} 的查询结果列「{cname}」",
                "sql": sql, "source": "src1", "verifiable": True,
            })
    if problems:
        print("❌ 未就绪：以下查询没能复算（不许静默跳过）：", file=sys.stderr)
        for p in problems:
            print("   " + p, file=sys.stderr)
        return 2
    # 合并 rla_note 登记的非 SQL 数字（pandas / 纯 Python 算出来的）
    notes_path = Path(args.ledger).with_suffix(".notes.jsonl")
    if notes_path.exists():
        try:
            import rla_note
            notes = rla_note.load_buffer(notes_path)
        except Exception:  # noqa: BLE001
            notes = []
        if notes:
            by_id = {str(n.get("id")): n for n in numbers}
            added = 0
            for rec in notes:
                rid = str(rec["id"])
                if rid in by_id:
                    # 同 id 冲突：note 的显式登记优先，但要吵一声（掩盖会让人以为是 SQL 那条）
                    print(f"   ⚠️ note 登记的 {rid} 与录像条目重名，以 note 为准", file=sys.stderr)
                else:
                    added += 1
                by_id[rid] = rec
            numbers = list(by_id.values())
            print(f"   合并 note 登记 {added} 条（非 SQL 计算，不可复算）")

    if not numbers:
        print("❌ 未就绪：既没有可记账的 SQL，也没有 rla_note 登记的数字", file=sys.stderr)
        print("   纯 pandas 项目请在脚本里用 from rla_note import note 登记", file=sys.stderr)
        return 2

    # L2：如果给了 metrics.yaml，给账本条目认领稳定身份（可选，不写也能跑）
    claimed = 0
    if args.metrics:
        try:
            import metrics as MT
            defs = MT.load(args.metrics)
            claimed = MT.apply_claim(numbers, defs)
            print(f"   已按 {Path(args.metrics).name} 认领 {claimed}/{len(numbers)} 条指标的稳定身份")
        except Exception as e:  # noqa: BLE001
            print(f"❌ 未就绪：metrics.yaml 有问题 —— {e}", file=sys.stderr)
            return 2

    ledger = {
        "schema": "report-ledger/1.0",
        "report": {
            "name": args.report_name,
            "files": [f.strip() for f in args.report_files.split(",") if f.strip()],
            "data_as_of": args.data_as_of,
            "generated_at": now_iso(),
            "agent": args.agent,
        },
        "sources": [src_meta] if src_meta else [],
        "numbers": numbers,
    }
    out = Path(args.ledger)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(ledger, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"✅ 账本已生成：{out}｜{len(numbers)} 个数字｜{len(records)} 条查询（去重后）")
    if skipped:
        print(f"   跳过非查询语句 {len(skipped)} 条（DDL/SET 等）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
