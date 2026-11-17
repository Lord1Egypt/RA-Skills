#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""host_cost.py — office-token-booster 真实宿主用量接入（隔离层，防屎山）

把「宿主平台的真实 Token / 耗时用量」接入提效账本，让 skill_tokens 从「用户自报」
升级为「宿主实测」。设计红线（与三层解耦一致）：

- 单一抽象 HostCostProvider：fetch_recent(days) -> list[CostRecord]。
- 两个实现：
    - EventCostProvider       —— 包装一次宿主回报的 event["cost"]（真实路径，
                                 在此升级为可单测的一等公民）。
    - LocalProvider  —— 只读本机宿主 的本地用量数据
                                 （~/.workbuddy/traces、workbuddy.db、usage-log.json）。
                                 仅在用户显式触发「导入宿主用量」时启用；读取**有界**
                                 （深度上限 3 层、文件数上限 2000、只认 .json/.jsonl/.log、
                                 跳过符号链接），不遍历目录外任何路径。
- 全程纯标准库、无网络、无硬编码密钥、无副作用（只读 + 纯解析）。
- 任何解析失败都降级为「跳过该条 / 返回空列表」，绝不抛异常炸掉调用方。

为何不污染内核：本模块只产出 CostRecord，由 skill_bridge / ledger_agent 在需要时
取用；diagnose / qa / report_engine 一行都不动。
"""

from __future__ import annotations

import json
import os
import sys
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Protocol, runtime_checkable

# 允许从任意目录运行（与兄弟模块一致）。
sys.path.insert(0, str(Path(__file__).resolve().parent))


@dataclass
class CostRecord:
    """一条宿主真实用量记录。

    skill_tokens / skill_minutes 来自宿主实测；task_type 为该次任务的归类
    （宿主若未提供则留 None，由调用方决定如何落到账本类型）。
    """

    date: str                         # YYYY-MM-DD
    skill_tokens: int = 0
    skill_minutes: int = 0
    model: str = ""
    task_type: Optional[str] = None
    session_id: str = ""
    source: str = "host"             # 来源标识（local_traces / event）

    def to_ledger_entry(self, *, baseline_tokens: int = 0, baseline_minutes: int = 0,
                        note: str = "") -> dict:
        """转成标准账本草稿（skill 用实测值，baseline 默认 0 待补）。

        把「宿主实测成本」直接灌进账本，让 skill_tokens 不再靠用户估算；
        baseline 仍代表「笨办法手搓成本」，平台无从获得，故默认 0、需用户补填。
        """
        return {
            "date": self.date,
            "type": self.task_type or "AI办公任务",
            "model": self.model,
            "session_id": self.session_id,
            "baseline_tokens": int(baseline_tokens),
            "skill_tokens": int(self.skill_tokens),
            "baseline_minutes": int(baseline_minutes),
            "skill_minutes": int(self.skill_minutes),
            "note": note or f"宿主实测({self.source})",
            "source": self.source,
        }


@runtime_checkable
class HostCostProvider(Protocol):
    """宿主用量提供方契约。实现只需提供 fetch_recent(days) -> list[CostRecord]。"""

    def fetch_recent(self, days: int) -> list["CostRecord"]:
        ...


def _today_iso() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def _coerce_int(v) -> int:
    if v is None:
        return 0
    try:
        return int(float(v))
    except (TypeError, ValueError):
        return 0


def _within_days(iso_date: str, days: int) -> bool:
    try:
        d = datetime.strptime(iso_date, "%Y-%m-%d")
    except (TypeError, ValueError):
        return False
    lo = datetime.now() - timedelta(days=days)
    hi = datetime.now() + timedelta(days=1)
    return lo <= d <= hi


# ─────────────────────────────────────────────────────────────
# 实现 1：事件成本（包装一次宿主回报的 event["cost"]）
# ─────────────────────────────────────────────────────────────

class EventCostProvider:
    """把单次宿主事件里的 cost 当成「最近一条」用量记录，便于单测与复用。"""

    def __init__(self, event: dict):
        self._event = event or {}

    def fetch_recent(self, days: int = 1) -> list[CostRecord]:
        cost = self._event.get("cost") or {}
        tok = _coerce_int(cost.get("skill_tokens"))
        mins = _coerce_int(cost.get("skill_minutes"))
        if tok == 0 and mins == 0:
            return []
        return [CostRecord(
            date=_today_iso(),
            skill_tokens=tok,
            skill_minutes=mins,
            model=str(cost.get("model", "") or ""),
            task_type=self._event.get("type"),
            source="event",
        )]


# ─────────────────────────────────────────────────────────────
# 实现 2：本机宿主本地用量（本机只读，无网络 / 无密钥）
# ─────────────────────────────────────────────────────────────

# 本机宿主 数据根（与 agent-analytics-report 同源）。
_LOCAL_ROOT = Path(os.path.expanduser("~")) / ".workbuddy"
_TRACES_DIR = _LOCAL_ROOT / "traces"
_DB_PATH = _LOCAL_ROOT / "workbuddy.db"
_USAGE_LOG = _LOCAL_ROOT / "usage-log.json"

# 扫描边界（隐私护栏）：宿主目录虽由用户显式授权读取，仍不允许无界遍历。
_SCAN_MAX_DEPTH = 3      # traces/<session_id>/trace_<hash>.json 需要 2 层，留 1 层余量
_SCAN_MAX_FILES = 2000   # 单次读取文件数上限，防止超大目录拖垮与过度读取
_TRACE_SUFFIXES = (".json", ".jsonl", ".log")


def _iter_trace_files(traces_dir: Path):
    """在 traces 目录下**有界**枚举可解析的 trace 文件。

    比 `rglob("*")` 多三层约束：
    1. 深度上限 `_SCAN_MAX_DEPTH`——不无限下钻；
    2. 文件数上限 `_SCAN_MAX_FILES`——达到即停；
    3. 只认 `.json/.jsonl/.log`，且**跳过符号链接**——避免链接指向目录外。

    保留对嵌套子目录的支持（真实宿主即 traces/<session_id>/trace_<hash>.json）。
    """
    found = []
    root_depth = len(traces_dir.parts)
    for dirpath, dirnames, filenames in os.walk(traces_dir, followlinks=False):
        here = Path(dirpath)
        if len(here.parts) - root_depth >= _SCAN_MAX_DEPTH:
            dirnames[:] = []          # 到深度上限即停止下钻
        dirnames[:] = [d for d in dirnames if not (here / d).is_symlink()]
        for name in sorted(filenames):
            if len(found) >= _SCAN_MAX_FILES:
                return found
            fp = here / name
            if fp.is_symlink() or fp.suffix.lower() not in _TRACE_SUFFIXES:
                continue
            found.append(fp)
    return found


def _extract_tokens(obj: dict) -> tuple[int, int]:
    """从一条 trace 记录里容忍地抽取 (skill_tokens, skill_minutes)。

    调用方应先把嵌套结构（如 {"trace": {...}}）解成 trace 级 dict 再传入。
    不同宿主版本的字段名可能漂移，这里多键兜底的「防屎山」写法：
    解析不到就返回 (0, 0)，绝不让单条脏数据炸掉整体。
    额外兜底：trace 级 `duration`（毫秒）折算成 skill_minutes，补全耗时维度。
    """
    if not isinstance(obj, dict):
        return 0, 0
    # ── token：标量键（含字典值里的 total / prompt+completion）──
    tok = 0
    scalar_keys = ("effective_tokens", "effectiveTokens", "total_tokens", "totalTokens",
                   "skill_tokens", "tokens")
    for k in scalar_keys:
        v = obj.get(k)
        if isinstance(v, dict):
            tok = (_coerce_int(v.get("total")) or _coerce_int(v.get("totalTokens"))
                   or _coerce_int(v.get("total_tokens")))
            if tok == 0:
                tok = _coerce_int(v.get("prompt_tokens")) + _coerce_int(v.get("completion_tokens"))
            if tok:
                break
        elif _coerce_int(v):
            tok = _coerce_int(v)
            break
    # 顶层 usage / token_usage 嵌套（OpenAI、Claude、多数 LLM API 通用）
    if tok == 0:
        for nk in ("usage", "token_usage", "tokenUsage"):
            u = obj.get(nk)
            if isinstance(u, dict):
                tok = _coerce_int(u.get("total_tokens")) or _coerce_int(u.get("total"))
                if tok == 0:
                    tok = _coerce_int(u.get("prompt_tokens")) + _coerce_int(u.get("completion_tokens"))
                if tok:
                    break
    min_keys = ("effective_minutes", "skill_minutes", "minutes", "duration_min")
    mins = 0
    for k in min_keys:
        v = obj.get(k)
        if _coerce_int(v):
            mins = _coerce_int(v)
            break
    # duration(ms) → 分钟 兜底（真实宿主 trace 常见 duration 字段）
    if mins == 0:
        d = obj.get("duration")
        if isinstance(d, (int, float)) and d > 0:
            mins = max(1, round(d / 60000))
    return tok, mins


def _extract_date(obj: dict) -> str:
    # 兼容真实宿主的 ISO 时间戳 startedAt/endedAt，以及测试用的 date/day 等
    for k in ("date", "day", "timestamp", "created_at", "time", "startedAt", "endedAt"):
        v = obj.get(k)
        if isinstance(v, str) and len(v) >= 10:
            return v[:10]
    return _today_iso()


def _read_trace_file(path: Path) -> Optional[dict]:
    """容忍地读取一个 trace 文件：先试整文件 JSON，再试 JSONL（每行一个对象）。"""
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return None
    if not text.strip():
        return None
    try:
        return json.loads(text)            # 1) 整文件 JSON
    except json.JSONDecodeError:
        pass
    for line in text.splitlines():         # 2) JSONL：取首个可解析对象
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
            if isinstance(obj, dict):
                return obj
        except json.JSONDecodeError:
            continue
    return None


class LocalProvider:
    """只读本机宿主 的本地用量（traces / db / usage-log），返回真实 CostRecord。

    红线：只读、纯解析、任何异常都降级（返回空/跳过），不碰网络、不碰密钥、不改文件。
    schema 在不同宿主版本可能漂移，所有字段抽取都走 _extract_tokens /
    _extract_date 的容忍逻辑；解析不到就当没有。无数据时不报错，返回空列表。
    """

    def __init__(self, root: Path = _LOCAL_ROOT):
        self.root = Path(root)

    def fetch_recent(self, days: int = 7) -> list[CostRecord]:
        records: list[CostRecord] = []
        traces_dir = self.root / "traces"
        if not traces_dir.is_dir():
            return []
        # 真实宿主把 trace 存在 traces/<session_id>/trace_<hash>.json（嵌套子目录），
        # 故需递归；但用「有界枚举」替代无边界遍历（深度/文件数上限 + 只认白名单后缀 + 跳过符号链接）。
        for p in _iter_trace_files(traces_dir):
            try:
                obj = _read_trace_file(p)
            except Exception:
                continue
            if not isinstance(obj, dict):
                continue
            # 真实 trace 结构是 {"trace": {...}, "spans": [...]}；测试用扁平文件则 trace 字段缺失。
            tr = obj.get("trace") if isinstance(obj.get("trace"), dict) else obj
            tok, mins = _extract_tokens(tr)
            if tok == 0:          # 0 token 的空/异常会话不计入消耗
                continue
            _models = (tr.get("modelInfo") or {}).get("models") or []
            model = _models[0] if _models else (tr.get("model") or "")
            rec = CostRecord(
                date=_extract_date(tr),
                skill_tokens=tok,
                skill_minutes=mins,
                model=str(model),
                task_type=tr.get("task_type") or tr.get("type"),
                session_id=str(tr.get("session_id") or tr.get("sessionId")
                               or obj.get("session_id") or ""),
                source="local_traces",
            )
            if _within_days(rec.date, days):
                records.append(rec)
        return records


class GenericJsonProvider:
    """宿主无关的用量提供方：读取任意主机导出的「用量 JSON / JSONL」文件。

    用途：尚未有专属 Provider 的 Agent 平台（例如尚未发布的天禧 AI 等开发者社区
    写的 Skill 宿主）只要能把每次会话的 token / 耗时以 JSON 形式导出，本 provider
    即可用容忍抽取器（_extract_tokens / _extract_date）解析，无需改 skill 内核。

    支持的形态：
      - 整文件 JSON：一个对象，或对象数组（每个元素代表一次会话）
      - JSONL：每行一个对象
      - 字段名漂移由 _extract_tokens / _extract_date 兜底（OpenAI/Claude 的
        usage.{prompt_tokens,completion_tokens,total_tokens} 等均可识别）
    红线：只读、纯解析，异常降级为跳过/空列表，绝不抛异常炸掉调用方。
    """

    def __init__(self, path: Path):
        self.path = Path(path)

    def fetch_recent(self, days: int = 7) -> list[CostRecord]:
        if not self.path.is_file():
            return []
        try:
            text = self.path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            return []
        if not text.strip():
            return []
        objs: list[dict] = []
        # 1) 整文件 JSON（对象 或 对象数组）
        try:
            parsed = json.loads(text)
            if isinstance(parsed, list):
                objs = [o for o in parsed if isinstance(o, dict)]
            elif isinstance(parsed, dict):
                objs = [parsed]
        except json.JSONDecodeError:
            # 2) JSONL：逐行取首个可解析对象
            for line in text.splitlines():
                line = line.strip()
                if not line:
                    continue
                try:
                    o = json.loads(line)
                    if isinstance(o, dict):
                        objs.append(o)
                except json.JSONDecodeError:
                    continue
        records: list[CostRecord] = []
        for o in objs:
            tr = o.get("trace") if isinstance(o.get("trace"), dict) else o
            tok, mins = _extract_tokens(tr)
            if tok == 0:
                continue
            _models = (tr.get("modelInfo") or {}).get("models") or []
            model = _models[0] if _models else (tr.get("model") or "")
            records.append(CostRecord(
                date=_extract_date(tr),
                skill_tokens=tok,
                skill_minutes=mins,
                model=str(model),
                task_type=tr.get("task_type") or tr.get("type") or o.get("type"),
                session_id=str(tr.get("sessionId") or tr.get("session_id")
                               or o.get("session_id") or ""),
                source="generic_json",
            ))
        return [r for r in records if _within_days(r.date, days)]


def get_default_provider() -> Optional[HostCostProvider]:
    """返回默认宿主用量提供方：本机宿主 数据存在则用本地读取器，否则 None。"""
    if _TRACES_DIR.is_dir() or _DB_PATH.is_file() or _USAGE_LOG.is_file():
        return LocalProvider()
    return None


# ─────────────────────────────────────────────────────────────
# 便捷：把真实用量转成账本草稿（dry-run，不写盘）
# ─────────────────────────────────────────────────────────────

def draft_entries_from_host(provider: HostCostProvider, days: int = 7, *,
                            baseline_tokens: int = 0,
                            baseline_minutes: int = 0,
                            baseline_ratio: float = None) -> list[dict]:
    """用宿主真实用量生成账本草稿列表（skill 取实测值）。

    baseline 代表「笨办法手搓成本」，平台无从获得，默认 0 待补。
    若给出 baseline_ratio（如 3.0 表示手搓成本约为实测的 3 倍），则按
    skill_tokens * ratio 估算 baseline，便于先看到一份「假设性」提效报告；
    ratio 仅为用户主观假设，非实测扣费。
    """
    recs = provider.fetch_recent(days)
    entries = []
    for r in recs:
        bt = baseline_tokens
        bm = baseline_minutes
        if baseline_ratio:
            bt = round(r.skill_tokens * baseline_ratio) if r.skill_tokens else bt
            bm = round(r.skill_minutes * baseline_ratio) if r.skill_minutes else bm
        entries.append(r.to_ledger_entry(baseline_tokens=bt, baseline_minutes=bm))
    return entries


def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="办公室 Token 洞察 · 真实宿主用量接入（只读本机宿主 数据）")
    parser.add_argument("--days", type=int, default=7, help="最近 N 天（默认 7）")
    parser.add_argument("--json", action="store_true", help="以 JSON 输出原始记录")
    args = parser.parse_args()

    provider = get_default_provider()
    if provider is None:
        print("[信息] 未检测到本机宿主 用量数据（~/.workbuddy/traces 等不存在）。")
        print("        宿主用量接入为可选能力；无数据时技能仍按『用户自报成本』正常工作。")
        return 0
    recs = provider.fetch_recent(args.days)
    if args.json:
        print(json.dumps([r.__dict__ for r in recs], ensure_ascii=False, indent=2))
    else:
        print(f"=== 检测到本机宿主 最近 {args.days} 天用量（{len(recs)} 条）===")
        for r in recs[:20]:
            print(f"  {r.date}  {r.skill_tokens:,} tok / {r.skill_minutes} min"
                  f"  模型={r.model or '?'}  任务={r.task_type or '未归类'}")
        if len(recs) > 20:
            print(f"  … 其余 {len(recs) - 20} 条略")
    return 0


if __name__ == "__main__":
    sys.exit(main())
