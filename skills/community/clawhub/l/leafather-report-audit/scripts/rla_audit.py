#!/usr/bin/env python3
"""rla_audit.py — 报告数字审计主入口（内核）。

一句话：**报告里的每个指标数字，要么有出生证明，要么不许发。**

用法：
    # 基本：拿账本审报告
    python3 scripts/rla_audit.py --ledger ledger.json

    # 覆盖报告文件（默认用账本 report.files）
    python3 scripts/rla_audit.py --ledger ledger.json --files a.md b.pptx

    # 复算（验证账本里的数字是不是真的）
    python3 scripts/rla_audit.py --ledger ledger.json --mount "data=/path/your.parquet"

    # 只要可读结论，不写文件
    python3 scripts/rla_audit.py --ledger ledger.json --no-write

退出码：0 通过｜1 不通过｜2 未就绪（配置/数据缺失，不算通过）
"""
from __future__ import annotations

import argparse
import ast
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import policy as PL     # noqa: E402
import rla_extract  # noqa: E402




class NotReady(Exception):
    pass


REQUIRED_NUM = ("id", "label", "value", "caliber")   # unit 可选：自动采集时拿不到单位


def now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


# ---------------------------------------------------------------- 账本校验
def validate(ledger: dict) -> tuple[list[str], list[str]]:
    """返回 (错误, 警告)。错误 → 退出码 2。"""
    errs, warns = [], []
    # 顶层必须是对象。2026-10-28 实测：把一份「裸 numbers 数组」账本（dsh 侧 s1 那种
    # 顶层是 metric 数组的形态）喂进来，会在下面第 58 行 AttributeError: 'list' object
    # has no attribute 'get' —— 崩栈而不是给人话。这里提前拦住，报得清楚。
    if not isinstance(ledger, dict):
        errs.append(
            f"账本顶层必须是对象（report-ledger/1.0 的 dict），当前是 {type(ledger).__name__}。"
            '若手里是裸指标数组，请包成 {"schema":"report-ledger/1.0",'
            ' "report":{...}, "numbers":[...]}'
        )
        return errs, warns
    # 单位口径硬规矩：账本 value 必须是基本单位（元/个/单/家），不能用「万元/千」这类换算单位。
    # 否则报告里写「34.0 万元」会被解析成 340000，和账本的 34.0 对不上（2026-10-25 自检撞到）。
    bad_unit = [n.get("id") for n in (ledger.get("numbers") or [])
                if any(u in str(n.get("unit") or "") for u in ("万", "千", "亿"))]
    if bad_unit:
        warns.append(f'{len(bad_unit)} 条账本的 unit 用了换算单位（万元/千/亿）：'
                     f'{", ".join(map(str, bad_unit[:5]))}。'
                     f'请把 value 换回基本单位（元），unit 写「元」')
    if ledger.get("schema") != "report-ledger/1.0":
        warns.append(f'schema 不是 report-ledger/1.0（当前 {ledger.get("schema")!r}），按兼容模式处理')
    rep = ledger.get("report") or {}
    for k in ("name", "files", "data_as_of", "generated_at"):
        if not rep.get(k):
            errs.append(f"report.{k} 缺失")
    nums = ledger.get("numbers")
    if not isinstance(nums, list) or not nums:
        errs.append("numbers 为空 —— 没有账本就谈不上审计（不算通过）")
        return errs, warns
    seen = set()
    for i, n in enumerate(nums, 1):
        tag = n.get("id") or f"#{i}"
        for k in REQUIRED_NUM:
            if n.get(k) in (None, ""):
                errs.append(f"{tag}：缺字段 {k}")
        if tag in seen:
            errs.append(f"{tag}：id 重复")
        seen.add(tag)
        # 派生条目用 expr 验证，不要求 sql（2026-10-25）
        if n.get("verifiable", True) and not n.get("sql") and not n.get("expr"):
            errs.append(f"{tag}：verifiable=true 但既没有 sql 也没有 expr"
                        "（不可复算就不能算已验证）")
        if n.get("expr") and not n.get("derived_from"):
            errs.append(f"{tag}：有 expr 但没写 derived_from（说不出依赖哪几个指标）")
        if n.get("verifiable") is False and not n.get("origin"):
            errs.append(f"{tag}：verifiable=false 但没写 origin（不给来历等于不诚实）")
        if n.get("sql") and not n.get("source"):
            warns.append(f"{tag}：有 sql 但没指 source，复算时按默认源处理")
    return errs, warns


# ---------------------------------------------------------------- 复算
def _unit_value(raw, unit, is_ratio: bool = False) -> float:
    """按单位把原始值换算成账本口径（与 rla_ledger.to_value 同一套规则）。

    内联而不 import rla_ledger：那边顶部 import rla_audit（用 _eval_expr），
    互相 import 会成环。
    """
    v = float(raw)
    u = str(unit or "").strip()
    ul = u.lower()
    pct = {"pct", "%", "％", "百分比", "percent"}
    if is_ratio and (ul in pct or ul == "pct1"):
        return round(v * 100, 1)
    if ul == "pct1":
        return round(v, 1)
    if ul in pct:
        return round(v * 100, 1)
    if u in ("元", "金额"):
        return round(v, 2)
    return round(v, 4)


def recompute(ledger: dict, mounts: dict[str, str], use_gateway: str | None, pol: dict,
              use_command: str | None = None) -> tuple[list[str], dict]:
    """跑 SQL 验账本值。返回 (错误列表, 复算结果{id: 实际值})。"""
    errs, got = [], {}
    nums = [n for n in ledger["numbers"] if n.get("verifiable", True) and n.get("sql")]
    if not nums:
        return errs, got

    conn = None
    if mounts:
        import rla_collect
        try:
            conn, _ = rla_collect.build_source(mounts)
        except SystemExit as e:
            raise NotReady(f"数据源挂载失败：{e}") from e
    elif use_command:
        # --command 接法：SQL 从 stdin 进、CSV 从 stdout 出。没有 duckdb 也能复算。
        # 拆分交给 rla_collect.split_command：Windows 上必须 posix=False，否则反斜杠路径被吃掉
        import rla_collect
        conn = rla_collect.CommandConn(rla_collect.split_command(use_command))

    for n in nums:
        sql = n["sql"]
        try:
            if conn is not None:
                cur = conn.execute(sql)
                row = cur.fetchone()
                if row is None:
                    errs.append(f'{n["id"]}：复算无返回行')
                    continue
                # 比率型指标（SQL 返回 num/den 两列）：必须算除法，不能取第一列。
                # 2026-11-16 仁合通真实验证抓到：avg_doc_amt / top1_share 两条
                # 复算拿的是分子（9 亿），与账本的比值对不上，被误判为"复算不一致"。
                cols = [str(d[0]).lower() for d in (getattr(cur, "description", None) or [])]
                if "num" in cols and "den" in cols:
                    d_ = float(row[cols.index("den")] or 0)
                    if not d_:
                        errs.append(f'{n["id"]}：分母为 0')
                        continue
                    actual = float(row[cols.index("num")]) / d_
                    actual = _unit_value(actual, n.get("unit"), is_ratio=True)
                else:
                    actual = float(row[0])
            elif use_gateway:
                actual = _run_gateway(use_gateway, sql)
            else:
                continue
        except Exception as e:  # noqa: BLE001
            errs.append(f'{n["id"]}：复算失败 {type(e).__name__}: {e}')
            continue
        got[n["id"]] = actual
        expect = float(n["value"])
        if not PL.close_ledger(actual, expect, pol):
            errs.append(f'{n["id"]}（{n["label"]}）：账本写 {expect}，复算是 {actual}')
    return errs, got


def _run_gateway(gw: str, sql: str) -> float:
    import csv
    import os
    import subprocess
    import tempfile
    fd, out = tempfile.mkstemp(suffix=".csv")
    os.close(fd)
    p = subprocess.run([sys.executable, gw, "--sql", sql, "--out", out, "--limit", "10", "--timeout", "120"],
                       capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError(p.stderr[-300:])
    with open(out, encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        raise RuntimeError("网关无返回行")
    return float(list(rows[0].values())[0])


# ---------------------------------------------------------------- 配对
_EXPR_MAX_LEN = 2000

# 表达式里只允许这些 AST 节点：数字、四则运算、取模、幂、一元正负、括号
_ALLOWED_NODES = (
    ast.Expression, ast.BinOp, ast.UnaryOp, ast.Constant,
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow,
    ast.USub, ast.UAdd, ast.Load,
)


def _calc_node(node: ast.AST) -> float:
    """按白名单递归求值（不调用 eval / compile，结构上没有代码执行的可能）。"""
    if isinstance(node, ast.Constant):
        if isinstance(node.value, bool) or not isinstance(node.value, (int, float)):
            raise ValueError("表达式里只能有数字")
        return float(node.value)
    if isinstance(node, ast.UnaryOp):
        v = _calc_node(node.operand)
        if isinstance(node.op, ast.USub):
            return -v
        if isinstance(node.op, ast.UAdd):
            return +v
        raise ValueError("不支持的一元运算")
    if isinstance(node, ast.BinOp):
        a, b = _calc_node(node.left), _calc_node(node.right)
        op = node.op
        if isinstance(op, ast.Add):
            return a + b
        if isinstance(op, ast.Sub):
            return a - b
        if isinstance(op, ast.Mult):
            return a * b
        if isinstance(op, ast.Div):
            if b == 0:
                raise ValueError("除数为 0")
            return a / b
        if isinstance(op, ast.Pow):
            # 幂最容易用来拖死进程（9**9**9**9），直接限死规模
            if abs(b) > 64 or abs(a) > 1e9:
                raise ValueError("幂运算超出允许范围")
            return a ** b
        raise ValueError("不支持的二元运算")
    raise ValueError(f"表达式含不允许的语法：{type(node).__name__}")


def _eval_expr(expr: str, by_id: dict) -> float:
    """算派生表达式：把指标 id 替换成数值后，用 AST 白名单求值。

    为什么不用 eval（2026-10-26 改，上架安全审查口径）：
        账本的 expr 字段**是第三方写的**，属于外部输入。eval 哪怕加了字符集白名单，
        也始终是"需要论证才安全"；而通用安全清单（skill-vetter、鼎实验室的
        skills-security-check）看到内置求值函数就标红旗。改成 AST 白名单 + 自己递归求值后，
        结构上就没有代码执行的可能：只认数字、四则运算、括号、一元正负，其余节点一律拒绝。
    """
    s = str(expr)
    if len(s) > _EXPR_MAX_LEN:
        raise ValueError(f"表达式过长（>{_EXPR_MAX_LEN} 字符）")
    for k in sorted(by_id, key=len, reverse=True):
        v = by_id[k].get("value")
        if v is None:
            raise ValueError(f"派生引用的 {k} 没有数值")
        s = s.replace(k, f"({float(v)})")
    if not re.fullmatch(r"[\d\.\s\+\-\*\/\(\)eE]+", s):
        raise ValueError(f"表达式含不允许的字符：{s[:60]}")
    try:
        tree = ast.parse(s, mode="eval")
    except SyntaxError as e:
        raise ValueError(f"表达式语法错误：{e.msg}") from e
    for node in ast.walk(tree):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"表达式含不允许的语法：{type(node).__name__}")
    return _calc_node(tree.body)


def verify_derived(ledger: dict, pol: dict) -> list[str]:
    """验证账本里声明的派生：按 expr 算出来，是否等于声明的 value。

    这是"声明 + 验证"模式 —— 审计只核对，不搜索。
    """
    errs = []
    by_id = {n["id"]: n for n in ledger["numbers"]}
    for n in ledger["numbers"]:
        df = n.get("derived_from")
        if not df:
            continue
        expr = n.get("expr")
        if not expr:
            errs.append(f'{n["id"]}（{n.get("label","")}）：声明了 derived_from 却没有 expr')
            continue
        miss = [x for x in (df if isinstance(df, list) else [df]) if x not in by_id]
        if miss:
            errs.append(f'{n["id"]}：derived_from 引用了不存在的指标 {miss}')
            continue
        try:
            actual = _eval_expr(expr, by_id)
        except Exception as e:  # noqa: BLE001
            errs.append(f'{n["id"]}：派生算式无法计算（{e}）')
            continue
        if not PL.close_ledger(actual, float(n["value"]), pol):
            errs.append(f'{n["id"]}（{n.get("label","")}）：声明 {expr} 应为 {actual:.4g}，'
                        f'账本却写 {n["value"]}')
    return errs


def pair(report_nums: list[dict], ledger: dict, pol: dict) -> tuple[list[dict], list[dict]]:
    """报告数字 → 账本条目。返回 (matched, unmatched)。"""
    nums = ledger["numbers"]
    by_value = {}
    for n in nums:
        try:
            v = float(n["value"])
        except (TypeError, ValueError):
            continue
        by_value.setdefault(round(v, 6), []).append(n)

    matched, unmatched, ambiguous, weak = [], [], [], []
    for r in report_nums:
        if r["kind"] != "metric":
            continue
        # A：量纲必须一致（报告写 % 的，不能配到"场景数"；反之亦然）
        r_dim = "pct" if r.get("unit_hint") == "pct1" else "count"
        cand = [n for n in by_value.get(round(r["value"], 6), [])
                if _dim_ok(r_dim, _dim(n.get("unit")))]
        if not cand:  # 宽容差匹配（四舍五入 / 百分比小数位）
            cand = [n for n in nums
                    if isinstance(n.get("value"), (int, float))
                    and _dim_ok(r_dim, _dim(n.get("unit")))
                    and PL.close(r.get("raw", ""), r["value"], float(n["value"]), pol)]
        if cand:
            best = min(cand, key=lambda n: _ctx_distance(r["context"], str(n.get("label", ""))))
            dist = _ctx_distance(r["context"], str(best.get("label", "")))
            # 锚定是**必要条件**（2026-10-25）：值相等但上下文说不清是哪个指标 → 不算命中。
            # 曾经只对 <10 的小值要求锚定，结果"准确率 84%"照样配上"84 场景数"。
            # dist==5 表示"标签里没有可锚定的词"（如 label 就叫「场景数」，词全在通用词表里）。
            # 这是账本 label 写得泛，不该罚报告方 —— 只要值唯一就认，但标注 weak_label。
            if dist == 5:
                if len(cand) == 1:
                    matched.append({"report": r, "ledger": best, "how": "exact",
                                    "role": best.get("role", "indicator"),
                                    "anchor": "weak_label"})
                else:
                    ambiguous.append({"report": r, "cands": cand[:3]})
                continue
            if dist >= 9:
                # 撤掉 unique 兜底（2026-10-25）：实测"值唯一就放行"精度只有 61%
                # （18 条里 7 条假），是第三次"兜底宽容变误配"。
                # 但值唯一的那些**不是判死**，单独列为"弱锚定待补"：
                #   值对得上、账本里唯一，只是报告上下文没说清 → 请报告方补上下文，而不是我们替它猜。
                too_small = r_dim == "count" and abs(float(r["value"])) < SMALL_VALUE
                if len(cand) == 1 and not too_small:
                    weak.append({"report": r, "ledger": best})
                    continue
                ambiguous.append({"report": r, "cands": cand[:3]})
                continue
            matched.append({"report": r, "ledger": best, "how": "exact",
                            "role": best.get("role", "indicator"),
                            "anchor": "strong" if dist == 0 else "weak"})
            continue
        # 不再搜索派生（2026-10-25 改造）：
        # 审计器在这里"找一个能圆上的算式"等于替被审计方辩护，
        # 且实测随账本规模退化 —— 195 条指标时任意编造的数字 100% 能被圆上。
        # 现在派生必须由账本显式声明（derived_from + expr），审计只做验证。
        unmatched.append(r)
    return matched, unmatched, ambiguous, weak


SMALL_VALUE = 10        # 小于它、且上下文无锚点 → 这个数字本身不可区分（只对计数生效）
PCT_UNITS = {"pct", "pct1", "%", "％", "百分比", "percent"}


def _dim(unit) -> str:
    """量纲：pct / count / unknown。

    账本条目没写 unit 时返回 unknown —— 这时不强制量纲（自动采集拿不到单位），
    否则会把"账本没标单位"误判成"量纲不符"而误杀。
    """
    u = str(unit or "").strip().lower()
    if u in PCT_UNITS:
        return "pct"
    if not u:
        return "unknown"
    return "count"


def _dim_ok(report_dim: str, ledger_dim: str) -> bool:
    return ledger_dim == report_dim or ledger_dim == "unknown"


# 通用词：出现在哪都算"锚定"就没有意义了（"场景"两个字报告里到处都是）
GENERIC_WORDS = {"场景", "数据", "数量", "合计", "总计", "占比", "比例", "情况",
                 "其中", "全部", "整体", "个数", "单位", "数值", "级", "层"}
# 这些字单独或组合都太泛，切出来的碎片（如「场景数」→「景数」）不该当锚定词
GENERIC_CHARS = set("".join(GENERIC_WORDS))


def _ctx_distance(ctx: str, label: str) -> int:
    """标签里的"专有词"是否出现在上下文。0=锚定 / 5=标签无专有词 / 9=有词但上下文没有。

    2026-10-25 修：原来"标签里任意中文词出现"就算锚定，
    而「贝那鲁肽 场景」里的「场景」在报告里遍地都是 → 25 条 GLP-1 的 1 被误判命中。
    现在排除通用词，并要求"锚定"是命中的必要条件，不再是同值时的择优条件。
    """
    if not label:
        return 9
    # 中文没有空格，整串匹配会失败（"覆盖店员"≠"覆盖门店 / 店员"）。
    # 改成二元切分：覆盖店员 → 覆盖 / 盖店 / 店员
    grams = set()
    for block in re.findall(r"[\u4e00-\u9fa5]+", label):
        if len(block) == 1:
            continue
        for i in range(len(block) - 1):
            g = block[i:i + 2]
            # 整词在通用表里，或两个字都是通用字（"景数""场景"这种碎片）→ 不算锚定词
            if g in GENERIC_WORDS or all(c in GENERIC_CHARS for c in g):
                continue
            grams.add(g)
    en = re.findall(r"[A-Za-z]{2,}", label)          # GLP / ATC 这类
    cands = list(grams) + en
    if not cands:
        return 5
    return 0 if any(w in ctx for w in cands) else 9


# ---------------------------------------------------------------- 报告
def _norm_form(raw: str) -> str:
    """报告里数字的写法归一（去千分位/空格），用于比较"同一件事写法是否一致"。"""
    return str(raw).replace(",", "").replace("，", "").replace(" ", "").strip()


def check_cross_file(matched: list[dict]) -> list[tuple[str, str, str]]:
    """跨件一致（闸门3）：同一账本条目，在多份交付件里的写法必须一致。

    为什么要按"账本记录 id"分组，而不是按 metric_id：
        实测某客户 143 条账里，110 条都认领成 ship.amt_net（净发货额），
        但它们分别是月度/周度/省份/客户等不同筛选 —— 按 metric_id 分组会把它们混成一个。
        账本记录 id 才是"这一个数"的唯一身份。
    """
    from collections import defaultdict
    groups = defaultdict(list)
    for m in matched:
        groups[m["ledger"]["id"]].append(m)

    issues = []
    for lid, items in groups.items():
        files = {x["report"]["file"] for x in items}
        if len(files) < 2:
            continue                      # 只有一份提到，不涉及跨件
        forms = defaultdict(list)
        for x in items:
            forms[_norm_form(x["report"]["raw"])].append(f'{x["report"]["file"]}:{x["report"]["loc"]}')
        if len(forms) > 1:
            label = items[0]["ledger"].get("label") or lid
            detail = "；".join(f"{k}（{', '.join(v[:2])}）" for k, v in forms.items())
            issues.append((lid, label, detail))
    return issues


def check_must(matched: list[dict], must_ids: list[str], files: list) -> list[str]:
    """闸门4 必现：配置的核心指标必须出现在**每个**交付件里。"""
    if not must_ids:
        return []
    per_file = {}
    for m in matched:
        mid = m["ledger"].get("metric_id")
        if mid:
            per_file.setdefault(m["report"]["file"], set()).add(mid)
    issues = []
    for f in files:
        have = per_file.get(f.name, set())
        missing = [x for x in must_ids if x not in have]
        if missing:
            issues.append(f"{f.name} 缺少必现指标：{', '.join(missing)}")
    return issues


def check_leak(files: list, checks: dict) -> list[str]:
    """闸门5 泄漏：客户版不得出现内部标记。"""
    import fnmatch
    pats = checks.get("leak_patterns") or []
    rules = checks.get("leak_rules") or []
    # 防假绿（2026-10-25 实测撞到）：配了客户版匹配模式、却没配任何泄漏规则时，
    # 检查压根不跑，结论却显示"通过" —— 等于盖了个空章。
    # 现在改成明确报"未配置"，不让它静默通过。
    if pats and not rules:
        return ["⚠️ 泄漏检查未配置规则（policy.checks.leak_rules 为空）—— "
                "客户版实际未检查，不能当作已通过"]
    if not pats:
        return []
    issues = []
    for f in files:
        if not any(fnmatch.fnmatch(f.name, p) for p in pats):
            continue
        try:
            txt = f.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for rule in rules:
            rgx = rule.get("regex")
            if not rgx:
                continue
            for m in re.finditer(rgx, txt):
                line = txt[:m.start()].count("\n") + 1
                issues.append(f'{f.name} 客户版泄漏「{rule.get("name", rgx)}」：'
                              f'{m.group(0)[:40]}（L{line}）')
                break          # 每条规则每文件报一次，避免刷屏
    return issues


def _sort_by_policy(categorized: list[tuple[str, str]], pol: dict):
    """按 policy 把 (类别, 说明) 分成 FAIL / REVIEW / 丢弃（未归类）。"""
    f = set(pol["verdict"]["fail"])
    r = set(pol["verdict"]["review"])
    fails = [m for c, m in categorized if c in f]
    revs = [m for c, m in categorized if c in r and c not in f]
    dropped = [f"{c}：{m}" for c, m in categorized if c not in f and c not in r]
    return fails, revs, dropped


DATE_HINT_RE = re.compile(r"(20\d{2})[-/年](\d{1,2})[-/月](\d{1,2})")


def date_mismatch_hint(paths: list, ledger_cap: str) -> str | None:
    """报告里提到别的数据截止日 → 提示"可能是口径不同"，而不是只说"来源不明"。

    这是**帮它定位**，不是放它过：账本没有的数字照样拦，
    但我们告诉它"大概率为啥对不上"，省得它瞎猜。
    """
    found = set()
    for p in paths:
        try:
            txt = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for m in DATE_HINT_RE.finditer(txt):
            y, mo, d = (int(x) for x in m.groups())
            if 1 <= mo <= 12 and 1 <= d <= 31:
                found.add(f"{y:04d}-{mo:02d}-{d:02d}")
    if not found:
        return None
    others = sorted(x for x in found if x != ledger_cap)
    if not others:
        return None
    return (f"报告提到日期 {', '.join(others[:3])}，而账本数据截止是 {ledger_cap}。"
            f"**若这些数字是另一口径算出的，请把它们也算进账本并各自标注 data_as_of**；"
            f"否则说明数字确实没有出处。")


# ---------------------------------------------------- 交付层辅助（v3.5.0，不参与判定）
# 这些函数只服务「产出物」（manifest / evidence.csv / html），
# 任何判定相关的东西都不许写进这里 —— 保 v3.4.5 的判定结果逐项不变。
def _sha16(path) -> str:
    """文件 sha256 前 16 位。读不到返回空串，不抛。"""
    import hashlib
    try:
        h = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(1 << 20), b""):
                h.update(chunk)
        return h.hexdigest()[:16]
    except OSError:
        return ""


def _skill_version() -> str:
    """从技能根 SKILL.md 的 frontmatter 读 version；读不到返回 unknown。"""
    try:
        txt = (HERE.parent / "SKILL.md").read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return "unknown"
    m = re.search(r"^version:\s*([0-9][\w.\-]*)", txt, re.M)
    return m.group(1) if m else "unknown"


def _env_info() -> dict:
    """环境指纹。取不到的写 unknown / 未安装，不编。"""
    import platform
    info = {
        "skill_version": _skill_version(),
        "python": platform.python_version(),
        "duckdb": "未安装",
        "os": f"{platform.system()} {platform.release()}",
    }
    try:
        import duckdb
        info["duckdb"] = str(getattr(duckdb, "__version__", "unknown"))
    except Exception:  # noqa: BLE001
        pass
    return info


def _audit_id(data_as_of, ledger_path: Path) -> str:
    """审计编号 RLA-<数据截止日去连字符>-<账本hash8>。

    刻意不带时刻：同一账本 + 同一数据截止日，无论跑几次都是同一个编号，
    这样"这份凭证是不是最新那次"能一眼看出（时刻放 manifest.generated_at）。
    data_as_of 缺失时用 NODATE 占位，不编造日期。
    """
    asof = re.sub(r"[^0-9A-Za-z]", "", str(data_as_of or "")) or "NODATE"
    return f"RLA-{asof}-{_sha16(ledger_path)[:8] or '00000000'}"


def _build_matrix(matched: list) -> list:
    """跨件矩阵数据：按账本条目 id 聚合到各交付件（只服务渲染，不做判定）。

    一个格子可能是"同一 id 在同一文件里出现多次"，所以 cells[file] 是列表。
    渲染层决定显示原文还是归一化值（已定：显示原文，判定用归一化值）。
    """
    from collections import OrderedDict
    by_id: "OrderedDict[str, dict]" = OrderedDict()
    for m in matched:
        lg, rp = m["ledger"], m["report"]
        lid = str(lg.get("id"))
        row = by_id.setdefault(
            lid, {"ledger_id": lid, "label": lg.get("label") or lid, "cells": {}})
        row["cells"].setdefault(rp["file"], []).append(
            {"raw": rp.get("raw"), "value": rp.get("value"), "loc": rp.get("loc")})
    return list(by_id.values())


# ---------------------------------------------------------------- 审计回执（manifest）
MANIFEST_SCHEMA = "rla-audit-manifest/1.0"
_VERDICT_CODE = {"✅ 通过": "pass", "⚠️ 需人工复核": "review", "❌ 不通过": "fail"}


def _verdict_code(verdict: str) -> str:
    """判定 → 机器可读枚举。措辞若变，按关键词兜住（不轻易返回 unknown）。"""
    v = str(verdict or "")
    if v in _VERDICT_CODE:
        return _VERDICT_CODE[v]
    if "不通过" in v:
        return "fail"
    if "复核" in v:
        return "review"
    if "通过" in v:
        return "pass"
    return "unknown"


def _is_absish(s: str) -> bool:
    """像不像绝对路径：/x、C:\\x、\\\\server\\x。"""
    return bool(re.match(r"^(?:[A-Za-z]:[\\/]|\\\\|/)", str(s or "")))


def _sanitize_argv(argv: list) -> str:
    """拼一条「可以给别人看」的复现命令。

    为什么必须脱敏：原始 argv 含 D:\\testdata\\客户A\\... 这类路径，回执外发
    就等于把客户目录结构送出去。这里一律换成 <path:文件名>，并在 manifest
    的 limitations 里说明「复现时请换成自己的路径」。
    """
    parts = ["scripts/rla_audit.py"]
    for a in argv[1:]:
        s = str(a)
        if "=" in s:
            k, v = s.split("=", 1)
            if _is_absish(v):
                parts.append(f"{k}=<path:{os.path.basename(v)}>")
                continue
        parts.append(f"<path:{os.path.basename(s)}>" if _is_absish(s) else s)
    return " ".join(f'"{p}"' if " " in p else p for p in parts)


def _result_fingerprint(matched: list, recomputed: dict) -> str:
    """结果指纹：账本 id + 复算值。同一账本 + 同一数据 → 同指纹；数据变了 → 指纹变。

    比「只存输入 hash」更有用：它证明的是「这次算出来的结果」而不是「文件没动」。
    """
    import hashlib
    items = sorted(
        f'{m["ledger"].get("id")}={recomputed.get(m["ledger"].get("id"), "-")}'
        for m in matched
    )
    return hashlib.sha256("|".join(items).encode()).hexdigest()[:16]


def _basename_only(p) -> str:
    """只留文件名。回执可能外发，任何来源字段都不许带目录结构。"""
    s = str(p or "")
    if not s:
        return ""
    if "内置默认" in s:
        return s
    return s.replace("\\", "/").rstrip("/").split("/")[-1] or s


def _public_inputs(inputs: dict) -> dict:
    """剥掉下划线开头的内部字段（如 _abs 绝对路径），只留能外发的。"""
    out = {}
    for k, v in (inputs or {}).items():
        if isinstance(v, dict):
            out[k] = {kk: vv for kk, vv in v.items() if not kk.startswith("_")}
        elif isinstance(v, list):
            out[k] = [
                {kk: vv for kk, vv in f.items() if not kk.startswith("_")}
                if isinstance(f, dict) else f
                for f in v
            ]
        else:
            out[k] = v
    return out


def build_manifest(res: dict, argv: list) -> dict:
    """审计回执（机检）。同样的 res + argv → 同样的内容（除 generated_at）。"""
    cov = res.get("coverage")
    inputs = res.get("inputs") or {}
    pol = res.get("policy") or {}
    matched = res.get("matched") or []
    recomputed = res.get("recomputed") or {}

    # 完整性自检：把输入文件的 hash 再算一遍，与记录值比对
    # （抓「生成回执的过程中文件被改掉」这类并发问题，不是自己跟自己对）
    checks = []
    for name in ("ledger", "policy"):
        rec = inputs.get(name) or {}
        actual = _sha16(rec.get("_abs") or "") if rec.get("_abs") else ""
        checks.append({"name": f"{name}_hash",
                       "expected": rec.get("sha256_16") or "",
                       "actual": actual,
                       "ok": bool(actual) and actual == rec.get("sha256_16")})
    for f in inputs.get("report_files") or []:
        actual = _sha16(f.get("_abs") or "") if f.get("_abs") else ""
        checks.append({"name": f"report:{f.get('path')}",
                       "expected": f.get("sha256_16") or "",
                       "actual": actual,
                       "ok": bool(actual) and actual == f.get("sha256_16")})

    return {
        "schema": MANIFEST_SCHEMA,
        "audit_id": res.get("audit_id"),
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "verdict": {
            "code": _verdict_code(res.get("verdict")),
            "label": res.get("verdict"),
            "exit_code": res.get("exit_code"),
        },
        # coverage 双写：ratio 是引擎内部口径，percent 是与外部系统对接的口径
        # （dsh 侧用 100.0，我们内部用 1.0 —— 双写省掉「差 100 倍」这类事故）
        "coverage": {
            "ratio": cov,
            "percent": None if cov is None else round(float(cov) * 100, 1),
            "matched": res.get("n_matched"),
            "should": res.get("n_should"),
            "min_ratio": res.get("pol_min_ratio"),
        },
        "counts": {
            "ledger": res.get("n_ledger"), "verifiable": res.get("n_verifiable"),
            "recomputed_ok": res.get("n_recomputed_ok"),
            "extracted": res.get("n_extracted"), "metric": res.get("n_metric"),
            "matched": res.get("n_matched"), "matched_indicator": res.get("n_matched_indicator"),
            "matched_support": res.get("n_matched_support"),
            "unmatched": res.get("n_unmatched"), "weak": res.get("n_weak"),
            "ambiguous": res.get("n_ambiguous"), "exempt": res.get("n_exempt_struct"),
        },
        "inputs": _public_inputs(inputs),
        "environment": res.get("env") or {},
        "reproduce_cmd": res.get("reproduce_cmd") or _sanitize_argv(argv),
        "outputs": {
            "audit_md": (res.get("outputs") or {}).get("audit_md"),
            "audit_html": (res.get("outputs") or {}).get("audit_html"),
            "evidence_csv": (res.get("outputs") or {}).get("evidence_csv"),
        },
        "integrity": {
            "ok": all(c["ok"] for c in checks) if checks else False,
            "result_fingerprint": _result_fingerprint(matched, recomputed),
            "recomputed_count": len(recomputed),
            "checks": checks,
        },
        "policy": {"source": _basename_only(pol.get("source")), "hash": pol.get("hash"),
                   "rounding": pol.get("rounding")},
        "limitations": [
            "只证明「报告里的数字 = 账本里的数字」，不证明账本口径选得对。",
            "账本若本身口径有误，复算同样会通过。",
            "复现命令中的路径已脱敏为 <path:文件名>，复现时请换成自己的路径。",
        ],
    }


# ---------------------------------------------------------------- 证据清单（evidence.csv）
EVIDENCE_COLS = [
    "report_file", "loc", "raw", "value", "unit", "role",
    "ledger_id", "label", "caliber", "sql", "ledger_value", "recomputed", "delta",
    "how", "verdict", "anchor", "note",
    # 预留（当前留空）：将来报告由模板产出时，数字自带 ID 与单元格坐标，直接填这几列
    "number_id", "block_id", "cell_row", "cell_col",
]

# 会被 Excel 当公式执行的首字符（CSV 注入）
_CSV_DANGER = ("=", "+", "-", "@", "\t", "\r")


def _csv_safe(v):
    """防 CSV 注入：首字符是 = + - @ 时前置单引号。

    只用在**文本列**上。数值列（value/recomputed/delta）绝不能转义，
    否则 Excel 会把它们当文本，用户就没法排序求和了。
    """
    s = "" if v is None else str(v)
    return "'" + s if s.startswith(_CSV_DANGER) else s


def _evidence_rows(res: dict) -> list[dict]:
    """一行 = 报告里出现的一个数字。五类都要进（含豁免），
    否则「未纳入审计的数字」在别处查不到 —— 那正是最容易藏问题的地方。"""
    rows = []
    recomputed = res.get("recomputed") or {}

    for m in res.get("matched") or []:
        rp, lg = m["report"], m["ledger"]
        lid = str(lg.get("id"))
        rec = recomputed.get(lid)
        val = rp.get("value")
        rows.append({
            "report_file": rp.get("file"), "loc": rp.get("loc"), "raw": rp.get("raw"),
            "value": val, "unit": lg.get("unit") or rp.get("unit_hint") or "",
            "role": lg.get("role", "indicator"),
            "ledger_id": lid, "label": lg.get("label"), "caliber": lg.get("caliber"),
            "sql": lg.get("sql"), "ledger_value": lg.get("value"), "recomputed": rec,
            "delta": (round(float(val) - float(rec), 6)
                      if isinstance(val, (int, float)) and isinstance(rec, (int, float)) else ""),
            "how": m.get("how"), "verdict": "ok", "anchor": m.get("anchor", ""),
            "note": "",
        })

    for w in res.get("weak") or []:
        rp, lg = w["report"], w["ledger"]
        rows.append({
            "report_file": rp.get("file"), "loc": rp.get("loc"), "raw": rp.get("raw"),
            "value": rp.get("value"), "unit": lg.get("unit") or "", "role": lg.get("role", ""),
            "ledger_id": lg.get("id"), "label": lg.get("label"), "caliber": lg.get("caliber"),
            "sql": lg.get("sql"), "ledger_value": lg.get("value"), "recomputed": "",
            "delta": "", "how": "weak", "verdict": "review", "anchor": "weak",
            "note": "值在账本里唯一，但上下文没说清是哪个指标 → 建议补上下文或在 label 加区分词",
        })

    for amb in res.get("ambiguous") or []:
        rp = amb["report"]
        cands = amb.get("cands") or []
        rows.append({
            "report_file": rp.get("file"), "loc": rp.get("loc"), "raw": rp.get("raw"),
            "value": rp.get("value"), "unit": rp.get("unit_hint") or "", "role": "",
            "ledger_id": "", "label": "", "caliber": "", "sql": "",
            "ledger_value": "", "recomputed": "", "delta": "",
            "how": "ambiguous", "verdict": "review", "anchor": "",
            "note": "可能对应：" + "、".join(str(c.get("label") or c.get("id")) for c in cands) + "（需人工判定）",
        })

    for u in res.get("unmatched") or []:
        rows.append({
            "report_file": u.get("file"), "loc": u.get("loc"), "raw": u.get("raw"),
            "value": u.get("value"), "unit": u.get("unit_hint") or "", "role": "",
            "ledger_id": "", "label": "", "caliber": "", "sql": "",
            "ledger_value": "", "recomputed": "", "delta": "",
            "how": "unmatched", "verdict": "fail", "anchor": "",
            "note": "账本里没有这个数字的出处 → 必须补账或改报告",
        })

    for e in res.get("exempt") or []:
        rows.append({
            "report_file": e.get("file"), "loc": e.get("loc"), "raw": e.get("raw"),
            "value": "", "unit": "", "role": "",
            "ledger_id": "", "label": "", "caliber": "", "sql": "",
            "ledger_value": "", "recomputed": "", "delta": "",
            "how": "exempt", "verdict": "exempt", "anchor": "",
            "note": f"按规则豁免（{e.get('kind')}），不计入应审",
        })
    return rows


def write_evidence_csv(res: dict, path: Path) -> int:
    """写 evidence.csv（utf-8-sig，Excel 中文不乱码）。返回行数。"""
    import csv
    rows = _evidence_rows(res)
    path.parent.mkdir(parents=True, exist_ok=True)
    # utf-8-sig 带 BOM：Windows Excel 直接双击打开中文才不乱码（实测坑）
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=EVIDENCE_COLS, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            out = {}
            for k in EVIDENCE_COLS:
                v = r.get(k, "")
                # 文本列过注入防护；数值列原样（否则 Excel 不认数）
                out[k] = v if k in ("value", "ledger_value", "recomputed", "delta") else _csv_safe(v)
            w.writerow(out)
    return len(rows)


# ---------------------------------------------------------------- 人话字典（v3.5.0）
# 类别 → 人话。「弱锚定」「ambiguous_number」这类词老板看不懂，结论里必须翻译。
_CATEGORY_LABEL = {
    "ledger_mismatch": "复算对不上",
    "unmatched_number": "来源不明",
    "precision_mismatch": "精度不符",
    "weak_anchor": "弱锚定",
    "ambiguous_number": "无法判定",
    "cross_file_mismatch": "多份交付件数字打架",
    "must_missing": "核心指标缺失",
    "leak": "泄漏内部口径",
    "no_metric": "没认出任何指标",
    "low_coverage": "覆盖率不足",
    "not_recomputed": "未复算",
    "unverifiable_entry": "账本声明不可复算",
    "unscanned_image": "图片内容未扫描",
    "snapshot_mismatch": "账本过期",
    "unrendered_placeholder": "占位符未渲染",
    "invariant_violation": "不变式未通过",
    "metric_unused": "算了没用",
}

# 改法：报警谁都会，关键是告诉它「怎么改」。写具体动作，不写"请检查"。
_FIX_HINTS = {
    "ledger_mismatch": "先确认哪个对：数据变了就更新账本 value 后重跑；账本写错了就改账本；"
                       "不许直接改报告去迁就错账本。",
    "unmatched_number": "两条路选一条：①在账本里补一条（label + caliber + sql 三件套，"
                        "可用 --export-missing 生成模板）；②把报告里这个数字删掉或换成有出处的数。",
    "precision_mismatch": "报告的小数位与账本口径不一致，按 policy 的舍入规则统一。",
    "weak_anchor": "值在账本里唯一但报告没说清是哪个指标：在报告里补一句口径（如「（含税）」），"
                   "或在账本 label 里加区分词。",
    "ambiguous_number": "上下文锚不住、可能对应多个指标：报告里把说法写明确（加维度/口径），"
                        "或把账本里这几个指标的 label 区分开。",
    "cross_file_mismatch": "多份交付件写了不同值：统一成同一个数（以账本为准），改完重跑。",
    "must_missing": "核心指标没出现在这份交付件里：补上；若这份文件本来就该缺，调整 policy 的 must 配置。",
    "leak": "客户版里出现了内部口径：删掉或改成对外说法。",
    "no_metric": "一个指标都没认出来：换用更常见的说法（如「销售金额」而不是「钱数」），"
                 "或把这些数字直接写进账本。",
    "low_coverage": "有数字没查到出处：打开 evidence.csv，筛 verdict 为空的行，逐个补账或改报告。",
    "not_recomputed": "本次没复算（没给数据源）：加 --mount 或 --command 重跑，否则算术没验过。",
    "unverifiable_entry": "账本有条目声明为不可复算：补上 SQL 让它可复算，否则这条永远不算通过。",
    "unscanned_image": "报告里有图片没被扫描：图片里的数字没进审计范围，需人工确认。",
    "snapshot_mismatch": "数据文件变了但账本没重算 → 先跑 python3 scripts/rla_ledger.py 重建账本，再重新审计。",
    "unrendered_placeholder": "报告里还有 [[id]] 占位符没被渲染 → 用 rla_render.sub() 出稿，别把模板当成品交付。",
    "invariant_violation": "指标之间的大小关系不成立（如单据数 > 明细行数）→ 先查数据和口径，不是改报告能解决的。",
    "metric_unused": "账本里有指标没被任何交付件引用（可能是废弃指标，也可能是漏写了）→ 确认后可删或补进报告。",
}


def _strip_label_prefix(msg: str, label: str) -> str:
    """issue 的 message 前面常自带类别词（如「来源不明：」），渲染时别重复一遍。"""
    for pre in (f"{label}：", f"{label}:"):
        if msg.startswith(pre):
            return msg[len(pre):].lstrip()
    return msg


HTML_CSS = """
:root{--ink:#1a1a1a;--muted:#5f5e5a;--line:#d9d7cf;--bg:#f7f6f2;
      --pass:#3b6d11;--passbg:#eaf3de;--review:#854f0b;--reviewbg:#faf3e2;
      --fail:#a32d2d;--failbg:#fcebeb;--blue:#185fa5;--bluebg:#eef4fb}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:"PingFang SC","Microsoft YaHei",system-ui,sans-serif;color:var(--ink);
     background:var(--bg);line-height:1.65;font-size:14px}
.page{max-width:1100px;margin:0 auto;padding:40px 32px 64px;background:#fff}
h1{font-size:24px;letter-spacing:.5px}
h2{font-size:17px;margin:36px 0 10px;padding-left:10px;border-left:4px solid var(--ink)}
.meta{color:var(--muted);font-size:12.5px;margin-top:8px;display:flex;gap:14px;flex-wrap:wrap}
.meta b{color:var(--ink);font-weight:600}
.banner{margin:22px 0 8px;padding:18px 22px;border-radius:8px;border:1px solid var(--line)}
.banner .v{font-size:20px;font-weight:600}
.banner .s{font-size:13.5px;margin-top:6px;color:var(--muted)}
.b-pass{background:var(--passbg);border-color:#cfe0b4}.b-pass .v{color:var(--pass)}
.b-review{background:var(--reviewbg);border-color:#f0dcae}.b-review .v{color:var(--review)}
.b-fail{background:var(--failbg);border-color:#f3c6c6}.b-fail .v{color:var(--fail)}
.grid{display:grid;grid-template-columns:180px 1fr;gap:22px;align-items:center;margin:18px 0}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:10px}
.card{border:1px solid var(--line);border-radius:8px;padding:12px 14px;background:#fbfaf7}
.card .n{font-size:22px;font-weight:600}
.card .l{font-size:12px;color:var(--muted);margin-top:2px}
.card.warn .n{color:var(--review)}.card.bad .n{color:var(--fail)}
table{width:100%;border-collapse:collapse;font-size:13px;margin:8px 0}
th,td{border:1px solid var(--line);padding:7px 10px;text-align:left;vertical-align:top}
th{background:#f1efe8;font-weight:600;white-space:nowrap}
td.num{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
td.bad{background:var(--failbg);color:var(--fail);font-weight:600}
details{border:1px solid var(--line);border-radius:8px;margin:10px 0;background:#fdfdfb}
details>summary{cursor:pointer;padding:9px 14px;background:#f6f5f0;border-radius:8px 8px 0 0;
                font-weight:600;list-style:none}
details>summary::-webkit-details-marker{display:none}
details>summary::before{content:"▸ ";color:var(--muted)}
details[open]>summary::before{content:"▾ "}
.dbody{padding:6px 10px 12px}
pre{background:#f4f3ee;border:1px solid var(--line);border-radius:6px;padding:8px 10px;
    overflow-x:auto;font-family:Consolas,monospace;font-size:11.5px;line-height:1.5;white-space:pre-wrap}
.toolbar{display:flex;gap:8px;margin:10px 0 4px}
.toolbar button{border:1px solid var(--line);background:#f6f5f0;border-radius:6px;
                padding:5px 12px;font-size:12.5px;cursor:pointer}
.toolbar button:hover{background:#efeee8}
.issue{border-left:3px solid var(--fail);background:var(--failbg);padding:10px 14px;
       border-radius:0 6px 6px 0;margin:8px 0}
.issue.rev{border-left-color:var(--review);background:var(--reviewbg)}
.issue .t{font-weight:600;font-size:13.5px}
.issue .d{color:var(--muted);font-size:12.5px;margin-top:3px}
.issue .fix{font-size:12.5px;margin-top:6px}
.tag{display:inline-block;font-size:11px;padding:1px 7px;border-radius:10px;
     background:#efeee8;color:var(--muted);margin-right:6px}
.kv{width:100%;font-size:12.5px}
.kv td{border:none;border-bottom:1px dashed var(--line);padding:5px 4px}
.kv td:first-child{color:var(--muted);width:170px;white-space:nowrap}
footer{margin-top:34px;padding-top:14px;border-top:1px solid var(--line);
       font-size:12px;color:var(--muted);display:flex;justify-content:space-between;gap:16px}
.warnbox{margin:14px 0;padding:12px 16px;background:var(--reviewbg);border-radius:6px;
         border:1px solid #f0dcae;font-size:13px}
@media print{
  body{background:#fff}.page{padding:0}
  details>summary{display:none}
  details{border:none}
  .dbody{display:block!important;padding:0}
  .toolbar{display:none}
}
"""


def _banner_class(code: str) -> str:
    return {"pass": "b-pass", "review": "b-review", "fail": "b-fail"}.get(code, "b-review")


def _donut_svg(pct, min_ratio=None) -> str:
    """覆盖率环形图（内联 SVG，零依赖）。pct 为 None 时画空环。"""
    import math
    r = 54
    circ = 2 * math.pi * r
    p = 0.0 if pct is None else max(0.0, min(1.0, float(pct)))
    dash = circ * p
    color = "#3b6d11" if (min_ratio is None or p >= float(min_ratio)) else "#a32d2d"
    label = "—" if pct is None else f"{p * 100:.0f}%"
    tick = ""
    if min_ratio is not None:
        ang = 2 * math.pi * float(min_ratio)
        x1 = 70 + r * math.cos(ang)
        y1 = 70 + r * math.sin(ang)
        x2 = 70 + (r + 9) * math.cos(ang)
        y2 = 70 + (r + 9) * math.sin(ang)
        tick = (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                f'stroke="#854f0b" stroke-width="2"/>')
    return (
        f'<svg viewBox="0 0 140 140" width="140" height="140" role="img" aria-label="审计覆盖率">'
        f'<circle cx="70" cy="70" r="{r}" fill="none" stroke="#e8e6df" stroke-width="12"/>'
        f'<circle cx="70" cy="70" r="{r}" fill="none" stroke="{color}" stroke-width="12" '
        f'stroke-linecap="round" stroke-dasharray="{dash:.1f} {circ - dash:.1f}" '
        f'transform="rotate(-90 70 70)"/>'
        f'{tick}'
        f'<text x="70" y="66" text-anchor="middle" font-size="22" font-weight="600" fill="{color}">{label}</text>'
        f'<text x="70" y="86" text-anchor="middle" font-size="11" fill="#5f5e5a">审计覆盖率</text>'
        f'</svg>'
    )


def render_html(res: dict) -> str:
    """审计凭证（单文件 HTML，内联 CSS/SVG，零外部依赖，断网可开）。

    安全硬要求：所有动态内容一律 html.escape —— 报告原文/上下文/SQL 都是外部输入，
    少转一处就是自伤（这份文件还要发给人看）。
    """
    import html as _h
    E = lambda v: _h.escape("" if v is None else str(v))  # noqa: E731

    cov = res.get("coverage")
    pol = res.get("policy") or {}
    env = res.get("env") or {}
    inputs = res.get("inputs") or {}
    outs = res.get("outputs") or {}
    matched = res.get("matched") or []
    recomputed = res.get("recomputed") or {}
    issues = res.get("issues") or []
    fails = [i for i in issues if i.get("level") == "fail"]
    revs = [i for i in issues if i.get("level") == "review"]
    code = _verdict_code(res.get("verdict"))
    min_ratio = res.get("pol_min_ratio")

    P = []
    P.append('<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">')
    P.append('<meta name="viewport" content="width=device-width,initial-scale=1">')
    P.append(f'<title>审计凭证 · {E(res.get("report_name"))} · {E(res.get("audit_id"))}</title>')
    P.append(f'<style>{HTML_CSS}</style></head><body><div class="page">')

    # ── 标题 + ① 结论横幅 ────────────────────────────────────────
    P.append(f'<h1>数字审计凭证 · {E(res.get("report_name"))}</h1>')
    P.append('<div class="meta">'
             f'<span>审计时间 <b>{E(res.get("audited_at"))}</b></span>'
             f'<span>数据截止 <b>{E(res.get("data_as_of") or "未声明")}</b></span>'
             f'<span>审计编号 <b>{E(res.get("audit_id"))}</b></span>'
             '</div>')
    bits = []
    if cov is not None:
        bits.append(f'覆盖率 {cov:.0%}（追溯 {res.get("n_matched")} / 应审 {res.get("n_should")}）')
    if fails:
        bits.append(f'拦下 {len(fails)} 条必须改')
    if revs:
        bits.append(f'{len(revs)} 条需人工复核')
    P.append(f'<div class="banner {_banner_class(code)}">'
             f'<div class="v">{E(res.get("verdict"))}</div>'
             f'<div class="s">{E("　—　".join(bits))}</div></div>')

    # ── ② 覆盖率环 + ③ 计数卡 ───────────────────────────────────
    P.append('<div class="grid">')
    P.append(_donut_svg(cov, min_ratio))
    P.append('<div class="cards">')
    cards = [
        (res.get("n_should"), "应审数字", ""),
        (res.get("n_matched"), "追溯到出处", ""),
        (res.get("n_recomputed_ok"), "复算通过", ""),
        (len(fails), "拦下必须改", "bad" if fails else ""),
        (len(revs), "需人工复核", "warn" if revs else ""),
        (res.get("n_exempt_struct"), "未纳入审计", ""),
    ]
    for n, label, cls in cards:
        P.append(f'<div class="card {cls}"><div class="n">{E(n)}</div>'
                 f'<div class="l">{E(label)}</div></div>')
    P.append('</div></div>')

    # ── ④ 检查执行情况（防空转：哪项跳过了直接显形）─────────────
    ex = res.get("exec_status") or []
    if ex:
        P.append('<h2>检查执行情况</h2>')
        P.append('<table><tr><th>检查</th><th>本次执行</th></tr>')
        for k, v in ex:
            flag = "（跳过）" if "跳过" in str(v) else ""
            P.append(f'<tr><td>{E(k)}</td><td>{E(v)}{E(flag)}</td></tr>')
        P.append('</table>')

    # ── ⑤ 拦下问题 / ⑥ 需人工复核 ──────────────────────────────
    def issue_block(title, items, cls):
        if not items:
            return
        P.append(f'<h2>{E(title)}（{len(items)} 条）</h2>')
        for it in items:
            label = _CATEGORY_LABEL.get(it.get("category"), it.get("category"))
            msg = _strip_label_prefix(str(it.get("message") or ""), str(label))
            hint = _FIX_HINTS.get(it.get("category"))
            P.append(f'<div class="issue {cls}">')
            P.append(f'<div class="t">{E(label)}：{E(msg)}</div>')
            if hint:
                P.append(f'<div class="fix">→ {E(hint)}</div>')
            P.append('</div>')

    issue_block("拦下的问题（必须改）", fails, "")
    issue_block("需人工复核（不拦，但不能当已验证）", revs, "rev")

    if res.get("hint"):
        P.append(f'<div class="warnbox"><b>线索：可能是口径不同</b><br>{E(res.get("hint"))}</div>')

    # ── ⑧ 跨件一致性矩阵（多份交付件时才有）───────────────────
    mv = _matrix_view(res)
    if mv:
        files, mrows = mv
        bad = [r for r in mrows if not r["consistent"]]
        P.append(f'<h2>跨件一致性（{len(files)} 份交付件，{len(mrows)} 个指标，'
                 f'{len(bad)} 处不一致）</h2>')
        P.append('<table><tr><th>指标（账本 ID）</th>'
                 + "".join(f'<th>{E(f)}</th>' for f in files) + '</tr>')
        for r in mrows:
            P.append(f'<tr><td>{E(r["label"])}（{E(r["ledger_id"])}）</td>')
            for f in files:
                v = r["cells"].get(f)
                cls = '" class="bad"' if (f in r.get("odd", set())) else ""
                P.append(f'<td{cls}>{E("—" if v is None else v)}</td>')
            P.append('</tr>')
        P.append('</table>')
        if bad:
            P.append('<div class="warnbox">红色格 = 同一指标在不同交付件里写法/数值不一致，'
                     '以账本为准统一后重跑。</div>')

    # ── ⑦ 全量证据（按文件分组，默认展开第一组）────────────────
    from collections import OrderedDict
    by_file: "OrderedDict[str, list]" = OrderedDict()
    for m in matched:
        by_file.setdefault(m["report"].get("file"), []).append(m)

    P.append(f'<h2>全量证据（{len(matched)} 条）</h2>')
    if matched:
        P.append('<div class="toolbar">'
                 '<button onclick="document.querySelectorAll(\'details.ev\').forEach(d=>d.open=true)">全部展开</button>'
                 '<button onclick="document.querySelectorAll(\'details.ev\').forEach(d=>d.open=false)">全部收起</button>'
                 '</div>')
    for idx, (fname, items) in enumerate(by_file.items()):
        opened = " open" if idx == 0 else ""
        P.append(f'<details class="ev"{opened}><summary>{E(fname)}（{len(items)} 条）</summary>'
                 '<div class="dbody"><table>')
        P.append('<tr><th>报告原文</th><th>位置</th><th>账本 ID</th><th>指标</th>'
                 '<th>口径</th><th>复算值</th><th>判定方式</th><th>锚定</th><th>SQL</th></tr>')
        for m in items:
            rp, lg = m["report"], m["ledger"]
            lid = str(lg.get("id"))
            rec = recomputed.get(lid)
            how = "直接命中" if m.get("how") == "exact" else "派生"
            sql = str(lg.get("sql") or "")
            sql_cell = (f'<details><summary>看 SQL</summary><pre>{E(sql)}</pre></details>'
                        if sql else "—")
            P.append(
                f'<tr class="evrow"><td>{E(rp.get("raw"))}</td><td>{E(rp.get("loc"))}</td>'
                f'<td>{E(lid)}</td><td>{E(lg.get("label"))}</td>'
                f'<td>{E(lg.get("caliber"))}</td>'
                f'<td class="num">{"—" if rec is None else E(rec)}</td>'
                f'<td>{E(how)}</td><td>{E(m.get("anchor") or "")}</td>'
                f'<td>{sql_cell}</td></tr>')
        P.append('</table></div></details>')

    # ── ⑧ 未纳入审计的数字 ─────────────────────────────────────
    exs = res.get("exempt_summary") or {}
    if exs or res.get("exempt"):
        P.append('<h2>未纳入审计的数字</h2>')
        if exs:
            P.append('<table><tr><th>类别</th><th>个数</th></tr>')
            for k, v in exs.items():
                P.append(f'<tr><td>{E(k)}</td><td class="num">{E(v)}</td></tr>')
            P.append('</table>')
        P.append('<div class="warnbox">这些按规则不算指标（日期/序号/年份等）。'
                 '若其中有本该审计的关键数字，请写进账本，否则它不在覆盖范围内。</div>')

    # ── ⑨ 凭证元信息 ───────────────────────────────────────────
    P.append('<h2>凭证元信息</h2>')
    P.append('<table class="kv">')
    rows = [
        ("审计编号", res.get("audit_id")),
        ("技能版本", env.get("skill_version")),
        ("Python", env.get("python")),
        ("duckdb", env.get("duckdb")),
        ("操作系统", env.get("os")),
        ("审计策略", f'{os.path.basename(str(pol.get("source") or ""))}'
                   f'（hash {pol.get("hash")}｜舍入 {pol.get("rounding")}）'),
        ("账本文件", (inputs.get("ledger") or {}).get("path")),
        ("账本 hash", (inputs.get("ledger") or {}).get("sha256_16")),
        ("报告文件", "、".join(
            f'{f.get("path")}（{f.get("sha256_16")}）'
            for f in (inputs.get("report_files") or [])) or "—"),
        ("复现命令", res.get("reproduce_cmd") or "—"),
    ]
    for k, v in rows:
        P.append(f'<tr><td>{E(k)}</td><td><code>{E(v)}</code></td></tr>')
    P.append('</table>')

    # ── ⑩ 局限 ─────────────────────────────────────────────────
    P.append('<h2>局限</h2>')
    P.append('<ul style="margin-left:20px;font-size:13px">')
    P.append('<li>只证明「报告里的数字 = 账本里的数字」，<b>不证明账本口径选得对</b></li>')
    P.append('<li>账本本身口径若有误，复算同样会通过</li>')
    n_ver = res.get("n_verifiable") or 0
    n_ok = res.get("n_recomputed_ok") or 0
    P.append(f'<li>{"本次全部可复算条目均已复算" if n_ok >= n_ver else f"本次有 {n_ver - n_ok} 条未复算"}</li>')
    P.append('</ul>')

    # ── ⑪ 页脚 ─────────────────────────────────────────────────
    P.append(f'<footer><span>含内部口径与 SQL 原文，<b>仅限内部使用</b>，不随报告外发</span>'
             f'<span>{E(res.get("audit_id"))} · rla_audit {E(env.get("skill_version"))}</span></footer>')
    P.append('</div></body></html>')
    return "".join(P)


def _matrix_view(res: dict):
    """跨件矩阵视图：(files, rows) 或 None（不足 2 份交付件时不出矩阵）。

    判定用归一化写法 _norm_form（与既有闸门3 check_cross_file 同口径），
    显示用原文 —— 人认得出，机器判得准。
    """
    m = res.get("matrix") or []
    files: list[str] = []
    for row in m:
        for f in row.get("cells") or {}:
            if f not in files:
                files.append(f)
    if len(files) < 2:
        return None
    rows = []
    for row in m:
        cells_map = row.get("cells") or {}
        if len(cells_map) < 2:      # 只在一份文件里出现的指标，没有可比性
            continue
        cells, forms = {}, set()
        for f in files:
            items = cells_map.get(f) or []
            if not items:
                cells[f] = None
                continue
            raw = items[0].get("raw")
            cells[f] = raw
            forms.add(_norm_form(str(raw)))
        # 标出「少数派」：以多数写法为基准，只标少数那份；
        # 若两派各占一半（1:1），无法判断谁对 → 两列都标，别假装知道答案。
        from collections import Counter
        cnt = Counter(_norm_form(str(cells[f])) for f in files if cells[f] is not None)
        odd: set = set()
        if cnt:
            top = max(cnt.values())
            major = {k for k, v in cnt.items() if v == top}
            tie = len(major) > 1
            for f in files:
                if cells[f] is None:
                    continue
                if tie or _norm_form(str(cells[f])) not in major:
                    odd.add(f)
        rows.append({"ledger_id": row.get("ledger_id"), "label": row.get("label"),
                     "cells": cells, "consistent": len(forms) <= 1, "odd": odd})
    if not rows:
        return None
    return files, rows


def _suggest_sql(ledger: dict, u: dict) -> str:
    """给待补条目一条可填空的 SQL 模板。

    刻意不猜列名：猜错比不给更糟（会让人以为"填上去就对了"）。
    表名从账本已有 SQL 里取第一个 FROM，取不到就用占位符。
    """
    tables = []
    for n in ledger.get("numbers") or []:
        m = re.search(r"\bFROM\s+([A-Za-z_][\w.]*)", str(n.get("sql") or ""), re.I)
        if m and m.group(1) not in tables:
            tables.append(m.group(1))
    t = tables[0] if tables else "<表名>"
    return ("-- 待补：报告里出现 {raw}（{file} {loc}）\n"
            "-- 把 <列名>/<条件> 换成你的实际字段；跑通后把值填进 value、把这条 SQL 填进 sql\n"
            "SELECT round(sum(<列名>), 2) FROM {t} WHERE <条件>").format(
                raw=u.get("raw"), file=u.get("file"), loc=u.get("loc"), t=t)


def render_md(res: dict) -> str:
    """人读的结论报告（v3.5.0 重构）。

    与 3.4.5 的区别：
      - 判定依据说人话（不再是 12 行计数表）
      - 拦下的问题**带改法**（不只是"错了"）
      - 证据只留最该看的 5 条（3.4.5 是"按匹配顺序的前 40 条"，纯噪音）
      - 末尾必须有局限声明（可信度的一部分）
    全量证据在 audit.html / evidence.csv，不在 md 里堆。
    """
    L = []
    cov = res.get("coverage")
    pol = res.get("policy") or {}
    outs = res.get("outputs") or {}
    N = lambda k: res.get(k, 0)  # noqa: E731

    # ── ① 一句话结论 ────────────────────────────────────────────
    L.append(f'# 数字审计结论 · {res["report_name"]}')
    L.append("")
    bits = []
    if cov is not None:
        bits.append(f'覆盖率 {cov:.0%}（追溯 {N("n_matched")} / 应审 {N("n_should")}）')
    problems = res.get("problems") or []
    reviews = res.get("reviews") or []
    if problems:
        bits.append(f"拦下 {len(problems)} 条必须改")
    if reviews:
        bits.append(f"{len(reviews)} 条需人工复核")
    L.append("## 一句话结论")
    L.append("")
    L.append(f'**{res["verdict"]}**' + ("　—　" + "，".join(bits) if bits else ""))
    L.append("")

    # ── ② 判定依据（说人话）─────────────────────────────────────
    L.append("## 判定依据")
    L.append("")
    L.append("| 项 | 结果 |")
    L.append("|---|---|")
    n_exempt = N("n_exempt_struct")
    L.append(f'| 应审数字 | {N("n_should")} 个'
             + (f'（另有 {n_exempt} 个日期/序号/年份，按规则豁免）' if n_exempt else "") + " |")
    L.append(f'| 追溯到出处 | {N("n_matched")} 个'
             f'（指标 {N("n_matched_indicator")} / 支撑数据 {N("n_matched_support")}） |')
    rec_ok, n_ver = N("n_recomputed_ok"), N("n_verifiable")
    L.append(f'| 复算（重跑 SQL 对数） | {rec_ok} / {n_ver} 条'
             + ("" if rec_ok == n_ver else "　⚠️ 有未复算") + " |")
    L.append(f'| 来源不明 | {N("n_unmatched")} 个 |')
    L.append(f'| 弱锚定（值对得上、但上下文说不清） | {N("n_weak")} 个 |')
    L.append(f'| 无法判定（上下文锚不住） | {N("n_ambiguous")} 个 |')
    ex = res.get("exec_status") or []
    if ex:
        L.append(f'| 检查执行情况 | {"｜".join(f"{k} {v}" for k, v in ex)} |')
    min_ratio = res.get("pol_min_ratio")
    if min_ratio is not None and cov is not None:
        flag = "✅ 达标" if cov >= min_ratio else "❌ 未达红线"
        L.append(f"| 覆盖率红线 | {min_ratio:.0%}（本次 {cov:.0%}，{flag}） |")
    L.append("")

    # ── ③ 拦下的问题（必须改，带改法）───────────────────────────
    fails = [i for i in (res.get("issues") or []) if i.get("level") == "fail"]
    if fails:
        L.append("## 拦下的问题（必须改）")
        L.append("")
        for n, it in enumerate(fails, 1):
            label = _CATEGORY_LABEL.get(it["category"], it["category"])
            L.append(f'{n}. **{label}**：{_strip_label_prefix(it["message"], label)}')
            hint = _FIX_HINTS.get(it["category"])
            if hint:
                L.append(f'   > 怎么改：{hint}')
        L.append("")

    # ── ④ 需人工复核（不拦，但不能当已验证）─────────────────────
    revs = [i for i in (res.get("issues") or []) if i.get("level") == "review"]
    if revs:
        L.append("## 需人工复核（不拦，但不能当已验证）")
        L.append("")
        for n, it in enumerate(revs, 1):
            label = _CATEGORY_LABEL.get(it["category"], it["category"])
            L.append(f'{n}. **{label}**：{_strip_label_prefix(it["message"], label)}')
            hint = _FIX_HINTS.get(it["category"])
            if hint:
                L.append(f'   > 建议：{hint}')
        L.append("")

    # ── 跨件矩阵（多份交付件时才有）─────────────────────────────
    mv = _matrix_view(res)
    if mv:
        files, mrows = mv
        bad = [r for r in mrows if not r["consistent"]]
        L.append(f'## 跨件一致性（{len(files)} 份交付件，{len(mrows)} 个指标）')
        L.append("")
        L.append("| 指标（账本 ID） | " + " | ".join(files) + " |")
        L.append("|---" * (len(files) + 1) + "|")
        show = bad + [r for r in mrows if r["consistent"]][:5]
        for r in show:
            cells = []
            for f in files:
                v = r["cells"].get(f)
                if v is None:
                    cells.append("—")
                elif r["consistent"]:
                    cells.append(str(v))
                elif f in r.get("odd", set()):
                    cells.append(f"**{v}** ❌")
                else:
                    cells.append(str(v))
            L.append(f'| {r["label"]}（{r["ledger_id"]}） | ' + " | ".join(cells) + " |")
        if len(show) < len(mrows):
            L.append(f'| … | ' + " | ".join(["　"] * len(files)) + " |")
            L.append("")
            L.append(f'> 完整矩阵（{len(mrows)} 行）见 audit.html')
        L.append("")
        L.append(f'**{len(bad)} 处不一致**' if bad else "**全部一致**")
        L.append("")

    hint = res.get("hint")
    if hint:
        L.append("## 🧭 线索：可能是口径不同")
        L.append("")
        L.append(hint)
        L.append("")

    # ── ⑤ 最该看的 5 条证据（全量在 html / csv）────────────────
    matched = res.get("matched") or []
    if matched:
        L.append(f'## 最该看的 5 条证据（全量 {len(matched)} 条见「证据去哪看」）'
                 if len(matched) > 5 else f'## 已追溯的数字（{len(matched)} 条）')
        L.append("")
        L.append("| 报告里的数 | 位置 | 出处 | 方式 | 复算值 |")
        L.append("|---|---|---|---|---|")
        recomputed = res.get("recomputed") or {}
        for m in matched[:5]:
            rp, lg = m["report"], m["ledger"]
            lid = str(lg.get("id"))
            how = "直接命中" if m.get("how") == "exact" else f'派生（{lg.get("caliber")}）'
            rec = recomputed.get(lid)
            L.append(f'| {rp.get("raw")} | {rp.get("file")}:{rp.get("loc")} | '
                     f'{lg.get("label")}（{lid}） | {how} | '
                     f'{"—" if rec is None else rec} |')
        L.append("")

    # ── ⑥ 覆盖情况 ─────────────────────────────────────────────
    L.append("## 覆盖情况（查了多少、没查什么）")
    L.append("")
    if cov is not None:
        L.append(f'- 审计覆盖率：{cov:.0%}（追溯 {N("n_matched")} / 应审 {N("n_should")}）')
    else:
        L.append("- 审计覆盖率：—（报告里没有像数据的数字）")
    exs = res.get("exempt_summary") or {}
    if exs:
        L.append("- 未纳入审计：" + "、".join(f"{k} {v}" for k, v in exs.items())
                 + "（这些不是指标，默认豁免；若其中有本该审计的数字，请写进账本）")
    skipped = [f"{k} {v}" for k, v in (res.get("exec_status") or []) if "跳过" in str(v)]
    L.append("- 跳过的检查：" + ("；".join(skipped) if skipped else "无"))
    L.append("")

    # ── ⑦ 口径与来源 ───────────────────────────────────────────
    L.append("## 口径与来源")
    L.append("")
    if pol:
        L.append(f'- 审计策略：{os.path.basename(str(pol.get("source")))}'
                 f'（hash {pol.get("hash")}｜舍入 {pol.get("rounding")}）')
    L.append(f'- 数据截止：{res.get("data_as_of") or "未声明"}')
    L.append(f'- 报告文件：{", ".join(res.get("files") or []) or "（无）"}')
    L.append(f'- 审计编号：{res.get("audit_id") or "—"}')
    L.append("")

    # ── ⑧ 证据去哪看 ───────────────────────────────────────────
    L.append("## 证据去哪看")
    L.append("")
    if outs.get("audit_html"):
        L.append(f'- **审计凭证页面**（全量 {len(matched)} 条证据，可点开、含 SQL 与复算值）'
                 f'→ `{outs["audit_html"]}`')
    L.append(f'- **一行一个数字**（Excel 可筛可排序）→ `{outs.get("evidence_csv") or "evidence.csv"}`')
    if outs.get("manifest_json") or outs.get("evidence_csv"):
        L.append(f'- **机检回执**（编号、环境、输入 hash、复现命令）→ `manifest.json`')
    L.append("")

    # ── ⑨ 局限（必须写）────────────────────────────────────────
    L.append("## 局限")
    L.append("")
    L.append("- 只证明「报告里的数字 = 账本里的数字」，**不证明账本口径选得对**")
    L.append("- 账本本身口径若有误，复算同样会通过 —— 口径对不对，得人或上游定义来保证")
    if rec_ok < n_ver:
        L.append(f"- 本次有 {n_ver - rec_ok} 条未复算（没给数据源），这部分算术没验过")
    else:
        L.append("- 本次全部可复算条目均已复算")
    L.append("")
    L.append("---")
    L.append("")
    L.append("> 由 rla_audit 生成。判定规则：只对「被识别为指标」的数字要求可追溯；"
             "账本里 `verifiable:false` 的条目视为未验证（不计入通过）。")
    return "\n".join(L)


# ---------------------------------------------------------------- 主流程
def main() -> int:
    import deps_check as DC
    DC.banner(allow_degrade=True)   # 依赖体检（没有 duckdb 也能用 --command 走完）
    ap = argparse.ArgumentParser(description="报告数字审计")
    ap.add_argument("--ledger", required=True)
    ap.add_argument("--files", nargs="*", default=None, help="覆盖账本里的报告文件")
    ap.add_argument("--mount", action="append", default=[], help='"视图名=路径"，可重复')
    ap.add_argument("--gateway", default=None, help="用取数网关脚本复算（--sql/--out 协议）")
    ap.add_argument("--command", default=None,
                    help="通用取数复算：SQL 从 stdin 进、CSV 从 stdout 出"
                         "（没有 duckdb 时用它；cmd_sqlite.py 就是现成例子）")
    ap.add_argument("--out", default=None, help="结论输出路径（默认与账本同目录 audit.md）")
    ap.add_argument("--no-write", action="store_true")
    ap.add_argument("--no-html", action="store_true",
                    help="不写 audit.html（审计凭证页面）")
    ap.add_argument("--no-manifest", action="store_true",
                    help="不写 manifest.json 与 evidence.csv（机检档案）。默认写：它们是凭证，不是装饰")
    ap.add_argument("--policy", default=None, help="审计策略 YAML（默认：技能根 policy.yaml，没有就用内置默认）")
    ap.add_argument("--json", action="store_true", help="同时打印机器可读摘要")
    ap.add_argument("--export-missing", default=None,
                    help="把「报告里有、账本没有」的数字导出成待补账本（JSON），交给报告方补全")
    args = ap.parse_args()

    pol_path = args.policy
    if pol_path is None:
        cand = HERE.parent / PL.POLICY_NAME
        pol_path = cand if cand.exists() else None
    try:
        pol = PL.load(pol_path)
    except PL.PolicyError as e:
        print(f"❌ 未就绪：策略有问题 —— {e}", file=sys.stderr)
        return 2

    lp = Path(args.ledger)
    if not lp.exists():
        print(f"❌ 未就绪：账本不存在 {lp}", file=sys.stderr)
        return 2
    try:
        ledger = json.loads(lp.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as e:
        print(f"❌ 未就绪：账本不是合法 JSON：{e}", file=sys.stderr)
        return 2

    # 账本里的 report.files 是元信息；用 --files 显式指定时以命令行为准。
    # 有些账本（尤其 rla_ledger 从定义生成、deliverables 没配的）files 是空的，
    # 这时不该因为元信息缺失就判"账本不合格" —— 补齐后再校验。
    if args.files and isinstance(ledger, dict):
        _rep = ledger.get("report")
        if isinstance(_rep, dict) and not _rep.get("files"):
            _rep["files"] = [Path(f).name for f in args.files]

    errs, warns = validate(ledger)
    if errs:
        print("❌ 未就绪：账本不合格（不算通过）", file=sys.stderr)
        for e in errs:
            print("   " + e, file=sys.stderr)
        return 2

    rep = ledger["report"]
    files = args.files if args.files is not None else rep.get("files") or []
    base = lp.parent
    paths = [(base / f) if not Path(f).is_absolute() else Path(f) for f in files]
    missing = [p for p in paths if not p.exists()]
    if missing:
        # 区分两种"找不到"：真不存在 vs 按账本目录解析后不存在（后者的报错最误导人）
        msgs = []
        for p in missing:
            if Path(p.name).exists():
                msgs.append(f"{p}（文件在 CWD 存在，但按账本目录 {base} 解析后找不到——"
                            f"请用绝对路径，或改成相对账本目录的写法）")
            else:
                msgs.append(str(p))
        print("❌ 未就绪：报告文件不存在：" + "；".join(msgs), file=sys.stderr)
        return 2
    if not paths:
        print("❌ 未就绪：没有报告文件可审（report.files 为空）", file=sys.stderr)
        return 2

    mounts = {}
    for m in args.mount:
        if "=" not in m:
            print(f'❌ --mount 格式应为 "视图名=路径"：{m}', file=sys.stderr)
            return 2
        k, v = m.split("=", 1)
        mounts[k.strip()] = v.strip()

    problems: list[str] = []
    # 先验证账本里声明的派生（声明 + 验证，不搜索）
    derr = verify_derived(ledger, pol)
    problems.extend(derr)
    try:
        rec_errs, recomputed = recompute(ledger, mounts, args.gateway, pol, args.command)
    except NotReady as e:
        print(f"❌ 未就绪：{e}", file=sys.stderr)
        return 2
    problems.extend(rec_errs)

    # 抽数字（同时收集"扫不到"的提示，例如 PPT 内图片）
    all_nums, extract_warns = [], []
    for p in paths:
        try:
            nums, warns = rla_extract.extract_with_warnings(p)
        except SystemExit as e:
            print(f"❌ 未就绪：{e}", file=sys.stderr)
            return 2
        all_nums.extend(nums)
        extract_warns.extend(warns)
    from collections import Counter
    # v3.5.0：豁免项要留明细（不只是计数），否则 evidence.csv 里「未纳入审计的数字」查不到
    exempt_nums = [n for n in all_nums if n["kind"] != "metric"]
    exempt = Counter(n["kind"] for n in exempt_nums)
    metric_nums = [n for n in all_nums if n["kind"] == "metric"]

    matched, unmatched, ambiguous, weak = pair(metric_nums, ledger, pol)

    # 覆盖率（2026-10-26 方案 A）：分母扣掉"明确不是数据的"（日期/序号/年份），
    # 剩下的都是"看着像数据"的数字——它们才该有出处。
    n_exempt_struct = sum(v for k, v in exempt.items() if k in ("date", "ordinal", "year"))
    n_should = len(all_nums) - n_exempt_struct
    coverage = (len(matched) / n_should) if n_should > 0 else None

    verifiable = [n for n in ledger["numbers"] if n.get("verifiable", True)]
    res = {
        "report_name": rep.get("name"),
        "audited_at": now(),
        "data_as_of": rep.get("data_as_of"),
        "files": [p.name for p in paths],
        "n_ledger": len(ledger["numbers"]),
        "n_verifiable": len(verifiable),
        "n_recomputed_ok": len(recomputed),
        "n_extracted": len(all_nums),
        "n_metric": len(metric_nums),
        "n_matched": len(matched),
        "n_matched_indicator": sum(1 for m in matched if m.get("role", "indicator") == "indicator"),
        "n_matched_support": sum(1 for m in matched if m.get("role") == "support"),
        "n_unmatched": len(unmatched),
        "n_ambiguous": len(ambiguous),
        "n_weak": len(weak),
        "n_exempt_struct": n_exempt_struct,
        "n_should": n_should,
        "coverage": coverage,
        "weak": weak,          # v3.5.0：不在这里截断（截断移到渲染层），否则 html/csv 永远拿不全
        "ambiguous": ambiguous,
        "problems": problems,
        "unmatched": unmatched,
        "matched": matched,
        "exempt_summary": dict(exempt),
        "exempt": [{"raw": n.get("raw"), "file": n.get("file"), "loc": n.get("loc"),
                    "kind": n.get("kind")} for n in exempt_nums],
    }
    # ---- 打类别，交 policy 决定算 FAIL 还是 REVIEW ----
    categorized: list[tuple[str, str]] = []
    for e in problems:
        categorized.append(("ledger_mismatch", e))
    for u in unmatched:
        categorized.append(("unmatched_number", f'来源不明：{u["raw"]} @ {u["file"]} {u["loc"]}'))
    # ── 闸门6 数据快照（账本是否过期）──────────────────────────
    # v3.6.0：账本记了 data_fingerprint 就说明它绑定了一版数据。
    # 数据文件变了没重算 → 账本里的数字是旧的，必须拦（否则审的是历史快照）
    _fp_recorded = (rep.get("data_fingerprint") or {}) if isinstance(rep, dict) else {}
    if _fp_recorded:
        try:
            import rla_render as _RR
            _cur = _RR._current_fingerprint(lp)
        except Exception:  # noqa: BLE001
            _cur = None
        _d = lambda x: str(x.get("digest") or "") if isinstance(x, dict) else str(x or "")  # noqa: E731
        if _cur is not None:
            _a, _b = _d(_fp_recorded), _d(_cur)
            if _a != _b:
                categorized.append((
                    "snapshot_mismatch",
                    f"账本指纹 {_a[:16]}… ≠ 当前数据 {_b[:16]}…：账本已过期"))

    # ── 闸门7 占位符闭合（[[id]] 必须都能对上账本，成品里不许残留）──
    _ID_RE = re.compile(r"\[\[\s*(P:)?\s*([\w.\-]+)\s*\]\]")
    _known = {str(n.get("id")) for n in ledger.get("numbers") or []}
    _used: set[str] = set()
    for _p in paths:
        try:
            _txt = _p.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        _hits = _ID_RE.findall(_txt)
        if _hits:
            # 成品里还留着 [[id]] → 忘了渲染，交出去就是模板
            categorized.append((
                "unrendered_placeholder",
                f"{_p.name} 里残留 {len(_hits)} 个 [[id]] 占位符（未渲染）"))
        _used |= {m[1] for m in _hits}
    # 也从 ledger.yaml 的 deliverables 收集引用（成品可能不在 --files 里）
    _cfgy = lp.parent / "ledger.yaml"
    if _cfgy.exists():
        try:
            import yaml as _yaml
            _cfg = _yaml.safe_load(_cfgy.read_text(encoding="utf-8-sig")) or {}
            for _rel in (_cfg.get("deliverables") or []) + (_cfg.get("templates") or []):
                _q = Path(_rel) if Path(_rel).is_absolute() else (lp.parent / _rel)
                if _q.exists():
                    _used |= {m[1] for m in _ID_RE.findall(_q.read_text(encoding="utf-8", errors="ignore"))}
        except Exception:  # noqa: BLE001
            pass
    if _used:
        _missing = sorted(_used - _known)
        if _missing:
            categorized.append((
                "unrendered_placeholder",
                f"用了没算：交付件引用了账本里没有的指标 {_missing[:6]}"))
        _unused = sorted(_known - _used)
        if _unused:
            categorized.append((
                "metric_unused",
                f"算了没用（WARN）：{len(_unused)} 条指标未被任何交付件引用 {_unused[:6]}"))

    # 闸门4 必现 / 闸门5 泄漏
    checks = pol.get("checks") or {}
    for msg in check_must(matched, checks.get("must") or [], paths):
        categorized.append(("must_missing", msg))
    for msg in check_leak(paths, checks):
        categorized.append(("leak", msg))

    # 闸门3：跨件一致（多份交付件不能各说一套）
    if len({p.name for p in paths}) > 1:
        for lid, label, detail in check_cross_file(matched):
            categorized.append(("cross_file_mismatch",
                                f'跨件不一致：{label}（{lid}）在各件写法不同 —— {detail}'))

    for wk in weak:
        rp = wk["report"]
        categorized.append(("weak_anchor",
                            f'弱锚定待补：{rp["raw"]} @ {rp["file"]} {rp["loc"]}'
                            f'（账本里值唯一，但上下文没说清是哪个指标）'))
    for a in ambiguous:
        rp = a["report"]
        names = "、".join(str(c.get("label", c.get("id"))) for c in a["cands"])
        categorized.append(("ambiguous_number",
                            f'无法判定：{rp["raw"]} @ {rp["file"]} {rp["loc"]}'
                            f'（上下文锚不住，可能对应 {names}）'))

    verifiable_nums = [n for n in ledger["numbers"] if n.get("verifiable", True) and n.get("sql")]
    if verifiable_nums and not mounts and not args.gateway and not args.command:
        categorized.append(("not_recomputed",
                            f"账本有 {len(verifiable_nums)} 条可复算数字，但本次未复算"
                            "（加 --mount 或 --gateway 才能核验算术）"))
    unver = [n for n in ledger["numbers"] if n.get("verifiable") is False]
    if unver:
        orgs = "；".join(f'{n["id"]}:{n.get("origin", "未说明")}' for n in unver[:5])
        categorized.append(("unverifiable_entry", f"账本有 {len(unver)} 条声明为不可复算（{orgs}）"))
    for w in extract_warns:
        categorized.append(("unscanned_image", f"未覆盖：{w}"))

    # ── 覆盖率闸门（方案 A，2026-10-26）：没有可查的东西 ≠ 全都查过了
    #    背景：判"这个数字要不要追"靠词表。词表外的说法会被当成杂项豁免，
    #    实测同一份报告只把「总行数」改成「样本池规模」，4 个数字全被豁免、结论仍显示 ✅ 通过。
    #    这条闸门不改"查什么"，只保证结论不说谎：审得太少就不许说通过。
    cov_cfg = pol.get("coverage") or {}
    min_ratio = float(cov_cfg.get("min_ratio", 0.9))
    min_metric = int(cov_cfg.get("min_metric", 1))
    if n_should > 0 and len(metric_nums) < min_metric:
        categorized.append(("no_metric",
                            f"这次没有任何数字被认定为「指标」（抽到 {len(all_nums)} 个数字，"
                            f"其中 {n_should} 个看着像数据）。没有可查的东西不等于全都查过了，"
                            "不能算通过——请换用更常见的说法，或把这些数字写进账本"))
    elif coverage is not None and coverage < min_ratio:
        miss = n_should - len(matched)
        big_misc = sum(1 for n in all_nums
                       if n["kind"] == "misc" and rla_extract.looks_like_data(n.get("raw", "")))
        extra = f"（其中 {big_misc} 个是千分位/百分比/上千的大数，最该有出处）" if big_misc else ""
        categorized.append(("low_coverage",
                            f"审计覆盖率 {coverage:.0%}（追溯 {len(matched)} / 应审 {n_should}）"
                            f"低于 {min_ratio:.0%}：还有 {miss} 个数字没查到出处{extra}"))

    hint = date_mismatch_hint(paths, rep.get("data_as_of", ""))
    if hint and unmatched:
        categorized.append(("unmatched_number", f"[线索] {hint}"))

    fails, reviews, dropped = _sort_by_policy(categorized, pol)
    # 抓到了、却没在 policy 的 fail/review 里归类 → 绝不能静默丢弃。
    # 这是"盖空章"的另一种形态：检查跑了、结果没人看、结论照样说通过。
    # 保守处理：不判失败，但也绝不判通过 —— 降为需人工复核，并把内容列出来。
    res["dropped"] = dropped
    res["reviews"] = reviews
    res["hint"] = hint if unmatched else None
    res["policy"] = {"source": pol.get("_source") or "内置默认", "hash": pol["_hash"],
                     "rounding": pol["numeric"]["rounding"]}
    # ── 交付层数据（v3.5.0 Step 1）──────────────────────────────────
    # 只加字段，不动任何判定量（verdict / exit_code / fails / reviews / dropped / 各 n_*）。
    res["recomputed"] = dict(recomputed)          # 账本 id → 复算值
    res["matrix"] = _build_matrix(matched)        # 跨件矩阵数据
    res["pol_min_ratio"] = float((pol.get("coverage") or {}).get("min_ratio", 0.9))
    _fset, _rset = set(fails), set(reviews)
    res["issues"] = [                             # 结构化问题清单：类别 + 级别 + 原文
        {"category": c, "message": m,
         "level": ("fail" if m in _fset else "review" if m in _rset else "dropped")}
        for c, m in categorized
    ]
    _pol_src = str(pol.get("_source") or "")
    _pol_is_file = bool(_pol_src) and os.path.exists(_pol_src)
    res["inputs"] = {
        # _abs 只用于 integrity 自检（要能读到文件），对外输出前一律剥掉；
        # path / source 一律只留文件名 —— 回执可能外发，不能带目录结构
        "ledger": {"path": lp.name, "_abs": str(lp), "sha256_16": _sha16(lp)},
        "policy": {"source": os.path.basename(_pol_src) if _pol_is_file else (_pol_src or "内置默认"),
                   "_abs": _pol_src if _pol_is_file else "",
                   "sha256_16": _sha16(_pol_src) if _pol_is_file else ""},
        "report_files": [{"path": p.name, "_abs": str(p), "sha256_16": _sha16(p)} for p in paths],
    }
    res["env"] = _env_info()
    res["audit_id"] = _audit_id(res.get("data_as_of"), lp)
    res["reproduce_cmd"] = _sanitize_argv(sys.argv)   # md/html/manifest 共用，只算一次
    # ── 检查自检：哪些检查真跑了、哪些跳过了（一眼看出"空转"）
    checks_cfg = pol.get("checks") or {}
    leaks_on = bool(checks_cfg.get("leak_rules")) and bool(checks_cfg.get("leak_patterns"))
    client_files = [p for p in paths
                    if any(__import__("fnmatch").fnmatch(p.name, pat)
                           for pat in (checks_cfg.get("leak_patterns") or []))]
    exec_status = [
        ("复算", f"{len(recomputed)}/{len(verifiable_nums)}" if (mounts or args.gateway or args.command)
                 else f"跳过（未给数据源，{len(verifiable_nums)} 条待复算）"),
        ("跨件一致", f"{len(paths)} 份" if len(paths) > 1 else "跳过（仅 1 份文件）"),
        ("必现", f"{len(checks_cfg.get('must') or [])} 条"
                 if checks_cfg.get("must") else "跳过（未配置 must）"),
        ("泄漏", f"{len(client_files)} 份客户版" if leaks_on
                 else ("跳过（识别到客户版但没配规则）" if client_files else "跳过（未识别到客户版）")),
    ]
    res["exec_status"] = exec_status
    res["verdict"], exit_code = PL.decide(fails, reviews, pol)
    res["exit_code"] = exit_code          # v3.5.0：manifest 要用（只是把已有值存下来，不参与判定）
    if dropped and exit_code == 0:
        # 有检查结果没被归类 → 不能当"通过"（策略配置漏了，不该让问题混过去）
        res["verdict"], exit_code = "⚠️ 需人工复核", 3
        res["reviews"] = list(reviews) + [
            f"策略未归类（policy.verdict 里缺这些类别，本次按「需复核」处理）：{d}" for d in dropped
        ]

    # 导出待补账本：不是放行，是把"该补什么"明确交给报告方
    if args.export_missing:
        out = Path(args.export_missing)
        # v3.5.0：ambigubous 也要进清单（原来只收 unmatched），
        # 且**保留 report-ledger/1.0** 结构 —— 导出的东西必须能被 --ledger 直接读回。
        todo = [(u, "unmatched") for u in unmatched] + \
               [(a["report"], "ambiguous") for a in ambiguous]
        missing = []
        for i, (u, kind) in enumerate(todo, 1):
            missing.append({
                "id": f"m{i}", "label": "", "value": u.get("value"),
                "unit": u.get("unit_hint") or "", "role": "support",
                "caliber": "", "verifiable": False,
                "origin": (f"待补（{kind}）：出现在 {u.get('file')} {u.get('loc')}，"
                           f"上下文「{(u.get('context') or '')[:40]}」"),
                "suggest_sql": _suggest_sql(ledger, u),
            })
        out.write_text(json.dumps({
            "schema": "report-ledger/1.0",
            "purpose": "backfill-checklist",   # 标明这是「待补清单」，不是可直接审计的账本
            "report": {"name": f"{rep.get('name')} · 待补账",
                       # files 必须写实际报告文件：补完 numbers 后这个文件要能直接当账本重跑
                       "files": [Path(f).name for f in (files or rep.get("files") or [])],
                       "data_as_of": rep.get("data_as_of", ""), "generated_at": now()},
            "sources": [],
            "status": "clean" if not missing else "needs_backfill",
            "note": ("报告内所有指标均已追溯，无待补账项" if not missing
                     else f"{len(missing)} 条待补（unmatched {len(unmatched)} / "
                          f"ambiguous {len(ambiguous)}）：补 label/caliber/sql 后合并进账本"),
            "numbers": missing,
        }, ensure_ascii=False, indent=2), encoding="utf-8")
        if missing:
            print(f"\n📋 待补清单已导出：{out}（{len(missing)} 条："
                  f"来源不明 {len(unmatched)} / 无法判定 {len(ambiguous)}）")
        else:
            print(f"\n📋 待补清单已导出：{out}（status=clean：报告内所有指标均已追溯）")

    # 先定 outputs（md / html / manifest 三处引用同一份，避免各说各话），再渲染
    out = Path(args.out) if args.out else (lp.parent / "audit.md")
    res["outputs"] = {"audit_md": out.name}
    if not args.no_html:
        res["outputs"]["audit_html"] = out.with_suffix(".html").name if out.suffix else f"{out.name}.html"
    if not args.no_manifest:
        res["outputs"]["evidence_csv"] = "evidence.csv"
        res["outputs"]["manifest_json"] = "manifest.json"

    md = render_md(res)
    if not args.no_write:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(md, encoding="utf-8")
        print(md)
        print(f"\n（结论已写入 {out}）")
        if not args.no_html:
            hp = out.parent / res["outputs"]["audit_html"]
            hp.write_text(render_html(res), encoding="utf-8")
            print(f"（审计凭证已写入 {hp}（{hp.stat().st_size / 1024:.0f} KB））")
        # 审计回执：默认与结论同目录。--no-write 时一并跳过（不落任何文件）
        if not args.no_manifest:
            csv_path = out.parent / res["outputs"]["evidence_csv"]
            n_rows = write_evidence_csv(res, csv_path)
            man = build_manifest(res, sys.argv)
            mpath = out.parent / "manifest.json"
            mpath.write_text(json.dumps(man, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"（证据清单已写入 {csv_path}（{n_rows} 行））")
            print(f"（审计回执已写入 {mpath} · {man['audit_id']} · "
                  f"verdict={man['verdict']['code']} · integrity.ok={man['integrity']['ok']}）")
    else:
        print(md)

    if args.json:
        print(json.dumps({k: res[k] for k in
                          ("verdict", "n_ledger", "n_matched", "n_unmatched", "problems")},
                         ensure_ascii=False, default=str))

    for w in warns:
        print(f"⚠️  {w}", file=sys.stderr)
    return exit_code


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(130)
