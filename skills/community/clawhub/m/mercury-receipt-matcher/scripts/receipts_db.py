#!/usr/bin/env python3
import argparse
import csv
import json
import re
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

DB_PATH = Path('/workspace/receipts.db')
SCHEMA_PATH = Path(__file__).resolve().parent.parent / 'references' / 'schema.sql'

SECTION_HEADER_RE = re.compile(r'^\d{1,2}-[A-Za-z]{3}\s*,*\s*$')
MONEY_CLEAN_RE = re.compile(r'[^0-9\-.,]')
LOG_LINE_RE = re.compile(r'^(\d+) \| ([0-9\-]+) \| (.*?) \| \$?([0-9,]+(?:\.[0-9]{2})?) \| ([A-Z/ ]+) \| (.*?) \| (.*)$')

@dataclass
class TxnRow:
    source_file: str
    source_row_number: int
    txn_date: str
    merchant: str
    amount_cents: int
    csv_status: Optional[str]
    source_account: Optional[str]
    bank_description: Optional[str]
    reference: Optional[str]
    note: Optional[str]
    last_four: Optional[str]
    cardholder_name: Optional[str]
    cardholder_email: Optional[str]
    merchant_type: Optional[str]
    category: Optional[str]
    gl_code: Optional[str]
    timestamp_utc: Optional[str]
    raw_csv_json: str
    normalized_status: str
    status_reason: Optional[str]


def ensure_db(conn: sqlite3.Connection):
    conn.executescript(SCHEMA_PATH.read_text())
    conn.execute("ALTER TABLE transactions ADD COLUMN canonical_key TEXT") if not column_exists(conn, 'transactions', 'canonical_key') else None
    conn.execute("ALTER TABLE transactions ADD COLUMN duplicate_of_transaction_id INTEGER REFERENCES transactions(id)") if not column_exists(conn, 'transactions', 'duplicate_of_transaction_id') else None
    conn.execute("ALTER TABLE transactions ADD COLUMN reconciliation_status TEXT") if not column_exists(conn, 'transactions', 'reconciliation_status') else None
    conn.execute("ALTER TABLE transactions ADD COLUMN reconciliation_note TEXT") if not column_exists(conn, 'transactions', 'reconciliation_note') else None
    conn.execute("ALTER TABLE transactions ADD COLUMN actionable_status TEXT") if not column_exists(conn, 'transactions', 'actionable_status') else None
    conn.commit()


def column_exists(conn: sqlite3.Connection, table: str, column: str) -> bool:
    rows = conn.execute(f'PRAGMA table_info({table})').fetchall()
    return any(r[1] == column for r in rows)


def normalize_money_to_cents(value: str) -> int:
    s = (value or '').strip()
    if not s:
        return 0
    s = MONEY_CLEAN_RE.sub('', s)
    s = s.replace(',', '')
    if s in {'', '-', '.'}:
        return 0
    return int(round(float(s) * 100))


def normalize_date(value: str) -> str:
    value = (value or '').strip()
    if not value:
        return value
    if re.match(r'^\d{4}-\d{2}-\d{2}$', value):
        return value
    m = re.match(r'^(\d{1,2})/(\d{1,2})/(\d{2,4})$', value)
    if m:
        month, day, year = m.groups()
        if len(year) == 2:
            year = '20' + year
        return f'{year.zfill(4)}-{month.zfill(2)}-{day.zfill(2)}'
    m = re.match(r'^(\d{1,2})-(\d{1,2})-(\d{4})$', value)
    if m:
        month, day, year = m.groups()
        return f'{year.zfill(4)}-{month.zfill(2)}-{day.zfill(2)}'
    return value


def normalize_merchant(value: str) -> str:
    value = (value or '').strip().lower()
    value = re.sub(r'\s+', ' ', value)
    value = value.replace('.com', '')
    return value


def canonical_key(txn_date: str, merchant: str, amount_cents: int, last_four: Optional[str]) -> str:
    return f'{txn_date}|{normalize_merchant(merchant)}|{amount_cents}|{(last_four or "").strip()}'


def normalize_status(amount_cents: int, merchant: str) -> tuple[str, Optional[str]]:
    merchant_l = (merchant or '').lower()
    if amount_cents > 0:
        return 'refund', 'Positive amount in CSV'
    if any(x in merchant_l for x in ['facebook', 'reddit']):
        return 'pending', 'Ad charge, likely low receipt probability'
    return 'pending', None


def import_csv(conn: sqlite3.Connection, csv_path: Path):
    with csv_path.open(newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        rownum = 0
        inserted = 0
        skipped = 0
        for raw in reader:
            rownum += 1
            first = (raw.get('Date (UTC)') or '').strip()
            if not first or SECTION_HEADER_RE.match(first):
                continue
            merchant = (raw.get('Description') or '').strip()
            amount_cents = normalize_money_to_cents(raw.get('Amount', ''))
            txn_date = normalize_date(first)
            status, reason = normalize_status(amount_cents, merchant)
            last_four = (raw.get('Last Four Digits') or '').strip() or None
            ckey = canonical_key(txn_date, merchant, amount_cents, last_four)
            tx = TxnRow(
                source_file=str(csv_path),
                source_row_number=rownum,
                txn_date=txn_date,
                merchant=merchant,
                amount_cents=amount_cents,
                csv_status=(raw.get('Status') or '').strip() or None,
                source_account=(raw.get('Source Account') or '').strip() or None,
                bank_description=(raw.get('Bank Description') or '').strip() or None,
                reference=(raw.get('Reference') or '').strip() or None,
                note=(raw.get('Note') or '').strip() or None,
                last_four=last_four,
                cardholder_name=(raw.get('Name On Card') or '').strip() or None,
                cardholder_email=(raw.get('Cardholder Email') or '').strip() or None,
                merchant_type=((raw.get('Merchant Type') or raw.get('Mercury Category') or '').strip() or None),
                category=(raw.get('Category') or '').strip() or None,
                gl_code=(raw.get('GL Code') or '').strip() or None,
                timestamp_utc=normalize_date((raw.get('Timestamp') or '').split(' ')[0]) + ('T' + (raw.get('Timestamp') or '').split(' ')[1] + ':00Z' if ' ' in (raw.get('Timestamp') or '') else '') if raw.get('Timestamp') else None,
                raw_csv_json=json.dumps(raw, ensure_ascii=False),
                normalized_status=status,
                status_reason=reason,
            )
            cur = conn.execute(
                '''INSERT OR IGNORE INTO transactions (
                    source_file, source_row_number, txn_date, merchant, amount_cents, csv_status,
                    source_account, bank_description, reference, note, last_four, cardholder_name,
                    cardholder_email, merchant_type, category, gl_code, timestamp_utc, raw_csv_json,
                    status, status_reason, canonical_key
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (
                    tx.source_file, tx.source_row_number, tx.txn_date, tx.merchant, tx.amount_cents, tx.csv_status,
                    tx.source_account, tx.bank_description, tx.reference, tx.note, tx.last_four, tx.cardholder_name,
                    tx.cardholder_email, tx.merchant_type, tx.category, tx.gl_code, tx.timestamp_utc, tx.raw_csv_json,
                    tx.normalized_status, tx.status_reason, ckey,
                )
            )
            if cur.rowcount:
                inserted += 1
            else:
                skipped += 1
        conn.commit()
    return inserted, skipped


def import_legacy_log(conn: sqlite3.Connection, log_path: Path):
    if not log_path.exists():
        return 0
    migrated = 0
    with log_path.open(encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\n')
            if not line or line.startswith('ROW | '):
                continue
            m = LOG_LINE_RE.match(line)
            if not m:
                continue
            row_num, date_s, merchant, amount_s, status_s, account, detail = m.groups()
            source_row_number = int(row_num)
            tx = conn.execute(
                'SELECT id FROM transactions WHERE source_row_number = ? ORDER BY id LIMIT 1',
                (source_row_number,)
            ).fetchone()
            if not tx:
                continue
            tx_id = tx[0]
            normalized = 'needs_review'
            reason = detail.strip()
            if 'FORWARDED' in detail:
                normalized = 'forwarded'
            elif status_s.strip() == 'FOUND':
                normalized = 'matched'
            elif 'restaurant' in detail.lower() or 'no email receipt expected' in detail.lower():
                normalized = 'skipped_no_receipt_expected'
            elif 'NOT FOUND' in line:
                normalized = 'not_found'
            elif 'NOT PROCESSED' in line:
                normalized = 'pending'
            elif 'CREDIT/REFUND' in status_s:
                normalized = 'refund'
            conn.execute(
                'UPDATE transactions SET status = ?, status_reason = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
                (normalized, reason, tx_id)
            )
            migrated += 1
    conn.commit()
    return migrated


def refresh_canonical_keys(conn: sqlite3.Connection):
    rows = conn.execute(
        '''SELECT id, txn_date, merchant, amount_cents, last_four
           FROM transactions'''
    ).fetchall()
    for row in rows:
        normalized_txn_date = normalize_date(row[1])
        conn.execute(
            'UPDATE transactions SET txn_date = ?, canonical_key = ? WHERE id = ?',
            (normalized_txn_date, canonical_key(normalized_txn_date, row[2], row[3], row[4]), row[0])
        )
    conn.commit()


def dedupe(conn: sqlite3.Connection):
    refresh_canonical_keys(conn)
    rows = conn.execute(
        '''SELECT id, canonical_key, source_file, source_row_number, status, txn_date
           FROM transactions
           WHERE canonical_key IS NOT NULL
           ORDER BY canonical_key, 
             CASE status WHEN 'forwarded' THEN 0 WHEN 'matched' THEN 1 WHEN 'not_found' THEN 2 WHEN 'pending' THEN 3 ELSE 4 END,
             source_row_number ASC, id ASC'''
    ).fetchall()
    groups = {}
    for row in rows:
        groups.setdefault(row[1], []).append(row)

    linked = 0
    flagged = 0
    for ckey, items in groups.items():
        if len(items) < 2:
            continue
        canonical = items[0]
        canonical_id = canonical[0]
        canonical_status = canonical[4]
        has_forwarded = any(i[4] == 'forwarded' for i in items)
        has_pending = any(i[4] == 'pending' for i in items)
        for item in items[1:]:
            conn.execute(
                'UPDATE transactions SET duplicate_of_transaction_id = ? WHERE id = ?',
                (canonical_id, item[0])
            )
            linked += 1
        if has_forwarded and has_pending:
            for item in items:
                if item[4] == 'pending':
                    conn.execute(
                        '''UPDATE transactions
                           SET reconciliation_status = 'mercury_not_matched',
                               reconciliation_note = 'Transaction was previously forwarded in another import but still appears as missing in a newer report',
                               actionable_status = 'error_revisit_required'
                           WHERE id = ?''',
                        (item[0],)
                    )
                    flagged += 1
            conn.execute(
                '''UPDATE transactions
                   SET reconciliation_status = COALESCE(reconciliation_status, 'previously_forwarded')
                   WHERE id = ?''',
                (canonical_id,)
            )
    conn.commit()
    return linked, flagged


def summary(conn: sqlite3.Connection):
    rows = conn.execute('SELECT status, COUNT(*) FROM transactions GROUP BY status ORDER BY status').fetchall()
    return rows


def reconciliation_summary(conn: sqlite3.Connection):
    return conn.execute(
        '''SELECT COALESCE(reconciliation_status, 'none') AS reconciliation_status, COUNT(*)
           FROM transactions
           GROUP BY COALESCE(reconciliation_status, 'none')
           ORDER BY reconciliation_status'''
    ).fetchall()


def next_batch(conn: sqlite3.Connection, limit: int = 5):
    return conn.execute(
        '''SELECT id, source_row_number, txn_date, merchant, amount_cents, status, status_reason, reconciliation_status, actionable_status
           FROM transactions
           WHERE (status IN ('pending', 'forward_failed', 'needs_review') OR actionable_status = 'error_revisit_required')
             AND duplicate_of_transaction_id IS NULL
           ORDER BY
             CASE WHEN actionable_status = 'error_revisit_required' THEN 0 ELSE 1 END,
             txn_date DESC,
             source_row_number ASC
           LIMIT ?''',
        (limit,)
    ).fetchall()


def flagged_rows(conn: sqlite3.Connection, limit: int = 20):
    return conn.execute(
        '''SELECT id, source_file, source_row_number, txn_date, merchant, amount_cents, status, reconciliation_status, reconciliation_note, duplicate_of_transaction_id, actionable_status
           FROM transactions
           WHERE reconciliation_status IS NOT NULL OR actionable_status IS NOT NULL
           ORDER BY
             CASE WHEN actionable_status = 'error_revisit_required' THEN 0 ELSE 1 END,
             txn_date DESC, source_row_number ASC
           LIMIT ?''',
        (limit,)
    ).fetchall()


def export_report(conn: sqlite3.Connection, out_path: Path):
    rows = conn.execute(
        '''SELECT source_row_number, txn_date, merchant, amount_cents, status, status_reason, reconciliation_status, reconciliation_note, actionable_status
           FROM transactions ORDER BY txn_date DESC, source_row_number ASC'''
    ).fetchall()
    with out_path.open('w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['row', 'date', 'merchant', 'amount', 'status', 'reason', 'reconciliation_status', 'reconciliation_note', 'actionable_status'])
        for row in rows:
            amount = row[3] / 100
            writer.writerow([row[0], row[1], row[2], f'{amount:.2f}', row[4], row[5] or '', row[6] or '', row[7] or '', row[8] or ''])


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest='cmd', required=True)

    sub.add_parser('init')

    p_import_csv = sub.add_parser('import-csv')
    p_import_csv.add_argument('csv_path')

    p_import_log = sub.add_parser('import-log')
    p_import_log.add_argument('log_path')

    sub.add_parser('summary')
    sub.add_parser('dedupe')
    sub.add_parser('reconciliation-summary')

    p_next = sub.add_parser('next-batch')
    p_next.add_argument('--limit', type=int, default=5)

    p_flagged = sub.add_parser('flagged')
    p_flagged.add_argument('--limit', type=int, default=20)

    p_export = sub.add_parser('export-report')
    p_export.add_argument('out_path')

    args = parser.parse_args()
    conn = sqlite3.connect(DB_PATH)
    ensure_db(conn)

    if args.cmd == 'init':
        print(f'initialized {DB_PATH}')
    elif args.cmd == 'import-csv':
        inserted, skipped = import_csv(conn, Path(args.csv_path))
        print(json.dumps({'inserted': inserted, 'skipped': skipped}, indent=2))
    elif args.cmd == 'import-log':
        migrated = import_legacy_log(conn, Path(args.log_path))
        print(json.dumps({'migrated': migrated}, indent=2))
    elif args.cmd == 'summary':
        print(json.dumps([{ 'status': s, 'count': c } for s, c in summary(conn)], indent=2))
    elif args.cmd == 'dedupe':
        linked, flagged = dedupe(conn)
        print(json.dumps({'linked_duplicates': linked, 'flagged_mercury_not_matched': flagged}, indent=2))
    elif args.cmd == 'reconciliation-summary':
        print(json.dumps([{ 'reconciliation_status': s, 'count': c } for s, c in reconciliation_summary(conn)], indent=2))
    elif args.cmd == 'next-batch':
        rows = next_batch(conn, args.limit)
        print(json.dumps([
            {
                'id': r[0], 'source_row_number': r[1], 'txn_date': r[2], 'merchant': r[3],
                'amount_cents': r[4], 'status': r[5], 'status_reason': r[6], 'reconciliation_status': r[7], 'actionable_status': r[8]
            }
            for r in rows
        ], indent=2))
    elif args.cmd == 'flagged':
        rows = flagged_rows(conn, args.limit)
        print(json.dumps([
            {
                'id': r[0], 'source_file': r[1], 'source_row_number': r[2], 'txn_date': r[3], 'merchant': r[4],
                'amount_cents': r[5], 'status': r[6], 'reconciliation_status': r[7],
                'reconciliation_note': r[8], 'duplicate_of_transaction_id': r[9], 'actionable_status': r[10]
            }
            for r in rows
        ], indent=2))
    elif args.cmd == 'export-report':
        export_report(conn, Path(args.out_path))
        print(f'exported {args.out_path}')

    conn.close()


if __name__ == '__main__':
    main()
