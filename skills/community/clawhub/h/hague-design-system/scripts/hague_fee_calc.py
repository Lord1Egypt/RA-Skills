#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""海牙体系国际规费计算器（离线快照版）

用途
----
按 WIPO《费用表》与《单独指定费》快照，计算外观设计国际申请 / 国际注册续展所需的
**CHF 国际规费**，并可选折算 CNY。用于答复费用问题时的"先算草稿"，随后仍须按技能
SKILL.md §3.4 的费用权威源声明在 WIPO 官网实时核对。

设计原则（与技能知识库一致）
---------------------------
1. 只算 CHF 国际规费（海牙注册费用均向 WIPO 缴纳）：不含 CNIPA 侧费用
   （限特定国内后续程序，如复审费、恢复权利请求费等），也不含代理费。
2. 缺数据即回「无」：单独指定费未内置的缔约方，脚本拒绝估算并以退出码 3 结束，
   提示先到 WIPO 单独指定费明细页核对，再经 --designate CC:ind:金额 传入。
3. 快照过期即拒绝：--as-of 早于快照生效日，或距快照核验日超过 stale_after_days，
   默认拒绝计算（可用 --allow-stale 强制，会打印醒目警告）。

用法示例
--------
# 查看快照元信息
python hague_fee_calc.py --show-snapshot

# 中国指定：1 件申请、1 项外观设计、6 幅视图、经 eHague 电子提交
python hague_fee_calc.py --designs 1 --reproductions 6 --efiling --designate CN:ind

# 多项设计 + 中国 + 某缔约方单独指定费（实时核对值由命令行传入）
python hague_fee_calc.py --designs 3 --reproductions 9 --efiling \
    --designate CN:ind --designate JP:ind:1200:design

# 续展（首续）+ 宽限期内缴费
python hague_fee_calc.py --type renewal --renewal-number 1 --designs 1 \
    --designate CN:ind --grace

# 美国：小实体减费 + 计入第 2 部分（第 2 部分金额未标明基数，默认按每件申请）
python hague_fee_calc.py --designs 1 --reproductions 6 --efiling \
    --designate US:ind --entity US=small --include-part2

# 韩国：按洛迦诺类别切换为标准指定费第 3 级（第 5 类属特例类别）
python hague_fee_calc.py --designs 1 --reproductions 6 --efiling \
    --designate KR:ind --locarno-class 5

# OAPI：按交存计费 + LDC 减费档
python hague_fee_calc.py --designs 1 --reproductions 6 --efiling --ldc \
    --designate OA:ind --deposit single

# 最不发达国家减费 + CNY 折算
python hague_fee_calc.py --designs 1 --reproductions 6 --efiling --ldc \
    --designate KR:ind --cny-rate 8.0 --rate-source 2026-09-24 中国银行牌价

指定缔约方语法
--------------
    CC:std1 | CC:std2 | CC:std3      标准指定费（非审查局缔约方，等级以其声明为准）
    CC:ind                           单独指定费（读取脚本内置快照，目前仅中国 CN）
    CC:ind:金额                      单独指定费，金额为实时核对后传入
    CC:ind:金额:design               同上，但该金额按「每项外观设计」计收
    CC:ind:金额:app                  同上，但该金额按「每件申请」计收（默认）

退出码
------
    0  正常
    2  参数错误
    3  回「无」（快照不适用、数据缺失或已过期）
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import math
import sys
from pathlib import Path

DATA_FILE = Path(__file__).with_name("fee_data.json")

CALCULATOR_URL = "https://hague.wipo.int/#/fee-calculator?type=DTR"
SCHEDULE_URL = "https://www.wipo.int/en/web/hague-system/fees/sched"
INDIVIDUAL_URL = "https://www.wipo.int/en/web/hague-system/fees/individ-fee"

LIMITS = {"designs": (1, 100), "reproductions": (1, 500), "paper_pages": (0, 100), "words": (0, 500)}

DISCLAIMERS = [
    "本结果为离线快照估算，仅含 WIPO 国际局收取的 CHF 国际规费。",
    "不含 CNIPA 侧费用（限特定国内后续程序，如复审费、恢复权利请求费等）与代理费。",
    "对外答复前须实时核对：费用计算器 / 费用表 / 单独指定费明细页（见下方链接）。",
    "正式金额以 eHague 提交页显示、以及国际局最终核算为准。",
]


class NoDataError(Exception):
    """对应技能 六 6.4 约束B：数据无法确认时回「无」，不得编造。"""


def load_snapshot() -> dict:
    if not DATA_FILE.exists():
        raise NoDataError(f"无：费用快照文件缺失（{DATA_FILE.name}），无法计算，请改用 WIPO 官网核对。")
    with DATA_FILE.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def parse_date(text: str, label: str) -> _dt.date:
    try:
        return _dt.date.fromisoformat(text)
    except ValueError as exc:  # pragma: no cover - 参数校验路径
        raise SystemExit(f"参数错误：{label} 需为 YYYY-MM-DD 格式，收到 {text!r}") from exc


def check_snapshot(data: dict, as_of: _dt.date, allow_stale: bool) -> list[str]:
    meta = data["meta"]
    notes: list[str] = []
    effective = parse_date(meta["schedule_effective_date"], "快照生效日")
    if as_of < effective:
        raise NoDataError(
            f"无：本快照为 {meta['schedule_version']}（生效日 {effective.isoformat()}），"
            f"不能用于 {as_of.isoformat()} 的申请/续展，请以 WIPO 费用表当时版本为准。"
        )
    verified = parse_date(meta["verified_on"], "快照核验日")
    age = (as_of - verified).days
    if age > int(meta["stale_after_days"]) and not allow_stale:
        raise NoDataError(
            f"无：快照核验日 {verified.isoformat()} 距计算日 {as_of.isoformat()} 已 {age} 天，"
            f"超过 {meta['stale_after_days']} 天上限，须先按 {SCHEDULE_URL} 实时核对后再用"
            f"（如确需强制计算，加 --allow-stale）。"
        )
    if age > int(meta["stale_after_days"]):
        notes.append(f"⚠️ 快照已过期 {age} 天（核验日 {verified.isoformat()}），本次为强制计算，务必实时核对。")
    return notes


def within(name: str, value: int) -> int:
    low, high = LIMITS[name]
    if not low <= value <= high:
        raise SystemExit(f"参数错误：{name} 须在 {low}–{high} 之间（与 WIPO 计算器上限一致），收到 {value}")
    return value


def idx(block: dict, designs: int) -> int:
    """首件金额 + 附加件数 × 附加金额。"""
    return int(block["first_design"]) + (designs - 1) * int(block["additional_design"])


UNIT_ALIASES = {"app": "app", "application": "app", "design": "design", "per_design": "design"}


def ind_item(prefix: str, code: str, amount: int, unit: str, designs: int, extra: str = "") -> tuple[str, int]:
    """单独指定费条目：按「每件申请」（app）或「每项外观设计」（design）计收。"""
    if unit == "app":
        basis, cost = "按每件申请计收", amount
    else:
        basis, cost = f"按每项设计计收：{amount} × {designs}", amount * designs
    label = f"{prefix} {code}（{basis}）"
    if extra:
        label += f"｜{extra}"
    return label, cost


def parse_designation(raw: str) -> tuple[str, str, int | None, str]:
    parts = raw.split(":")
    if len(parts) < 2:
        raise SystemExit(f"参数错误：缔约方写法应为 CC:类型[:金额[:计费单位]]，收到 {raw!r}")
    code = parts[0].strip().upper()
    kind = parts[1].strip().lower()
    if kind not in {"ind", "std1", "std2", "std3"}:
        raise SystemExit(f"参数错误：{code} 的类型须为 ind / std1 / std2 / std3，收到 {kind!r}")
    amount = None
    unit = "app"
    if kind == "ind":
        if len(parts) >= 3 and parts[2].strip():
            try:
                amount = int(float(parts[2]))
            except ValueError as exc:
                raise SystemExit(f"参数错误：{code} 的单独指定费金额须为数字，收到 {parts[2]!r}") from exc
        if len(parts) >= 4 and parts[3].strip():
            raw_unit = parts[3].strip().lower()
            unit = UNIT_ALIASES.get(raw_unit)
            if unit is None:
                raise SystemExit(f"参数错误：{code} 的计费单位须为 app/application 或 design，收到 {raw_unit!r}")
    return code, kind, amount, unit


def lookup_individual(data: dict, code: str) -> dict:
    entry = data.get("individual", {}).get(code)
    if not entry:
        raise NoDataError(
            f"无：未内置 {code} 的单独指定费。请先以 {INDIVIDUAL_URL} 实时核对，"
            f"再以 --designate {code}:ind:金额[:app|design] 传入后计算。"
        )
    return entry


ENTITY_SUFFIX = {"default": "", "small": "_small", "micro": "_micro", "reduced": "_reduced"}


def entity_amount(entry: dict, key: str, entity: str) -> int | None:
    value = entry.get(f"{key}{ENTITY_SUFFIX.get(entity, '')}")
    return int(value) if value is not None else None


def resolve_individual_application(data: dict, args: argparse.Namespace, code: str, designs: int) -> dict:
    """判定某缔约方在**申请阶段**适用的费用结构与金额，返回 {items, notes}。"""
    entry = lookup_individual(data, code)
    items: list[dict] = []
    notes: list[str] = []
    entity = args.entity_map.get(code, "default")

    # ① 洛迦诺类别特例（如韩国：特定类别适用标准指定费第 3 级，而非单独指定费）
    classes = entry.get("standard_fee_classes")
    if args.locarno_class and classes and args.locarno_class in classes:
        kind = "std3"
        block = (data["schedule"]["ldc_reduction"]["application"]["standard_designation"][kind]
                 if args.ldc else data["schedule"]["application"]["standard_designation"][kind])
        items.append({"label": f"标准指定费 {code}（{kind.upper()}，{designs} 项设计；类目特例：洛迦诺第 {args.locarno_class} 类）",
                      "amount": idx(block, designs)})
        notes.append(f"{code}：依其声明，洛迦诺第 {args.locarno_class} 类的设计适用标准指定费第 3 级，不适用单独指定费。")
        return {"items": items, "notes": notes}

    # ② 注册日特例（如土库曼斯坦：早期注册适用标准指定费）
    cutoff = entry.get("standard_fee_before_registration_date")
    if cutoff and args.registration_date and args.registration_date.isoformat() < cutoff:
        raise NoDataError(
            f"无：{code} 对国际注册日早于 {cutoff} 的注册适用标准指定费，但页面未指明适用级数；"
            f"请以 --designate {code}:std1|std2|std3（等级以该缔约方声明为准）明确后重算。"
        )

    unit = entry.get("unit")
    if unit not in {"application", "design", "first_additional", "deposit"}:
        raise NoDataError(f"无：{code} 的计费单位 {unit!r} 无法识别，请核对 {INDIVIDUAL_URL}。")
    if not entry.get("unit_verified", False):
        notes.append(f"{code}：页面未标注计费单位，本次按「{'每项外观设计' if unit == 'design' else '每件申请'}」处理，须复核。")

    # ③ 交存制（如 OAPI）
    if unit == "deposit":
        if not args.deposit:
            raise NoDataError(f"无：{code} 按交存计收，请以 --deposit single 或 --deposit multiple 指明交存类型后重算。")
        block = entry.get("application_ldc") if args.ldc and entry.get("application_ldc") else entry.get("application", {})
        amount = block.get(f"{args.deposit}_deposit")
        if amount is None:
            raise NoDataError(f"无：快照缺少 {code} 的交存费数额，请以 {INDIVIDUAL_URL} 核对后传入。")
        tag = "（LDC 减费档）" if args.ldc and entry.get("application_ldc") else ""
        items.append({"label": f"单独指定费 {code}（{'单一' if args.deposit == 'single' else '多项'}交存{tag}）｜快照",
                      "amount": int(amount)})
        return {"items": items, "notes": notes}

    base = entity_amount(entry, "application", entity)
    if base is None:
        if entity != "default":
            notes.append(f"{code}：快照无「{entity}」档位，已按默认档计算；该缔约方的减费条件须复核。")
        base = entry.get("application")
    if base is None:
        raise NoDataError(f"无：快照缺少 {code} 的申请阶段单独指定费，请以 {INDIVIDUAL_URL} 核对后传入实时值。")

    additional = entity_amount(entry, "application_additional", entity)
    if additional is None:
        additional = entry.get("application_additional")
    if unit == "design" and additional is None:
        total = int(base) * designs
        basis = f"按每项设计计收：{int(base)} × {designs}"
    else:
        add = int(additional or 0)
        total = int(base) + add * (designs - 1)
        basis = f"第一项 {int(base)}" + (f" ＋ 每增加一项 {add}×{designs - 1}" if designs > 1 else "")
    tags = "快照" if entity == "default" else f"快照·{entity} 档"
    items.append({"label": f"单独指定费 {code}（{basis}）｜{tags}", "amount": total})

    # ④ 分两部分缴纳（如美国、墨西哥）：第 2 部分
    if args.include_part2:
        part2 = entity_amount(entry, "application_part2", entity)
        if part2 is None:
            part2 = entry.get("application_part2")
        bracket_note = ""
        if entry.get("application_part2_brackets") and args.registration_date:
            iso = args.registration_date.isoformat()
            for bracket in entry["application_part2_brackets"]:
                if bracket["from"] <= iso <= bracket["to"]:
                    part2 = int(bracket.get(ENTITY_SUFFIX.get(entity, "").lstrip("_"), bracket.get("default")))
                    bracket_note = f"，按注册日 {iso} 适用过渡档 {bracket['from']}–{bracket['to']}"
                    break
        if part2 is None:
            raise NoDataError(f"无：快照缺少 {code} 的第 2 部分单独指定费，请以 {INDIVIDUAL_URL} 核对后传入。")
        factor = designs if args.part2_basis == "design" else 1
        basis = f"每项设计 × {designs}" if factor != 1 else "按每件国际申请计"
        items.append({"label": f"单独指定费 {code} 第 2 部分（{int(part2)}，{basis}{bracket_note}；页面未标明计费基数，须复核）",
                      "amount": int(part2) * factor})
        notes.append(f"{code}：第 2 部分单独指定费在第 1 部分之后缴纳（细则第12条第(3)款），缴纳时点与基数以国际局通知及官网为准。")

    if entry.get("note"):
        notes.append(f"{code}：{entry['note']}")
    return {"items": items, "notes": notes}


def resolve_individual_renewal(data: dict, args: argparse.Namespace, code: str, designs: int,
                               renewal_number: int) -> dict:
    """判定某缔约方在**续展阶段**适用的费用结构与金额，返回 {items, notes}。"""
    entry = lookup_individual(data, code)
    items: list[dict] = []
    notes: list[str] = []
    entity = args.entity_map.get(code, "default")

    if entry.get("renewal_status") == "unlisted":
        raise NoDataError(
            f"无：{code} 在 WIPO 单独指定费页面的续展阶段未列数额，不得按申请阶段金额或标准指定费推算；"
            f"请以 {INDIVIDUAL_URL} 与 WIPO 费用计算器核对后续展。"
        )

    # 类别特例（如韩国续展，按国际注册日区分类别表）
    rule = entry.get("standard_fee_classes_renewal")
    if rule and args.locarno_class:
        classes = rule.get("from_2020_12_01", [])
        if args.registration_date and args.registration_date.isoformat() < "2020-12-01":
            classes = rule.get("before_2020_12_01", classes)
        if args.locarno_class in classes:
            block = data["schedule"]["renewal"]["standard_designation"]
            items.append({"label": f"续展标准指定费 {code}（{designs} 项设计；类目特例：洛迦诺第 {args.locarno_class} 类）",
                          "amount": idx(block, designs)})
            notes.append(f"{code}：该洛迦诺类别的续展适用标准指定费（页面脚注，按国际注册日区分适用类别）。")
            return {"items": items, "notes": notes}

    renewals = entry.get("renewals") or []
    if not renewals:
        raise NoDataError(f"无：快照缺少 {code} 的续展阶段单独指定费，请以 {INDIVIDUAL_URL} 核对。")
    if renewal_number <= len(renewals):
        amount = int(renewals[renewal_number - 1])
    elif "renewal_overflow" in entry:
        amount = int(entry["renewal_overflow"])
        notes.append(f"{code}：第 {renewal_number} 次续展按页面「Subsequent renewals」口径计 {amount} CHF。")
    else:
        raise NoDataError(
            f"无：快照仅列 {code} 至第 {len(renewals)} 次续展，请以 {INDIVIDUAL_URL} 核对第 {renewal_number} 次的数额。"
        )

    reduced = entry.get("renewals_reduced") or []
    if entity == "reduced" and len(reduced) >= renewal_number:
        amount = int(reduced[renewal_number - 1])
        notes.append(f"{code}：按减免档计算（页面未说明减免条件，须复核）。")

    unit = entry.get("renewal_unit") or entry.get("unit")
    if not entry.get("renewal_unit_verified", entry.get("unit_verified", False)):
        notes.append(f"{code}：续展阶段计费单位页面未标注，本次按现行结构处理，须复核。")
    additional = entry.get("renewal_additional")
    if unit == "first_additional" and additional is not None:
        total = amount + int(additional) * (designs - 1)
        basis = f"第一项 {amount}" + (f" ＋ 每增加一项 {int(additional)}×{designs - 1}" if designs > 1 else "")
    elif unit == "design":
        total = amount * designs
        basis = f"按每项设计计收：{amount} × {designs}"
    else:
        total = amount
        basis = "按每件申请计收"
    items.append({"label": f"续展单独指定费 {code}（第{renewal_number}次续展｜{basis}）｜快照", "amount": total})
    if entry.get("note"):
        notes.append(f"{code}：{entry['note']}")
    return {"items": items, "notes": notes}


def compute(data: dict, args: argparse.Namespace, as_of: _dt.date) -> dict:
    sched = data["schedule"]
    ldc = sched["ldc_reduction"] if args.ldc else None
    notes = check_snapshot(data, as_of, args.allow_stale)

    if args.ldc:
        notes.append(
            "已按最不发达国家（LDC）减费计算基本费、公布费与标准指定费；单独指定费仅在缔约方已声明 LDC 减缴档时"
            "按该档计算（如 OAPI 单一 8／多项 12），其余缔约方不自动减缴（WIPO 对该项仅为鼓励性建议）。"
        )
    if args.type == "renewal" and args.reproductions != args.designs:
        notes.append("续展阶段无公布费，已忽略 --reproductions 取值。")
    if args.paper_pages > 0 and args.efiling:
        notes.append("已同时给出 --efiling 与 --paper-pages：按纸件页数计入按页附加费；电子提交可免除该项。")
    if args.paper_pages == 0 and not args.efiling and args.reproductions > 0 and args.type == "application":
        notes.append("未声明提交形式：默认按电子提交（eHague）计算，故不含纸件按页附加费。")

    items: list[dict] = []

    if args.type == "application":
        if ldc:
            basic_first = int(ldc["application"]["basic_first_design"])
            basic_add = int(ldc["application"]["basic_additional_design"])
            pub_each = int(ldc["application"]["publication_per_reproduction"])
            page_extra = int(ldc["application"]["paper_extra_page_after_first"])
        else:
            block = sched["application"]["basic"]
            basic_first, basic_add = int(block["first_design"]), int(block["additional_design"])
            pub = sched["application"]["publication"]
            pub_each, page_extra = int(pub["per_reproduction"]), int(pub["paper_extra_page_after_first"])

        basic = basic_first + (args.designs - 1) * basic_add
        items.append({"label": f"基本费（{args.designs} 项外观设计：首件 {basic_first} + 附加 {args.designs - 1}×{basic_add}）", "amount": basic})

        pub_total = args.reproductions * pub_each
        items.append({"label": f"公布费（{args.reproductions} 幅复制件 × {pub_each}）", "amount": pub_total})

        if args.paper_pages > 1:
            pages = args.paper_pages - 1
            items.append({"label": f"纸件复制件按页附加费（第1页之后 {pages} 页 × {page_extra}）", "amount": pages * page_extra})

        if args.description_words > 100:
            extra = args.description_words - 100
            if ldc:
                cost = math.ceil(extra / 5) * int(ldc["application"]["description_per_5_words_beyond_100"])
                items.append({"label": f"说明超字数附加费（超 {extra} 字，每 5 字 1 CHF）", "amount": cost})
            else:
                per_word = int(sched["application"]["description_surcharge"]["per_word_beyond"])
                items.append({"label": f"说明超字数附加费（超 {extra} 字 × {per_word}）", "amount": extra * per_word})

        for code, kind, amount, unit in args.designations:
            if kind.startswith("std"):
                if ldc:
                    std_block = ldc["application"]["standard_designation"][kind]
                else:
                    std_block = sched["application"]["standard_designation"][kind]
                cost = idx(std_block, args.designs)
                items.append({"label": f"标准指定费 {code}（{kind.upper()}，{args.designs} 项设计）", "amount": cost})
            else:
                if amount is not None:
                    label, cost = ind_item("单独指定费", code, amount, unit, args.designs, "实时核对值（非快照）")
                    items.append({"label": label, "amount": cost})
                else:
                    plan = resolve_individual_application(data, args, code, args.designs)
                    items.extend(plan["items"])
                    notes.extend(plan["notes"])

    else:  # renewal
        block = sched["renewal"]["basic"]
        basic = idx(block, args.designs)
        items.append({"label": f"续展基本费（{args.designs} 项外观设计：首件 {block['first_design']} + 附加 {args.designs - 1}×{block['additional_design']}）", "amount": basic})

        for code, kind, amount, unit in args.designations:
            if kind.startswith("std"):
                std_block = sched["renewal"]["standard_designation"]
                cost = idx(std_block, args.designs)
                items.append({"label": f"续展标准指定费 {code}（{args.designs} 项设计）", "amount": cost})
            else:
                if amount is not None:
                    stage = f"第{args.renewal_number}次续展"
                    label, cost = ind_item("续展单独指定费", code, amount, unit, args.designs,
                                           f"{stage}｜实时核对值（非快照）")
                    items.append({"label": label, "amount": cost})
                else:
                    plan = resolve_individual_renewal(data, args, code, args.designs, args.renewal_number)
                    items.extend(plan["items"])
                    notes.extend(plan["notes"])

        if args.grace:
            grace = round(basic * int(sched["renewal"]["grace_additional"]["percent"]) / 100)
            items.append({"label": f"宽限期额外费（续展基本费的 {sched['renewal']['grace_additional']['percent']}%）", "amount": grace})

    total = sum(item["amount"] for item in items)
    result = {
        "status": "ok",
        "snapshot": {
            "schedule_version": data["meta"]["schedule_version"],
            "individual_version": data["meta"]["individual_version"],
            "verified_on": data["meta"]["verified_on"],
        },
        "inputs": {
            "type": args.type,
            "designs": args.designs,
            "reproductions": args.reproductions,
            "paper_pages": args.paper_pages,
            "description_words": args.description_words,
            "ldc": bool(args.ldc),
            "renewal_number": args.renewal_number if args.type == "renewal" else None,
            "grace": bool(args.grace) if args.type == "renewal" else False,
            "as_of": as_of.isoformat(),
            "locarno_class": args.locarno_class,
            "registration_date": args.registration_date.isoformat() if args.registration_date else None,
            "include_part2": bool(args.include_part2),
            "deposit": args.deposit,
            "entity_map": args.entity_map,
            "designations": [
                {"code": c, "kind": k, "amount_override": a, "unit": u} for c, k, a, u in args.designations
            ],
        },
        "items": items,
        "total_chf": total,
        "total_cny": round(total * args.cny_rate, 2) if args.cny_rate else None,
        "notes": notes,
        "disclaimers": DISCLAIMERS,
        "links": {"calculator": CALCULATOR_URL, "schedule": SCHEDULE_URL, "individual": INDIVIDUAL_URL},
    }
    return result


def render_text(result: dict, args: argparse.Namespace) -> str:
    snap = result["snapshot"]
    inputs = result["inputs"]
    if inputs["type"] == "application":
        scenario = f"国际申请（{inputs['designs']} 项设计、{inputs['reproductions']} 幅复制件）"
    else:
        scenario = f"国际注册续展（第 {inputs['renewal_number']} 次续展、{inputs['designs']} 项设计"
        scenario += "、宽限期内" if inputs["grace"] else "、正常期限内"
        scenario += "）"
    if inputs["ldc"]:
        scenario += "；LDC 减费"
    lines = [
        "海牙体系国际规费估算（离线快照）",
        f"快照：费用表 {snap['schedule_version']}；单独指定费 {snap['individual_version']}；核验日 {snap['verified_on']}",
        f"情形：{scenario}",
        "",
    ]
    for item in result["items"]:
        lines.append(f"- {item['label']}：{item['amount']} CHF")
    lines.append("")
    lines.append(f"合计：{result['total_chf']} CHF")
    if result["total_cny"] is not None:
        source = f"（汇率来源：{args.rate_source}）" if args.rate_source else "（未提供汇率来源，须自行注明）"
        lines.append(f"折算：{result['total_cny']} CNY @ 1 CHF≈{args.cny_rate} {source}")
    if result["notes"]:
        lines.append("")
        for note in result["notes"]:
            lines.append(f"※ {note}")
    lines.append("")
    lines.append("提示：")
    for item in result["disclaimers"]:
        lines.append(f"- {item}")
    lines.append(f"- 费用计算器：{CALCULATOR_URL}")
    lines.append(f"- 费用表：{SCHEDULE_URL}｜单独指定费明细：{INDIVIDUAL_URL}")
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="海牙体系国际规费计算器（离线快照版，仅 CHF 国际规费）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--type", choices=["application", "renewal"], default="application", help="业务类型：国际申请（默认）或国际注册续展")
    parser.add_argument("--designs", type=int, default=1, help="外观设计件数（1–100，默认 1）")
    parser.add_argument("--reproductions", type=int, default=None, help="复制件（视图）幅数（1–500，默认等于设计件数）")
    parser.add_argument("--renewal-number", type=int, choices=list(range(1, 11)), default=1, help="第几次续展（1–10，默认第 1 次）")
    parser.add_argument("--designate", action="append", default=[], metavar="CC:TYPE[:AMOUNT[:app|design]]", help="指定缔约方，可重复；类型 ind / std1 / std2 / std3")
    parser.add_argument("--entity", action="append", default=[], metavar="CC=default|small|micro|reduced",
                        help="缔约方减费档（可重复，如 US=small、TU=reduced、MX=reduced、IL=reduced）")
    parser.add_argument("--locarno-class", type=int, default=None,
                        help="设计的洛迦诺类别（1–32；用于韩国等按类别改适用标准指定费的特例）")
    parser.add_argument("--registration-date", default=None,
                        help="国际注册日 YYYY-MM-DD（用于按注册日区分的规则：美国第 2 部分过渡档、韩国续展类别表、土库曼斯坦适用性）")
    parser.add_argument("--include-part2", action="store_true",
                        help="计入分两部分缴纳的单独指定费第 2 部分（美国、墨西哥）")
    parser.add_argument("--part2-basis", choices=["app", "design"], default="app",
                        help="第 2 部分的计费基数（默认按每件国际申请；页面未标明，须复核）")
    parser.add_argument("--deposit", choices=["single", "multiple"], default=None,
                        help="按交存计费的缔约方（如 OAPI）：单一交存或多交存")
    parser.add_argument("--paper-pages", type=int, default=0, help="纸件提交时复制件页数（0–100；仅纸件计按页附加费）")
    parser.add_argument("--efiling", action="store_true", help="声明经 eHague 电子提交（免除纸件按页附加费）")
    parser.add_argument("--description-words", type=int, default=0, help="说明书字数（超过 100 字部分加费）")
    parser.add_argument("--ldc", action="store_true", help="适用最不发达国家（LDC）减费")
    parser.add_argument("--grace", action="store_true", help="续展处于宽限期，加计续展基本费 50%% 的额外费")
    parser.add_argument("--cny-rate", type=float, default=None, help="可选：1 CHF 折多少 CNY（用于折算）")
    parser.add_argument("--rate-source", default=None, help="可选：汇率来源说明")
    parser.add_argument("--as-of", default=None, help="计算基准日 YYYY-MM-DD（默认今天；用于判断快照适用性与陈旧度）")
    parser.add_argument("--allow-stale", action="store_true", help="快照过期时强制计算（会打印警告）")
    parser.add_argument("--json", action="store_true", help="以 JSON 输出（机器可读）")
    parser.add_argument("--show-snapshot", action="store_true", help="仅打印快照元信息后退出")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.designations = [parse_designation(raw) for raw in args.designate]
    args.entity_map: dict[str, str] = {}
    for raw in args.entity:
        if "=" not in raw:
            parser.error(f"--entity 写法应为 CC=档位（如 US=small），收到 {raw!r}")
        code, status = raw.split("=", 1)
        status = status.strip().lower()
        if status not in ENTITY_SUFFIX:
            parser.error(f"--entity 档位须为 default / small / micro / reduced，收到 {status!r}")
        args.entity_map[code.strip().upper()] = status
    args.registration_date = (parse_date(args.registration_date, "--registration-date")
                              if args.registration_date else None)
    if args.locarno_class is not None and not 1 <= args.locarno_class <= 32:
        parser.error("--locarno-class 须在 1–32 之间（洛迦诺分类大类号）")

    try:
        data = load_snapshot()
    except NoDataError as exc:
        print(str(exc), file=sys.stderr)
        return 3

    if args.show_snapshot:
        meta = data["meta"]
        print(json.dumps(meta, ensure_ascii=False, indent=2))
        return 0

    as_of = parse_date(args.as_of, "--as-of") if args.as_of else _dt.date.today()
    args.designs = within("designs", args.designs)
    args.reproductions = args.designs if args.reproductions is None else within("reproductions", args.reproductions)
    args.paper_pages = within("paper_pages", args.paper_pages)
    args.description_words = within("words", args.description_words)
    if not args.designations:
        parser.error("至少需要一个 --designate 指定缔约方")

    try:
        result = compute(data, args, as_of)
    except NoDataError as exc:
        print(str(exc), file=sys.stderr)
        return 3

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(render_text(result, args))
    return 0


if __name__ == "__main__":
    try:  # Windows 控制台默认编码可能导致中文输出失败
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:  # pragma: no cover
        pass
    raise SystemExit(main())
