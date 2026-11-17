#!/usr/bin/env python3
"""rla_render.py — 渲染层：文档取数字的唯一入口（v3.6.0）

替代 report-ledger 的 `rl_render.py`。核心不是"格式化"，而是**纪律**：

    渲染前必须校验数据快照。数据文件变了但没重算账本 → 拒绝渲染。

这样"文档里是旧数字"这类事故在**生成阶段**就被拦住，不用等到审计。

用法（在项目的生成脚本里）：

    import rla_render as RN
    RN.N("rt.ship.amt")            # 902,454,290.84（千分位）
    RN.P("rt.ship.top1_share")     # 16.9%（自动带 %）
    RN.R("rt.ship.docs")           # 6291（原值）
    RN.sub("本期发货 [[rt.ship.docs]] 单")   # 模板替换
    RN.sub("占比 [[P:rt.ship.top1_share]]")  # 百分比版

命令行：

    python3 scripts/rla_render.py --ids                 # 列出全部指标与值
    python3 scripts/rla_render.py --sub "本期 [[rt.ship.docs]] 单"
    python3 scripts/rla_render.py --verify              # 只校验快照，不过期则退出码 0

设计约束：
  · **只读账本，绝不写** —— 账本是唯一真相，渲染层不许产生新数据
  · **找不到 id 直接抛错**，不许静默返回空（否则文档里会留空白或 0）
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

ID_RE = re.compile(r"\[\[\s*(P:)?\s*([\w.\-]+)\s*\]\]")
_STATE: dict = {"numbers": None, "report": None, "path": None}


class RenderError(Exception):
    """渲染失败（数据过期、id 不存在等）。绝不吞掉。"""


# ------------------------------------------------------------------ 账本定位
def find_ledger(start: Path | None = None, max_up: int = 3) -> Path:
    """从当前目录向上找 ledger.json（最多 max_up 层）。"""
    p = (start or Path.cwd()).resolve()
    for _ in range(max_up + 1):
        cand = p / "ledger.json"
        if cand.exists():
            return cand
        if p.parent == p:
            break
        p = p.parent
    raise RenderError("找不到 ledger.json（已向上找 3 层）。"
                      "先跑 rla_ledger.py 生成账本，或用 --ledger 指定")


# ------------------------------------------------------------------ 加载与校验
def _digest_of(x) -> str:
    """指纹可能是字符串（rla_collect.fingerprint_files 的返回）或 dict（旧格式）。"""
    if isinstance(x, dict):
        return str(x.get("digest") or "")
    return str(x or "")


def _current_fingerprint(ledger_path: Path) -> str | None:
    """按账本同目录的 ledger.yaml 里 source.fingerprint.files 重算当前指纹。"""
    cfg_path = ledger_path.parent / "ledger.yaml"
    if not cfg_path.exists():
        return None
    try:
        import yaml
        cfg = yaml.safe_load(cfg_path.read_text(encoding="utf-8-sig")) or {}
    except Exception:  # noqa: BLE001
        return None
    files = ((cfg.get("source") or {}).get("fingerprint") or {}).get("files") or []
    paths = [Path(f) if Path(f).is_absolute() else (cfg_path.parent / f) for f in files]
    paths = [p for p in paths if p.exists()]
    if not paths:
        return None
    import rla_collect as RC
    return RC.fingerprint_files([str(p) for p in paths])


def load(ledger: str | Path | None = None, verify_snapshot: bool = True) -> None:
    """加载账本；verify_snapshot=True 时校验数据新鲜度。"""
    path = Path(ledger).resolve() if ledger else find_ledger()
    if not path.exists():
        raise RenderError(f"账本不存在：{path}")
    d = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(d, dict) or d.get("schema") != "report-ledger/1.0":
        raise RenderError(f"{path.name} 不是 report-ledger/1.0 账本")
    numbers = {}
    for n in d.get("numbers") or []:
        if n.get("id") is not None:
            numbers[str(n["id"])] = n
    if not numbers:
        raise RenderError(f"{path.name} 里没有任何指标")
    _STATE.update(numbers=numbers, report=d.get("report") or {}, path=path)

    if verify_snapshot:
        recorded = _digest_of((_STATE["report"] or {}).get("data_fingerprint"))
        if recorded:
            cur = _current_fingerprint(path)
            if cur and cur != recorded:
                raise RenderError(
                    "数据已变，账本过期，拒绝渲染。\n"
                    f"  账本指纹 {recorded[:16]}…\n"
                    f"  当前指纹 {str(cur)[:16]}…\n"
                    "→ 先重跑：python3 scripts/rla_ledger.py"
                )


def _need():
    if _STATE["numbers"] is None:
        load()


def ids() -> list[str]:
    _need()
    return sorted(_STATE["numbers"])


def _rec(iid: str) -> dict:
    _need()
    r = _STATE["numbers"].get(str(iid))
    if r is None:
        raise RenderError(f"账本里没有这个指标：{iid}（可用 --ids 看全部）")
    return r


# ------------------------------------------------------------------ 三个渲染函数
def R(iid: str):
    """原值（不做任何格式化）。"""
    return _rec(iid).get("value")


def N(iid: str) -> str:
    """千分位数字。元 保留 2 位；整数不带小数。"""
    r = _rec(iid)
    v = float(r.get("value"))
    u = str(r.get("unit") or "")
    if u in ("元", "金额"):
        return f"{v:,.2f}"
    if abs(v - round(v)) < 1e-9:
        return f"{int(round(v)):,}"
    return f"{v:,.2f}"


def P(iid: str) -> str:
    """百分比。账本里的值已经是百分数（pct 已 ×100），这里只补 %。"""
    r = _rec(iid)
    v = float(r.get("value"))
    return f"{v:g}%"


def sub(text: str) -> str:
    """模板替换：[[id]] → 千分位；[[P:id]] → 百分比。"""
    def rep(m: re.Match) -> str:
        is_pct, iid = bool(m.group(1)), m.group(2)
        return P(iid) if is_pct else N(iid)
    return ID_RE.sub(rep, str(text))


# ------------------------------------------------------------------ CLI
def main() -> int:
    ap = argparse.ArgumentParser(description="渲染层：从账本取数字")
    ap.add_argument("--ledger", default=None, help="账本路径（默认向上找 ledger.json）")
    ap.add_argument("--ids", action="store_true", help="列出全部指标与值")
    ap.add_argument("--sub", default=None, help="做一次模板替换并打印")
    ap.add_argument("--verify", action="store_true", help="只校验数据快照")
    ap.add_argument("--no-verify", action="store_true", help="跳过快照校验（不推荐）")
    args = ap.parse_args()

    try:
        load(args.ledger, verify_snapshot=not args.no_verify)
    except RenderError as e:
        print(f"❌ {e}", file=sys.stderr)
        return 2

    if args.verify:
        print(f"✅ 账本与数据一致：{_STATE['path']}")
        return 0
    if args.sub:
        try:
            print(sub(args.sub))
        except RenderError as e:
            print(f"❌ {e}", file=sys.stderr)
            return 2
        return 0
    if args.ids:
        for i in ids():
            r = _rec(i)
            print(f"  {i:<30}{str(r.get('value')):>18}  {r.get('unit', '')}")
        return 0

    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
