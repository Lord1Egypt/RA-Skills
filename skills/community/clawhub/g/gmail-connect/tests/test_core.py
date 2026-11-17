import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import threading
import time
import unittest
from unittest.mock import patch
import urllib.error
import urllib.request

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from gmail_connect.core import Gmail,Store,Problem,READ,SEND,valid_id
from gmail_connect.server import Wizard

class CoreTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.s=Store(self.tmp.name);self.g=Gmail(self.s)
 def tearDown(self):self.tmp.cleanup()
 def connect_stub(self):
  self.s.write('tokens.json',{'email':'a@example.com','scope':READ+' '+SEND,'access_token':'test','refresh_token':'test','expires_at':time.time()+999})
 def test_permissions(self):
  self.s.write('tokens.json',{'fake':True})
  self.assertEqual((self.s.root.stat().st_mode & 0o777),0o700)
  self.assertEqual(((self.s.root/'tokens.json').stat().st_mode & 0o777),0o600)
 def test_reject_web_oauth(self):
  with self.assertRaises(Problem):self.g.import_client({'web':{'client_id':'abc'}})
 def test_ignore_uploaded_endpoints(self):
  self.g.import_client({'installed':{'client_id':'abc.apps.googleusercontent.com','client_secret':'secret','token_uri':'https://evil.test'}})
  self.assertNotIn('token_uri',self.s.read('client.json'))
 def test_pkce_and_state(self):
  self.g.import_client({'installed':{'client_id':'abc.apps.googleusercontent.com','client_secret':'secret'}})
  url,pending=self.g.begin('http://127.0.0.1:8766/oauth/callback')
  self.assertIn('code_challenge_method=S256',url)
  with self.assertRaises(Problem):self.g.finish(pending,'code','wrong')
  pending['created']=time.time()-601
  with self.assertRaises(Problem):self.g.finish(pending,'code',pending['state'])
 def test_path_injection(self):
  for value in ('../profile','a?format=raw','',None):
   with self.assertRaises(Problem):valid_id(value)
 def test_headers_injection(self):
  self.connect_stub()
  with self.assertRaises(Problem):self.g.draft('a@example.com','x\nBcc: bad@example.com','body')
 def test_sync_pagination_cursor_and_dedup(self):
  self.s.put('cursor','10')
  pages=[{'history':[{'messagesAdded':[{'message':{'id':'a'}}]}],'nextPageToken':'next','historyId':'20'},
         {'history':[{'messagesAdded':[{'message':{'id':'a'}},{'message':{'id':'b'}}]}],'historyId':'30'}]
  with patch.object(self.g,'api',side_effect=pages) as api, patch.object(self.g,'message',side_effect=lambda mid:{'id':mid,'labels':['INBOX']}):
   self.g.sync()
  self.assertEqual(self.s.get('cursor'),'30');self.assertEqual(len(self.g.events()['events']),2)
  self.assertEqual(api.call_args_list[1].args[1]['pageToken'],'next')
 def test_failed_fetch_preserves_cursor(self):
  self.s.put('cursor','10')
  with patch.object(self.g,'api',return_value={'history':[{'messagesAdded':[{'message':{'id':'a'}}]}],'historyId':'20'}),patch.object(self.g,'message',side_effect=Problem('offline',503)):
   with self.assertRaises(Problem):self.g.sync()
  self.assertEqual(self.s.get('cursor'),'10')
 def test_history_404_recovery(self):
  self.s.put('cursor','old')
  with patch.object(self.g,'api',side_effect=[Problem('expired',404),{'historyId':'new'},{'messages':[{'id':'a'}]}]),patch.object(self.g,'message',return_value={'id':'a','labels':['INBOX']}):
   result=self.g.sync()
  self.assertTrue(result['historyGap']);self.assertEqual(self.s.get('cursor'),'new')
  self.assertEqual(self.g.events()['events'][0]['kind'],'snapshot')
 def test_sync_not_advance_on_403(self):
  self.s.put('cursor','10')
  with patch.object(self.g,'api',side_effect=Problem('no',403)):
   with self.assertRaises(Problem):self.g.sync()
  self.assertEqual(self.s.get('cursor'),'10')
 def test_draft_send_only_once(self):
  self.connect_stub();d=self.g.draft('b@example.com','Test','Body')
  with patch.object(self.g,'api',return_value={'id':'sent'}) as api:
   self.g.send_approved(d['id'])
   with self.assertRaises(Problem):self.g.send_approved(d['id'])
  self.assertEqual(api.call_count,1)
 def test_uncertain_send_never_retried(self):
  self.connect_stub();d=self.g.draft('b@example.com','Test','Body')
  with patch.object(self.g,'api',side_effect=Problem('timeout',503)) as api:
   with self.assertRaises(Problem):self.g.send_approved(d['id'])
   with self.assertRaises(Problem):self.g.send_approved(d['id'])
  self.assertEqual(api.call_count,1);self.assertEqual(self.g.drafts()[0]['status'],'unknown-check-sent')
 def test_disconnect_clears_state(self):
  self.connect_stub();self.g.draft('b@example.com','Test','Body');self.s.put('cursor','1')
  self.g.disconnect()
  self.assertFalse(self.g.status()['connected']);self.assertEqual(self.g.drafts(),[]);self.assertIsNone(self.s.get('cursor'))
 def test_tokens_not_in_status(self):
  self.connect_stub();out=json.dumps(self.g.status());self.assertNotIn('access_token',out);self.assertNotIn('refresh_token',out)
 def test_refresh(self):
  self.connect_stub();t=self.s.read('tokens.json');t['expires_at']=0;self.s.write('tokens.json',t)
  self.s.write('client.json',{'client_id':'test','client_secret':'test'})
  with patch('gmail_connect.core.request',return_value={'access_token':'new','expires_in':3600}):self.assertEqual(self.g.token(),'new')
  self.assertEqual(self.s.read('tokens.json')['refresh_token'],'test')

class HTTPTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.server=Wizard(Gmail(Store(self.tmp.name)),0)
  self.thread=threading.Thread(target=self.server.serve_forever,daemon=True);self.thread.start()
 def tearDown(self):self.server.shutdown();self.server.server_close();self.thread.join();self.tmp.cleanup()
 def call(self,path,headers=None,data=None):
  req=urllib.request.Request(self.server.origin+path,headers=headers or {},data=data)
  return urllib.request.urlopen(req,timeout=3)
 def test_requires_capability(self):
  with self.assertRaises(urllib.error.HTTPError) as c:self.call('/api/status')
  self.assertEqual(c.exception.code,401)
 def test_rebinding_host_rejected(self):
  with self.assertRaises(urllib.error.HTTPError) as c:self.call('/',{'Host':'attacker.test'})
  self.assertEqual(c.exception.code,403)
 def test_cross_site_post_rejected(self):
  with self.assertRaises(urllib.error.HTTPError) as c:self.call('/api/drafts',{'Authorization':'Bearer '+self.server.key,'Origin':'https://evil.test','Content-Type':'application/json'},b'{}')
  self.assertEqual(c.exception.code,403)
 def test_authorized_post(self):
  with self.call('/api/drafts',{'Authorization':'Bearer '+self.server.key,'Origin':self.server.origin,'Content-Type':'application/json'},b'{}') as r:self.assertEqual(json.load(r),[])
 def test_static_security_headers(self):
  with self.call('/') as r:
   self.assertIn("frame-ancestors 'none'",r.headers['Content-Security-Policy']);self.assertEqual(r.headers['Referrer-Policy'],'no-referrer')
  with self.call('/guide.css') as r:
   self.assertEqual(r.headers['Content-Type'],'text/css');self.assertIn(b'details.guide',r.read())
 def test_callback_wrong_state_not_consumed(self):
  self.server.pending={'state':'right'}
  with self.assertRaises(urllib.error.HTTPError):self.call('/oauth/callback?state=wrong&code=secret')
  self.assertIsNotNone(self.server.pending)
 def test_status_redacted(self):
  with self.call('/api/status',{'Authorization':'Bearer '+self.server.key}) as r:
   result=json.load(r);self.assertFalse(result['connected']);self.assertFalse(result['gatewayChanged'])

class RegressionTests(unittest.TestCase):
 def test_unrelated_label_is_not_arrival(self):
  with tempfile.TemporaryDirectory() as root:
   g=Gmail(Store(root));g.s.put('cursor','10')
   changes={'history':[{'labelsAdded':[{'message':{'id':'old'},'labelIds':['STARRED']}]}],'historyId':'11'}
   with patch.object(g,'api',return_value=changes),patch.object(g,'message') as message:g.sync()
   self.assertFalse(message.called);self.assertEqual(g.events()['events'],[]);self.assertEqual(g.s.get('cursor'),'11')
 def test_inbox_label_is_relevant(self):
  with tempfile.TemporaryDirectory() as root:
   g=Gmail(Store(root));g.s.put('cursor','10')
   changes={'history':[{'labelsAdded':[{'message':{'id':'old'},'labelIds':['INBOX']}]}],'historyId':'11'}
   with patch.object(g,'api',return_value=changes),patch.object(g,'message',return_value={'id':'old','labels':['INBOX']}):g.sync()
   self.assertEqual(len(g.events()['events']),1)
 def test_service_rollback_stops_and_disables_new_unit(self):
  from gmail_connect import service
  with tempfile.TemporaryDirectory() as home:
   store=Store(Path(home)/'state');calls=[]
   with patch('gmail_connect.service.Path.home',return_value=Path(home)),patch('gmail_connect.service.os.geteuid',return_value=1000),patch.object(service,'status',side_effect=[{'active':False},{'active':False}]),patch.object(service,'enabled_state',return_value='not-found'),patch.object(service,'run',side_effect=lambda args:calls.append(args)):
    with self.assertRaises(Problem):service.install(store)
   self.assertIn(['systemctl','--user','stop',service.UNIT],calls)
   self.assertIn(['systemctl','--user','disable',service.UNIT],calls)
   self.assertFalse((Path(home)/'.config/systemd/user'/service.UNIT).exists())
 def test_service_rollback_restores_existing_unit_and_state(self):
  from gmail_connect import service
  with tempfile.TemporaryDirectory() as home:
   store=Store(Path(home)/'state');unit=Path(home)/'.config/systemd/user'/service.UNIT;unit.parent.mkdir(parents=True)
   original='# Managed by gmail-connect; old unit\n';unit.write_text(original);calls=[]
   with patch('gmail_connect.service.Path.home',return_value=Path(home)),patch('gmail_connect.service.os.geteuid',return_value=1000),patch.object(service,'status',side_effect=[{'active':True},{'active':False}]),patch.object(service,'enabled_state',return_value='enabled'),patch.object(service,'run',side_effect=lambda args:calls.append(args)):
    with self.assertRaises(Problem):service.install(store)
   self.assertEqual(unit.read_text(),original)
   self.assertIn(['systemctl','--user','enable',service.UNIT],calls)
   self.assertEqual(calls[-1],['systemctl','--user','start',service.UNIT])
 def test_oauth_finish_and_replay_account_reset(self):
  with tempfile.TemporaryDirectory() as root:
   g=Gmail(Store(root));g.import_client({'installed':{'client_id':'abc.apps.googleusercontent.com','client_secret':'x'}})
   g.s.write('tokens.json',{'email':'old@example.com'});g.s.put('cursor','old');g.draft('b@example.com','Old','Body')
   _,pending=g.begin('http://127.0.0.1:8766/oauth/callback')
   with patch('gmail_connect.core.request',side_effect=[{'access_token':'access','refresh_token':'refresh','scope':READ,'expires_in':3600},{'emailAddress':'new@example.com'}]):g.finish(pending,'code',pending['state'])
   self.assertEqual(g.status()['email'],'new@example.com');self.assertIsNone(g.s.get('cursor'));self.assertEqual(g.drafts(),[])

if __name__=='__main__':unittest.main()
