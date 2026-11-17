#!/usr/bin/env python3
"""Exercise restart, concurrency, idempotency, isolation and waiting behaviour."""
import concurrent.futures
import sqlite3
import tempfile
import unittest
from pathlib import Path

from artifact_contract import native_audit_identity, native_runtime_event_identity
from run_journal import Journal


class JournalTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name)/'journal.sqlite'
        self.j = Journal(self.path)
        self.j.create('run-test','customer-a','2.0.3','monthly_report')

    def tearDown(self):
        self.j.close()
        self.tmp.cleanup()

    def add(self,key,kind,payload):
        return self.j.append('run-test','customer-a',key,kind,payload)

    def member(self,event_type='member_started'):
        return dict(**native_runtime_event_identity(event_type,'2.0.3'),role='data-analyst',host='test-fixture',
                    agent_task_id='fixture-agent',attempt_id='a1')

    def test_restart_and_return(self):
        self.add('start','member_started',self.member())
        self.j.close()
        self.j=Journal(self.path)
        self.assertEqual(len(self.j.status('run-test','customer-a')['waiting']),1)
        self.add('return','member_returned',dict(**self.member('member_returned'),handoff_sha256='a'*64))
        self.assertFalse(self.j.status('run-test','customer-a')['waiting'])

    def test_scope(self):
        with self.assertRaisesRegex(ValueError,'scope_mismatch'):
            self.j.status('run-test','customer-b')

    def test_idempotency(self):
        a=self.add('same','phase',{'phase':'inventory'})
        b=self.add('same','phase',{'phase':'inventory'})
        self.assertEqual(a,b)
        with self.assertRaisesRegex(ValueError,'idempotency'):
            self.add('same','phase',{'phase':'analysis'})

    def test_early_completion(self):
        with self.assertRaisesRegex(ValueError,'transition'):
            self.add('early','phase',{'phase':'complete'})

    def test_unsolicited_return(self):
        with self.assertRaisesRegex(ValueError,'not_waiting'):
            self.add('return','member_returned',dict(**self.member('member_returned'),handoff_sha256='a'*64))

    def test_late_return_cannot_replace(self):
        self.add('start','member_started',self.member())
        self.add('r1','member_returned',dict(**self.member('member_returned'),handoff_sha256='a'*64))
        with self.assertRaisesRegex(ValueError,'not_waiting'):
            self.add('r2','member_returned',dict(**self.member('member_returned'),handoff_sha256='b'*64))

    def test_legacy_member_event_cannot_count_as_current_collaboration(self):
        legacy=dict(role='data-analyst',host='test-fixture',agent_task_id='fixture-agent',attempt_id='a1')
        with self.assertRaisesRegex(ValueError,'runtime_event_identity_invalid'):
            self.add('legacy-start','member_started',legacy)

    def test_legacy_completion_event_cannot_finish_current_run(self):
        payload=dict(receipt_file='completion.json',receipt_sha256='a'*64,report_revision='R1')
        with self.assertRaisesRegex(ValueError,'receipt_identity_invalid'):
            self.add('legacy-completion','delivery_completed',payload)

    def test_credentials(self):
        with self.assertRaisesRegex(ValueError,'credential'):
            self.add('secret','connector_observation',{'reason':'test','nested':{'access_token':'synthetic'}})

    def test_immutable(self):
        self.add('first','phase',{'phase':'inventory'})
        with self.assertRaises(sqlite3.IntegrityError):
            self.j.db.execute("UPDATE events SET body='{}'")

    def test_parallel_writers(self):
        def worker(i):
            j=Journal(self.path)
            try:
                return j.append('run-test','customer-a',f'event-{i}','human_correction',
                                dict(**native_audit_identity('human_feedback','2.0.3'),reason=f'fixture {i}'))
            finally:
                j.close()
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
            list(pool.map(worker,range(12)))
        self.assertEqual(len(self.j.events('run-test','customer-a')),12)

    def test_unknown_measurement_stays_unknown(self):
        self.add('model','model_observation',dict(**native_audit_identity('model_observation','2.0.3'),
                 model_alias='host-default',task_class='diagnosis',cost=None,latency_ms=None))
        self.assertIsNone(self.j.events('run-test','customer-a')[0]['payload']['cost'])


if __name__=='__main__':
    unittest.main()
