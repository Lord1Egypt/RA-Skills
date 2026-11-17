"""马德里国际注册规费计算器（WIPO 侧，CHF）。

数据源：scripts/madrid_fee_data.json（与 references/madrid-fees.md 双写，
一致性由 scripts/selftest.py 校验）。两者均为易变数据的基准快照，
出具正式金额前须按 SKILL.md §3.0 联网核验。

用法示例：
    python madrid_fee.py --countries US,JP,KR --classes 8
    python madrid_fee.py --countries CN,EU --classes 3 --collective
    python madrid_fee.py --countries US --classes 1 --renewal --late
    python madrid_fee.py --countries CU,US --classes 3 --origin CN
    python madrid_fee.py --countries JP --classes 2 --later-designation

覆盖规则（依据 WIPO Schedule of Fees, 2023-02-01 版）：
  - 基本费：无色 653 / 彩色 903（费用表第 2.1 项，仅按颜色分档，不区分电子/纸质）；
  - 附加费：超 3 类每类 100；**所指定缔约方全部为单独规费国时不收**（第 2.2 项）；
  - 补充费：100/缔约方，仅对**未声明单独规费**的缔约方计收（第 2.3 项，非「协定缔约方」）；
  - 单独规费：代替补充费，按各缔约方自定费率计（第 2.4 项）；
  - 后期指定：基本费 300，无附加费（第 5 项）；
  - 续展：基本费 653，附加费/补充费或单独规费同申请阶段（第 6 项）；
  - 宽限期附加费：**基本费的 50%**（第 6.5 项），不是「应缴总额的 50%」。
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

DATA_FILE = Path(__file__).resolve().with_name("madrid_fee_data.json")

STAGE_APPLICATION = "国际申请"
STAGE_RENEWAL = "续展"
STAGE_LATER_DESIGNATION = "后期指定"


def _configure_stdout() -> None:
    """Windows 管道/重定向下避免 cp936 编码错误。"""
    reconfigure = getattr(sys.stdout, "reconfigure", None)
    if reconfigure is not None:
        try:
            reconfigure(encoding="utf-8")
        except (ValueError, OSError):  # 已被重定向为不可重配置对象
            pass


def load_fee_data(path: Path | str | None = None) -> dict:
    """读取费用数据文件（默认 scripts/madrid_fee_data.json）。"""
    target = Path(path) if path else DATA_FILE
    if not target.exists():
        raise FileNotFoundError(f"费用数据文件不存在：{target}")
    with target.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def round_half_up(value: float) -> int:
    """四舍五入到整数（Python 内置 round 为银行家舍入，会得到 326，故自行实现）。

    宽限期附加费 = 基本费 × 50% = 653 × 0.5 = 326.5 CHF，须进位到整 CHF；
    精确的应付金额仍以 WIPO 官方账单 / Fee Calculator 为准。
    """
    return int(value + 0.5) if value >= 0 else -int(-value + 0.5)


def parse_charge_date(value) -> date:
    """解析计费日期，接受 YYYY/MM/DD、YYYY-MM-DD 或 YYYYMMDD（空值 = 当日）。"""
    if value in (None, ""):
        return date.today()
    if isinstance(value, date):
        return value
    text = str(value).strip().replace("/", "-")
    if len(text) == 8 and text.isdigit():
        text = f"{text[:4]}-{text[4:6]}-{text[6:]}"
    try:
        return date.fromisoformat(text)
    except ValueError as exc:
        raise ValueError(f"计费日期格式不合法：{value!r}，应为 YYYY/MM/DD 或 YYYY-MM-DD") from exc


def apply_effective_changes(data: dict, charge_date: date) -> tuple[dict, list[str], list[str]]:
    """按计费日期套用已公告的费率调整。

    返回 (套用后的 individual_fees 深拷贝, 已套用说明, 须实测复核项)。
    仅套用数据文件中「已有官方实测记录」的调整；未公告的组件一律提示复核，
    不做推测性外推。
    """
    individual = json.loads(json.dumps(data.get("individual_fees", {})))
    applied: list[str] = []
    warnings: list[str] = []
    for block in data.get("effective_date_changes", []):
        effective = date.fromisoformat(block["effective_date"])
        if charge_date < effective:
            continue
        for code, patch in block["changes"].items():
            entry = individual.setdefault(code, {})
            for stage_key, stage_patch in patch.items():
                entry.setdefault(stage_key, {}).update(stage_patch)
            applied.append(f"{code} 自 {block['effective_date']} 起适用新费率")
        for item in block.get("undocumented_components", []):
            warnings.append(
                f"{item.replace(':', ' 的 ')} 侧是否同步调整未经实测公告，须以 "
                "madrid_feecalc_live.py --date 复核（本脚本不外推）"
            )
    return individual, applied, warnings


def _amount_for_mode(spec: dict, classes: int) -> tuple[int, str]:
    """按计费模式计算某缔约方的规费金额，返回 (金额, 明细说明)。"""
    mode = spec.get("mode")
    if mode == "flat":
        return int(spec["amount"]), f"{spec['amount']}（不限类数）"
    if mode == "per_class":
        rate = int(spec["amount"])
        return rate * classes, f"{rate}/类 × {classes} 类"
    if mode == "first_then_additional":
        first, additional = int(spec["first"]), int(spec["additional"])
        total = first + additional * max(0, classes - 1)
        return total, f"{first}（第 1 类）+ {additional} × {max(0, classes - 1)}（附加类）"
    if mode == "first_second_additional":
        first, second, additional = int(spec["first"]), int(spec["second"]), int(spec["additional"])
        total = first + (second if classes >= 2 else 0) + additional * max(0, classes - 2)
        parts = [f"{first}（第 1 类）"]
        if classes >= 2:
            parts.append(f"{second}（第 2 类）")
        parts.append(f"{additional} × {max(0, classes - 2)}（附加类）")
        return total, " + ".join(parts)
    if mode == "block_then_additional":
        block_classes = int(spec["block_classes"])
        block_amount = int(spec["block_amount"])
        additional = int(spec["additional"])
        over = max(0, classes - block_classes)
        total = block_amount + additional * over
        return total, f"{block_amount}（前 {block_classes} 类）+ {additional} × {over}（附加类）"
    raise ValueError(f"未知计费模式：{mode!r}")


def _select_spec(entry: dict, stage: str, collective: bool) -> tuple[dict | None, list[str]]:
    """挑选适用的费率规格：集体/证明商标规格优先，其次普通商标规格。"""
    notes: list[str] = []
    collective_block = entry.get("collective") or {}
    if stage == STAGE_RENEWAL:
        if collective and "renewal" in collective_block:
            return collective_block["renewal"], notes
        if collective:
            notes.append("该缔约方未在数据源中列出集体/证明商标专用费率，已按普通商标费率计算，须核验官方页面。")
        return entry.get("renewal"), notes
    if collective and "application" in collective_block:
        return collective_block["application"], notes
    if collective:
        notes.append("该缔约方未在数据源中列出集体/证明商标专用费率，已按普通商标费率计算，须核验官方页面。")
    return entry.get("application"), notes


def _grace_spec(entry: dict, collective: bool) -> dict | None:
    """续展宽限期适用费率（部分缔约方在宽限期内提高单独规费）。"""
    if collective:
        collective_block = entry.get("collective") or {}
        if "renewal_grace" in collective_block:
            return collective_block["renewal_grace"]
    return entry.get("renewal_grace")


def calculate_madrid_fee(countries, num_classes, color=False, renewal=False, late=False,
                         later_designation=False, ldc=False, collective=False,
                         origin=None, data=None, charge_date=None) -> dict:
    """计算一件马德里国际注册/续展/后期指定的 WIPO 侧规费（CHF）。

    参数：
        countries: 指定缔约方 ISO 代码列表，如 ["US","JP","KR"]
        num_classes: 商品/服务类别数（≥1）
        color: True = 商标图样含彩色（基本费 903），False = 无色（653）
        renewal: True = 续展阶段
        late: True = 在宽限期内缴费（续展阶段适用，加收基本费 50%）
        later_designation: True = 后期指定（基本费 300，无附加费）
        ldc: True = 原属缔约方为最不发达国家（基本费减为 10%）
        collective: True = 集体/证明商标（部分缔约方费率更高）
        origin: 原属缔约方 ISO 代码（仅用于保全条款提示，不参与计算）
        charge_date: 计费日期（YYYY/MM/DD 或 YYYY-MM-DD；默认当日）。
            已公告的费率调整按该日期生效；跨生效日报价应分别按生效前/后各算一套。
    """
    data = data or load_fee_data()
    wipo = data["wipo_fees"]
    not_listed = data.get("not_listed_examples", {})

    billing_day = parse_charge_date(charge_date)
    individual, change_notes, change_warnings = apply_effective_changes(data, billing_day)

    codes = [str(c).strip().upper() for c in (countries or []) if str(c).strip()]
    if not codes:
        raise ValueError("countries 不能为空，至少指定一个缔约方")
    if num_classes < 1:
        raise ValueError("num_classes 必须 ≥ 1（商品/服务至少 1 类）")
    if late and not renewal:
        raise ValueError("--late 仅在续展阶段（--renewal）有意义")
    if later_designation and renewal:
        raise ValueError("--later-designation 与 --renewal 不可同时使用")

    stage = STAGE_LATER_DESIGNATION if later_designation else (STAGE_RENEWAL if renewal else STAGE_APPLICATION)

    # ---- 基本费（第 2.1 / 5.1 / 6.1 项）----
    if stage == STAGE_LATER_DESIGNATION:
        basic = int(wipo["subsequent_designation_basic"])
        basic_note = "后期指定基本费（费用表第 5.1 项），不含附加费"
    elif stage == STAGE_RENEWAL:
        basic = int(wipo["renewal_basic"])
        basic_note = "续展基本费（第 6.1 项；费用表未区分颜色与提交方式）"
    else:
        key = "color" if color else "black_white"
        if ldc:
            basic = int(wipo["basic_application_ldc"][key])
            basic_note = f"国际申请基本费 LDC 减免档（第 2.1 项，10% 取整：{'彩色' if color else '无色'}）"
        else:
            basic = int(wipo["basic_application"][key])
            basic_note = f"国际申请基本费（第 2.1 项，{'彩色 903' if color else '无色 653'}）"

    # ---- 各缔约方规费：单独规费 or 补充费（第 2.3/2.4、5.2/5.3、6.3/6.4 项）----
    per_country: dict[str, dict] = {}
    individual_total = 0
    complementary_total = 0
    individual_count = 0
    second_part_total = 0
    notes: list[str] = []

    for item in change_notes:
        notes.append(f"已公告费率调整已生效：{item}。")
    notes.extend(change_warnings)

    for code in codes:
        entry = individual.get(code)
        if entry is None:
            complementary_total += int(wipo["complementary_fee_per_contracting_party"])
            if code in not_listed:
                remark = not_listed[code].get("reason", "未声明单独规费")
            else:
                remark = "未在单独规费数据源中列名（或 ISO 代码有误）；已按补充费计，须核验官方页面"
            per_country[code] = {
                "类型": "补充费",
                "金额": int(wipo["complementary_fee_per_contracting_party"]),
                "明细": remark,
            }
            continue

        individual_count += 1
        spec, spec_notes = _select_spec(entry, stage, collective)
        for note in spec_notes:
            notes.append(f"{code}：{note}")
        if spec is None:
            per_country[code] = {
                "类型": "单独规费",
                "金额": None,
                "明细": "数据源缺少该阶段费率，须联网核验",
            }
            continue
        amount, detail = _amount_for_mode(spec, num_classes)
        if late and stage == STAGE_RENEWAL:
            grace_spec = _grace_spec(entry, collective)
            if grace_spec:
                if grace_spec.get("additive"):
                    amount += int(grace_spec["amount"])
                    detail += f" + 宽限期追加 {grace_spec['amount']}（不限类数）"
                else:
                    amount, grace_detail = _amount_for_mode(grace_spec, num_classes)
                    detail = f"{grace_detail}（宽限期费率）"
        per_country[code] = {"类型": "单独规费", "金额": amount, "明细": detail}
        individual_total += amount
        if entry.get("note"):
            notes.append(f"{code}：{entry['note']}")
        if stage != STAGE_RENEWAL and "second_part" in entry:
            sp = entry["second_part"]
            second_part_total += int(sp["amount"])
            notes.append(f"{code}：{sp['note']}")

    # ---- 附加费（第 2.2 / 6.2 项；后期指定无附加费）----
    supplementary = 0
    all_individual = individual_count == len(codes)
    if stage == STAGE_LATER_DESIGNATION:
        supplementary_note = "后期指定不设附加费（费用表第 5 项仅含基本费与补充费/单独规费）"
    elif all_individual:
        supplementary_note = "所指定缔约方全部为单独规费国，依第 2.2/6.2 项不收附加费"
    else:
        supplementary = max(0, num_classes - 3) * int(wipo["supplementary_fee_per_class_beyond_three"])
        supplementary_note = f"{num_classes} 类中超出 3 类的 {max(0, num_classes - 3)} 类 × {wipo['supplementary_fee_per_class_beyond_three']}"
        if individual_count:
            supplementary_note += "（有缔约方适用补充费，故按全部类别计附加费）"

    # ---- 宽限期附加费（第 6.5 项：基本费的 50%）----
    grace_surcharge = 0
    if late:
        pct = int(wipo["grace_surcharge_percent_of_basic"])
        exact = basic * pct / 100
        grace_surcharge = round_half_up(exact)
        notes.append(
            f"宽限期附加费按基本费的 {pct}% 计（第 6.5 项官方原文：50% of the amount of the fee "
            f"payable under item 6.1），不是「应缴总额的 50%」；"
            f"{basic} × {pct}% = {exact:g} CHF，已按整 CHF 四舍五入计为 {grace_surcharge}，"
            "实际应付以 WIPO 官方账单 / Fee Calculator 为准。"
        )

    total = basic + supplementary + complementary_total + individual_total + grace_surcharge + second_part_total

    if origin:
        notes.append(
            "保全条款核验：如原属缔约方与被指定缔约方均为协定 + 议定书双参加国，"
            "该国单独规费声明在双方关系中不生效力，应改按补充费 100 CHF 计"
            "（议定书第 9 条之六(1)(b)、费用表第 2.4/5.3/6.4 项）。本计算器不代为判断双参加国身份。"
        )
    notes.append(
        "单独规费、汇率、规费表均为易变数据；本结果为基准快照估算，最终以 WIPO 官方 "
        "Fee Calculator 与缴费通知为准（https://madrid.wipo.int/feecalcapp/）。"
    )
    snapshot_day = date.fromisoformat(data["meta"]["reference_date"])
    pending = [b for b in data.get("effective_date_changes", [])
               if date.fromisoformat(b["effective_date"]) > billing_day]
    if pending:
        items = []
        for block in pending:
            codes = "、".join(sorted(block["changes"]))
            items.append(f"{block['effective_date']}（{codes}）")
        notes.append(
            "跨生效日提示：尚有已公告但未生效的费率调整——" + "；".join(items)
            + "。若实际提交/缴费日跨过该日期，须按生效前、生效后各出一套预算（可用 "
            "madrid_feecalc_live.py --date YYYY/MM/DD 分别实测）。"
        )
    elif (billing_day - snapshot_day).days > 90:
        notes.append(
            f"计费日 {billing_day.isoformat()} 晚于本数据快照基准日 {snapshot_day.isoformat()} 逾 90 天，"
            "期间可能另有未公告的费率调整——正式报价前请用 madrid_feecalc_live.py --date "
            f"{billing_day.strftime('%Y/%m/%d')} 实测官方计算器。"
        )

    return {
        "stage": stage,
        "charge_date": billing_day.isoformat(),
        "designated_contracting_parties": codes,
        "classes": num_classes,
        "color_mark": color,
        "collective_mark": collective,
        "ldc_reduction": ldc,
        "basic_fee": {"amount": basic, "note": basic_note},
        "supplementary_fee": {"amount": supplementary, "note": supplementary_note},
        "complementary_fee_total": complementary_total,
        "individual_fee_total": individual_total,
        "grace_surcharge": grace_surcharge,
        "second_part_fee": second_part_total,
        "total_chf": total,
        "per_contracting_party": per_country,
        "data_baseline": {
            "reference_date": data["meta"]["reference_date"],
            "fee_schedule_version": data["meta"]["fee_schedule_version"],
            "individual_fees_last_update": data["meta"]["individual_fees_last_update"],
            "sources": data["meta"]["sources"],
        },
        "notes": notes,
    }


def main(argv=None) -> int:
    _configure_stdout()
    parser = argparse.ArgumentParser(
        description="马德里国际注册规费计算器（WIPO 侧 CHF；数据源 scripts/madrid_fee_data.json）",
        epilog="官方在线计算器：https://madrid.wipo.int/feecalcapp/",
    )
    parser.add_argument("--countries", required=True, help="指定缔约方 ISO 代码，逗号分隔，如 US,JP,KR")
    parser.add_argument("--classes", type=int, required=True, help="商品/服务类别数")
    parser.add_argument("--color", action="store_true", help="商标图样含彩色（基本费 903，否则 653）")
    parser.add_argument("--collective", action="store_true", help="集体/证明商标（部分缔约方费率更高）")
    parser.add_argument("--renewal", action="store_true", help="续展阶段")
    parser.add_argument("--late", action="store_true", help="宽限期内缴费（加收基本费 50%%）")
    parser.add_argument("--later-designation", action="store_true", help="后期指定（基本费 300，无附加费）")
    parser.add_argument("--ldc", action="store_true", help="原属缔约方为最不发达国家（基本费减为 10%%）")
    parser.add_argument("--origin", help="原属缔约方 ISO 代码（仅用于保全条款提示）")
    parser.add_argument("--date", dest="charge_date",
                        help="计费日期 YYYY/MM/DD（默认当日）；已公告的费率调整按该日期生效，跨生效日应分别核算")
    parser.add_argument("--data", help="自定义费用数据文件路径（默认 scripts/madrid_fee_data.json）")
    parser.add_argument("--mode", choices=["electronic", "paper"], help="[已废弃] 现行费用表不区分电子/纸质，该参数仅作兼容")
    parser.add_argument("--ascii", action="store_true", help="输出 ASCII 转义（避免终端编码问题）")
    args = parser.parse_args(argv)

    try:
        result = calculate_madrid_fee(
            args.countries.split(","), args.classes, color=args.color,
            renewal=args.renewal, late=args.late, later_designation=args.later_designation,
            ldc=args.ldc, collective=args.collective, origin=args.origin,
            data=load_fee_data(args.data) if args.data else None,
            charge_date=args.charge_date,
        )
    except (ValueError, FileNotFoundError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=args.ascii, indent=2))
        return 2

    if args.mode:
        result["notes"].insert(0, "提示：--mode 已废弃；现行费用表基本费仅按颜色分档，电子/纸质同价。")

    print(json.dumps(result, ensure_ascii=args.ascii, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
