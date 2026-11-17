"""Synthetic platform-read boundary tests; never real platform acceptance."""
import copy
import json
import sys
import tempfile
import unittest
from datetime import datetime, timezone, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from connectors import MockPlatformConnector
from connectors.contract import canonical_hash
from execution_store import ExecutionStore
from platform_read_guard import PlatformReadGateway
from run_journal import Journal, digest, encoded


VERSION='2.0.3-candidate.1'


class CountingMock(MockPlatformConnector):
    def __init__(self, now):
        super().__init__()
        self.now=now
        self.reads=0

    def read(self,*args):
        self.reads += 1
        result=super().read(*args)
        result['read_at']=self.now.isoformat()
        return result


class FakeApiConnector:
    def __init__(self, now):
        self.now=now
        self.reads=0
        self.failure=None

    def capabilities(self):
        return dict(schema_version='1.0',connector_id='fake-api',platform='test-api',
                    connector_version='1.0.0',mode='api',status='read_only_verified',
                    read_actions=['campaign.get'],write_actions=[],conditional_write=False,
                    auth_type='api_key_ref',verified_at=self.now.isoformat())

    def read(self,resource,platform_id):
        self.reads += 1
        data={'status':'active','budget':1200}
        read_at=self.now if self.failure!='stale' else self.now-timedelta(minutes=10)
        fingerprint=canonical_hash({'resource':resource,'platform_id':platform_id,'data':data})
        if self.failure=='fingerprint': fingerprint='0'*64
        return dict(status='PASS',connector_id='fake-api',platform='test-api',resource=resource,
                    platform_id=platform_id,data=data,source_fingerprint=fingerprint,
                    read_at=read_at.isoformat())


class PlatformReadTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.api_counter=0
        self.now=datetime.now(timezone.utc)
        self.identity=dict(client_scope='synthetic',platform='mock',account_id='acct1',store_id='store1')
        self.binding=dict(**self.identity,connector_id='mock-platform')
        self.journal=Journal(Path(self.temp.name)/'mock.sqlite'); self.addCleanup(self.journal.close)
        self.journal.create('run1','synthetic',VERSION,'platform-read-test')
        self.connector=CountingMock(self.now)
        self.gateway=PlatformReadGateway(self.journal,self.connector,self.binding,clock=lambda:self.now)
        self.request=dict(request_id='req1',run_id='run1',team_version=VERSION,resource='campaign',
                          platform_id='cmp-001',acceptance_mode='synthetic',**self.identity)
        self.credential=dict(**self.identity,credential_id='CRsynthetic',provider='test',
                             secret_ref='vault://never-output',scope=['campaign.get'],status='active',
                             expires_at=(self.now+timedelta(hours=1)).isoformat())

    def test_mock_read_is_explicitly_synthetic_and_schema_valid(self):
        result=self.gateway.read(self.request,self.credential)
        self.assertTrue(result['simulated'])
        self.assertFalse(result['platform_connection_verified'])
        self.assertFalse(result['formal_acceptance_completed'])
        self.assertFalse(result['write_attempted'])
        self.assertEqual(result['data_sha256'],digest(result['data']))
        self.assertNotIn('vault://',encoded(result))
        self.assertEqual([result],self.journal.status('run1','synthetic')['platform_reads'])
        from jsonschema import Draft202012Validator
        root=Path(__file__).resolve().parents[1]
        schema=json.loads((root/'schemas'/'platform-read-observation.schema.json').read_text(encoding='utf-8'))
        self.assertEqual([],list(Draft202012Validator(schema).iter_errors(result)))

    def test_same_request_replays_without_another_connector_call(self):
        first=self.gateway.read(self.request,self.credential)
        self.assertEqual(first,self.gateway.read(self.request,self.credential))
        self.assertEqual(1,self.connector.reads)
        changed=copy.deepcopy(self.request); changed['platform_id']='different'
        with self.assertRaisesRegex(ValueError,'request_id_conflict'):
            self.gateway.read(changed,self.credential)
        self.assertEqual(1,self.connector.reads)

    def test_mock_cannot_claim_live_acceptance(self):
        self.request['acceptance_mode']='live'
        with self.assertRaisesRegex(ValueError,'live_mode_requires_api'):
            self.gateway.read(self.request,self.credential)
        self.assertEqual(0,self.connector.reads)

    def test_scope_expiry_and_plaintext_credential_fail_before_read(self):
        cases=[]
        wrong=copy.deepcopy(self.credential); wrong['store_id']='other'; cases.append(wrong)
        expired=copy.deepcopy(self.credential); expired['expires_at']=(self.now-timedelta(seconds=1)).isoformat(); cases.append(expired)
        unscoped=copy.deepcopy(self.credential); unscoped['scope']=[]; cases.append(unscoped)
        plaintext=copy.deepcopy(self.credential); plaintext['access_token']='do-not-log'; cases.append(plaintext)
        for credential in cases:
            with self.subTest(credential=list(credential)),self.assertRaises(ValueError):
                self.gateway.read(self.request,credential)
        self.assertEqual(0,self.connector.reads)

    def test_request_cannot_carry_credential_material(self):
        self.request['secret_ref']='vault://forbidden-in-request'
        with self.assertRaisesRegex(ValueError,'request_invalid'):
            self.gateway.read(self.request,self.credential)
        self.assertEqual(0,self.connector.reads)

    def _api(self):
        self.api_counter += 1
        connector=FakeApiConnector(self.now)
        binding=dict(client_scope='synthetic',platform='test-api',account_id='acct1',
                     store_id='store1',connector_id='fake-api')
        root=Path(self.temp.name)/('execution-store-'+str(self.api_counter))
        store=ExecutionStore.create(root,[binding]); self.addCleanup(store.close)
        store.bind_run('api-run',binding,VERSION,'platform-read-test')
        request=dict(request_id='api-req',run_id='api-run',team_version=VERSION,resource='campaign',
                     platform_id='cmp-live',acceptance_mode='live',
                     client_scope='synthetic',platform='test-api',account_id='acct1',store_id='store1')
        credential=dict(client_scope='synthetic',platform='test-api',account_id='acct1',store_id='store1',
                        credential_id='CRapi',provider='test',secret_ref='vault://api-ref',
                        scope=['campaign.get'],status='active',expires_at=(self.now+timedelta(hours=1)).isoformat())
        return connector,store.read_gateway(connector,binding,clock=lambda:self.now),request,credential

    def test_api_read_requires_authoritative_store_and_stays_nonfinal(self):
        connector,gateway,request,credential=self._api()
        result=gateway.read(request,credential)
        self.assertFalse(result['simulated'])
        self.assertTrue(result['platform_connection_verified'])
        self.assertFalse(result['independently_authenticated'])
        self.assertFalse(result['formal_acceptance_completed'])
        self.assertEqual('native_platform_api_observation',result['evidence_kind'])
        with self.assertRaisesRegex(ValueError,'authoritative_store_required'):
            PlatformReadGateway(gateway.journal,connector,gateway.binding,clock=lambda:self.now).read(
                dict(request,request_id='without-store'),credential)

    def test_stale_or_fingerprint_mismatch_api_response_is_blocked(self):
        for failure,reason in (('stale','not_current'),('fingerprint','fingerprint_invalid')):
            with self.subTest(failure=failure):
                connector,gateway,request,credential=self._api()
                connector.failure=failure; request['request_id']+='-'+failure
                with self.assertRaisesRegex(ValueError,reason): gateway.read(request,credential)

    def test_journal_rejects_tampered_read_data(self):
        result=self.gateway.read(self.request,self.credential)
        tampered=copy.deepcopy(result); tampered['request_id']='req2'; tampered['read_id']='read-'+'0'*32
        tampered['data']['budget']=9999
        with self.assertRaisesRegex(ValueError,'data_fingerprint_invalid'):
            self.journal.append('run1','synthetic','platform-read:req2','platform_read_observed',tampered)


if __name__=='__main__': unittest.main()
