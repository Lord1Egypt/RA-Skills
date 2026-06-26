#!/usr/bin/env python3
"""
categorize.py — Suggest spending categories for parsed transactions.

Reads the unified JSON from parse_csv.py and outputs an annotated JSON
with a suggested 'category' field for each transaction. The LLM reviews
and adjusts categories before generating a report.

Usage:
    python3 categorize.py transactions.json [--budget budget.json] [--output categorized.json]
"""

import json
import os
import sys
import argparse
import re


# ── Default category keyword map ──────────────────────────────────────────────
# Keys: category name. Values: list of regex patterns (case-insensitive).
# Checked in order — first match wins.

CATEGORY_RULES = [
    ("Income", [
        r"\bdirect deposit\b",
        r"\bpayroll\b",
        r"\bpaycheck\b",
        r"\bsalary\b",
        r"\bwage\b",
        r"\bincome\b",
        r"\bvenmo.*from\b",  # money received
        r"\bzelle.*from\b",
        r"\baccount credit\b",
        r"\btax refund\b",
        r"\brefund\b",
    ]),
    ("Housing", [
        r"\brent\b",
        r"\bmortgage\b",
        r"\bhoa\b",
        r"\bproperty tax\b",
        r"\bhome insurance\b",
        r"\brenters insurance\b",
        r"\bstorage\b",
        r"\bleasing\b",
    ]),
    ("Utilities", [
        r"\belectric\b",
        r"\bgas\b",
        r"\bwater\b",
        r"\bpge\b",
        r"\bconsolidated edison\b",
        r"\binternet\b",
        r"\bcomcast\b",
        r"\bxfinity\b",
        r"\bverizon\b",
        r"\bat&t\b",
        r"\bt-mobile\b",
        r"\bsprint\b",
        r"\bphone\b",
        r"\butility\b",
        r"\bwaste\b",
        r"\btrash\b",
        r"\bsewer\b",
    ]),
    ("Subscriptions", [
        r"\bnetflix\b",
        r"\bhulu\b",
        r"\bdisney\+?\b",
        r"\bspotify\b",
        r"\bapple music\b",
        r"\bapple.*subscription\b",
        r"\bgoogle.*one\b",
        r"\byoutube.*premium\b",
        r"\bamazon prime\b",
        r"\bamazon.*membership\b",
        r"\bpatreon\b",
        r"\bsubstack\b",
        r"\bnotion\b",
        r"\bchatgpt\b",
        r"\bopenai\b",
        r"\bclaude\b",
        r"\banthropic\b",
        r"\bhbo\b",
        r"\bparagraph\b",
        r"\bexpressvpn\b",
        r"\bnordvpn\b",
        r"\bvpn\b",
        r"\bicloud\b",
        r"\bdropbox\b",
        r"\bcloud storage\b",
        r"\bgithub\b",
        r"\btwitch\b",
        r"\bcrunchyroll\b",
        r"\bparamount\+?\b",
        r"\bpeacock\b",
    ]),
    ("Food & Dining", [
        r"\brestaurant\b",
        r"\bpizza\b",
        r"\bburger\b",
        r"\bsushi\b",
        r"\bcafe\b",
        r"\bcoffee\b",
        r"\bstarbucks\b",
        r"\bdunkin\b",
        r"\bchipotle\b",
        r"\bmcdonald'?s?\b",
        r"\bsubway\b",
        r"\bwendy\b",
        r"\btaco bell\b",
        r"\bchick-fil-a\b",
        r"\bdomino\b",
        r"\bpapa john\b",
        r"\bdoorDash\b",
        r"\bubereats\b",
        r"\bgrubhub\b",
        r"\binstacart\b",
        r"\bwhole foods\b",
        r"\btrader joe'?s?\b",
        r"\bkroger\b",
        r"\bsafeway\b",
        r"\bpublix\b",
        r"\baldi\b",
        r"\bwegmans\b",
        r"\bgrocery\b",
        r"\bmarket\b",
        r"\bdeli\b",
        r"\bbistro\b",
        r"\bbakery\b",
        r"\bbar\b",
        r"\bbrew\b",
        r"\bpub\b",
        r"\btavern\b",
    ]),
    ("Transportation", [
        r"\buber\b",
        r"\blyft\b",
        r"\btaxi\b",
        r"\bcab\b",
        r"\bgas station\b",
        r"\bshell\b",
        r"\bbp\b",
        r"\bexxon\b",
        r"\bmobil\b",
        r"\bchevron\b",
        r"\bmarathon\b",
        r"\bcitgo\b",
        r"\bsunoco\b",
        r"\bcar wash\b",
        r"\bauto\b",
        r"\bparking\b",
        r"\btoll\b",
        r"\btrain\b",
        r"\bmetro\b",
        r"\bsubway transit\b",
        r"\bbus\b",
        r"\bflight\b",
        r"\bairline\b",
        r"\bdelta\b",
        r"\bunited airlines\b",
        r"\bsouthwest\b",
        r"\bamerican airlines\b",
        r"\brentacar\b",
        r"\bhertz\b",
        r"\bavis\b",
        r"\bcar rental\b",
        r"\bmechanic\b",
        r"\bjiffy lube\b",
        r"\bpep boys\b",
        r"\bautozone\b",
        r"\bo'reilly\b",
    ]),
    ("Health", [
        r"\bpharmacy\b",
        r"\bcvs\b",
        r"\bwalgreens\b",
        r"\brite aid\b",
        r"\bdoctor\b",
        r"\bdental\b",
        r"\bvision\b",
        r"\bclinic\b",
        r"\bhospital\b",
        r"\bmedical\b",
        r"\bhealth\b",
        r"\btherapy\b",
        r"\bpsych\b",
        r"\boptom\b",
        r"\bdr\.\b",
        r"\bgym\b",
        r"\bplanet fitness\b",
        r"\bequinox\b",
        r"\bla fitness\b",
        r"\bpeloton\b",
        r"\bfitness\b",
        r"\bprescription\b",
        r"\binsurance.*health\b",
        r"\bhealth.*insurance\b",
    ]),
    ("Entertainment", [
        r"\bcinema\b",
        r"\btheater\b",
        r"\bmovie\b",
        r"\bconcert\b",
        r"\bticket\b",
        r"\bsports\b",
        r"\bstadium\b",
        r"\barcade\b",
        r"\bsteam\b",
        r"\bxbox\b",
        r"\bplaystation\b",
        r"\bnintendo\b",
        r"\bgame\b",
        r"\bshow\b",
        r"\bmuseum\b",
        r"\bzoo\b",
        r"\bamusement\b",
        r"\beach esc\b",
        r"\bkaraoke\b",
        r"\bnightclub\b",
        r"\bclub\b",
        r"\bbowling\b",
        r"\bminigolf\b",
    ]),
    ("Shopping", [
        r"\bamazon\b",
        r"\bwalmmart\b",
        r"\bwalmart\b",
        r"\btarget\b",
        r"\bcostco\b",
        r"\bsam'?s club\b",
        r"\bbest buy\b",
        r"\bapple store\b",
        r"\bipple\b",
        r"\bnewegg\b",
        r"\betsy\b",
        r"\bebay\b",
        r"\bshein\b",
        r"\bnike\b",
        r"\badidas\b",
        r"\bh&m\b",
        r"\bzara\b",
        r"\bgap\b",
        r"\bold navy\b",
        r"\buniqlo\b",
        r"\bnordstrom\b",
        r"\bmacy\b",
        r"\bkohl\b",
        r"\btj maxx\b",
        r"\bmarshalls\b",
        r"\bhome depot\b",
        r"\blowe'?s\b",
        r"\bikea\b",
        r"\bcrate.*barrel\b",
        r"\bwayfair\b",
        r"\bfurniture\b",
        r"\bclothing\b",
        r"\bapparel\b",
        r"\bshoe\b",
        r"\bbooks\b",
    ]),
]

DEFAULT_CATEGORY = "Other"


# ── Categorization logic ──────────────────────────────────────────────────────

def categorize_transaction(description: str, tx_type: str, original_category: str = None) -> tuple:
    """
    Returns (category, confidence) where confidence is 'high', 'medium', or 'low'.
    - Income credits are always categorized as Income.
    - Keyword matches are 'high' confidence.
    - Falls back to original_category (medium) or 'Other' (low).
    """
    desc_lower = description.lower()

    # Income: credits that aren't refunds get Income category
    # (refunds are handled by the Income rules which include 'refund')
    if tx_type == "credit":
        for pattern in CATEGORY_RULES[0][1]:  # Income patterns
            if re.search(pattern, desc_lower, re.IGNORECASE):
                return ("Income", "high")
        # Unmatched credits are likely income/refunds
        return ("Income", "medium")

    # Check keyword rules
    for category, patterns in CATEGORY_RULES:
        if category == "Income":
            continue  # Already handled above for credits
        for pattern in patterns:
            if re.search(pattern, desc_lower, re.IGNORECASE):
                return (category, "high")

    # Fall back to original bank category if available
    if original_category:
        # Map common bank categories to our categories
        bank_category_map = {
            "food & drink": "Food & Dining",
            "food and drink": "Food & Dining",
            "groceries": "Food & Dining",
            "restaurants": "Food & Dining",
            "gas": "Transportation",
            "automotive": "Transportation",
            "travel": "Transportation",
            "health & wellness": "Health",
            "health and wellness": "Health",
            "medical": "Health",
            "bills & utilities": "Utilities",
            "bills and utilities": "Utilities",
            "entertainment": "Entertainment",
            "shopping": "Shopping",
            "personal": "Shopping",
            "home": "Housing",
            "rent": "Housing",
            "income": "Income",
            "payment": "Other",
            "transfer": "Other",
            "fees & adjustments": "Other",
            "fees and adjustments": "Other",
        }
        mapped = bank_category_map.get(original_category.lower())
        if mapped:
            return (mapped, "medium")
        # Unknown bank category — include it but flag as low confidence
        return (original_category, "low")

    return (DEFAULT_CATEGORY, "low")


def categorize_all(transactions: list) -> list:
    """Categorize a list of transactions. Returns annotated list."""
    result = []
    low_confidence = []

    for i, tx in enumerate(transactions):
        category, confidence = categorize_transaction(
            tx.get("description", ""),
            tx.get("type", "debit"),
            tx.get("original_category"),
        )
        annotated = dict(tx)
        annotated["category"] = category
        annotated["confidence"] = confidence
        result.append(annotated)

        if confidence in ("low", "medium"):
            low_confidence.append((i, tx.get("description", ""), category, confidence))

    if low_confidence:
        sys.stderr.write(
            f"\nINFO: {len(low_confidence)} transactions need LLM review (low/medium confidence):\n"
        )
        for idx, desc, cat, conf in low_confidence[:20]:  # Show first 20
            sys.stderr.write(f"  [{idx}] '{desc}' → {cat} ({conf} confidence)\n")
        if len(low_confidence) > 20:
            sys.stderr.write(f"  ... and {len(low_confidence) - 20} more\n")

    return result


def generate_summary(transactions: list) -> dict:
    """Generate a quick summary for LLM review."""
    from collections import defaultdict

    by_category = defaultdict(list)
    for tx in transactions:
        by_category[tx["category"]].append(tx)

    summary = {}
    for cat, txs in sorted(by_category.items()):
        total = sum(t["amount"] for t in txs if t["type"] == "debit")
        count = len(txs)
        summary[cat] = {
            "count": count,
            "total": round(total, 2),
            "sample_descriptions": list({t["description"] for t in txs[:5]}),
        }

    return summary


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Categorize parsed transactions")
    parser.add_argument("input", help="Path to transactions JSON (from parse_csv.py)")
    parser.add_argument("--budget", default=None, help="Path to budget config JSON (optional)")
    parser.add_argument("--output", default=None, help="Output JSON file path (default: stdout)")
    args = parser.parse_args()

    if not os.path.isfile(args.input):
        sys.stderr.write(f"ERROR: File not found: {args.input}\n")
        sys.exit(1)

    with open(args.input) as f:
        try:
            transactions = json.load(f)
        except json.JSONDecodeError as e:
            sys.stderr.write(f"ERROR: Invalid JSON in {args.input}: {e}\n")
            sys.exit(1)

    if not isinstance(transactions, list):
        sys.stderr.write("ERROR: Expected a JSON array of transactions\n")
        sys.exit(1)

    categorized = categorize_all(transactions)
    summary = generate_summary(categorized)

    output_data = {
        "transactions": categorized,
        "summary": summary,
        "meta": {
            "total_transactions": len(categorized),
            "requires_review": sum(1 for t in categorized if t["confidence"] in ("low", "medium")),
        },
    }

    output = json.dumps(output_data, indent=2)

    if args.output:
        with open(args.output, "w") as f:
            f.write(output)
        sys.stderr.write(f"INFO: Wrote categorized data to {args.output}\n")
        sys.stderr.write(f"INFO: {output_data['meta']['requires_review']} transactions need review\n")
    else:
        print(output)


if __name__ == "__main__":
    main()
