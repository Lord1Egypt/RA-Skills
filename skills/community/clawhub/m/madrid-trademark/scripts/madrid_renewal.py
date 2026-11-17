"""马德里国际注册续展窗口计算与提醒。

口径（依据议定书第 7 条、实施细则第 30/31 条与费用表第 6 项）：
  - 保护期：议定书 10 年 / 协定 20 年，每次续展同一期限；
  - 续展窗口：到期前 **6 个月**内可缴费，到期后 **6 个月**为宽限期；
  - 宽限期附加费 = **基本费的 50%（现值 653 × 50% = 327 CHF）**，不是「应缴总额的 50%」；
  - 续展登记日为应续展之日（即使在宽限期内缴纳）；
  - 续展**不得**对注册现状作任何修改（商品/服务调整须另办变更程序）。

用法示例：
    python madrid_renewal.py --register 2016-07-01 --protection-years 10
    python madrid_renewal.py --register 2020-02-29 --today 2026-09-23
"""

from __future__ import annotations

import argparse
import json
import sys

from madrid_dateutil import add_months, add_years, days_between, formalize, parse_date, today as resolve_today

EARLY_WINDOW_MONTHS = 6
GRACE_WINDOW_MONTHS = 6
VALID_PROTECTION_YEARS = (10, 20)


def _configure_stdout() -> None:
    reconfigure = getattr(sys.stdout, "reconfigure", None)
    if reconfigure is not None:
        try:
            reconfigure(encoding="utf-8")
        except (ValueError, OSError):
            pass


def _fee_defaults() -> dict:
    """从费用数据源读取续展基本费与宽限期附加费（缺失时降级为内置常量并标注）。"""
    try:
        from madrid_fee import load_fee_data  # 同目录模块

        wipo = load_fee_data()["wipo_fees"]
        return {
            "renewal_basic": int(wipo["renewal_basic"]),
            "grace_surcharge": int(wipo["grace_surcharge_amount"]),
            "source": "scripts/madrid_fee_data.json",
        }
    except Exception:  # noqa: BLE001 - 数据文件缺失时保持脚本可用
        return {"renewal_basic": 653, "grace_surcharge": 327,
                "source": "内置常量（未读取到 madrid_fee_data.json，请核验）"}


def check_renewal_status(registration_date, protection_years: int = 10, today=None) -> dict:
    """计算续展相关日期与当前阶段。

    参数：
        registration_date: 国际注册日 YYYY-MM-DD
        protection_years: 10（议定书）或 20（协定）
        today: 计算基准日（默认系统当日）；用于复现与测试。
    """
    if protection_years not in VALID_PROTECTION_YEARS:
        raise ValueError(f"protection_years 须为 {VALID_PROTECTION_YEARS} 之一（议定书 10 年 / 协定 20 年）")

    registration = parse_date(registration_date)
    reference_day = resolve_today(today)

    expiry = add_years(registration, protection_years)
    early_start = add_months(expiry, -EARLY_WINDOW_MONTHS)
    grace_end = add_months(expiry, GRACE_WINDOW_MONTHS)

    if reference_day < early_start:
        phase = "正常期"
        days_to_open = days_between(reference_day, early_start)
        tip = f"距可续展窗口开始还有 {days_to_open} 天"
        days_left = days_between(reference_day, expiry)
    elif reference_day <= expiry:
        phase = "提前续展期（可缴费）"
        days_left = days_between(reference_day, expiry)
        tip = f"可在窗口内缴纳续展费；距到期还有 {days_left} 天"
    elif reference_day <= grace_end:
        phase = "宽限期（加收附加费）"
        days_left = days_between(reference_day, grace_end)
        tip = f"宽限期内续展需另缴基本费 50% 的附加费；距宽限期届满还有 {days_left} 天"
    else:
        phase = "已过期"
        days_left = days_between(reference_day, grace_end)
        tip = "宽限期已届满，国际注册通常不可恢复；如需保护须重新申请"

    fees = _fee_defaults()
    grace_note = (
        f"宽限期附加费 = 续展基本费 {fees['renewal_basic']} × 50% = {fees['grace_surcharge']} CHF"
        f"（费用表第 6.5 项；数据来源：{fees['source']}）"
    )
    notes = [
        grace_note,
        "续展不得对注册现状作任何修改（商品/服务调整须另办变更程序，费用表第 7 项）。",
        "续展登记日为应续展之日，即使在宽限期内缴纳亦然（实施细则第 31 条）。",
        "可部分续展（仅续展部分商品/服务）；LDC 原属缔约方的基本费为 65 CHF，附加费按基本费的 50% 计。",
        "建议在截止日前预留 3-5 个工作日处理转账延迟；规费与汇率均须按 SKILL.md §3.0 联网核验。",
    ]

    return {
        "registration_date": formalize(registration),
        "protection_years": protection_years,
        "expiry_date": formalize(expiry),
        "early_renewal_start": formalize(early_start),
        "grace_period_end": formalize(grace_end),
        "reference_day": formalize(reference_day),
        "phase": phase,
        "days_left": days_left,
        "tip": tip,
        "grace_surcharge_chf": fees["grace_surcharge"],
        "renewal_basic_chf": fees["renewal_basic"],
        "notes": notes,
    }


def main(argv=None) -> int:
    _configure_stdout()
    parser = argparse.ArgumentParser(
        description="马德里国际注册续展窗口计算（提前 6 个月 / 宽限期 6 个月）",
    )
    parser.add_argument("--register", required=True, help="国际注册日 YYYY-MM-DD")
    parser.add_argument("--protection-years", type=int, default=10, choices=list(VALID_PROTECTION_YEARS),
                        help="保护期年数：10（议定书，默认）/ 20（协定）")
    parser.add_argument("--today", help="计算基准日 YYYY-MM-DD（默认系统当日，用于复现）")
    parser.add_argument("--ascii", action="store_true", help="输出 ASCII 转义（避免终端编码问题）")
    args = parser.parse_args(argv)

    try:
        result = check_renewal_status(args.register, args.protection_years, today=args.today)
    except ValueError as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=args.ascii, indent=2))
        return 2

    print(json.dumps(result, ensure_ascii=args.ascii, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
