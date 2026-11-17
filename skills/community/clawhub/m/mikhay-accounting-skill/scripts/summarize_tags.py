#!/usr/bin/env python3
"""Scan every ledger shard and total tags.

Do not hand-calculate these totals. Gross is spending before refunds. Net is
gross minus refunds. Refunds are not income. A record with several tags
contributes its full amount to each tag.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from decimal import Decimal
from pathlib import Path
from typing import Any

from ledgerlib import (
    CategoryCatalog,
    SkillConfig,
    fmt,
    fmt_pct,
    index_shard_files,
    is_refund,
    iter_ledger_files,
    load_file,
    load_skill_config,
    money,
    normalize_pair,
    pair_id,
    parse_tags,
    record_id,
    reimburse_ref,
)


class TagRollup:
    def __init__(self) -> None:
        self.gross = Decimal("0")
        self.refunds = Decimal("0")
        self.reimbursed = Decimal("0")
        self.transfer = Decimal("0")
        self.day_gross: dict[str, Decimal] = defaultdict(Decimal)
        self.day_refund: dict[str, Decimal] = defaultdict(Decimal)
        self.cat_gross: dict[str, Decimal] = defaultdict(Decimal)
        self.cat_refund: dict[str, Decimal] = defaultdict(Decimal)

    @property
    def net(self) -> Decimal:
        return self.gross - self.refunds - self.reimbursed


def collect(
    paths: list[Path],
    config: SkillConfig | None = None,
) -> tuple[list[dict[str, Any]], list[Path]]:
    records: list[dict[str, Any]] = []
    files: list[Path] = []
    for path in paths:
        candidates = iter_ledger_files(path) if path.is_dir() else [path]
        for candidate in candidates:
            book, errors = load_file(candidate)
            if not book.get("is_ledger", True):
                continue
            if errors:
                raise SystemExit(f"{candidate}: {errors[0]}")
            if config is not None:
                config.apply_to_book(book)
            files.append(candidate)
            records.extend(row for row in book["records"] if isinstance(row, dict))
    return records, files


def category_of(row: dict[str, Any], categories: CategoryCatalog | None = None) -> str:
    category = str(row.get("类别", "")).strip() or "未分类"
    subcategory = str(row.get("子类", "")).strip()
    category, _, _ = normalize_pair(category, subcategory, categories)
    return category


def day_of(row: dict[str, Any]) -> str:
    return str(row.get("时间", ""))[:10]


def rollup(
    records: list[dict[str, Any]],
    categories: CategoryCatalog | None = None,
) -> dict[str, TagRollup]:
    stats: dict[str, TagRollup] = defaultdict(TagRollup)
    by_id = {record_id(row): row for row in records if record_id(row)}
    pairs: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in records:
        if str(row.get("收支类型", "")).strip() == "转账" and not is_refund(row):
            pid = pair_id(row)
            if pid:
                pairs[pid].append(row)

    seen_pairs: set[str] = set()
    for row in records:
        if is_refund(row):
            target = by_id.get(str(row.get("refund_of", "")).strip())
            tags = parse_tags(target.get("tags")) if target is not None and parse_tags(target.get("tags")) else parse_tags(row.get("tags"))
            category = category_of(target, categories) if target is not None else category_of(row, categories)
            magnitude = abs(money(row.get("金额")))
            day = day_of(row)
            for tag in tags:
                item = stats[tag]
                item.refunds += magnitude
                item.day_refund[day] += magnitude
                item.cat_refund[category] += magnitude
            continue
        tx_type = str(row.get("收支类型", "")).strip()
        if tx_type == "报销":
            target = by_id.get(reimburse_ref(row))
            tags = parse_tags(target.get("tags")) if target is not None and parse_tags(target.get("tags")) else parse_tags(row.get("tags"))
            magnitude = abs(money(row.get("金额")))
            for tag in tags:
                stats[tag].reimbursed += magnitude
            continue
        if tx_type == "支出":
            tags = parse_tags(row.get("tags"))
            magnitude = abs(money(row.get("金额")))
            category = category_of(row, categories)
            day = day_of(row)
            for tag in tags:
                item = stats[tag]
                item.gross += magnitude
                item.day_gross[day] += magnitude
                item.cat_gross[category] += magnitude
            continue
        if tx_type != "转账":
            continue
        pid = pair_id(row)
        if pid:
            if pid in seen_pairs:
                continue
            seen_pairs.add(pid)
            legs = pairs.get(pid) or [row]
            outgoing = [leg for leg in legs if money(leg.get("金额")) < 0]
            source = outgoing[0] if outgoing else legs[0]
            tags = []
            seen_tags: set[str] = set()
            for leg in legs:
                for tag in parse_tags(leg.get("tags")):
                    if tag not in seen_tags:
                        seen_tags.add(tag)
                        tags.append(tag)
            magnitude = abs(money(source.get("金额")))
        else:
            tags = parse_tags(row.get("tags"))
            magnitude = abs(money(row.get("金额")))
        for tag in tags:
            stats[tag].transfer += magnitude
    return stats


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan all ledger shards and total tags.")
    parser.add_argument("paths", nargs="+", type=Path, help="Ledger files or directories. Every shard is scanned.")
    parser.add_argument("--shard", choices=["day", "month"], default="month", help="Basename key used to index shards.")
    parser.add_argument("--accounts", type=Path, help="Account config. Default: data/accounts.json when present.")
    parser.add_argument("--categories", type=Path, help="Category config. Default: data/categories.json when present.")
    parser.add_argument("--settings", type=Path, help="Workspace settings. Default: data/settings.json when present.")
    args = parser.parse_args()

    config = load_skill_config(args.paths, args.accounts, args.categories, args.settings)
    if config.errors:
        raise SystemExit("\n".join(config.errors))
    records, files = collect(args.paths, config)
    if not files:
        raise SystemExit("no ledger files found")
    grouped = index_shard_files(files, args.shard)
    keys = [key for key in sorted(grouped) if key != "unkeyed"]
    print("# 标签统计")
    print(f"扫描文件: {len(files)}")
    print(f"记录数: {len(records)}")
    print(f"分片({args.shard}): {', '.join(keys) if keys else '无'}")
    print("全部分片已扫描")

    stats = rollup(records, config.categories)
    if not stats:
        print("\n无标签")
        return 0

    ordered = sorted(stats.items(), key=lambda item: (item[1].net, item[0]), reverse=True)
    for tag, item in ordered:
        print(f"\n## {tag}")
        print(f"- 毛额: {fmt(item.gross)}")
        print(f"- 净额: {fmt(item.net)}")
        print(f"- 退款: {fmt(item.refunds)}")
        if item.reimbursed:
            print(f"- 已报销: {fmt(item.reimbursed)}")
        if item.transfer:
            print(f"- 内部转账: {fmt(item.transfer)}")
        days = sorted(set(item.day_gross) | set(item.day_refund))
        if days:
            print("\n### 按日")
            for day in days:
                gross = item.day_gross[day]
                net = gross - item.day_refund[day]
                print(f"- {day}: 毛额 {fmt(gross)}, 净额 {fmt(net)}")
        categories = sorted(set(item.cat_gross) | set(item.cat_refund))
        if categories:
            print("\n### 按类别")
            ranked = sorted(categories, key=lambda name: item.cat_gross[name] - item.cat_refund[name], reverse=True)
            for name in ranked:
                gross = item.cat_gross[name]
                net = gross - item.cat_refund[name]
                print(f"- {name}: 毛额 {fmt(gross)}, 净额 {fmt(net)}, 占比 {fmt_pct(net, item.net)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
