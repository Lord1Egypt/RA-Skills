#!/usr/bin/env python3
import argparse, json, sqlite3, sys
from pathlib import Path

DB = Path.home() / 'Library/Application Support/AddressBook/AddressBook-v22.abcddb'

BASE_QUERY = """
WITH base AS (
  SELECT
    Z_PK,
    COALESCE(NULLIF(TRIM(ZNAME), ''), TRIM(COALESCE(ZFIRSTNAME,'') || ' ' || COALESCE(ZLASTNAME,''))) AS display_name,
    ZFIRSTNAME,
    ZLASTNAME,
    ZORGANIZATION,
    ZJOBTITLE,
    ZNICKNAME,
    ZDEPARTMENT,
    ZME
  FROM ZABCDRECORD
)
SELECT
  b.Z_PK,
  b.display_name,
  b.ZFIRSTNAME AS first_name,
  b.ZLASTNAME AS last_name,
  b.ZORGANIZATION AS organization,
  b.ZJOBTITLE AS job_title,
  b.ZNICKNAME AS nickname,
  b.ZDEPARTMENT AS department,
  CASE WHEN b.ZME IS NULL THEN 0 ELSE b.ZME END AS is_me,
  GROUP_CONCAT(DISTINCT p.ZFULLNUMBER) AS phones,
  GROUP_CONCAT(DISTINCT e.ZADDRESS) AS emails
FROM base b
LEFT JOIN ZABCDPHONENUMBER p ON p.ZOWNER = b.Z_PK
LEFT JOIN ZABCDEMAILADDRESS e ON e.ZOWNER = b.Z_PK
"""


def rows_to_dicts(cur):
    cols = [d[0] for d in cur.description]
    out = []
    for r in cur.fetchall():
        item = dict(zip(cols, r))
        for key in ('phones', 'emails'):
            if item.get(key):
                item[key] = sorted({x.strip() for x in item[key].split(',') if x and x.strip()})
            else:
                item[key] = []
        item['display_name'] = item.get('display_name') or ''
        out.append(item)
    return out


def envelope(items, query=None, limit=None):
    return {
        'ok': True,
        'count': len(items),
        'query': query,
        'limit': limit,
        'items': items,
    }


def connect():
    if not DB.exists():
        print(json.dumps({"ok": False, "error": f"Contacts DB not found: {DB}"}, ensure_ascii=False, indent=2))
        sys.exit(2)
    con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    con.row_factory = sqlite3.Row
    return con


def fetch(sql, params):
    con = connect()
    cur = con.execute(sql, params)
    return rows_to_dicts(cur)


def cmd_list(args):
    sql = BASE_QUERY + " WHERE (b.display_name <> '' OR b.ZFIRSTNAME IS NOT NULL OR b.ZLASTNAME IS NOT NULL) GROUP BY b.Z_PK ORDER BY (b.display_name = ''), b.display_name COLLATE NOCASE LIMIT ?"
    items = fetch(sql, (args.limit,))
    print(json.dumps(envelope(items, limit=args.limit), ensure_ascii=False, indent=2))


def cmd_search(args):
    q = f"%{args.query}%"
    sql = BASE_QUERY + """
WHERE (
  b.display_name LIKE ? OR
  b.ZFIRSTNAME LIKE ? OR
  b.ZLASTNAME LIKE ? OR
  b.ZORGANIZATION LIKE ? OR
  b.ZJOBTITLE LIKE ? OR
  b.ZNICKNAME LIKE ? OR
  b.ZDEPARTMENT LIKE ? OR
  p.ZFULLNUMBER LIKE ? OR
  e.ZADDRESS LIKE ?
)
GROUP BY b.Z_PK
ORDER BY (b.display_name = ''), b.display_name COLLATE NOCASE
LIMIT ?
"""
    items = fetch(sql, (q, q, q, q, q, q, q, q, q, args.limit))
    print(json.dumps(envelope(items, query=args.query, limit=args.limit), ensure_ascii=False, indent=2))


def cmd_get(args):
    sql = BASE_QUERY + " WHERE b.display_name = ? GROUP BY b.Z_PK ORDER BY b.Z_PK LIMIT ?"
    items = fetch(sql, (args.name, args.limit))
    print(json.dumps(envelope(items, query=args.name, limit=args.limit), ensure_ascii=False, indent=2))


def cmd_exists(args):
    clauses = []
    params = []
    if args.name:
        clauses.append("b.display_name = ?")
        params.append(args.name)
    if args.phone:
        clauses.append("p.ZFULLNUMBER = ?")
        params.append(args.phone)
    if args.email:
        clauses.append("e.ZADDRESS = ?")
        params.append(args.email)
    if not clauses:
        print(json.dumps({'ok': False, 'error': 'Provide at least one of --name/--phone/--email'}, ensure_ascii=False, indent=2))
        sys.exit(2)
    sql = BASE_QUERY + " WHERE " + " OR ".join(f"({c})" for c in clauses) + " GROUP BY b.Z_PK ORDER BY b.Z_PK LIMIT ?"
    params.append(args.limit)
    items = fetch(sql, tuple(params))
    print(json.dumps({
        'ok': True,
        'exists': len(items) > 0,
        'count': len(items),
        'items': items,
    }, ensure_ascii=False, indent=2))


def main():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest='cmd', required=True)

    p = sp.add_parser('list')
    p.add_argument('--limit', type=int, default=20)
    p.set_defaults(func=cmd_list)

    p = sp.add_parser('search')
    p.add_argument('query')
    p.add_argument('--limit', type=int, default=20)
    p.set_defaults(func=cmd_search)

    p = sp.add_parser('get')
    p.add_argument('--name', required=True)
    p.add_argument('--limit', type=int, default=10)
    p.set_defaults(func=cmd_get)

    p = sp.add_parser('exists')
    p.add_argument('--name')
    p.add_argument('--phone')
    p.add_argument('--email')
    p.add_argument('--limit', type=int, default=20)
    p.set_defaults(func=cmd_exists)

    args = ap.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
