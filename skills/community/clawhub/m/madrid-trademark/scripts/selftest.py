"""马德里技能脚本自检（纯标准库，无第三方依赖）。

运行：
    python selftest.py          # 全部用例
    python selftest.py -v       # 打印每个用例的通过明细

覆盖：
  1. 日期工具：月末、闰年 2/29、自然月推进；
  2. 驳回期限：12 / 18 / 异议延长 25 个月、后期指定起算、越界入参拦截；
  3. 续展窗口：正常期 / 提前续展期 / 宽限期 / 已过期四阶段边界，宽限期附加费 = 基本费 50%；
  4. 规费计算：官费口径（附加费例外、后期指定无附加费、颜色与 LDC 档、宽限期按基本费计）、
     单独规费各计费模式、古巴第二段费、保全条款提示；
  5. 数据一致性：references/madrid-fees.md 的单独规费表与 madrid_fee_data.json 逐一比对。
"""

from __future__ import annotations

import io
import re
import sys
import traceback
from contextlib import redirect_stdout
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))

import madrid_dateutil as du  # noqa: E402
from madrid_deadline import (  # noqa: E402
    calculate_refusal_deadline,
    calculate_response_deadline,
    load_response_times,
    main as deadline_main,
)
from madrid_fee import (  # noqa: E402
    calculate_madrid_fee,
    load_fee_data,
    main as fee_main,
    parse_charge_date,
    round_half_up,
)
from madrid_renewal import check_renewal_status, main as renewal_main  # noqa: E402

FEES_MD = SKILL_DIR / "references" / "madrid-fees.md"

fee_calc = calculate_madrid_fee  # 测试内简写


def _configure_stdout() -> None:
    """Windows 管道/重定向下避免 cp936 编码错误（用例标题含中文与符号）。"""
    reconfigure = getattr(sys.stdout, "reconfigure", None)
    if reconfigure is not None:
        try:
            reconfigure(encoding="utf-8")
        except (ValueError, OSError):
            pass

# ---------------------------------------------------------------- 断言工具


class Failure(AssertionError):
    pass


def eq(actual, expected, label):
    if actual != expected:
        raise Failure(f"{label}：期望 {expected!r}，实际 {actual!r}")


def is_true(value, label):
    if not value:
        raise Failure(f"{label}：期望为真，实际 {value!r}")


def raises(exc_type, fn, label):
    try:
        fn()
    except exc_type:
        return
    except Exception as exc:  # noqa: BLE001
        raise Failure(f"{label}：期望抛出 {exc_type.__name__}，实际抛出 {type(exc).__name__}: {exc}") from exc
    raise Failure(f"{label}：期望抛出 {exc_type.__name__}，但未抛出")


# ---------------------------------------------------------------- 1. 日期工具


def test_dateutil():
    eq(du.formalize(du.add_months(du.parse_date("2026-01-31"), 1)), "2026-02-28", "add_months 月末兜底（1/31 → 2/28）")
    eq(du.formalize(du.add_months(du.parse_date("2024-02-29"), 12)), "2025-02-28", "add_months 闰年 2/29 + 12 个月")
    eq(du.formalize(du.add_months(du.parse_date("2020-02-29"), 120)), "2030-02-28", "add_years 闰年 2/29 + 10 年")
    eq(du.formalize(du.add_months(du.parse_date("2026-08-31"), 6)), "2027-02-28", "add_months 8/31 + 6 个月")
    eq(du.formalize(du.add_months(du.parse_date("2026-03-31"), -6)), "2025-09-30", "add_months 负向推进（3/31 − 6 个月）")
    eq(du.days_between(du.parse_date("2026-09-23"), du.parse_date("2027-01-15")), 114, "days_between 跨月计算")
    raises(ValueError, lambda: du.parse_date("2026/01/15"), "parse_date 非法格式")


# ---------------------------------------------------------------- 2. 驳回期限


def test_deadline():
    r12 = calculate_refusal_deadline("2026-01-15", base_months=12, today="2026-09-23")
    eq(r12["base_deadline"], "2027-01-15", "12 个月基准截止日")
    eq(r12["final_deadline"], "2027-01-15", "无异议时最迟截止日同基本截止日")
    eq(r12["days_to_base_deadline"], 114, "剩余天数")

    r18 = calculate_refusal_deadline("2026-01-15", base_months=18, today="2026-09-23")
    eq(r18["base_deadline"], "2027-07-15", "18 个月（已声明 5(2)(b)）截止日")

    r25 = calculate_refusal_deadline("2026-01-15", base_months=18, has_opposition=True, today="2026-09-23")
    eq(r25["final_deadline"], "2028-02-15", "异议延长后最迟截止日（18 + 7）")
    eq(r25["opposition_extension_months"], 7, "异议延长月数")

    # 12 个月 + 异议 → 不允许（第 5 条(2)(c) 以 18 个月声明为基础）
    raises(ValueError, lambda: calculate_refusal_deadline("2026-01-15", base_months=12, has_opposition=True),
           "12 个月基础上主张异议延长应被拦截")
    raises(ValueError, lambda: calculate_refusal_deadline("2026-01-15", base_months=6),
           "非 12/18 的 base_months 应被拦截")

    # 后期指定自登记日起算
    sub = calculate_refusal_deadline("2026-03-01", base_months=12, today="2026-09-23",
                                     kind="subsequent-designation")
    eq(sub["base_deadline"], "2027-03-01", "后期指定按登记日起算")
    is_true("后期指定登记日" in sub["start_date_kind"], "后期指定起算日类型标注")

    # 月末注册
    eq(calculate_refusal_deadline("2026-01-31", base_months=12)["base_deadline"], "2027-01-31", "月末注册 + 12 个月")
    eq(calculate_refusal_deadline("2026-08-31", base_months=12)["base_deadline"], "2027-08-31", "8/31 + 12 个月")

    # 状态机
    eq(calculate_refusal_deadline("2026-01-15", 12, today="2026-06-01")["status"], "仍在驳回期内", "驳回期内状态")
    eq(calculate_refusal_deadline("2026-01-15", 12, today="2026-12-20")["status"],
       "仍在驳回期内（距基本截止日不足 30 天，建议每周核查）", "临近截止日状态")
    is_true("已过" in calculate_refusal_deadline("2026-01-15", 12, today="2027-03-01")["status"], "期限已过状态")


# ---------------------------------------------------------------- 2b. 答复期限（Rule 17(7)）


def test_response_deadline():
    """答复临时驳回的期限：按日/按月、6 种起算基准、条件期限与未收录成员。"""
    # 中国：依职权 15 日、异议 30 日，自收到 WIPO 转交通知之日起算
    cn = calculate_response_deadline(cp="CN", received="2026-09-20", today="2026-09-25")
    eq(cn["limit"], "15 日", "中国依职权驳回 15 日")
    eq(cn["deadline"], "2026-10-05", "中国依职权截止日 = 收到日 + 15 日")
    eq(cn["computed_from"], "注册人收到通知之日（与官方基准一致）", "中国起算基准与收件日一致")
    eq(cn["days_remaining"], 10, "中国案例剩余天数")

    cn_op = calculate_response_deadline(cp="CN", opposition=True, received="2026-09-20")
    eq(cn_op["limit"], "30 日", "中国异议类驳回 30 日")
    eq(cn_op["deadline"], "2026-10-20", "中国异议类截止日 = 收到日 + 30 日")

    # 中国「视为送达」口径（实务中的 30 日复审期 = 15 日视为送达 + 15 日复审期）
    cn_notified = calculate_response_deadline(cp="CN", notified="2026-09-01", today="2026-09-25")
    eq(cn_notified["deemed_service_date"], "2026-09-16", "发文日起满 15 日视为送达")
    eq(cn_notified["deadline"], "2026-10-01", "视为送达口径截止日 = 视为送达日 + 15 日")
    eq(cn_notified["overall_days_from_wipo_notification"], 30,
       "依职权驳回：自发文日 30 日（实务口径「30 日复审期」）")

    cn_op_notified = calculate_response_deadline(cp="CN", opposition=True, notified="2026-09-01")
    eq(cn_op_notified["overall_days_from_wipo_notification"], 45,
       "异议类驳回：自发文日 45 日（15 日视为送达 + 30 日）")

    # 同时给出发文日与收件日 → 提示按较早者控制风险
    both = calculate_response_deadline(cp="CN", notified="2026-09-01", received="2026-09-20")
    eq(both["deadline"], "2026-10-01", "视为送达口径截止日")
    eq(both["deadline_from_received"], "2026-10-05", "实际收件口径截止日")
    is_true(any("较早者" in w for w in both["warnings"]), "两套口径并存时应提示取较早者")

    # 无「视为送达」规则的成员不得按发文日推算
    raises(ValueError, lambda: calculate_response_deadline(cp="FR", notified="2026-09-01"),
           "法国无视为送达规则，按发文日推算应被拒绝")

    # 法国：基准为 WIPO 转交之日（非收件日）→ 仅给收到日必须拒绝
    raises(ValueError, lambda: calculate_response_deadline(cp="FR", received="2026-09-20"),
           "非收件基准下仅给 --received 应被拒绝")
    fr = calculate_response_deadline(cp="FR", base_date="2026-09-20")
    eq(fr["limit"], "1 个月", "法国依职权驳回 1 个月")
    eq(fr["deadline"], "2026-10-20", "法国截止日 = 起算日 + 1 个月")
    is_true(fr["basis_observable_by_holder"] is False, "法国基准标注为注册人不可直接观察")

    # 德国：条件期限（4 个月 / 居所在德者 2 个月）→ 保守值取 2 个月
    de = calculate_response_deadline(cp="DE", base_date="2026-09-20")
    eq(de["deadline"], "2027-01-20", "德国主期限 4 个月")
    eq(de["deadline_conservative"], "2026-11-20", "德国保守期限按 2 个月")
    is_true(any("条件期限" in w for w in de["warnings"]), "条件期限应给出告警")

    # 美国异议类：基准为 TTAB 命令之日
    raises(ValueError, lambda: calculate_response_deadline(cp="US", opposition=True, received="2026-09-20"),
           "美国异议类不可按收件日计算")
    us = calculate_response_deadline(cp="US", opposition=True, base_date="2026-10-01")
    eq(us["limit"], "40 日", "美国异议类 40 日")
    eq(us["deadline"], "2026-11-10", "美国异议类截止日 = TTAB 命令日 + 40 日")

    # 不适用 / 未收录 / 手工兜底
    raises(ValueError, lambda: calculate_response_deadline(cp="JP", opposition=True, received="2026-09-20"),
           "日本异议类标注不适用应被拒绝")
    raises(ValueError, lambda: calculate_response_deadline(cp="KR", received="2026-09-20"),
           "未收录成员应被拒绝并给出提示")
    manual = calculate_response_deadline(limit_days=45, received="2026-09-20")
    eq(manual["deadline"], "2026-11-04", "手工期限 45 日")
    raises(ValueError, lambda: calculate_response_deadline(cp="CN"),
           "未提供 received/base-date 应被拒绝")


def test_response_times_data_matches_doc():
    """答复期限数据文件与 declarations.md 全表须一致（成员、名称、基准词汇）。"""
    data = load_response_times()
    members = data["members"]
    eq(len(members), 38, "WIPO Rule 17(7) 表收录成员数")

    meta = data["meta"]
    is_true("38" in meta["coverage"], "覆盖度说明应载明 38/117")

    doc = (SKILL_DIR / "references" / "madrid-declarations.md").read_text(encoding="utf-8")
    missing = []
    for code, entry in members.items():
        if entry["name_zh"] not in doc:
            missing.append(f"{code}({entry['name_zh']})")
        for key in ("ex_officio", "opposition"):
            limit = entry.get(key) or {}
            basis = limit.get("basis")
            if basis and basis not in data["basis_glossary"]:
                missing.append(f"{code}.{key} 的基准 {basis} 未在 glossary 中")
    if missing:
        raise Failure("答复期限数据与声明文档不一致：" + "、".join(missing))

    # 起算基准须为 6 种之一（页面原文口径）
    bases = {limit.get("basis") for entry in members.values()
             for limit in (entry.get("ex_officio") or {}, entry.get("opposition") or {})
             if limit.get("basis")}
    is_true(bases <= set(data["basis_glossary"]), f"所有基准均须在 glossary 中：{sorted(bases)}")


# ---------------------------------------------------------------- 3. 续展窗口


def test_renewal():
    normal = check_renewal_status("2016-07-01", 10, today="2025-12-31")
    eq(normal["phase"], "正常期", "到期前 6 个月之外为正常期")

    early = check_renewal_status("2016-07-01", 10, today="2026-01-01")
    eq(early["phase"], "提前续展期（可缴费）", "窗口开启日进入提前续展期")
    eq(early["early_renewal_start"], "2026-01-01", "提前续展窗口开始日")
    eq(early["expiry_date"], "2026-07-01", "到期日")

    grace = check_renewal_status("2016-07-01", 10, today="2026-08-01")
    eq(grace["phase"], "宽限期（加收附加费）", "到期后进入宽限期")
    eq(grace["grace_period_end"], "2027-01-01", "宽限期届满日")

    expired = check_renewal_status("2016-07-01", 10, today="2027-01-02")
    eq(expired["phase"], "已过期", "宽限期届满后为已过期")

    eq(grace["grace_surcharge_chf"], 327, "宽限期附加费 = 基本费 50%（327 CHF）")
    eq(grace["renewal_basic_chf"], 653, "续展基本费基准 653 CHF")
    eq(check_renewal_status("2016-07-01", 20, today="2026-08-01")["expiry_date"], "2036-07-01",
       "协定 20 年保护期")
    eq(check_renewal_status("2020-02-29", 10, today="2026-01-01")["expiry_date"], "2030-02-28",
       "闰年 2/29 注册 + 10 年")
    raises(ValueError, lambda: check_renewal_status("2016-07-01", 12), "非 10/20 保护期应被拦截")


# ---------------------------------------------------------------- 4. 规费计算


def test_fees():
    data = load_fee_data()
    wipo = data["wipo_fees"]
    eq(round_half_up(wipo["renewal_basic"] * wipo["grace_surcharge_percent_of_basic"] / 100), 327,
       "宽限期附加费精确值 326.5 按整 CHF 进位为 327")
    eq(wipo["grace_surcharge_amount"], 327, "数据文件中的宽限期附加费快照值为 327")

    # 全部为单独规费国 → 不收附加费
    all_ind = calculate_madrid_fee(["US", "JP", "KR"], 8)
    eq(all_ind["supplementary_fee"]["amount"], 0, "指定国全为单独规费国时不收附加费")
    eq(all_ind["basic_fee"]["amount"], 653, "无色基本费 653")
    eq(all_ind["per_contracting_party"]["US"]["金额"], 460 * 8, "美国按类计费")
    eq(all_ind["per_contracting_party"]["JP"]["金额"], 221 + 208 * 7, "日本第 1 类 + 附加类")
    eq(all_ind["per_contracting_party"]["KR"]["金额"], 150 * 8, "韩国按类计费")
    eq(all_ind["total_chf"], 653 + 0 + 460 * 8 + (221 + 208 * 7) + 150 * 8, "合计（全单独规费国）")

    # madrid-fees.md §十三 示例：5 个未列名缔约方、10 类、无色 = 1,853 CHF
    comp = calculate_madrid_fee(["RU", "ZZ", "YY", "WW", "VV"], 10)
    eq(comp["complementary_fee_total"], 500, "补充费 100 × 5 缔约方")
    eq(comp["supplementary_fee"]["amount"], 700, "附加费（10 − 3）× 100")
    eq(comp["total_chf"], 1853, "补充费口径示例合计 1,853 CHF")

    # 颜色 / LDC
    eq(calculate_madrid_fee(["RU"], 1, color=True)["basic_fee"]["amount"], 903, "彩色基本费 903")
    eq(calculate_madrid_fee(["RU"], 1, ldc=True)["basic_fee"]["amount"], 65, "LDC 无色基本费 65")
    eq(calculate_madrid_fee(["RU"], 1, ldc=True, color=True)["basic_fee"]["amount"], 90, "LDC 彩色基本费 90")

    # 后期指定：基本费 300，无附加费
    later = calculate_madrid_fee(["JP"], 2, later_designation=True)
    eq(later["basic_fee"]["amount"], 300, "后期指定基本费 300")
    eq(later["supplementary_fee"]["amount"], 0, "后期指定不收附加费")
    eq(later["total_chf"], 300 + (221 + 208), "后期指定合计")

    # 续展宽限期：附加费按基本费计，单独规费取宽限期费率
    late_us = calculate_madrid_fee(["US"], 1, renewal=True, late=True)
    eq(late_us["grace_surcharge"], 327, "宽限期附加费 327")
    eq(late_us["per_contracting_party"]["US"]["金额"], 249, "美国续展费率")
    eq(late_us["total_chf"], 653 + 327 + 249, "续展宽限期合计（美国）")

    late_br = calculate_madrid_fee(["BR"], 1, renewal=True, late=True)
    eq(late_br["per_contracting_party"]["BR"]["金额"], 292, "巴西宽限期内续展费率 292")

    late_oapi = calculate_madrid_fee(["OA"], 1, renewal=True, late=True)
    eq(late_oapi["per_contracting_party"]["OA"]["金额"], 699 + 182, "OAPI 宽限期为追加费（+182）")
    eq(late_oapi["total_chf"], 653 + 327 + 699 + 182, "OAPI 宽限期合计")

    # 古巴第二段费
    cu = calculate_madrid_fee(["CU"], 3)
    eq(cu["second_part_fee"], 72, "古巴第二段规费 72")
    eq(cu["total_chf"], 653 + 239 + 72, "古巴申请合计（含第二段）")

    # 集体商标与回退提示
    cn_collective = calculate_madrid_fee(["CN"], 3, collective=True)
    eq(cn_collective["per_contracting_party"]["CN"]["金额"], 661 + 331 * 2, "中国集体商标费率")
    us_collective = calculate_madrid_fee(["US"], 1, collective=True)
    is_true(any("集体/证明商标" in n for n in us_collective["notes"]), "无集体商标费率时给出回退提示")

    # 保全条款提示与入参校验
    is_true(any("保全条款" in n for n in calculate_madrid_fee(["FR"], 1, origin="CN")["notes"]),
            "指定 --origin 时给出保全条款提示")
    raises(ValueError, lambda: calculate_madrid_fee([], 1), "空缔约方列表应被拦截")
    raises(ValueError, lambda: calculate_madrid_fee(["US"], 0), "类别数 < 1 应被拦截")
    raises(ValueError, lambda: calculate_madrid_fee(["US"], 1, late=True), "非续展阶段使用 --late 应被拦截")
    raises(ValueError, lambda: calculate_madrid_fee(["US"], 1, renewal=True, later_designation=True),
           "--renewal 与 --later-designation 并用应被拦截")


# ---------------------------------------------------------------- 4b. 费率生效日


def test_effective_dates():
    """已公告的费率调整须按计费日期生效，且不得外推未公告的组件。"""
    eq(fee_calc(["ID"], 1, charge_date="2026-10-31")["per_contracting_party"]["ID"]["金额"], 91,
       "印尼在生效日前按旧值 91")
    eq(fee_calc(["ID"], 1, charge_date="2026-11-01")["per_contracting_party"]["ID"]["金额"], 125,
       "印尼自 2026-11-01 起按新值 125")
    eq(fee_calc(["IL"], 2, charge_date="2026-11-01")["per_contracting_party"]["IL"]["金额"], 503 + 354,
       "以色列第 1 类调为 503、附加类维持 354")
    eq(fee_calc(["IL"], 2, charge_date="2026-10-31")["per_contracting_party"]["IL"]["金额"], 471 + 354,
       "以色列生效日前按旧值 471")

    # 续展侧未获实测 → 须提示复核，不得沿用申请侧新值
    il_renewal = fee_calc(["IL"], 1, renewal=True, charge_date="2026-11-01")
    eq(il_renewal["per_contracting_party"]["IL"]["金额"], 840, "以色列续展侧保持快照值 840（未公告调整）")
    is_true(any("复核" in n for n in il_renewal["notes"]), "续展侧未实测应给出复核提示")

    # 尚未生效的调整 → 提示跨生效日须出两套预算
    is_true(any("跨生效日提示" in n for n in fee_calc(["ID"], 1, charge_date="2026-09-25")["notes"]),
            "计费日早于生效日时应提示跨生效日")
    is_true(all("跨生效日提示" not in n for n in fee_calc(["ID"], 1, charge_date="2026-11-05")["notes"]),
            "已生效后不再提示跨生效日")

    # 日期解析格式
    eq(parse_charge_date("2026/11/01"), parse_charge_date("2026-11-01"), "斜杠与短横线格式等价")
    raises(ValueError, lambda: parse_charge_date("2026.11.01"), "非法日期格式应被拦截")

    # fees.md 须记录同两项调整（防止「数据文件改了、文档没改」）
    text = FEES_MD.read_text(encoding="utf-8")
    for token in ("125", "503"):
        is_true(token in text, f"madrid-fees.md 应记录 2026-11-01 调整中的 {token}")


# ---------------------------------------------------------------- 5. 数据一致性

CLASS_SPEC = re.compile(r"[（(](?:第|前)?\s*\d*\s*类(?:以内)?[）)]")
TRAILING_PAREN = re.compile(r"[（(][^（()）]*[）)]\s*$")
INT_TOKEN = re.compile(r"\d[\d,]*")


def _strip_trailing_parenthetical(name: str) -> str:
    return TRAILING_PAREN.sub("", name).strip()


def _ints_in_cell(cell: str) -> set[int]:
    if "同左" in cell:
        return set()
    cleaned = CLASS_SPEC.sub("", cell)
    return {int(token.replace(",", "")) for token in INT_TOKEN.findall(cleaned)}


def _ints_in_json(value) -> set[int]:
    found: set[int] = set()
    if isinstance(value, bool):
        return found
    if isinstance(value, int):
        found.add(value)
    elif isinstance(value, dict):
        for item in value.values():
            found |= _ints_in_json(item)
    elif isinstance(value, list):
        for item in value:
            found |= _ints_in_json(item)
    return found


def _parse_md_individual_fee_rows() -> dict[str, list[str]]:
    rows: dict[str, list[str]] = {}
    text = FEES_MD.read_text(encoding="utf-8")
    in_window = False
    for line in text.splitlines():
        if "主要缔约方单独规费速查" in line:
            in_window = True
            continue
        if in_window and line.startswith("## "):
            break
        if not in_window or not line.strip().startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 3 or cells[0] in ("缔约方", ""):
            continue
        if set(cells[0]) <= set("-: "):
            continue
        rows[_strip_trailing_parenthetical(cells[0])] = cells[1:3]
    return rows


def test_fees_md_matches_json():
    if not FEES_MD.exists():
        raise Failure(f"找不到 references/madrid-fees.md：{FEES_MD}")
    data = load_fee_data()
    individual = data["individual_fees"]
    not_listed = data.get("not_listed_examples", {})
    complementary = data["wipo_fees"]["complementary_fee_per_contracting_party"]

    rows = _parse_md_individual_fee_rows()
    is_true(len(rows) > 50, f"应从 madrid-fees.md 解析出逐一列名的缔约方（实际 {len(rows)} 行）")

    by_name = {entry["name_zh"]: code for code, entry in individual.items()}
    not_listed_names = {entry["name_zh"] for entry in not_listed.values()}
    missing_in_json = sorted(set(rows) - set(by_name) - not_listed_names)
    if missing_in_json:
        raise Failure(f"madrid-fees.md 中有、madrid_fee_data.json 中无的缔约方：{missing_in_json}")
    missing_in_md = sorted(set(by_name) - set(rows))
    if missing_in_md:
        raise Failure(f"madrid_fee_data.json 中有、madrid-fees.md 中无的缔约方：{missing_in_md}")

    mismatches: list[str] = []
    for name, (app_cell, renewal_cell) in rows.items():
        md_ints = _ints_in_cell(app_cell) | _ints_in_cell(renewal_cell)
        if name in by_name:
            json_ints = _ints_in_json(individual[by_name[name]])
        else:  # 未列名缔约方（如俄罗斯）：md 只应出现标准补充费
            json_ints = {complementary}
        extra = sorted(md_ints - json_ints)
        if extra:
            mismatches.append(f"{name}({by_name.get(name, '未列名')})：md 中的 {extra} 在 JSON 中找不到")
    if mismatches:
        raise Failure("fees.md 与 fee_data.json 不一致：\n    " + "\n    ".join(mismatches))


# ---------------------------------------------------------------- 6. CLI 冒烟测试


def _run_cli(entry, argv):
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        code = entry(argv)
    return code, buffer.getvalue()


def test_cli_smoke():
    """命令行入口冒烟：参数解析（含中文帮助文本与 % 转义）、退出码与关键字段。"""
    cases = [
        (fee_main, ["--countries", "US,JP", "--classes", "3"], '"total_chf"'),
        (fee_main, ["--countries", "BR", "--classes", "1", "--renewal", "--late"], '"grace_surcharge"'),
        (fee_main, ["--countries", "CU", "--classes", "3", "--collective"], '"second_part_fee"'),
        (fee_main, ["--countries", "ID,IL", "--classes", "2", "--date", "2026/11/01"], '"charge_date"'),
        (fee_main, ["--countries", "ID", "--classes", "1", "--date", "2026-10-31"], '"total_chf"'),
        (deadline_main, ["--register", "2026-01-15", "--declared-18", "--opposition",
                         "--today", "2026-09-23"], '"final_deadline"'),
        (deadline_main, ["--register", "2026-01-15", "--base-months", "12"], '"base_months"'),
        (renewal_main, ["--register", "2016-07-01", "--today", "2026-09-23"], '"phase"'),
        (deadline_main, ["--respond", "--cp", "CN", "--received", "2026-09-20"], '"deadline"'),
        (deadline_main, ["--respond", "--cp", "CN", "--opposition", "--received", "2026-09-20"],
         '"refusal_type"'),
        (deadline_main, ["--respond", "--limit-months", "3", "--received", "2026-09-20"], '"limit"'),
        (deadline_main, ["--respond", "--cp", "CN", "--notified", "2026-09-01"], '"deemed_service_date"'),
    ]
    for entry, argv, token in cases:
        code, output = _run_cli(entry, argv)
        eq(code, 0, f"CLI 退出码（{' '.join(argv)}）")
        is_true(token in output, f"CLI 输出应包含 {token}（{' '.join(argv)}）")

    # 非法参数应返回退出码 2 并输出 error 字段
    code, output = _run_cli(fee_main, ["--countries", "US", "--classes", "0"])
    eq(code, 2, "非法类别数应返回退出码 2")
    is_true('"error"' in output, "非法入参应输出 error 字段")

    code, output = _run_cli(deadline_main, ["--register", "2026-01-15", "--base-months", "12", "--opposition"])
    eq(code, 2, "12 个月 + 异议应返回退出码 2")


def test_version_consistency():
    """版本一致性：frontmatter（单一真源）与文末同步点必须一致。"""
    skill_md = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")

    m_fm = re.search(r'^version:\s*["\']?([0-9]+\.[0-9]+\.[0-9]+)', skill_md, re.MULTILINE)
    is_true(m_fm is not None, "frontmatter 应含 SemVer version 字段")
    v_fm = m_fm.group(1)

    m_tail = re.search(r'^> \*\*版本\*\*：v([0-9]+\.[0-9]+\.[0-9]+)', skill_md, re.MULTILINE)
    is_true(m_tail is not None, "SKILL.md 文末应含版本行")
    eq(m_tail.group(1), v_fm, "SKILL.md 文末版本 == frontmatter")


INDEX_NAME = "madrid-file-index.md"
INDEX_LARGE = ["madrid-agreement.md", "madrid-protocol.md", "madrid-regulations.md",
               "madrid-admin-instructions.md"]


def regenerate_index():
    """重生成 madrid-file-index.md 的第 0 节（体积表）与第 I 节（章节→行号索引）。"""
    d = SKILL_DIR / "references"
    sizes = []
    for p in sorted(d.iterdir()):
        if p.is_file() and p.name != INDEX_NAME:
            b = p.read_bytes()
            sizes.append("| `%s` | %d | %d |" % (p.name, len(b), b.count(b"\n")))
    blocks = []
    for name in INDEX_LARGE:
        p = d / name
        if not p.exists():
            continue
        src = p.read_text(encoding="utf-8").splitlines()
        blocks.append("### %s（%d 行）" % (name, len(src)))
        blocks.append("| 行号 | 章节 |")
        blocks.append("| --- | --- |")
        for i, s in enumerate(src, 1):
            if s.startswith("## "):
                blocks.append("| %d | %s |" % (i, s[3:].strip()))
        blocks.append("")
    path = d / INDEX_NAME
    txt = path.read_text(encoding="utf-8")
    txt = re.sub(r"(?s)<!-- SIZE_TABLE_START -->.*?<!-- SIZE_TABLE_END -->",
                 "<!-- SIZE_TABLE_START -->\n| 文件 | 字节 | 行数 |\n| --- | --- | --- |\n"
                 + "\n".join(sizes) + "\n<!-- SIZE_TABLE_END -->", txt, count=1)
    txt = re.sub(r"(?s)<!-- LINE_INDEX_START -->.*?<!-- LINE_INDEX_END -->",
                 "<!-- LINE_INDEX_START -->\n" + "\n".join(blocks) + "\n<!-- LINE_INDEX_END -->", txt, count=1)
    txt = txt.replace("\r\n", "\n").replace("\n", "\r\n")
    path.write_text(txt, encoding="utf-8", newline="")
    return path


def test_reference_integrity():
    """引用存在性：SKILL.md 与全部 references/*.md 中的 @references/… 指针必须存在（含 .md 与 .pdf）。"""
    pat = re.compile(r"@references/([^\s`|]+?\.(?:md|pdf))")
    targets = [SKILL_DIR / "SKILL.md"] + sorted((SKILL_DIR / "references").glob("*.md"))
    missing = []
    for p in targets:
        for m in pat.finditer(p.read_text(encoding="utf-8")):
            if not (SKILL_DIR / "references" / m.group(1)).exists():
                missing.append("%s -> %s" % (p.name, m.group(1)))
    is_true(not missing, "引用目标均存在；缺失：%s" % missing)


def test_no_orphan_references():
    """孤儿文件：references/ 下每个文件都应被 SKILL.md 或某个 references/*.md 提及。"""
    d = SKILL_DIR / "references"
    files = sorted(p for p in d.iterdir() if p.is_file())
    md = {p.name: p.read_text(encoding="utf-8") for p in files if p.suffix == ".md"}
    skill_txt = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    orphans = []
    for p in files:
        others = skill_txt + "".join(t for n, t in md.items() if n != p.name)
        if p.name not in others:
            orphans.append(p.name)
    is_true(not orphans, "无孤儿文件；孤儿：%s" % orphans)


def _index_text():
    return (SKILL_DIR / "references" / "madrid-file-index.md").read_text(encoding="utf-8")


def test_file_index_size_table():
    """体积表漂移：madrid-file-index.md 第 0 节声明的字节/行数须与磁盘一致，且覆盖全部 references 文件。"""
    rows = {}
    for m in re.finditer(r"^\|\s*`([^`]+\.md)`\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|", _index_text(), re.MULTILINE):
        rows[m.group(1)] = (int(m.group(2)), int(m.group(3)))
    is_true(rows, "第 0 节体积表应可解析")
    d = SKILL_DIR / "references"
    actual = {}
    for p in sorted(d.iterdir()):
        if p.is_file() and p.name != "madrid-file-index.md":
            b = p.read_bytes()
            actual[p.name] = (len(b), b.count(b"\n"))
    bad = [n for n in rows if n in actual and actual[n] != rows[n]] + [n for n in rows if n not in actual]
    missing = [n for n in actual if n not in rows]
    is_true(not bad, "体积表与磁盘一致；偏差：%s" % [(n, rows.get(n), actual.get(n)) for n in bad])
    is_true(not missing, "体积表已覆盖全部文件；未登记：%s" % missing)


def test_file_index_line_numbers():
    """索引行号有效性：madrid-file-index.md 第 I 节声明的行号处须确为所声明章节。"""
    cur, checked, bad = None, 0, []
    for ln in _index_text().splitlines():
        mf = re.match(r"^###\s+(\S+\.md)", ln.strip())
        if mf:
            cur = mf.group(1)
            continue
        mr = re.match(r"^\|\s*(\d+)\s*\|\s*(.+?)\s*\|$", ln.strip())
        if mr and cur:
            n, title = int(mr.group(1)), mr.group(2)
            p = SKILL_DIR / "references" / cur
            if not p.exists():
                bad.append("%s 不存在" % cur)
                continue
            src = p.read_text(encoding="utf-8").splitlines()
            if not (1 <= n <= len(src)):
                bad.append("%s:%d 越界" % (cur, n))
                continue
            if title in src[n - 1]:
                checked += 1
            else:
                bad.append("%s:%d 期望含「%s」实际「%s」" % (cur, n, title, src[n - 1].strip()[:40]))
    is_true(checked >= 8, "行号索引应覆盖 4 个法律全文文件（实测 %d 条）" % checked)
    is_true(not bad, "行号索引与磁盘对齐；偏差：%s" % bad)


PLATFORM_REQUIRED_FIELDS = ["description", "description_zh", "description_en", "version", "author"]
PLATFORM_ALLOWED_ROOT = {
    "SKILL.md", "references", "scripts", "templates",
    "_meta.json", "_user_meta.json", "_skillhub_meta.json", "_icon.png",
}


def test_platform_structure():
    """平台结构合规（依据开放平台《技能》文档 https://open.workbuddy.cn/docs/skill）：
    ① SKILL.md = YAML frontmatter + Markdown 正文；② 5 个必填字段齐全；
    ③ 一级条目仅平台标准 4 项（外加平台运行期写入的白名单文件）；④ 子资源目录下无子目录（严格 2 级）；
    ⑤ scripts/ 各文件已在 SKILL.md 中声明。
    """
    skill_md = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    lines = skill_md.splitlines()

    # ① frontmatter 结构
    is_true(bool(lines) and lines[0].strip() == "---", "SKILL.md 首行应为 ---（YAML frontmatter 起始）")
    end = next((i for i, l in enumerate(lines[1:], 1) if l.strip() == "---"), None)
    is_true(end is not None, "frontmatter 应有闭合的 ---")
    fm_keys = [l.split(":", 1)[0].strip() for l in lines[1:end] if re.match(r"^[A-Za-z_-]+:", l)]

    # ② 5 个必填字段
    miss = [f for f in PLATFORM_REQUIRED_FIELDS if f not in fm_keys]
    is_true(not miss, "frontmatter 缺少平台必填字段：%s" % miss)

    # ③ 一级条目
    root = {p.name for p in SKILL_DIR.iterdir()}
    for need in ("SKILL.md", "references", "scripts", "templates"):
        is_true(need in root, "缺少平台标准一级条目：%s" % need)
    extra = sorted(root - PLATFORM_ALLOWED_ROOT)
    is_true(not extra, "一级条目含非平台标准项：%s" % extra)

    # ④ 子资源目录下无子目录（严格 2 级；可捕获 __pycache__）
    subdirs = []
    for d in ("references", "scripts", "templates"):
        p = SKILL_DIR / d
        if p.is_dir():
            subdirs += ["%s/%s" % (d, c.name) for c in p.iterdir() if c.is_dir()]
    is_true(not subdirs, "子资源目录下不得有子目录（严格 2 级）：%s" % subdirs)

    # ⑤ scripts 已在 SKILL.md 声明
    undeclared = sorted(p.name for p in (SKILL_DIR / "scripts").iterdir()
                        if p.is_file() and p.name not in skill_md)
    is_true(not undeclared, "scripts/ 文件未在 SKILL.md 中声明：%s" % undeclared)


ENCODING_SKIP_SUFFIX = {".pdf", ".png", ".jpg", ".zip", ".pyc"}


def test_encoding_purity():
    """行尾纯度（家族约定）：Markdown（SKILL.md / references / templates）= 纯 CRLF；
    scripts/ 下 .py 与 .json = LF；均须无 BOM、无 \r\r\n、无孤立 CR。
    （仅查家族约定的文本类文件，二进制资源不在此列。）
    """
    targets = [(SKILL_DIR / "SKILL.md", "CRLF")]
    for sub, expect in (("references", "CRLF"), ("templates", "CRLF"), ("scripts", "LF")):
        d = SKILL_DIR / sub
        if not d.is_dir():
            continue
        for p in sorted(d.iterdir()):
            if p.is_file() and p.suffix.lower() not in ENCODING_SKIP_SUFFIX:
                targets.append((p, expect))

    bad = []
    for p, expect in targets:
        b = p.read_bytes()
        rel = "%s/%s" % (p.parent.name, p.name) if p.parent != SKILL_DIR else p.name
        if b.startswith(b"\xef\xbb\xbf"):
            bad.append("%s 含 UTF-8 BOM" % rel)
            continue
        dbl = b.count(b"\r\r\n")
        lone = b.count(b"\r") - b.count(b"\r\n")
        if dbl or lone:
            bad.append("%s 行尾不纯（\\r\\r\\n ×%d，孤立 CR ×%d）" % (rel, dbl, lone))
            continue
        crlf_n, lf_n = b.count(b"\r\n"), b.count(b"\n") - b.count(b"\r\n")
        if expect == "CRLF" and lf_n:
            bad.append("%s 应为纯 CRLF，却含裸 LF ×%d" % (rel, lf_n))
        elif expect == "LF" and crlf_n:
            bad.append("%s 应为纯 LF，却含 CRLF ×%d" % (rel, crlf_n))
    is_true(not bad, "行尾纯度合规；异常：%s" % bad)


# ---------------------------------------------------------------- 运行器

TESTS = [
    ("日期工具（月末/闰年/自然月）", test_dateutil),
    ("驳回期限（12/18/25 与后期指定）", test_deadline),
    ("答复期限（Rule 17(7)：15/30 日与 6 种起算基准）", test_response_deadline),
    ("答复期限数据与声明文档一致（38 成员）", test_response_times_data_matches_doc),
    ("续展窗口（四阶段与宽限期附加费）", test_renewal),
    ("规费计算（口径、模式、第二段费）", test_fees),
    ("费率生效日（2026-11-01 调整与跨生效日提示）", test_effective_dates),
    ("数据一致性（fees.md ↔ fee_data.json）", test_fees_md_matches_json),
    ("命令行入口冒烟（参数解析与退出码）", test_cli_smoke),
    ("版本一致性（frontmatter / SKILL 文末）", test_version_consistency),
    ("引用存在性（@references 指针，含 .md 与 .pdf）", test_reference_integrity),
    ("孤儿文件（references 未被任何文件引用）", test_no_orphan_references),
    ("体积表漂移（madrid-file-index 第 0 节）", test_file_index_size_table),
    ("索引行号有效性（madrid-file-index 第 I 节）", test_file_index_line_numbers),
    ("平台结构合规（frontmatter 必填字段 / 一级条目 / 2 级目录 / scripts 声明）", test_platform_structure),
    ("行尾纯度（Markdown CRLF / scripts LF / 无 BOM 无 \\r\\r\\n）", test_encoding_purity),
]


def main(argv=None) -> int:
    _configure_stdout()
    argv = list(sys.argv[1:] if argv is None else argv)
    verbose = "-v" in argv
    if "--fix-index" in argv:
        regenerate_index()
        print("[FIX] madrid-file-index.md 已重生成（体积表 + 行号索引）")
    failures = []
    for label, fn in TESTS:
        try:
            fn()
        except Exception as exc:  # noqa: BLE001
            failures.append((label, exc))
            print(f"[FAIL] {label}: {exc}")
            if verbose:
                traceback.print_exc()
        else:
            print(f"[PASS] {label}")

    print("-" * 60)
    if failures:
        print(f"自检未通过：{len(failures)}/{len(TESTS)} 组用例失败")
        return 1
    print(f"自检全部通过：{len(TESTS)}/{len(TESTS)} 组用例")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
