#!/usr/bin/env python3
"""Summarize included and excluded net worth, credit cards, and a card forecast."""

from __future__ import annotations

import argparse
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path
from typing import Any

from ledgerlib import (
    accumulate,
    credit_mode,
    default_account_catalog,
    decimal_value,
    fmt,
    fmt_pct,
    find_optional_data_file,
    is_refund,
    load_file,
    load_skill_config,
    merge_account_policy,
    money,
    normalize_include,
    parse_time,
    target_account,
)
from project_assets import parse_cutoff, project


def latest_snapshots(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    latest: dict[str, dict[str, Any]] = {}
    for row in rows:
        account = str(row.get("账户", "")).strip()
        if not account:
            continue
        current = str(row.get("时间", ""))
        if account not in latest or current >= str(latest[account].get("时间", "")):
            latest[account] = row
    return latest


def inclusion_map(
    data: dict[str, Any],
    snapshots: list[dict[str, Any]],
    base_catalog: dict[str, dict[str, Any]] | None = None,
) -> dict[str, dict[str, Any]]:
    catalog, errors = merge_account_policy(data.get("account_policy") or [], base=base_catalog)
    if errors:
        raise SystemExit(errors[0])
    for row in sorted(snapshots, key=lambda item: str(item.get("时间", ""))):
        account = str(row.get("账户", "")).strip()
        if not account:
            continue
        flag = normalize_include(row.get("纳入", ""))
        kind = str(row.get("账户类型", "")).strip()
        current = catalog.get(account, {"kind": kind or "资产", "include": "included"})
        if kind in {"资产", "负债"}:
            current["kind"] = kind
        if flag:
            current["include"] = flag
        catalog[account] = current
    return catalog


def section_totals(rows: list[dict[str, Any]]) -> tuple[Decimal, Decimal]:
    assets = Decimal("0")
    liabilities = Decimal("0")
    for row in rows:
        balance = money(row.get("余额"))
        if row.get("账户类型") == "负债":
            liabilities += max(-balance, Decimal("0"))
        else:
            assets += balance
    return assets, liabilities


def print_section(title: str, rows: list[dict[str, Any]], snapshots: dict[str, dict[str, Any]]) -> tuple[Decimal, Decimal]:
    print(f"\n## {title}")
    if not rows:
        print("- 无")
        return Decimal("0"), Decimal("0")
    for row in rows:
        account = str(row.get("账户", ""))
        balance = money(row.get("余额"))
        snap = snapshots.get(account)
        if snap is not None:
            observed = money(snap.get("余额", snap.get("金额")))
            print(f"- {account}: {fmt(balance)}（快照 {fmt(observed)}）")
        else:
            print(f"- {account}: {fmt(balance)}")
    assets, liabilities = section_totals(rows)
    print(f"- 总资产: {fmt(assets)}")
    print(f"- 总负债: {fmt(liabilities)}")
    print(f"- 净资产: {fmt(assets - liabilities)}")
    return assets, liabilities


def _blank(value: Any) -> bool:
    return str(value if value is not None else "").strip() == ""


def net_charges(records: list[dict[str, Any]], card: str, start: date, end: date) -> Decimal:
    total = Decimal("0")
    for row in records:
        stamp = parse_time(row.get("时间"))
        if stamp is None or not (start < stamp.date() <= end):
            continue
        if str(row.get("账户", "")).strip() != card:
            continue
        magnitude = abs(money(row.get("金额")))
        tx_type = str(row.get("收支类型", "")).strip()
        if is_refund(row) or tx_type == "报销":
            total -= magnitude
        elif tx_type == "支出":
            total += magnitude
    return total


def repayments_between(records: list[dict[str, Any]], card: str, start: date, end: date) -> Decimal:
    total = Decimal("0")
    for row in records:
        if str(row.get("收支类型", "")).strip() != "还款":
            continue
        if target_account(row) != card:
            continue
        stamp = parse_time(row.get("时间"))
        if stamp is None or not (start < stamp.date() <= end):
            continue
        total += abs(money(row.get("金额")))
    return total


def forecast(
    data: dict[str, Any],
    records: list[dict[str, Any]],
    as_of: date,
    catalog: dict[str, dict[str, Any]],
    invest_out_subcategory: str = "赎回",
) -> None:
    from ledgerlib import cycle_start, due_date_for_cycle, previous_cycle_start

    print("\n## 预测")
    cards = data.get("credit_accounts") or []
    month_rows = [row for row in records if str(row.get("时间", "")).startswith(as_of.strftime("%Y-%m"))]
    flows = accumulate(month_rows, catalog, None, invest_out_subcategory)
    projected_due = Decimal("0")
    if not cards:
        print("- 无信贷账户")
    for row in cards:
        account = str(row.get("账户", "")).strip()
        bill_assumed = _blank(row.get("账单日"))
        due_assumed = _blank(row.get("还款日"))
        bill_day = 1 if bill_assumed else int(row.get("账单日"))
        due_day = 10 if due_assumed else int(row.get("还款日"))
        if bill_assumed:
            print(f"- 警告: {account} 未填账单日，假定为 1 日")
        if due_assumed:
            print(f"- 警告: {account} 未填还款日，假定为 10 日")
        start = cycle_start(as_of, bill_day)
        previous = previous_cycle_start(start, bill_day)
        statement = max(net_charges(records, account, start, as_of), Decimal("0"))
        previous_charges = net_charges(records, account, previous, start)
        paid = repayments_between(records, account, start, as_of)
        if previous_charges == 0 and paid == 0 and str(row.get("欠款", "")).strip() != "":
            repayment = money(row.get("欠款"))
        else:
            repayment = max(previous_charges - paid, Decimal("0"))
        due = due_date_for_cycle(start, due_day, bill_day)
        if due.year == as_of.year and due.month == as_of.month:
            projected_due += repayment
        assumed = []
        if bill_assumed:
            assumed.append("假定账单日")
        if due_assumed:
            assumed.append("假定还款日")
        suffix = f", {'、'.join(assumed)}" if assumed else ""
        print(
            f"- {account}: 预计账单 {fmt(statement)}, 预计还款 {fmt(repayment)}, "
            f"还款日 {due.isoformat()}{suffix}"
        )
    cash = flows.income - flows.cash_expense_net - projected_due - flows.investment_net
    cash_line = (
        f"- 本月现金流: 收入 {fmt(flows.income)} - 现金花销净额 {fmt(flows.cash_expense_net)} "
        f"- 预计还款 {fmt(projected_due)}"
    )
    if flows.investment_net != 0:
        cash_line += f" - 投资净投入 {fmt(flows.investment_net)}"
    print(f"{cash_line} = {fmt(cash)}")


def load_records(
    data: dict[str, Any],
    ledgers: list[Path],
    config: Any = None,
) -> list[dict[str, Any]]:
    records = [row for row in data.get("records", []) if isinstance(row, dict)]
    for path in ledgers:
        book, errors = load_file(path)
        if errors and not book.get("records"):
            raise SystemExit(f"{path}: {errors[0]}")
        if config is not None:
            config.apply_to_book(book)
        records.extend(row for row in book.get("records", []) if isinstance(row, dict))
    return records


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize assets, liabilities, and optional card forecast.")
    parser.add_argument("file", type=Path)
    parser.add_argument("--ledger", action="append", type=Path, default=[], help="Extra ledger shard. Can be repeated.")
    parser.add_argument("--as-of", help="Date for inference and forecast, YYYY-MM-DD. Default: today.")
    parser.add_argument("--cc-method", choices=["A", "B"], default="A", help="Credit-card snapshot method. Default: A.")
    parser.add_argument("--forecast", action="store_true", help="Project card statements and the current-month cash flow.")
    parser.add_argument("--items", type=Path, help="Optional items.json. Residual is listed and not added to any total.")
    parser.add_argument("--accounts", type=Path, help="Account config. Default: data/accounts.json when present.")
    parser.add_argument("--categories", type=Path, help="Category config. Default: data/categories.json when present.")
    parser.add_argument("--settings", type=Path, help="Workspace settings. Default: data/settings.json when present.")
    args = parser.parse_args()

    config = load_skill_config([args.file, *args.ledger], args.accounts, args.categories, args.settings)
    if config.errors:
        raise SystemExit("\n".join(config.errors))
    book, errors = load_file(args.file)
    if errors and not book.get("is_ledger", True):
        raise SystemExit(errors[0])
    data = {
        "records": book["records"],
        "asset_snapshots": book["asset_snapshots"],
        "credit_accounts": book["credit_accounts"],
        "installment_plans": book["installment_plans"],
        "repayment_reminders": book["repayment_reminders"],
        "account_policy": book["account_policy"],
        "credit_policy": book.get("credit_policy") or {},
    }
    cutoff = parse_cutoff(args.as_of) if args.as_of else datetime.combine(date.today(), datetime.max.time().replace(microsecond=0))
    if args.as_of and cutoff is None:
        raise SystemExit("--as-of must be YYYY-MM-DD")
    as_of_date = cutoff.date() if cutoff else date.today()
    config.apply_to_book(data)
    records = load_records(data, args.ledger, config)
    inferred = project(
        data,
        records,
        cutoff,
        cc_method=args.cc_method,
        catalog=config.catalog,
        credit_cards=config.credit_cards,
    )
    snapshots = latest_snapshots(data["asset_snapshots"])
    catalog = inclusion_map(data, data["asset_snapshots"], config.catalog)
    included = []
    excluded = []
    for row in inferred["账户余额"]:
        account = str(row.get("账户", ""))
        flag = catalog.get(account, {}).get("include", "included")
        if flag == "excluded":
            excluded.append(row)
        else:
            included.append(row)

    print(f"# 资产统计: {args.file.name}")
    print(f"日期: {as_of_date.isoformat()}")
    print(f"信用卡余额算法: {inferred['信用卡余额算法']}")
    included_assets, included_liabilities = print_section("计入净资产", included, snapshots)
    excluded_assets, excluded_liabilities = print_section("备查账户", excluded, snapshots)
    unknown = inferred.get("未建立基线账户") or []
    if unknown:
        print("\n## 未建立基线账户")
        for name in unknown:
            flag = catalog.get(name, {}).get("include", "included")
            label = "备查" if flag == "excluded" else "计入"
            print(f"- {name}: {label}")

    print("\n## 汇总")
    print(f"- 总资产: {fmt(included_assets)}")
    print(f"- 总负债: {fmt(included_liabilities)}")
    print(f"- 净资产: {fmt(included_assets - included_liabilities)}")
    print(f"- 备查净值: {fmt(excluded_assets - excluded_liabilities)}")

    flows = accumulate(records, catalog, config.categories)
    if flows.invest_in or flows.invest_out or flows.invest_accounts:
        print("\n## 投资")
        print(f"- 投资净投入: {fmt(flows.investment_net)}")
        print("- 市值只来自已有快照；不查行情，也不做定时更新")
        printed_pnl = False
        for account in sorted(flows.invest_accounts):
            snap = snapshots.get(account)
            if snap is None:
                continue
            market = money(snap.get("余额", snap.get("金额")))
            contributed = flows.invest_by_account.get(account, Decimal("0"))
            print(
                f"- {account}: 快照市值 {fmt(market)}, 累计净投入 {fmt(contributed)}, "
                f"浮动盈亏 {fmt(market - contributed)}"
            )
            printed_pnl = True
        if not printed_pnl:
            print("- 无市值快照，不估算浮动盈亏")

    if data["credit_accounts"]:
        policy = data.get("credit_policy") or {}
        print("\n## 信贷账户")
        ordered = sorted(data["credit_accounts"], key=lambda item: str(item.get("账户", "")))
        for row in ordered:
            account = str(row.get("账户", ""))
            marker = "备查" if catalog.get(account, {}).get("include") == "excluded" else "计入"
            mode = credit_mode(row, policy)
            debt = fmt(money(row.get("欠款")))
            if mode == "with_limit":
                print(
                    f"- {account}: 欠款 {debt}, 额度 {row.get('额度', '')}, "
                    f"可用 {row.get('可用额度', '')}, {marker}"
                )
            else:
                print(f"- {account}: 欠款 {debt}, {marker}")
        print("\n## 信用敞口")
        total_debt = Decimal("0")
        limit_debt = Decimal("0")
        limit_sum = Decimal("0")
        available_sum = Decimal("0")
        any_limit = False
        for row in ordered:
            account = str(row.get("账户", ""))
            debt = money(row.get("欠款"))
            total_debt += debt
            due = str(row.get("还款日", "") or "").strip() or "未填"
            print(f"- {account}: 欠款 {fmt(debt)}, 还款日 {due}")
            mode = credit_mode(row, policy)
            if mode != "with_limit":
                continue
            any_limit = True
            limit = decimal_value(row.get("额度"))
            if limit is None:
                print(f"- 警告: {account} with_limit 模式缺少额度")
                continue
            available = decimal_value(row.get("可用额度"))
            if available is None:
                available = limit - debt
            elif abs((limit - debt) - available) > Decimal("1"):
                print(f"- 警告: {account} 可用额度与额度-欠款相差超过 1 元")
            limit_debt += debt
            limit_sum += limit
            available_sum += available
        print(f"- 总欠款: {fmt(total_debt)}")
        if any_limit and limit_sum > 0:
            print(f"- 总可用额度: {fmt(available_sum)}")
            print(f"- 使用率: {fmt_pct(limit_debt, limit_sum)}")
        elif any_limit:
            print("- 总可用额度: 未知")

    diffs = []
    for account, snap in sorted(snapshots.items()):
        inferred_row = next((row for row in inferred["账户余额"] if row.get("账户") == account), None)
        if inferred_row is None:
            continue
        observed = money(snap.get("余额", snap.get("金额")))
        projected = money(inferred_row.get("余额"))
        if observed != projected:
            diffs.append((account, observed, projected))
    if diffs:
        print("\n## 快照与推演差额")
        for account, observed, projected in diffs:
            print(f"- {account}: 快照 {fmt(observed)}, 推演 {fmt(projected)}, 差额 {fmt(projected - observed)}")

    if data["installment_plans"]:
        print("\n## 分期计划")
        for row in sorted(data["installment_plans"], key=lambda item: str(item.get("下一还款日", ""))):
            principal = money(row.get("本金"))
            paid = int(row.get("已还期数", 0) or 0)
            total = int(row.get("总期数", 0) or 0)
            per_period = money(row.get("每期金额"))
            remaining_periods = max(total - paid, 0)
            remaining_amount = per_period * remaining_periods if per_period else principal
            print(
                f"- {row.get('id', '')} {row.get('账户', '')}: 剩余 {remaining_periods}/{total} 期, "
                f"待还 {fmt(remaining_amount)}, 下一还款日 {row.get('下一还款日', '')}"
            )

    if data["repayment_reminders"]:
        print("\n## 还款提醒")
        for row in sorted(data["repayment_reminders"], key=lambda item: str(item.get("时间", ""))):
            due = parse_time(row.get("时间"))
            status = str(row.get("状态", ""))
            overdue = due is not None and due.date() < as_of_date and status not in {"已还", "paid", "skipped"}
            prefix = "逾期" if overdue else status
            print(f"- {row.get('时间')} {row.get('账户')}: {fmt(money(row.get('金额')))} {prefix}")

    if args.forecast:
        forecast(
            data,
            records,
            as_of_date,
            catalog or default_account_catalog(),
            config.invest_out_subcategory,
        )

    items_path = args.items
    if items_path is None:
        search_paths = [args.file, *args.ledger]
        items_path = find_optional_data_file("items.json", search_paths)
        if items_path is None:
            items_path = find_optional_data_file("items/items.json", search_paths)
    if items_path is not None:
        from summarize_items import load_items, residual_of

        print("\n## 备查物品")
        print(f"- 残值合计: {fmt(residual_of(load_items(items_path)))}（不计入总资产、净资产、备查净值）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
