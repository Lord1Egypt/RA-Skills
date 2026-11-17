"""马德里驳回期限计算器（12 / 18 / 最长约 25 个月）。

口径（依据议定书第 5 条与协定第 5 条，2026-09-23 核验）：
  - 基准期限为 **12 个月**（议定书第 5 条(2)(a)；协定第 5 条同为 12 个月）；
  - 已依第 5 条(2)(b) 作出声明的缔约方为 **18 个月**——**必须逐案核验该国声明**，
    不得默认 18 个月（这是本技能历史版本的错误口径）；
  - 兼具第 5 条(2)(c) 声明且本案发生第三方异议的，最长约 **25 个月**（18 + 7）；
  - 后期指定（Subsequent Designation）自**登记日**起算，而非原国际注册日；
  - 保全条款（第 9 条之六(1)(b)）：原属缔约方与被指定缔约方均为协定 + 议定书
    双参加国时，该国第 5 条(2)(b)/(c) 声明在双方关系中不生效力，须另行核验。

用法示例（驳回期模式：局发出通知的 12/18/25 个月）：
    python madrid_deadline.py --register 2026-01-15 --base-months 12
    python madrid_deadline.py --register 2026-01-15 --declared-18
    python madrid_deadline.py --register 2026-01-15 --declared-18 --opposition
    python madrid_deadline.py --register 2026-03-01 --base-months 12 \
        --kind subsequent-designation --today 2026-09-23

答复期限模式（--respond：注册人答复临时驳回，依 WIPO Rule 17(7) 表逐国数据）：
    python madrid_deadline.py --respond --cp CN --received 2026-09-20
    python madrid_deadline.py --respond --cp CN --notified 2026-09-01        # 视为送达口径：发文日 + 30 日
    python madrid_deadline.py --respond --cp CN --notified 2026-09-01 --received 2026-09-20
    python madrid_deadline.py --respond --cp CN --opposition --received 2026-09-20
    python madrid_deadline.py --respond --cp US --opposition --base-date 2026-10-01
    python madrid_deadline.py --respond --limit-days 45 --received 2026-09-20   # 表未收录成员

答复期限模式的要点：WIPO 表只收录 38 个成员，且各成员起算基准有 6 种；只有
「注册人收到通知之日」类可按收件日直接倒计时，其余基准下本脚本要求提供
--base-date（否则拒绝计算），以免按收件日倒计时而高估剩余时间。
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import timedelta
from pathlib import Path

from madrid_dateutil import add_months, days_between, formalize, parse_date, today as resolve_today

RESPONSE_TIMES_FILE = Path(__file__).resolve().with_name("madrid_response_times.json")

BASE_MONTHS_DEFAULT = 12
BASE_MONTHS_EXTENDED = 18
OPPOSITION_EXTENSION_MONTHS = 7
VALID_BASE_MONTHS = (BASE_MONTHS_DEFAULT, BASE_MONTHS_EXTENDED)

KIND_LABELS = {
    "initial": "国际注册日（首发指定）",
    "subsequent-designation": "后期指定登记日",
    "subsequent_designation": "后期指定登记日",
}


def _configure_stdout() -> None:
    reconfigure = getattr(sys.stdout, "reconfigure", None)
    if reconfigure is not None:
        try:
            reconfigure(encoding="utf-8")
        except (ValueError, OSError):
            pass


def calculate_refusal_deadline(start_date, base_months: int = BASE_MONTHS_DEFAULT,
                               has_opposition: bool = False, today=None,
                               kind: str = "initial") -> dict:
    """计算驳回期与最迟截止日。

    参数：
        start_date: 起算日。首发指定填国际注册日；后期指定填后期指定**登记日**。
        base_months: 12（未声明）或 18（已依第 5 条(2)(b) 声明）。
        has_opposition: 是否发生第三方异议且该缔约方已作第 5 条(2)(c) 声明。
        today: 计算基准日（默认系统当日）；用于复现与测试。
        kind: "initial" | "subsequent-designation"，仅影响输出措辞。
    """
    if base_months not in VALID_BASE_MONTHS:
        raise ValueError(f"base_months 须为 {VALID_BASE_MONTHS} 之一（12=未声明，18=已依第 5 条(2)(b) 声明）")
    if has_opposition and base_months != BASE_MONTHS_EXTENDED:
        raise ValueError(
            "异议延长（第 5 条(2)(c)）以已声明第 5 条(2)(b) 的 18 个月为基础；"
            "base_months=12 时不得主张 25 个月，请先核验该国声明"
        )

    start = parse_date(start_date)
    reference_day = resolve_today(today)

    base_deadline = add_months(start, base_months)
    extension = OPPOSITION_EXTENSION_MONTHS if has_opposition else 0
    final_deadline = add_months(start, base_months + extension)

    remaining_base = days_between(reference_day, base_deadline)
    remaining_final = days_between(reference_day, final_deadline)

    if remaining_final <= 0:
        status = "最迟驳回期已过（未收到驳回即视为获得保护，须以官方通知为准）"
    elif remaining_base <= 0:
        status = "基本驳回期已过，异议延长程序中"
    elif remaining_base <= 30:
        status = "仍在驳回期内（距基本截止日不足 30 天，建议每周核查）"
    else:
        status = "仍在驳回期内"

    notes = []
    if base_months == BASE_MONTHS_DEFAULT:
        notes.append(
            "当前按基准 12 个月计算。请核验该缔约方是否已依议定书第 5 条(2)(b) 声明 18 个月"
            "（声明清单见 references/madrid-declarations.md）；若已声明，请改用 --declared-18。"
        )
    else:
        notes.append("已按 18 个月计算，前提是该缔约方确已作出第 5 条(2)(b) 声明，请保留核验记录。")
    if has_opposition:
        notes.append("异议延长 7 个月以该缔约方已作第 5 条(2)(c) 声明且本案确有第三方异议为前提。")
    notes.append(
        "保全条款核验：原属缔约方与被指定缔约方均为协定 + 议定书双参加国时，"
        "该国第 5 条(2)(b)/(c) 声明在双方关系中不生效力（第 9 条之六(1)(b)），可能回落至 12 个月。"
    )
    notes.append("各缔约方对「收到驳回通知后的答复时限」另有国内法规定（15 天至 6 个月不等），须另查第 17 条(7)及该国声明。")

    return {
        "start_date": formalize(start),
        "start_date_kind": KIND_LABELS.get(kind, KIND_LABELS["initial"]),
        "base_months": base_months,
        "base_deadline": formalize(base_deadline),
        "days_to_base_deadline": remaining_base,
        "opposition_extension_months": extension,
        "final_deadline": formalize(final_deadline),
        "days_to_final_deadline": remaining_final,
        "reference_day": formalize(reference_day),
        "status": status,
        "notes": notes,
    }


def load_response_times(path=None) -> dict:
    """读取 WIPO Rule 17(7) 答复期限数据（默认 scripts/madrid_response_times.json）。"""
    target = Path(path) if path else RESPONSE_TIMES_FILE
    if not target.exists():
        raise FileNotFoundError(f"答复期限数据文件不存在：{target}")
    with target.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def calculate_response_deadline(cp=None, opposition: bool = False, received=None,
                                base_date=None, today=None, limit_days=None,
                                limit_months=None, notified=None, data=None) -> dict:
    """计算「注册人答复临时驳回」的截止日（按日/按月，依 Rule 17(7) 逐国数据）。

    关键设计：**不以收到日倒计时一切**。WIPO 表中各成员的起算基准有 6 种，只有
    「注册人收到通知之日」类可按实际收件日直接计算；其余基准（局发出、WIPO 转交/
    收到、第 14 日、TTAB 命令）下按收件日倒计时会高估剩余时间，故本函数要求
    提供官方起算日（base_date），否则拒绝计算。

    参数：
        cp: 指定缔约方代码（如 CN、US、DE）。
        opposition: True = 异议类驳回，False = 依职权驳回。
        received: 注册人实际收到通知之日（仅当官方基准为「收到之日」类时可用）。
        base_date: 官方起算日（通知/记录载明的计日起算日）。
        today: 计算基准日（默认系统当日）。
        limit_days / limit_months: 手工期限兜底（用于该表未收录的成员）。
        notified: WIPO 发出通知之日——用于「视为送达」口径（如中国：发文之日起满 15 日
            视为送达，故依职权驳回相当于自发文日 30 日；异议类为 15+30 日）。
    """
    data = data or load_response_times()
    meta = data["meta"]
    members = data["members"]

    warnings: list[str] = []
    notes: list[str] = []
    member_info = None
    limit = None

    if limit_days or limit_months:
        if limit_days and limit_months:
            raise ValueError("--limit-days 与 --limit-months 只能二选一")
        value = int(limit_days or limit_months)
        unit = "days" if limit_days else "months"
        limit = {"value": value, "unit": unit, "basis": "manual"}
        notes.append("使用手工期限（未经 WIPO 表核验）；起算点由使用者自定，须记录依据。")
    else:
        code = str(cp or "").strip().upper()
        if not code:
            raise ValueError("须指定 --cp（指定缔约方代码），或改用手工期限 --limit-days / --limit-months")
        if code not in members:
            raise ValueError(
                f"{code} 未收录于 WIPO Rule 17(7) 答复期限表（该表仅 38 个成员）——"
                "未列名不等于无答复期限，须查该国 eMadrid 会员档案与驳回通知正文；"
                "确需计算时可改用手工兜底 --limit-days N / --limit-months N"
            )
        member_info = members[code]
        item_key = "opposition" if opposition else "ex_officio"
        limit = member_info.get(item_key)
        if limit is None or limit.get("applicable") is False:
            raise ValueError(
                f"{member_info['name_zh']}（{code}）对「{'异议类' if opposition else '依职权'}驳回」"
                "在 WIPO 表中标注为不适用，无法据此计算"
            )

    unit = limit["unit"]
    value = int(limit["value"])
    basis = limit.get("basis")
    basis_zh = data["basis_glossary"].get(basis, "手工期限（由使用者自定起算点）")
    observable = basis in data["observable_bases"] or basis == "manual"
    limit_display = f"{value} {'日' if unit == 'days' else '个月'}"
    member_label = member_info["name_zh"] if member_info else "（手工期限，未走 WIPO 表）"
    code_label = (cp or "").upper() if cp else "—"

    # ---- 视为送达口径（如中国：自 WIPO 发文日起满 15 日视为送达） ----
    deemed = (member_info or {}).get("deemed_service") if member_info else None
    deemed_served = None
    notified_day = parse_date(notified) if notified else None
    if notified and deemed:
        deemed_served = notified_day + timedelta(days=int(deemed["days"]))
        notes.append(
            f"已按「视为送达」口径计算：自 WIPO 发文日 {formalize(notified_day)} 起满 {deemed['days']} 日"
            f"（{formalize(deemed_served)}）视为送达，再起算答复期限"
            f"（依据：{deemed.get('legal_basis', '')}）。"
        )
    elif notified and not deemed:
        raise ValueError(
            f"{member_label}（{code_label}）的 WIPO 表中未记载「视为送达」规则，"
            "无法按发文日推算；请提供 --received（实际收件日）或 --base-date（官方起算日）"
        )

    # ---- 起算日判定：不以收件日倒计时非收件基准的期限 ----
    if notified and deemed_served:
        start = deemed_served
        start_source = f"视为送达日（WIPO 发文日 + {deemed['days']} 日）"
    elif base_date:
        start = parse_date(base_date)
        start_source = "官方起算日（使用者提供）"
        if observable and received and parse_date(received) != start:
            warnings.append(
                f"已按官方起算日 {formalize(start)} 计算；该成员官方基准为「{basis_zh}」，"
                f"与所提供的收到日 {received} 不同，请确认以哪一个为准。"
            )
    elif received and observable:
        start = parse_date(received)
        start_source = "注册人收到通知之日（与官方基准一致）"
    elif received and not observable:
        raise ValueError(
            f"{member_label}（{code_label}）的官方起算基准是「{basis_zh}」，"
            "不是收到日——按收到日倒计时会高估剩余时间，属危险做法。"
            "请改以通知/国际注册簿载明的日期提供 --base-date"
        )
    else:
        raise ValueError("须提供 --received（收件日）或 --base-date（官方起算日）")

    if unit == "days":
        deadline = start + timedelta(days=value)
        calc_note = f"自起算日起 {value} 日（按「次日起算」理解，即起算日 + {value} 日）"
    else:
        deadline = add_months(start, value)
        calc_note = f"自起算日起 {value} 个自然月（对应日；目标月不足时取月末）"
    if not observable:
        calc_note += "；手工期限，起算点由使用者自定"

    # 同时给出 WIPO 发文日与实际收件日时，按较早者控制风险
    alt_deadline = None
    if notified and deemed and received:
        alt_start = parse_date(received)
        alt_deadline = alt_start + timedelta(days=value) if unit == "days" else add_months(alt_start, value)
        earlier = min(deadline, alt_deadline)
        warnings.append(
            "同时提供了 WIPO 发文日与收件日，两套口径结果不同：视为送达口径截止 "
            f"{formalize(deadline)}、实际收件口径截止 {formalize(alt_deadline)}；"
            f"**应以较早者 {formalize(earlier)} 控制风险**（若通知载明期限，以通知为准）。"
        )

    conservative_deadline = deadline
    if limit.get("alternative"):
        alt = int(limit["alternative"])
        conservative_deadline = start + timedelta(days=alt) if unit == "days" else add_months(start, alt)
        warnings.append(
            f"该成员为**条件期限**：官方为 {value} {'日' if unit == 'days' else '个月'}，"
            f"特定情形下为 {alt} {'日' if unit == 'days' else '个月'}（{limit.get('footnote', '')}）。"
            "内部排期请按较短者设预警，最终以通知载明情形为准。"
        )
    if not observable and basis != "manual":
        warnings.append(
            f"官方起算基准为「{basis_zh}」，注册人不可直接观察——本案须以通知正文/国际注册簿"
            "载明日期为准，并留存该凭证。"
        )
    if limit.get("qualifier") == "at_least":
        notes.append("官方期限为「至少」，实际可能更长，但仍应按该下限排期。")
    if limit.get("special") == "appoint_local_representative":
        notes.append("该期限为指定当地代理人的期限（非答辩期限本身），须先完成代理指定。")
    if opposition and basis == "ttab_order":
        notes.append("美国异议类期限自 TTAB 命令之日起算，须以 TTAB 命令日期为 --base-date。")

    notes.append("期间末日如为当地法定节假日，通常顺延；请按当地规则与通知载明口径核对。")
    notes.append(
        "本期限（按日/月计）与 CNIPA 等指定局「发出驳回通知」的驳回期（12/18/25 个月）"
        "是两个不同期限，勿混用。"
    )
    notes.append(
        f"数据源：WIPO Rule 17(7) 汇总表（页头 {meta['page_last_update']}，表内 {meta['table_last_update']}）；"
        f"人类可读版见 {meta['human_readable']}。"
    )

    reference_day = resolve_today(today)
    return {
        "mode": "response_deadline",
        "contracting_party": member_label,
        "code": code_label,
        "refusal_type": "异议类驳回" if opposition else "依职权驳回",
        "limit": limit_display,
        "official_basis": basis,
        "official_basis_zh": basis_zh,
        "basis_observable_by_holder": observable,
        "computed_from": start_source,
        "start_date": formalize(start),
        "wipo_notification_date": formalize(notified_day) if notified_day else None,
        "deemed_service_date": formalize(deemed_served) if deemed_served else None,
        "overall_days_from_wipo_notification": (
            days_between(notified_day, deadline) if notified_day else None
        ),
        "calculation": calc_note,
        "deadline": formalize(deadline),
        "deadline_from_received": formalize(alt_deadline) if alt_deadline else None,
        "deadline_conservative": formalize(conservative_deadline),
        "reference_day": formalize(reference_day),
        "days_remaining": days_between(reference_day, conservative_deadline),
        "warnings": warnings,
        "notes": notes,
        "data_baseline": {
            "source": meta["source"],
            "page_last_update": meta["page_last_update"],
            "table_last_update": meta["table_last_update"],
            "coverage": meta["coverage"],
        },
    }


def main(argv=None) -> int:
    _configure_stdout()
    parser = argparse.ArgumentParser(
        description="马德里期限计算器：默认算「局发出驳回通知」的驳回期（12/18/异议延长 7 个月）；"
                    "加 --respond 则算「注册人答复临时驳回」的期限（Rule 17(7) 逐国数据）",
        epilog="驳回期务必先核验该国第 5 条(2)(b)/(c) 声明；答复期限见 madrid_response_times.json（38/117 成员）。",
    )
    parser.add_argument("--register",
                        help="[驳回期模式] 起算日 YYYY-MM-DD：首发指定填国际注册日；后期指定填后期指定登记日")
    parser.add_argument("--respond", action="store_true",
                        help="切换为「答复临时驳回」期限模式（配合 --cp / --received / --base-date）")
    parser.add_argument("--cp", help="[答复模式] 指定缔约方代码，如 CN、US、DE（数据源 38 个成员）")
    parser.add_argument("--received", help="[答复模式] 注册人实际收到 WIPO 转交通知之日 YYYY-MM-DD")
    parser.add_argument("--notified",
                        help="[答复模式] WIPO 发出通知之日 YYYY-MM-DD（适用于有「视为送达」规则的成员，"
                             "如中国：自发文日满 15 日视为送达）")
    parser.add_argument("--base-date",
                        help="[答复模式] 官方起算日 YYYY-MM-DD（官方基准非「收到之日」时必填）")
    parser.add_argument("--limit-days", type=int,
                        help="[答复模式] 手工期限（日），用于该表未收录的成员")
    parser.add_argument("--limit-months", type=int,
                        help="[答复模式] 手工期限（月），用于该表未收录的成员")
    parser.add_argument("--kind", choices=["initial", "subsequent-designation"], default="initial",
                        help="[驳回期模式] 起算日类型（仅影响输出措辞，默认 initial）")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--base-months", type=int, choices=list(VALID_BASE_MONTHS),
                       help="驳回期基准月数：12（未声明）/ 18（已依第 5 条(2)(b) 声明）")
    group.add_argument("--declared-18", action="store_true",
                       help="该缔约方已依第 5 条(2)(b) 声明 18 个月（等效 --base-months 18）")
    parser.add_argument("--country", choices=["agreement", "protocol"],
                        help="[兼容参数] agreement → 12 个月；protocol → 须配合 --declared-18 方为 18 个月")
    parser.add_argument("--opposition", action="store_true",
                        help="本案发生第三方异议且该国已作第 5 条(2)(c) 声明（仅 18 个月基础上适用）")
    parser.add_argument("--today", help="计算基准日 YYYY-MM-DD（默认系统当日，用于复现）")
    parser.add_argument("--ascii", action="store_true", help="输出 ASCII 转义（避免终端编码问题）")
    args = parser.parse_args(argv)

    if args.respond:
        try:
            result = calculate_response_deadline(
                cp=args.cp, opposition=args.opposition, received=args.received,
                base_date=args.base_date, today=args.today, notified=args.notified,
                limit_days=args.limit_days, limit_months=args.limit_months,
            )
        except (ValueError, FileNotFoundError) as exc:
            print(json.dumps({"error": str(exc)}, ensure_ascii=args.ascii, indent=2))
            return 2
        print(json.dumps(result, ensure_ascii=args.ascii, indent=2))
        return 0

    if not args.register:
        print(json.dumps(
            {"error": "驳回期模式须提供 --register；如要计算答复期限请加 --respond --cp <代码>"},
            ensure_ascii=args.ascii, indent=2))
        return 2

    notes = []
    if args.base_months is not None:
        base_months = args.base_months
    elif args.declared_18:
        base_months = BASE_MONTHS_EXTENDED
    elif args.country == "agreement":
        base_months = BASE_MONTHS_DEFAULT
    else:
        base_months = BASE_MONTHS_DEFAULT
        if args.country == "protocol":
            notes.append(
                "已忽略「protocol 即 18 个月」的旧口径：议定书基准为 12 个月，"
                "18 个月须以该国第 5 条(2)(b) 声明为前提（如需按 18 个月计算请加 --declared-18）。"
            )

    try:
        result = calculate_refusal_deadline(
            args.register, base_months=base_months,
            has_opposition=args.opposition, today=args.today, kind=args.kind,
        )
    except ValueError as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=args.ascii, indent=2))
        return 2

    if notes:
        result["notes"] = notes + result["notes"]
    print(json.dumps(result, ensure_ascii=args.ascii, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
