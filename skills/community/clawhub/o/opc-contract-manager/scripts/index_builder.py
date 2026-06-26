#!/usr/bin/env python3
"""
Build or update contracts/INDEX.json from individual metadata files.

Walks the contracts/ directory, finds all metadata.json files, validates them,
and merges into a single INDEX.json sorted by effective date descending.

Supports cross-contract insights generation when --insights flag is passed
or when 5+ contracts are indexed.

Usage:
    python3 index_builder.py [contracts_dir]
    python3 index_builder.py --rebuild [contracts_dir]
    python3 index_builder.py --insights [contracts_dir]
    python3 index_builder.py --validate [contracts_dir]

Options:
    --rebuild     Full rebuild (replace existing INDEX.json)
    --insights    Generate INSIGHTS.json + INSIGHTS.md
    --validate    Check metadata against expected fields, report issues
    --help        Show this help message

All flags can be combined. If contracts_dir is not specified, defaults to
./contracts in the current working directory.

Dependencies: Python 3.8+ stdlib only (no pip install required).
"""

import argparse
import json
import sys
from collections import Counter, defaultdict
from datetime import date, datetime
from pathlib import Path

REQUIRED_FIELDS = {"contract_id", "counterparty_name", "contract_type", "effective_date", "review_status"}

VALID_CONTRACT_TYPES = {
    "nda", "msa", "service-agreement", "contractor-agreement", "sow",
    "saas-subscription", "license", "partnership", "lease", "vendor",
    "referral", "reseller", "other"
}

VALID_RISK_LEVELS = {"critical", "high", "medium", "low", None}
VALID_REVIEW_STATUSES = {"draft", "under-review", "reviewed", "needs-revision"}


def parse_date(date_str):
    """Parse an ISO date string. Returns None if unparseable."""
    if not date_str or date_str in ("null", "unknown", "needs_manual_review"):
        return None
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None


def validate_metadata(metadata, file_path):
    """Validate a metadata dict against expected fields. Returns list of warnings."""
    warnings = []

    for field in REQUIRED_FIELDS:
        if field not in metadata or metadata[field] is None:
            warnings.append(f"Missing required field: {field}")

    ct = metadata.get("contract_type")
    if ct and ct not in VALID_CONTRACT_TYPES:
        warnings.append(f"Unknown contract_type: {ct}")

    rs = metadata.get("review_status")
    if rs and rs not in VALID_REVIEW_STATUSES:
        warnings.append(f"Unknown review_status: {rs}")

    rl = metadata.get("overall_risk_level")
    if rl and rl not in VALID_RISK_LEVELS:
        warnings.append(f"Unknown overall_risk_level: {rl}")

    for date_field in ("effective_date", "term_start", "term_end", "signature_date",
                       "renewal_notice_deadline", "next_action_due_date", "last_reviewed_at"):
        val = metadata.get(date_field)
        if val and val not in ("unknown", "needs_manual_review") and parse_date(val) is None:
            warnings.append(f"Invalid date format for {date_field}: {val}")

    if warnings:
        for w in warnings:
            print(f"  WARNING [{file_path}]: {w}", file=sys.stderr)

    return warnings


def load_existing_index(index_path):
    """Load existing INDEX.json if it exists."""
    if index_path.exists():
        try:
            with open(index_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            print("WARNING: Could not read existing INDEX.json, starting fresh.", file=sys.stderr)
    return []


def find_metadata_files(contracts_dir):
    """Find all metadata.json files in the contracts directory."""
    return sorted(contracts_dir.glob("*/metadata.json"))


def build_index(contracts_dir, rebuild=False):
    """Build or update the contract index."""
    index_path = contracts_dir / "INDEX.json"

    if rebuild:
        existing = []
        existing_ids = set()
    else:
        existing = load_existing_index(index_path)
        existing_ids = {entry.get("contract_id") for entry in existing}

    metadata_files = find_metadata_files(contracts_dir)
    new_count = 0
    updated_count = 0
    all_entries = {entry.get("contract_id"): entry for entry in existing}

    for mf in metadata_files:
        try:
            with open(mf, "r", encoding="utf-8") as f:
                metadata = json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"ERROR: Could not read {mf}: {e}", file=sys.stderr)
            continue

        contract_id = metadata.get("contract_id")
        if not contract_id:
            print(f"WARNING: No contract_id in {mf}, skipping.", file=sys.stderr)
            continue

        if contract_id in existing_ids and not rebuild:
            # Check if metadata has been updated
            if metadata != all_entries.get(contract_id):
                all_entries[contract_id] = metadata
                updated_count += 1
        else:
            all_entries[contract_id] = metadata
            new_count += 1

    # Sort by effective_date descending (newest first)
    sorted_entries = sorted(
        all_entries.values(),
        key=lambda x: x.get("effective_date") or "0000-00-00",
        reverse=True
    )

    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(sorted_entries, f, indent=2, ensure_ascii=False)

    total = len(sorted_entries)
    action = "Rebuilt" if rebuild else "Updated"
    print(f"{action} index. Added {new_count} new, updated {updated_count}. "
          f"Index now contains {total} contract(s).", file=sys.stderr)

    return sorted_entries


def validate_all(contracts_dir):
    """Validate all metadata files and report issues."""
    metadata_files = find_metadata_files(contracts_dir)
    total_warnings = 0

    if not metadata_files:
        print("No metadata.json files found.", file=sys.stderr)
        return

    for mf in metadata_files:
        try:
            with open(mf, "r", encoding="utf-8") as f:
                metadata = json.load(f)
            warnings = validate_metadata(metadata, mf)
            total_warnings += len(warnings)
        except (json.JSONDecodeError, IOError) as e:
            print(f"  ERROR [{mf}]: {e}", file=sys.stderr)
            total_warnings += 1

    print(f"\nValidation complete. {len(metadata_files)} file(s) checked, "
          f"{total_warnings} warning(s).", file=sys.stderr)


def generate_insights(contracts_dir, entries):
    """Generate cross-contract insights from indexed entries.

    Outputs:
    - contracts/INSIGHTS.json (structured, machine-readable)
    - contracts/INSIGHTS.md (human-readable)
    """
    if len(entries) < 2:
        print("Not enough contracts for insights (minimum 2).", file=sys.stderr)
        return

    insights = []
    today = date.today()

    # 1. Payment Terms Analysis
    payment_terms = [(e.get("payment_terms_days"), e.get("contract_id"))
                     for e in entries if isinstance(e.get("payment_terms_days"), int)]
    if payment_terms:
        days_list = [pt[0] for pt in payment_terms]
        avg_days = sum(days_list) / len(days_list)
        total_contracts = len(entries)
        extractable = len(payment_terms)

        insight = {
            "category": "payment_terms",
            "insight": f"Average payment cycle is {avg_days:.0f} days",
            "detail": None,
            "confidence": "high" if extractable >= total_contracts * 0.7 else ("medium" if extractable >= 3 else "low"),
            "based_on": f"{extractable} of {total_contracts} contracts had extractable payment terms",
            "missing_data_notes": f"{total_contracts - extractable} contracts had no explicit payment term" if extractable < total_contracts else None
        }
        if avg_days > 30:
            insight["detail"] = (
                f"Your average payment cycle ({avg_days:.0f} days) exceeds the net-30 industry norm "
                f"by {avg_days - 30:.0f} days. This may create cash flow pressure."
            )
        else:
            insight["detail"] = (
                f"Your average payment cycle ({avg_days:.0f} days) is at or below the net-30 norm. "
                f"This is healthy for cash flow."
            )
        insights.append(insight)

    # 2. Counterparty Risk Concentration
    counterparties = Counter(e.get("counterparty_name") for e in entries if e.get("counterparty_name"))
    total = len(entries)
    if counterparties:
        top_cp, top_count = counterparties.most_common(1)[0]
        concentration_pct = (top_count / total) * 100

        insight = {
            "category": "counterparty_concentration",
            "insight": f"Top counterparty ({top_cp}) represents {concentration_pct:.0f}% of contracts ({top_count} of {total})",
            "detail": None,
            "confidence": "medium",
            "based_on": f"Based on contract count, not actual revenue (revenue data not available)",
            "missing_data_notes": "Concentration is measured by contract count/value proxies, not recognized revenue"
        }
        if concentration_pct > 40:
            insight["detail"] = (
                f"WARNING: {top_cp} represents {concentration_pct:.0f}% of your contracts. "
                f"High concentration with a single counterparty is a significant risk for a solo entrepreneur. "
                f"Consider diversifying your client base."
            )
        elif concentration_pct > 25:
            insight["detail"] = (
                f"CAUTION: {top_cp} represents {concentration_pct:.0f}% of your contracts. "
                f"Monitor this concentration level and maintain an active pipeline of other prospects."
            )
        else:
            insight["detail"] = f"Client concentration appears healthy. No single counterparty dominates."
        insights.append(insight)

    # 3. Liability Exposure
    uncapped = [e for e in entries if e.get("liability_cap_type") == "uncapped"]
    capped = [e for e in entries if e.get("liability_cap_type") in ("fixed", "proportional", "mutual")]
    unknown_liability = total - len(uncapped) - len(capped)

    if uncapped or capped:
        insight = {
            "category": "liability_exposure",
            "insight": f"{len(uncapped)} contract(s) have uncapped liability",
            "detail": None,
            "confidence": "medium" if unknown_liability < total * 0.5 else "low",
            "based_on": f"{len(uncapped) + len(capped)} of {total} contracts had extractable liability data",
            "missing_data_notes": f"{unknown_liability} contracts had unknown liability terms" if unknown_liability > 0 else None
        }
        if uncapped:
            names = [e.get("counterparty_name", "Unknown") for e in uncapped]
            insight["detail"] = (
                f"Uncapped liability contracts: {', '.join(names)}. "
                f"Each of these represents unlimited financial exposure. "
                f"Consider renegotiating to add caps proportional to contract value."
            )
        else:
            insight["detail"] = "All contracts with extractable data have liability caps. Good risk management."
        insights.append(insight)

    # 4. Termination Risk Score
    tfc_contracts = [e for e in entries if e.get("tfc_present")]
    tfc_one_sided = [e for e in tfc_contracts if e.get("tfc_one_sided")]

    if tfc_contracts:
        insight = {
            "category": "termination_risk",
            "insight": f"{len(tfc_contracts)} of {total} contracts have TFC clauses ({len(tfc_one_sided)} one-sided)",
            "detail": None,
            "confidence": "medium",
            "based_on": f"TFC data available for {sum(1 for e in entries if 'tfc_present' in e)} of {total} contracts",
            "missing_data_notes": None
        }
        if tfc_one_sided:
            names = [e.get("counterparty_name", "Unknown") for e in tfc_one_sided]
            insight["detail"] = (
                f"One-sided TFC contracts (counterparty can terminate, you cannot): {', '.join(names)}. "
                f"These represent revenue that could disappear without warning. "
                f"Prioritize renegotiating these at renewal."
            )
        else:
            insight["detail"] = "All TFC clauses are mutual. This is balanced."
        insights.append(insight)

    # 5. Common Patterns
    patterns = []

    # Check NDA term limits
    ndas = [e for e in entries if e.get("contract_type") == "nda"]
    if len(ndas) >= 2:
        no_term = [e for e in ndas if not e.get("term_end")]
        if no_term:
            patterns.append(f"{len(no_term)} of {len(ndas)} NDAs have no defined end date")

    # Check non-compete prevalence
    nc_contracts = [e for e in entries if e.get("non_compete_present")]
    if nc_contracts:
        patterns.append(f"{len(nc_contracts)} of {total} contracts include non-compete clauses")

    # Check exclusivity
    excl_contracts = [e for e in entries if e.get("exclusivity_present")]
    if excl_contracts:
        patterns.append(f"{len(excl_contracts)} of {total} contracts include exclusivity provisions")

    if patterns:
        insights.append({
            "category": "common_patterns",
            "insight": "Notable patterns across your contract portfolio",
            "detail": "\n".join(f"- {p}" for p in patterns),
            "confidence": "high",
            "based_on": f"Analysis of {total} contracts",
            "missing_data_notes": None
        })

    # 6. Trend Data (if contracts span multiple dates)
    dated_entries = [(parse_date(e.get("effective_date")), e) for e in entries]
    dated_entries = [(d, e) for d, e in dated_entries if d is not None]
    dated_entries.sort(key=lambda x: x[0])

    if len(dated_entries) >= 3:
        # Check if payment terms are improving or worsening
        recent_half = dated_entries[len(dated_entries) // 2:]
        older_half = dated_entries[:len(dated_entries) // 2]

        recent_payments = [e.get("payment_terms_days") for _, e in recent_half
                          if isinstance(e.get("payment_terms_days"), int)]
        older_payments = [e.get("payment_terms_days") for _, e in older_half
                         if isinstance(e.get("payment_terms_days"), int)]

        if recent_payments and older_payments:
            recent_avg = sum(recent_payments) / len(recent_payments)
            older_avg = sum(older_payments) / len(older_payments)
            diff = recent_avg - older_avg

            trend = "worsening" if diff > 5 else ("improving" if diff < -5 else "stable")
            insights.append({
                "category": "trends",
                "insight": f"Payment terms trend: {trend}",
                "detail": (
                    f"Older contracts averaged {older_avg:.0f}-day payment terms. "
                    f"Recent contracts average {recent_avg:.0f} days. "
                    f"{'Consider pushing for shorter terms.' if trend == 'worsening' else ''}"
                ),
                "confidence": "low" if len(recent_payments) < 3 else "medium",
                "based_on": f"Comparing {len(older_payments)} older vs {len(recent_payments)} recent contracts",
                "missing_data_notes": None
            })

    # Write INSIGHTS.json
    insights_json_path = contracts_dir / "INSIGHTS.json"
    with open(insights_json_path, "w", encoding="utf-8") as f:
        json.dump({
            "generated_at": today.isoformat(),
            "total_contracts": total,
            "insights": insights
        }, f, indent=2, ensure_ascii=False)

    # Write INSIGHTS.md
    insights_md_path = contracts_dir / "INSIGHTS.md"
    lines = [
        "# Cross-Contract Insights",
        "",
        f"> Generated on {today.isoformat()} from {total} contract(s).",
        "> Based on AI-extracted metadata. Confidence levels indicate data quality.",
        "",
    ]

    for ins in insights:
        lines.append(f"## {ins['category'].replace('_', ' ').title()}")
        lines.append("")
        lines.append(f"**{ins['insight']}**")
        lines.append(f"*Confidence: {ins['confidence']}* — {ins['based_on']}")
        lines.append("")
        if ins.get("detail"):
            lines.append(ins["detail"])
            lines.append("")
        if ins.get("missing_data_notes"):
            lines.append(f"> Note: {ins['missing_data_notes']}")
            lines.append("")
        lines.append("---")
        lines.append("")

    with open(insights_md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Generated {len(insights)} insight(s) → INSIGHTS.json + INSIGHTS.md", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(
        description="Build or update contracts/INDEX.json from individual metadata files.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Examples:\n"
               "  python3 index_builder.py\n"
               "  python3 index_builder.py --rebuild ./contracts\n"
               "  python3 index_builder.py --insights --validate\n"
    )
    parser.add_argument("contracts_dir", nargs="?", default="./contracts",
                        help="Path to contracts directory (default: ./contracts)")
    parser.add_argument("--rebuild", action="store_true",
                        help="Full rebuild (replace existing INDEX.json)")
    parser.add_argument("--insights", action="store_true",
                        help="Generate INSIGHTS.json + INSIGHTS.md")
    parser.add_argument("--validate", action="store_true",
                        help="Validate metadata files against expected fields")

    args = parser.parse_args()
    contracts_dir = Path(args.contracts_dir)

    if not contracts_dir.exists():
        print(f"ERROR: Directory not found: {contracts_dir}", file=sys.stderr)
        sys.exit(1)

    if args.validate:
        validate_all(contracts_dir)

    entries = build_index(contracts_dir, rebuild=args.rebuild)

    # Auto-trigger insights if 5+ contracts or explicitly requested
    if args.insights or len(entries) >= 5:
        generate_insights(contracts_dir, entries)


if __name__ == "__main__":
    main()
