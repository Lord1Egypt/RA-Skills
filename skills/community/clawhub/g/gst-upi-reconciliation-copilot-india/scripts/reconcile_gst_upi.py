#!/usr/bin/env python3
import argparse
import csv
import datetime as dt
import json
import math
import re
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


DATE_FORMATS = [
    "%Y-%m-%d",
    "%d-%m-%Y",
    "%d/%m/%Y",
    "%m/%d/%Y",
    "%Y/%m/%d",
    "%d %b %Y",
    "%d %B %Y",
]


def parse_date(value: str) -> Optional[dt.date]:
    v = (value or "").strip()
    if not v:
        return None
    for fmt in DATE_FORMATS:
        try:
            return dt.datetime.strptime(v, fmt).date()
        except ValueError:
            continue
    return None


def normalize_str(value: str) -> str:
    return re.sub(r"\s+", " ", (value or "").strip().lower())


def parse_amount(value: str) -> Optional[float]:
    v = (value or "").strip()
    if not v:
        return None
    v = v.replace(",", "")
    v = re.sub(r"[^0-9.\-]", "", v)
    if v in {"", "-", "."}:
        return None
    try:
        return round(float(v), 2)
    except ValueError:
        return None


def safe_eq(a: Optional[float], b: Optional[float], tol: float = 0.01) -> bool:
    if a is None or b is None:
        return False
    return math.isclose(a, b, abs_tol=tol)


def extract_tokens(*values: str) -> List[str]:
    blob = " ".join(values).lower()
    tokens = re.findall(r"[a-z0-9]{4,}", blob)
    seen = set()
    out = []
    for t in tokens:
        if t not in seen:
            seen.add(t)
            out.append(t)
    return out


@dataclass
class GstRow:
    idx: int
    invoice_no: str
    invoice_date: Optional[dt.date]
    customer: str
    taxable_value: Optional[float]
    gst_amount: Optional[float]
    total_amount: Optional[float]


@dataclass
class UpiRow:
    idx: int
    txn_date: Optional[dt.date]
    amount: Optional[float]
    status: str
    txn_id: str
    utr: str
    payer: str
    note: str


def read_csv(path: str) -> List[Dict[str, str]]:
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def map_gst(rows: List[Dict[str, str]]) -> List[GstRow]:
    out = []
    for i, r in enumerate(rows):
        out.append(
            GstRow(
                idx=i,
                invoice_no=(r.get("invoice_no") or r.get("invoice_number") or "").strip(),
                invoice_date=parse_date(r.get("invoice_date") or r.get("date") or ""),
                customer=(r.get("customer_name") or r.get("party_name") or r.get("customer") or "").strip(),
                taxable_value=parse_amount(r.get("taxable_value") or r.get("taxable") or ""),
                gst_amount=parse_amount(r.get("gst_amount") or r.get("tax_amount") or ""),
                total_amount=parse_amount(r.get("total_amount") or r.get("grand_total") or r.get("invoice_total") or ""),
            )
        )
    return out


def map_upi(rows: List[Dict[str, str]]) -> List[UpiRow]:
    out = []
    for i, r in enumerate(rows):
        out.append(
            UpiRow(
                idx=i,
                txn_date=parse_date(r.get("txn_date") or r.get("date") or r.get("transaction_date") or ""),
                amount=parse_amount(r.get("amount") or r.get("txn_amount") or ""),
                status=normalize_str(r.get("status") or "success"),
                txn_id=(r.get("txn_id") or r.get("transaction_id") or "").strip(),
                utr=(r.get("utr") or r.get("rrn") or "").strip(),
                payer=(r.get("payer_name") or r.get("payer") or "").strip(),
                note=(r.get("note") or r.get("description") or r.get("remarks") or "").strip(),
            )
        )
    return out


def day_diff(a: Optional[dt.date], b: Optional[dt.date]) -> Optional[int]:
    if not a or not b:
        return None
    return abs((a - b).days)


def score_match(g: GstRow, u: UpiRow, date_window_days: int) -> Tuple[int, str]:
    if u.status and u.status not in {"success", "completed", "captured", "paid"}:
        return (-999, "upi-status-not-success")
    if not safe_eq(g.total_amount, u.amount):
        return (-999, "amount-mismatch")

    score = 100
    reasons = []

    dd = day_diff(g.invoice_date, u.txn_date)
    if dd is None:
        return (-999, "missing-or-invalid-date")
    if dd > date_window_days:
        return (-999, f"date-window-exceeded({dd}>{date_window_days})")
    score += max(0, 10 - dd)
    reasons.append(f"date-diff={dd}")

    invoice_tokens = extract_tokens(g.invoice_no)
    upi_tokens = extract_tokens(u.txn_id, u.utr, u.note, u.payer)
    overlap = set(invoice_tokens).intersection(set(upi_tokens))
    if overlap:
        score += 25
        reasons.append("invoice-ref-in-upi")

    cust_tokens = extract_tokens(g.customer)
    overlap_cust = set(cust_tokens).intersection(set(upi_tokens))
    if overlap_cust:
        score += 15
        reasons.append("customer-token-match")

    return (score, ";".join(reasons) if reasons else "amount-match")


def reconcile(gst_rows: List[GstRow], upi_rows: List[UpiRow], date_window_days: int) -> Tuple[List[Dict], List[GstRow], List[UpiRow]]:
    matched = []
    used_upi = set()

    for g in gst_rows:
        candidates = []
        for u in upi_rows:
            if u.idx in used_upi:
                continue
            score, reason = score_match(g, u, date_window_days)
            if score > 0:
                candidates.append((score, reason, u))

        if not candidates:
            continue

        candidates.sort(key=lambda x: x[0], reverse=True)
        best_score, reason, best_upi = candidates[0]
        used_upi.add(best_upi.idx)

        matched.append(
            {
                "invoice_no": g.invoice_no,
                "invoice_date": g.invoice_date.isoformat() if g.invoice_date else "",
                "customer_name": g.customer,
                "invoice_total": g.total_amount,
                "upi_txn_date": best_upi.txn_date.isoformat() if best_upi.txn_date else "",
                "upi_amount": best_upi.amount,
                "upi_txn_id": best_upi.txn_id,
                "upi_utr": best_upi.utr,
                "match_score": best_score,
                "match_reason": reason,
                "match_status": "MATCHED",
            }
        )

    matched_invoice_numbers = {m["invoice_no"] for m in matched}
    unreconciled_gst = [g for g in gst_rows if g.invoice_no not in matched_invoice_numbers]
    unreconciled_upi = [u for u in upi_rows if u.idx not in used_upi]

    return matched, unreconciled_gst, unreconciled_upi


def write_outputs(output_prefix: str, matched: List[Dict], unreconciled_gst: List[GstRow], unreconciled_upi: List[UpiRow]) -> Dict:
    recon_csv = f"{output_prefix}_reconciled.csv"
    gst_csv = f"{output_prefix}_gst_unmatched.csv"
    upi_csv = f"{output_prefix}_upi_unmatched.csv"
    summary_json = f"{output_prefix}_summary.json"

    with open(recon_csv, "w", encoding="utf-8", newline="") as f:
        fields = [
            "invoice_no",
            "invoice_date",
            "customer_name",
            "invoice_total",
            "upi_txn_date",
            "upi_amount",
            "upi_txn_id",
            "upi_utr",
            "match_score",
            "match_reason",
            "match_status",
        ]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in matched:
            w.writerow(r)

    with open(gst_csv, "w", encoding="utf-8", newline="") as f:
        fields = ["invoice_no", "invoice_date", "customer_name", "total_amount", "taxable_value", "gst_amount", "match_status"]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for g in unreconciled_gst:
            w.writerow(
                {
                    "invoice_no": g.invoice_no,
                    "invoice_date": g.invoice_date.isoformat() if g.invoice_date else "",
                    "customer_name": g.customer,
                    "total_amount": g.total_amount,
                    "taxable_value": g.taxable_value,
                    "gst_amount": g.gst_amount,
                    "match_status": "GST_UNMATCHED",
                }
            )

    with open(upi_csv, "w", encoding="utf-8", newline="") as f:
        fields = ["txn_date", "amount", "status", "txn_id", "utr", "payer", "note", "match_status"]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for u in unreconciled_upi:
            w.writerow(
                {
                    "txn_date": u.txn_date.isoformat() if u.txn_date else "",
                    "amount": u.amount,
                    "status": u.status,
                    "txn_id": u.txn_id,
                    "utr": u.utr,
                    "payer": u.payer,
                    "note": u.note,
                    "match_status": "UPI_UNMATCHED",
                }
            )

    total_gst = len(matched) + len(unreconciled_gst)
    total_upi = len(matched) + len(unreconciled_upi)
    matched_amount = round(sum((r.get("invoice_total") or 0) for r in matched), 2)
    total_gst_amount = round(matched_amount + sum((g.total_amount or 0) for g in unreconciled_gst), 2)

    summary = {
        "totals": {
            "gst_rows": total_gst,
            "upi_rows": total_upi,
            "matched_rows": len(matched),
            "gst_unmatched_rows": len(unreconciled_gst),
            "upi_unmatched_rows": len(unreconciled_upi),
        },
        "amounts": {
            "matched_amount": matched_amount,
            "gst_total_amount": total_gst_amount,
            "reconciliation_coverage_pct": round((matched_amount / total_gst_amount) * 100, 2) if total_gst_amount else 0,
        },
        "outputs": {
            "reconciled_csv": recon_csv,
            "gst_unmatched_csv": gst_csv,
            "upi_unmatched_csv": upi_csv,
        },
    }

    with open(summary_json, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    return summary


def main() -> int:
    p = argparse.ArgumentParser(description="Reconcile GST invoices against UPI statements")
    p.add_argument("--gst-csv", required=True, help="GST invoice CSV path")
    p.add_argument("--upi-csv", required=True, help="UPI transaction CSV path")
    p.add_argument("--output-prefix", required=True, help="Output file prefix")
    p.add_argument("--date-window-days", type=int, default=7, help="Allowed date difference for matching (default: 7)")
    args = p.parse_args()

    gst_raw = read_csv(args.gst_csv)
    upi_raw = read_csv(args.upi_csv)

    gst_rows = map_gst(gst_raw)
    upi_rows = map_upi(upi_raw)

    matched, gst_unmatched, upi_unmatched = reconcile(gst_rows, upi_rows, args.date_window_days)
    summary = write_outputs(args.output_prefix, matched, gst_unmatched, upi_unmatched)

    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
