#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ledger_agent.py — office-token-booster 长链路 Agent（B 线）

长链路 Agent = 诊断内核（diagnose） + 建议生成（propose） + 写回动作（append）。
本模块**只消费** `diagnose.py` 产出的 `Diagnosis` 对象，不 import `report_engine`、
也不 import `qa`，因此对话式诊断（qa）+ 报告渲染（report_engine）一行代码都不用动 ——
这正是三层解耦（内核 / 外壳分离）要换来的好处。

能力（采集任务 → 分析 → 给出省钱/提效建议 → 可选写回模板）：
1. propose_entry(diag, task_type, ...)      —— 建议生成：把刚完成的任务变成一条账本草稿，
                                               用该类型历史均值预填 baseline 估计。
2. propose_automation_targets(diag)         —— 建议生成：输出下一批「最该自动化」的任务类型。
3. append_entry(ledger_path, entry, ...)    —— 写回模板：原子写回账本（默认 dry-run，
                                               --apply 才真写；写前自动备份）。
4. run_long_chain(ledger_path, task_type)   —— 编排：load_ledger → diagnose → propose → append → 重新 diagnose。

设计原则（与内核一致）：
- 纯标准库、无第三方依赖、无网络、无硬编码密钥。
- 安全默认：CLI 不传 --apply 只预览，绝不改动用户文件。
- 所有数字来自内核 Diagnosis，保证与报告 / 追问三处一致。
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# 允许从任意目录运行（与 report_engine / qa 保持一致的 sibling import）。
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from diagnose import load_ledger, diagnose, format_number  # noqa: E402


# ─────────────────────────────────────────────────────────────
# 建议生成
# ─────────────────────────────────────────────────────────────

def _lookup_type(diag, task_type):
    """在 Diagnosis.by_type 里找该类型的聚合记录（dict），没有返回 None。"""
    for d in diag.by_type:
        if d["task_type"] == task_type:
            return d
    return None


def propose_entry(diag, task_type, *, date=None, skill_tokens=None, skill_minutes=None,
                  baseline_tokens=None, baseline_minutes=None, note=None,
                  quality_score=None):
    """把刚完成的任务转成一条账本草稿。

    基线（baseline）= 你不用本技能、自己手搓 / 反复试错的成本，平台无从获得，故优先用
    该类型的历史均值预填；若用户显式传入则用传入值。技能实际消耗（skill_*）同理。

    quality_score 为不降质量护栏的本次交付物质量分（0-100），由 executor 渲染时算出；
    仅当非 None 时写入 entry（缺省表示「未测」，diagnose 聚合时跳过，不污染均值）。

    返回 (entry_dict, meta_dict)：
      entry_dict  —— 标准账本字段（date/type/baseline_tokens/skill_tokens/baseline_minutes/
                     skill_minutes/note/quality_score），可直接 append 进 ledger。
      meta_dict   —— {history_found, estimated_fields, warnings}，供 CLI 提示哪些是估算值。
    """
    hist = _lookup_type(diag, task_type)
    meta = {"history_found": hist is not None, "estimated_fields": [], "warnings": []}
    cnt = hist["count"] if hist else 0

    # 基线估计（无历史时设为 0 并告警，提醒用户补填真实手搓成本）
    if baseline_tokens is None:
        if hist:
            baseline_tokens = round(hist["baseline_tokens"] / cnt)
        else:
            baseline_tokens = 0
            meta["warnings"].append(
                f"类型「{task_type}」无历史记录，baseline_tokens 暂置 0，请补填真实手搓成本")
            meta["estimated_fields"].append("baseline_tokens")
    if baseline_minutes is None:
        if hist:
            baseline_minutes = round(hist["baseline_minutes"] / cnt)
        else:
            baseline_minutes = 0
            meta["estimated_fields"].append("baseline_minutes")

    # 技能实际消耗（未提供则用该类型历史均值估算，并标记为估算）
    if skill_tokens is None:
        if hist:
            skill_tokens = round(hist["skill_tokens"] / cnt)
            meta["estimated_fields"].append("skill_tokens")
            meta["warnings"].append("skill_tokens 未提供，用该类型历史均值估算，建议填实际值")
        else:
            skill_tokens = 0
            meta["estimated_fields"].append("skill_tokens")
    if skill_minutes is None:
        if hist:
            skill_minutes = round(hist["skill_minutes"] / cnt)
            meta["estimated_fields"].append("skill_minutes")
        else:
            skill_minutes = 0
            meta["estimated_fields"].append("skill_minutes")

    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")

    entry = {
        "date": date,
        "type": task_type,
        "baseline_tokens": int(baseline_tokens),
        "skill_tokens": int(skill_tokens),
        "baseline_minutes": int(baseline_minutes),
        "skill_minutes": int(skill_minutes),
        "note": note or "",
    }
    if quality_score is not None:
        entry["quality_score"] = int(quality_score)
    return entry, meta


def propose_automation_targets(diag, top_n=3):
    """建议生成：输出下一批「最该自动化」的任务类型（按自动化 ROI 降序）。

    直接复用 Diagnosis.roi_targets（内核算好的 ROI 评分），不与 build_insights 的
    recommendations 重复造轮子，也保证报告与 Agent 建议同源。
    """
    if not diag.roi_targets:
        return ["账本暂无数据，先记录几笔任务再生成自动化建议。"]
    out = []
    for t in diag.roi_targets[:top_n]:
        out.append(
            f"「{t['task_type']}」：历史 {t['count']} 次，累计节省 {format_number(t['saved_tokens'])} Token"
            f"（ROI≈{t['roi_score']}），预估月省 {format_number(t['monthly_saved_tokens'])} Token，"
            f"优先做成可复用模板。"
        )
    return out


# ─────────────────────────────────────────────────────────────
# 写回模板（原子 + 备份 + 默认 dry-run）
# ─────────────────────────────────────────────────────────────

_BACKUP_KEEP = 10  # 时间戳备份保留份数上限（超出淘汰最旧），避免长期使用无界堆积


def _validate_entry(entry):
    """写回前校验单条 entry（**只校验不改写**，保持调用方传入的原值）。

    允许 `{}` 与字段缺失（下游 diagnose 会按缺省 0 处理）；
    字段存在但无法识别为整数时抛错——宁可拒绝写回，也不把损坏数据落盘。
    """
    if not isinstance(entry, dict):
        raise ValueError(f"entry 必须是 dict，实际为 {type(entry).__name__}")
    for key in ("baseline_tokens", "skill_tokens", "baseline_minutes", "skill_minutes"):
        if key not in entry:
            continue
        val = entry[key]
        if val is None or val == "":
            continue
        try:
            int(val)
        except (TypeError, ValueError):
            raise ValueError(f"entry[{key}]={val!r} 无法识别为整数，拒绝写回") from None
    return entry


def _load_or_empty(p: Path) -> dict:
    """读取账本；文件缺失 / 损坏 / 结构非 dict 时退回空账本。

    原文件内容不会丢——损坏场景下的原文会在备份步骤里留存为 .bak。
    """
    if not p.is_file():
        return {"tasks": []}
    try:
        with open(p, "r", encoding="utf-8") as f:
            ledger = json.load(f)
    except (json.JSONDecodeError, ValueError):
        ledger = {"tasks": []}
    return ledger if isinstance(ledger, dict) else {"tasks": []}


def _prune_backups(p: Path, keep: int = _BACKUP_KEEP) -> int:
    """只保留最近 keep 份时间戳备份，淘汰更旧的。返回删除数量。

    备份文件名形如 ledger.json.20260812T142501123456.bak，按名排序即按时间排序。
    清理失败不阻断主流程：此时备份仍在，宁可堆积也不要因清理异常丢掉写回结果。
    """
    backups = sorted(p.parent.glob(f"{p.name}.*.bak"))
    removed = 0
    for old in (backups[:-keep] if keep > 0 else []):
        try:
            old.unlink()
            removed += 1
        except OSError:
            pass
    return removed


def _write_ledger_atomic(p: Path, ledger: dict, backup: bool = True):
    """备份 + 原子替换写盘（append_entry / append_entries 共用单一写入口）。

    返回 backup_path_or_None。备份为独立时间戳文件，可回滚到任意留存版本；
    写盘成功后按 _BACKUP_KEEP 淘汰旧备份，控制目录体积。
    """
    backup_path = None
    if backup and p.is_file():
        ts = datetime.now().strftime("%Y%m%dT%H%M%S%f")
        backup_path = Path(str(p) + f".{ts}.bak")
        backup_path.write_text(p.read_text(encoding="utf-8"), encoding="utf-8")

    tmp = Path(str(p) + ".tmp")
    tmp.write_text(json.dumps(ledger, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(tmp, p)  # 原子替换（Windows 也安全）
    _prune_backups(p)
    return backup_path


def append_entry(ledger_path, entry, *, backup=True, dry_run=False):
    """把 entry 追加进 ledger 的 tasks 数组。

    - dry_run=True：只返回「将会写成的 ledger」dict，不碰磁盘（CLI 默认）。
    - dry_run=False：先备份原文件为 <path>.<时间戳>.bak，再原子写入。
    - entry 字段非法（数值不可识别）时**抛错拒写**，不污染账本。
    返回 (new_ledger_dict, backup_path_or_None)。
    """
    _validate_entry(entry)
    p = Path(ledger_path)
    ledger = _load_or_empty(p)

    tasks = ledger.get("tasks", [])
    if not isinstance(tasks, list):
        tasks = []
    tasks.append(entry)
    ledger["tasks"] = tasks

    if dry_run:
        return ledger, None
    return ledger, _write_ledger_atomic(p, ledger, backup=backup)


def append_entries(ledger_path, entries, *, backup=True, dry_run=False):
    """把多条 entry 一次性追加进 ledger 的 tasks 数组（append_entry 的批量版）。

    与 append_entry 同语义：dry_run 只返回新 ledger dict；否则先备份再原子写入。
    返回 (new_ledger_dict, backup_path_or_None)。
    """
    for entry in entries:
        _validate_entry(entry)
    p = Path(ledger_path)
    ledger = _load_or_empty(p)

    tasks = ledger.get("tasks", [])
    if not isinstance(tasks, list):
        tasks = []
    tasks.extend(entries)
    ledger["tasks"] = tasks

    if dry_run:
        return ledger, None
    return ledger, _write_ledger_atomic(p, ledger, backup=backup)


def import_host_usage(ledger_path, days=7, provider=None, *,
                      baseline_tokens=0, baseline_minutes=0, apply=False,
                      baseline_ratio=None):
    """把宿主真实用量导入为提效账本草稿（skill 取实测值，baseline 默认 0 待补）。

    默认 dry-run（只返回草稿与预览诊断，不碰磁盘）；apply=True 才批量写回。
    baseline_ratio：按 skill_tokens*ratio 估算 baseline（假设性，非实测），便于先看提效报告。
    返回 dict：{entries, count, applied, backup_path, new_diag, note}。
    """
    from host_cost import get_default_provider, draft_entries_from_host

    provider = provider or get_default_provider()
    if provider is None:
        return {"entries": [], "count": 0, "applied": False, "backup_path": None,
                "new_diag": None, "note": "未检测到本机宿主用量数据，跳过导入。"}

    entries = draft_entries_from_host(
        provider, days, baseline_tokens=baseline_tokens, baseline_minutes=baseline_minutes,
        baseline_ratio=baseline_ratio)
    if not entries:
        return {"entries": [], "count": 0, "applied": False, "backup_path": None,
                "new_diag": None, "note": f"最近 {days} 天无可用宿主用量记录。"}

    if not apply:
        new_diag = diagnose(entries)
        return {"entries": entries, "count": len(entries), "applied": False,
                "backup_path": None, "new_diag": new_diag, "note": "dry-run 预览，未写盘。"}

    # 写回前去重：宿主重复导入不会把同一会话追加成多条（修复真实缺口）。
    # 去重键：有 session_id 用之；无 session_id 的「宿主条目」退回内容签名；
    # 用户手记条目（无 source）一律保留，避免误删。
    existing_tasks = load_ledger(ledger_path)

    def _dedup_key(t: dict):
        sid = t.get("session_id")
        if sid:
            return ("sid", sid)
        if t.get("source"):  # 宿主产生但缺 session_id（如第三方 generic 导出）
            return ("sig", t.get("date"), t.get("type"), t.get("model"),
                    t.get("skill_tokens"), t.get("skill_minutes"),
                    t.get("baseline_tokens"), t.get("baseline_minutes"))
        return ("keep", id(t))  # 用户手记条目，不去重

    seen_keys = {_dedup_key(t) for t in existing_tasks}
    new_entries = [e for e in entries if _dedup_key(e) not in seen_keys]
    skipped = len(entries) - len(new_entries)

    new_ledger, bak = append_entries(
        ledger_path, new_entries, backup=True, dry_run=False)
    new_diag = diagnose(new_ledger["tasks"])
    return {"entries": new_entries, "count": len(new_entries),
            "skipped_duplicates": skipped, "applied": True,
            "backup_path": bak, "new_diag": new_diag,
            "note": f"已写回 {len(new_entries)} 条（跳过重复 {skipped} 条；备份：{bak}）。"}


# ─────────────────────────────────────────────────────────────
# 长链路编排
# ─────────────────────────────────────────────────────────────

def run_long_chain(ledger_path, task_type, *, apply=False, date=None,
                   skill_tokens=None, skill_minutes=None,
                   baseline_tokens=None, baseline_minutes=None, note=None,
                   quality_score=None):
    """长链路 Agent 主流程：读取 → 诊断 → 建议 → 写回 → 重新诊断。

    quality_score（不降质量护栏）透传给 propose_entry，写回账本后参与 diagnose 聚合。

    返回 dict：{old_diag, entry, meta, new_diag, ledger_path, applied, backup_path}。
    对话层（qa）/ 渲染层（report_engine）完全不参与，保证内核单一事实源。
    """
    tasks = load_ledger(ledger_path)
    old_diag = diagnose(tasks)
    entry, meta = propose_entry(old_diag, task_type, date=date,
                                skill_tokens=skill_tokens, skill_minutes=skill_minutes,
                                baseline_tokens=baseline_tokens, baseline_minutes=baseline_minutes,
                                note=note, quality_score=quality_score)
    # P0 护栏（质量门禁）：baseline 缺省（非用户显式 0）且会产生负节省时，
    # 拒绝写回——避免「baseline=0/skill=3000」污染账本、拉偏历史均值。
    _baseline_estimated = "baseline_tokens" in meta.get("estimated_fields", [])
    if apply and _baseline_estimated and entry["skill_tokens"] > 0:
        return {
            "old_diag": old_diag, "entry": entry, "meta": meta,
            "new_diag": old_diag, "ledger_path": ledger_path,
            "applied": False, "backup_path": None, "blocked": True,
            "block_reason": (
                f"类型「{task_type}」缺少真实手搓 baseline（baseline_tokens 未提供且账本无历史），"
                f"写回会产生负节省、污染账本。请补填 --baseline-tokens 后重试，"
                f"例如「记一笔 {task_type} 花了{entry['skill_tokens']} token "
                f"{entry['skill_minutes']}分钟，手搓要<你的估算> token」。"),
        }

    new_ledger, bak = append_entry(ledger_path, entry, backup=True, dry_run=not apply)
    new_diag = diagnose(new_ledger["tasks"])
    return {
        "old_diag": old_diag, "entry": entry, "meta": meta,
        "new_diag": new_diag, "ledger_path": ledger_path,
        "applied": apply, "backup_path": bak,
    }


# ─────────────────────────────────────────────────────────────
# CLI（薄包装，与内核解耦）
# ─────────────────────────────────────────────────────────────

def _resolve_import_provider(args):
    """根据 --provider / --provider-arg 解析 --import-host 的数据源 provider。

    返回：provider 实例；None 表示用默认（本机宿主）；False 表示参数错误（调用方 return 2）。
    """
    if args.provider is None or args.provider == "local":
        return None  # 交给 import_host_usage 用 get_default_provider()
    if args.provider == "generic":
        if not args.provider_arg:
            print("[错误] --provider generic 需要配合 --provider-arg <用法文件.json> 指定导出路径",
                  file=sys.stderr)
            return False
        from host_cost import GenericJsonProvider
        return GenericJsonProvider(Path(args.provider_arg))
    return None


def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="办公室提效 · 长链路自动记账（office-token-booster）")
    parser.add_argument("ledger", nargs="?", help="账本 JSON 路径")
    parser.add_argument("--ledger", dest="ledger", help="账本 JSON 路径（同位置参数）")
    parser.add_argument("--type", help="本次完成任务的类型（如 周报生成）")
    parser.add_argument("--date", help="任务日期 YYYY-MM-DD（默认今天）")
    parser.add_argument("--skill-tokens", type=int, help="本技能实际消耗 Token（未填则用历史均值估算）")
    parser.add_argument("--skill-minutes", type=int, help="本技能实际耗时分钟（未填则用历史均值估算）")
    parser.add_argument("--baseline-tokens", type=int, help="你手搓的成本 Token（未填则用该类型历史均值）")
    parser.add_argument("--baseline-minutes", type=int, help="你手搓的耗时分钟（未填则用该类型历史均值）")
    parser.add_argument("--note", help="备注")
    parser.add_argument("--apply", action="store_true",
                        help="真正写回账本（默认仅预览，不改动文件）")
    parser.add_argument("--targets", action="store_true",
                        help="改为输出「待自动化类型建议」而不写回")
    parser.add_argument("--import-host", action="store_true",
                        help="把本机宿主 真实用量导成账本草稿（dry-run 预览；加 --apply 写回）")
    parser.add_argument("--days", type=int, default=7,
                        help="--import-host 的时间窗（最近 N 天，默认 7）")
    parser.add_argument("--baseline-ratio", type=float, default=None,
                        help="宿主导入时按 skill_tokens*ratio 估算 baseline（假设性，非实测扣费）")
    parser.add_argument("--provider", choices=["local", "generic"], default=None,
                        help="--import-host 的数据源：local（默认，本机宿主 traces）"
                             "或 generic（任意主机导出的用法 JSON/JSONL 文件，需配 --provider-arg）")
    parser.add_argument("--provider-arg", default=None,
                        help="--provider generic 指向的用法文件 JSON/JSONL 路径")
    args = parser.parse_args()

    if not args.ledger:
        print("[错误] 请提供账本路径：python ledger_agent.py <ledger.json> --type ...",
              file=sys.stderr)
        return 2

    try:
        tasks = load_ledger(args.ledger)
    except (FileNotFoundError, ValueError, json.JSONDecodeError) as e:
        print(f"[错误] {e}", file=sys.stderr)
        return 2

    diag = diagnose(tasks)

    if args.import_host:
        provider = _resolve_import_provider(args)
        if provider is False:
            return 2
        res = import_host_usage(args.ledger, days=args.days, apply=args.apply,
                                baseline_ratio=args.baseline_ratio, provider=provider)
        print("=== 真实宿主用量导入 ===")
        print(res["note"])
        if args.baseline_ratio:
            print(f"[提示] 使用 --baseline-ratio {args.baseline_ratio}：baseline 按实测*"
                  f"{args.baseline_ratio} 估算（假设性，非实测扣费）。")
        if res["entries"]:
            print(f"草稿条目（{res['count']} 条，skill 取宿主实测，baseline "
                  f"{'按 ratio 估算' if args.baseline_ratio else '默认 0 待补'}）：")
            for e in res["entries"][:20]:
                print("  - " + json.dumps(e, ensure_ascii=False))
            if res["new_diag"]:
                if args.baseline_ratio:
                    print(f"估算节省 Token：{format_number(res['new_diag'].saved_tok)}"
                          f"（率 {res['new_diag'].token_save_pct:.1f}%，baseline 按 ratio"
                          f"={args.baseline_ratio} 假设估算，非实测扣费）")
                else:
                    print(f"预览节省 Token：{format_number(res['new_diag'].saved_tok)}"
                          f"（率 {res['new_diag'].token_save_pct:.1f}%，baseline 为 0 时仅为占位）")
        if res["applied"]:
            _skipped = res.get("skipped_duplicates", 0)
            _skip_note = f"，跳过重复 {_skipped} 条" if _skipped else ""
            print(f"[OK] 已写回 {res['ledger_path'] if 'ledger_path' in res else args.ledger}"
                  f"（备份：{res['backup_path']}{_skip_note}）")
        else:
            print("（未加 --apply，仅预览。加上 --apply 才会真正写入账本。）")
        return 0

    if args.targets:
        print("待自动化类型建议（按历史基线从高到低）：")
        for line in propose_automation_targets(diag):
            print(" - " + line)
        return 0

    if not args.type:
        print("[错误] 写回模式需要 --type；或加 --targets 仅看建议。", file=sys.stderr)
        return 2

    res = run_long_chain(args.ledger, args.type, apply=args.apply, date=args.date,
                         skill_tokens=args.skill_tokens, skill_minutes=args.skill_minutes,
                         baseline_tokens=args.baseline_tokens,
                         baseline_minutes=args.baseline_minutes, note=args.note)
    if res.get("blocked"):
        print("⚠️ " + res["block_reason"])
        print("（本次未写入账本。）")
        return 0
    entry, meta = res["entry"], res["meta"]
    old_d, new_d = res["old_diag"], res["new_diag"]

    print("=== 建议记账条目（propose_entry）===")
    print(json.dumps(entry, ensure_ascii=False, indent=2))
    if meta["estimated_fields"]:
        print(f"[提示] 以下字段为估算/缺省，建议复核：{', '.join(meta['estimated_fields'])}")
    for w in meta["warnings"]:
        print(f"[注意] {w}")

    print("\n=== 写回预览（默认 dry-run，不改动文件）===")
    print(f"任务数   ：{old_d.n} -> {new_d.n}")
    print(f"节省Token：{format_number(old_d.saved_tok)} -> {format_number(new_d.saved_tok)}"
          f"（省 {old_d.token_save_pct:.1f}% -> {new_d.token_save_pct:.1f}%）")
    print(f"节省分钟：{format_number(old_d.saved_min)} -> {format_number(new_d.saved_min)}"
          f"（省 {old_d.time_save_pct:.1f}% -> {new_d.time_save_pct:.1f}%）")

    if res["applied"]:
        print(f"\n[OK] 已写回 {res['ledger_path']}（备份：{res['backup_path']}）")
    else:
        print("\n（未加 --apply，仅预览。加上 --apply 才会真正写入账本。）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
