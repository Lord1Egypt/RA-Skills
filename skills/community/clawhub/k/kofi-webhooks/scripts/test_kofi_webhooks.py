"""Loopback integration tests; synthetic data only, temporary storage."""
from concurrent.futures import ThreadPoolExecutor
import http.client
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
from tempfile import TemporaryDirectory
from threading import Thread
import unittest
from unittest.mock import patch
from urllib.parse import urlencode

import kofi_webhooks as kofi


class WebhookTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.db = Path(self.temp.name) / 'events.sqlite3'
        self.token = 'synthetic-local-test-token'
        self.server = kofi.make_server(self.db, self.token, port=0)
        self.thread = Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    def tearDown(self):
        self.server.shutdown()
        self.thread.join()
        self.server.server_close()
        self.temp.cleanup()

    def event(self, identifier='test-1', **changes):
        event = dict(verification_token=self.token, message_id=identifier,
                     timestamp='2026-11-17T12:00:00Z', type='Donation',
                     amount='0.10', currency='USD', is_public=False,
                     from_name='Synthetic Supporter', email='synthetic@example.invalid',
                     message='Synthetic test; not a real payment', shipping=None,
                     shop_items=None, tier_name=None, is_subscription_payment=False,
                     is_first_subscription_payment=False)
        event.update(changes)
        return event

    def post(self, event=None, body=None, content_type='application/x-www-form-urlencoded', path='/kofi'):
        if body is None:
            body = urlencode({'data': json.dumps(event or self.event())}).encode()
        conn = http.client.HTTPConnection('127.0.0.1', self.server.server_port, timeout=5)
        try:
            conn.request('POST', path, body, {'Content-Type': content_type})
            response = conn.getresponse()
            return response.status, json.loads(response.read())
        finally:
            conn.close()

    def cli(self, *args):
        return subprocess.run([sys.executable, str(Path(kofi.__file__)), '--db', str(self.db), *args],
                              capture_output=True, text=True, encoding='utf-8', check=True)

    def test_default_database_uses_user_data_directory(self):
        key = 'LOCALAPPDATA' if sys.platform == 'win32' else 'XDG_DATA_HOME'
        with patch.dict(os.environ, {key: self.temp.name}):
            self.assertEqual(kofi.default_db_path(), Path(self.temp.name) / 'kofi-webhooks/events.sqlite3')
        # Explicit --db is already exercised by every CLI test.

    def test_durable_receipt_deduplication_and_secret_removal(self):
        self.assertEqual(self.post()[0], 200)
        self.assertEqual(self.post()[1], {'accepted': True, 'duplicate': True})
        # New server using the same DB simulates restart and re-delivery.
        other = kofi.make_server(self.db, self.token, port=0)
        try:
            self.assertFalse(kofi.record(other.db_path, kofi.decode_event(
                urlencode({'data': json.dumps(self.event())}).encode(),
                'application/x-www-form-urlencoded', self.token)))
        finally:
            other.server_close()
        rows = list(kofi.events(self.db))
        self.assertEqual(len(rows), 1)
        self.assertNotIn('verification_token', rows[0])
        self.assertNotIn(self.token.encode(), self.db.read_bytes())

    def test_reject_wrong_missing_token_and_malformed_payload(self):
        self.assertEqual(self.post(self.event(verification_token='wrong'))[0], 403)
        missing = self.event()
        del missing['verification_token']
        self.assertEqual(self.post(missing)[0], 403)
        for body in (b'data=%7Bbad', b'data=[]', b'other=value', b'data={}&data={}'): 
            self.assertEqual(self.post(body=body)[0], 400)
        self.assertEqual(self.post(body=b'{}', content_type='application/json')[0], 400)
        self.assertEqual(len(list(kofi.events(self.db))), 0)

    def test_invalid_amounts_and_booleans_are_not_accepted(self):
        for amount in ('NaN', 'Infinity', '-1', '1e100000', 'n/a'):
            self.assertEqual(self.post(self.event(amount=amount))[0], 400)
        self.assertEqual(self.post(self.event(is_subscription_payment='false'))[0], 400)

    def test_concurrent_duplicate_deliveries(self):
        with ThreadPoolExecutor(max_workers=6) as pool:
            results = list(pool.map(lambda _: self.post(), range(12)))
        self.assertTrue(all(status == 200 for status, _ in results))
        self.assertEqual(sum(not body['duplicate'] for _, body in results), 1)
        self.assertEqual(len(list(kofi.events(self.db))), 1)

    def test_storage_failure_is_retryable_not_acknowledged(self):
        with patch.object(kofi, 'record', side_effect=sqlite3.OperationalError('synthetic')):
            self.assertEqual(self.post()[0], 503)
        self.assertEqual(self.post()[0], 200)

    def test_currency_separation_precision_and_optional_payload_preservation(self):
        self.post(self.event())
        self.post(self.event('test-2', amount='0.20', type='Shop Order',
                             shop_items=[{'direct_link_code': 'synthetic', 'quantity': 2}],
                             future_field={'preserved': True}))
        self.post(self.event('test-3', amount='5.00', currency='EUR', type='Subscription',
                             is_subscription_payment=True, is_first_subscription_payment=True))
        self.post(self.event('test-4', amount='1.25', type='Commission'))
        summary = json.loads(self.cli('summary').stdout)
        self.assertEqual(summary['gross_totals_by_currency'], {'EUR': '5.00', 'USD': '1.55'})
        self.assertEqual(summary['received_events'], 4)
        second = [r for r in kofi.events(self.db) if r['message_id'] == 'test-2'][0]
        self.assertEqual(second['shop_items'][0]['quantity'], 2)
        self.assertTrue(second['future_field']['preserved'])

    def test_cli_redaction_export_and_no_overwrite(self):
        self.post()
        recent = json.loads(self.cli('list').stdout)
        self.assertNotIn('email', recent[0])
        for private in (False, True):
            output = Path(self.temp.name) / ('private.jsonl' if private else 'redacted.jsonl')
            args = ['export', '--output', str(output)] + (['--include-private'] if private else [])
            self.cli(*args)
            data = json.loads(output.read_text(encoding='utf-8'))
            self.assertEqual('email' in data, private)
            self.assertNotIn('verification_token', data)
            with self.assertRaises(subprocess.CalledProcessError):
                self.cli(*args)
        with self.assertRaises(subprocess.CalledProcessError):
            self.cli('export', '--output', str(self.db))
        self.assertEqual(len(list(kofi.events(self.db))), 1)

    def test_route_body_limit_and_health(self):
        self.assertEqual(self.post(path='/other')[0], 404)
        self.assertEqual(self.post(body=b'x' * (kofi.MAX_BODY + 1))[0], 413)
        conn = http.client.HTTPConnection('127.0.0.1', self.server.server_port, timeout=5)
        try:
            conn.request('GET', '/healthz')
            response = conn.getresponse()
            self.assertEqual(response.status, 200)
            self.assertEqual(json.loads(response.read()), {'status': 'ok'})
        finally:
            conn.close()


if __name__ == '__main__':
    unittest.main(verbosity=2)
