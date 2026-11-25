"""Ko-fi payment webhook receiver and local reporting (Python 3.10+, stdlib)."""
import argparse
import hmac
import json
import os
from pathlib import Path
import sqlite3
import sys
from contextlib import closing, contextmanager
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation, localcontext
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs

MAX_BODY = 1024 * 1024
PUBLIC_FIELDS = (
    'message_id', 'timestamp', 'type', 'amount', 'currency', 'is_public',
    'is_subscription_payment', 'is_first_subscription_payment', 'tier_name',
)


@contextmanager
def connect(path):
    with closing(sqlite3.connect(str(path), timeout=15)) as db:
        with db:
            yield db


def initialize(path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with connect(path) as db:
        db.execute('''CREATE TABLE IF NOT EXISTS events (
            message_id TEXT PRIMARY KEY, received_at TEXT NOT NULL,
            payload TEXT NOT NULL)''')


def decode_event(body, content_type, token):
    if content_type.split(';', 1)[0].strip().lower() != 'application/x-www-form-urlencoded':
        raise ValueError('Expected URL-encoded form')
    fields = parse_qs(body.decode('utf-8'), keep_blank_values=True, max_num_fields=16)
    if len(fields.get('data', [])) != 1:
        raise ValueError('Expected exactly one data field')
    event = json.loads(fields['data'][0])
    if not isinstance(event, dict):
        raise ValueError('Expected event object')
    received_token = event.get('verification_token')
    if not isinstance(received_token, str) or not hmac.compare_digest(
        received_token.encode('utf-8'), token.encode('utf-8')
    ):
        raise PermissionError('Invalid verification token')
    for key in ('message_id', 'type', 'amount', 'currency'):
        if not isinstance(event.get(key), str) or not event[key].strip():
            raise ValueError('Missing or invalid payment field')
    if len(event['message_id']) > 256 or len(event['currency']) > 16:
        raise ValueError('Invalid payment field length')
    try:
        amount = Decimal(event['amount'])
    except InvalidOperation as exc:
        raise ValueError('Invalid amount') from exc
    # Bound input complexity while permitting sub-cent currencies without rounding.
    if not amount.is_finite() or amount < 0 or len(event['amount']) > 64 or abs(amount.as_tuple().exponent) > 16:
        raise ValueError('Invalid amount')
    for key in ('is_public', 'is_subscription_payment', 'is_first_subscription_payment'):
        if key in event and not isinstance(event[key], bool):
            raise ValueError('Invalid boolean payment field')
    event.pop('verification_token')
    return event


def record(path, event):
    # Context manager commits before returning; storage failure must not get a 200.
    with connect(path) as db:
        result = db.execute(
            'INSERT OR IGNORE INTO events VALUES (?, ?, ?)',
            (event['message_id'], datetime.now(timezone.utc).isoformat(),
             json.dumps(event, ensure_ascii=False)),
        )
        inserted = result.rowcount == 1
    return inserted


class Handler(BaseHTTPRequestHandler):
    def setup(self):
        super().setup()
        self.connection.settimeout(15)

    def log_message(self, *_args):
        pass  # No request bodies, tokens, customer details or hostile URLs in logs.

    def respond(self, status, value):
        body = json.dumps(value).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        self.respond(200 if self.path == '/healthz' else 404,
                     {'status': 'ok'} if self.path == '/healthz' else {'error': 'Not found'})

    def do_POST(self):
        if self.path != '/kofi':
            self.respond(404, {'error': 'Not found'})
            return
        if self.headers.get('Transfer-Encoding'):
            self.respond(400, {'error': 'Transfer encoding not supported'})
            return
        try:
            size = int(self.headers.get('Content-Length', '-1'))
            if size < 0 or size > MAX_BODY:
                self.respond(413 if size > MAX_BODY else 411, {'error': 'Invalid body length'})
                return
            body = self.rfile.read(size)
            if len(body) != size:
                raise ValueError('Incomplete body')
            event = decode_event(body, self.headers.get('Content-Type', ''), self.server.token)
        except PermissionError:
            self.respond(403, {'error': 'Invalid verification token'})
            return
        except (ValueError, UnicodeError, RecursionError):
            self.respond(400, {'error': 'Invalid webhook payload'})
            return
        except (TimeoutError, OSError):
            self.respond(408, {'error': 'Request timed out'})
            return
        try:
            inserted = record(self.server.db_path, event)
        except (sqlite3.Error, OSError):
            self.respond(503, {'error': 'Storage unavailable; retry later'})
            return
        self.respond(200, {'accepted': True, 'duplicate': not inserted})


def make_server(db_path, token, host='127.0.0.1', port=8787):
    if not token:
        raise ValueError('Webhook verification token is required')
    initialize(db_path)
    server = ThreadingHTTPServer((host, port), Handler)
    server.db_path = db_path
    server.token = token
    return server


def events(path, limit=None):
    if not Path(path).is_file():
        raise ValueError('Database does not exist; no receiver history is available')
    # Reporting must not create or mutate the database.
    uri = Path(path).resolve().as_uri() + '?mode=ro'
    with closing(sqlite3.connect(uri, uri=True)) as db:
        query = 'SELECT received_at, payload FROM events ORDER BY rowid DESC'
        rows = db.execute(query + (' LIMIT ?' if limit is not None else ''),
                          (limit,) if limit is not None else ())
        for received_at, payload in rows:
            event = json.loads(payload)
            event['received_at'] = received_at
            yield event


def redact(event):
    return {key: event[key] for key in (*PUBLIC_FIELDS, 'received_at') if key in event}


def summarize(rows):
    totals, types, count = {}, {}, 0
    with localcontext() as ctx:
        ctx.prec = 128
        for event in rows:
            count += 1
            currency = event['currency']
            totals[currency] = totals.get(currency, Decimal('0')) + Decimal(event['amount'])
            types[event['type']] = types.get(event['type'], 0) + 1
    return {'received_events': count, 'gross_totals_by_currency': {
        key: format(value, 'f') for key, value in sorted(totals.items())
    }, 'counts_by_type': types, 'scope': 'Received events only; may include test deliveries'}


def default_db_path():
    if sys.platform == 'win32':
        base = Path(os.environ.get('LOCALAPPDATA') or (Path.home() / 'AppData/Local'))
    else:
        base = Path(os.environ.get('XDG_DATA_HOME') or (Path.home() / '.local/share'))
    return base / 'kofi-webhooks/events.sqlite3'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--db', type=Path, default=Path(os.environ.get(
        'KOFI_DB', str(default_db_path()))))
    sub = parser.add_subparsers(dest='command', required=True)
    serve = sub.add_parser('serve', help='Receive verified webhook POSTs')
    serve.add_argument('--host', default='127.0.0.1')
    serve.add_argument('--port', type=int, default=8787)
    serve.add_argument('--token-file', type=Path)
    listing = sub.add_parser('list', help='List recent redacted payment events')
    listing.add_argument('--limit', type=int, default=20)
    sub.add_parser('summary', help='Summarize received payments by currency')
    export = sub.add_parser('export', help='Export received events as JSONL')
    export.add_argument('--output', type=Path, required=True)
    export.add_argument('--include-private', action='store_true')
    args = parser.parse_args()
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    try:
        if args.command == 'serve':
            token = (args.token_file.read_text(encoding='utf-8-sig').strip()
                     if args.token_file else os.environ.get('KOFI_VERIFICATION_TOKEN', '').strip())
            server = make_server(args.db, token, args.host, args.port)
            print(json.dumps({'listening': f'http://{args.host}:{server.server_port}/kofi',
                              'live_delivery_verified': False}), flush=True)
            try:
                server.serve_forever()
            except KeyboardInterrupt:
                pass
            finally:
                server.server_close()
        elif args.command == 'list':
            if args.limit < 1:
                raise ValueError('Limit must be positive')
            print(json.dumps([redact(row) for row in events(args.db, args.limit)], ensure_ascii=False, indent=2))
        elif args.command == 'summary':
            print(json.dumps(summarize(events(args.db)), indent=2))
        else:
            if args.output.resolve() == args.db.resolve():
                raise ValueError('Export output must differ from database path')
            count = 0
            # Exclusive creation avoids accidentally overwriting an existing export.
            rows = events(args.db)
            first = next(rows, None)  # Check DB before creating output.
            with args.output.open('x', encoding='utf-8') as output:
                if first is not None:
                    import itertools
                    for row in itertools.chain([first], rows):
                        output.write(json.dumps(row if args.include_private else redact(row),
                                                ensure_ascii=False) + '\n')
                        count += 1
            print(json.dumps({'exported': count, 'output': str(args.output),
                              'includes_private': args.include_private}))
    except (ValueError, OSError, sqlite3.Error) as exc:
        # Do not print payloads or tokens; error categories are sufficient for CLI failures.
        parser.exit(1, f'{type(exc).__name__}: {str(exc) if isinstance(exc, ValueError) else "Operation failed; check paths, permissions and database"}\n')


if __name__ == '__main__':
    main()
