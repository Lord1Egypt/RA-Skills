import datetime as dt,io,json,os,subprocess,tempfile,unittest,zipfile,uuid,sys
from pathlib import Path
from unittest.mock import patch,MagicMock
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from core import *
import email_desk as mail

class Base(unittest.TestCase):
    def setUp(self):
        self.root=Path(os.environ.get('MOCHI_TEST_TEMP',tempfile.gettempdir()))/('case-'+uuid.uuid4().hex); self.root.mkdir(); self.st=Store(self.root,'test')
    def tearDown(self): self.st.db.close()
    def file(self,name,data):
        p=self.root/name; p.parent.mkdir(parents=True,exist_ok=True); p.write_bytes(data if isinstance(data,bytes) else data.encode()); return p

class EmailTests(Base):
    def config(self): return {'account':'demo','username':'demo@example.com','incoming':{'protocol':'imap','host':'imap.example.com','port':993,'security':'ssl'},'smtp':{'host':'smtp.example.com','port':465,'security':'ssl'},'passwordEnv':'MOCHI_TEST_PASS'}
    def msg(self,subject='你好',body='测试邮件'):
        m=mail.EmailMessage(); m['From']='sender@example.com'; m['To']='demo@example.com'; m['Subject']=subject; m.set_content(body); return m.as_bytes()
    def test_mime_roundtrip(self):
        m=mail.EmailMessage(); m['Subject']='每月账单'; m.set_content('正文'); m.add_attachment(b'abc',maintype='application',subtype='octet-stream',filename='中文.txt'); p=mail.parsed(m.as_bytes()); self.assertEqual(p['subject'],'每月账单'); self.assertEqual(p['attachments'][0]['sha256'],digest(b'abc')); self.assertIn('正文',p['text'])
    def test_html_drops_script(self):
        m=mail.EmailMessage(); m.set_content('<p>Hello</p><script>unsafe()</script>',subtype='html'); self.assertNotIn('unsafe',mail.parsed(m.as_bytes())['text'])
    def test_header_injection(self):
        with self.assertRaises(ValueError): mail.addresses(['a@example.com\r\nBcc:b@example.com'])
    def test_draft_bcc_private(self):
        d=mail.draft(self.st,{'draftId':'one','to':['to@example.com'],'bcc':['private@example.com'],'subject':'Hi','body':'Text'},self.config()); b=(self.st.home/'drafts/one.eml').read_bytes(); self.assertNotIn(b'Bcc:',b); self.assertIn('private@example.com',d['recipients'])
    def test_send_once(self):
        c=self.config(); d=mail.draft(self.st,{'draftId':'one','to':['to@example.com'],'body':'Hi'},c); s=MagicMock(); s.sendmail.return_value={}
        with patch.object(mail,'connect',return_value=s):
            a=mail.send(self.st,{'draftId':'one','sha256':d['sha256']},c); b=mail.send(self.st,{'draftId':'one','sha256':d['sha256']},c)
        self.assertEqual(s.sendmail.call_count,1); self.assertEqual(a['state'],'sent'); self.assertEqual(b['state'],'sent')
    def test_ambiguous_not_resent(self):
        c=self.config(); d=mail.draft(self.st,{'draftId':'one','to':['to@example.com']},c); s=MagicMock(); s.sendmail.side_effect=TimeoutError()
        with patch.object(mail,'connect',return_value=s):
            with self.assertRaises(TimeoutError): mail.send(self.st,{'draftId':'one','sha256':d['sha256']},c)
            with self.assertRaises(ValueError): mail.send(self.st,{'draftId':'one','sha256':d['sha256']},c)
        self.assertEqual(s.sendmail.call_count,1)
    def test_draft_tamper(self):
        c=self.config(); d=mail.draft(self.st,{'draftId':'one','to':['to@example.com']},c); (self.st.home/'drafts/one.eml').write_bytes(b'changed')
        with self.assertRaises(ValueError): mail.send(self.st,{'draftId':'one','sha256':d['sha256']},c)
    def test_imap_baseline_incremental_ack(self):
        c=self.config(); s=MagicMock(); s.select.return_value=('OK',[]); s.response.return_value=('UIDVALIDITY',[b'10']); ids=['1','2']
        def uid(cmd,*args):
            if cmd=='search': return 'OK',[' '.join(ids).encode()]
            if args[1]=='(RFC822.SIZE)': return 'OK',[b'1 (RFC822.SIZE 1000)']
            return 'OK',[(b'1 BODY',self.msg('Message '+args[0]))]
        s.uid.side_effect=uid
        with patch.object(mail,'connect',return_value=s):
            a=mail.sync(self.st,{'limit':1},c); self.assertTrue(a['baselineCreated']); self.assertEqual(len(self.st.pending()),0)
            ids.extend(['3','4']); b=mail.sync(self.st,{'limit':1},c); self.assertEqual(b['remaining'],1); self.assertEqual(len(self.st.pending()),1)
            mail.sync(self.st,{'limit':1},c); mail.sync(self.st,{'limit':1},c); self.assertEqual(len(self.st.pending()),2)
            self.st.ack([x['noticeId'] for x in self.st.pending()]); mail.sync(self.st,{},c); self.assertEqual(self.st.pending(),[])
    def test_uidvalidity_reset_baselines(self):
        self.st.put('cursor','demo|INBOX|imap',{'valid':'old','seen':['1']}); s=MagicMock(); s.select.return_value=('OK',[]); s.response.return_value=('UIDVALIDITY',[b'new']); s.uid.side_effect=[('OK',[b'']),];
        with patch.object(mail,'connect',return_value=s): result=mail.sync(self.st,{},self.config())
        self.assertTrue(result['baselineCreated']); self.assertEqual(self.st.pending(),[])
    def test_pop_uidl_incremental(self):
        c=self.config(); c['incoming']['protocol']='pop3'; s=MagicMock(); s.uidl.return_value=(b'OK',[b'1 unique1'],1); s.list.return_value=b'+OK 1 100'; s.retr.return_value=(b'OK',self.msg().split(b'\n'),100)
        with patch.object(mail,'connect',return_value=s):
            mail.sync(self.st,{},c); s.uidl.return_value=(b'OK',[b'1 unique1',b'2 unique2'],2); mail.sync(self.st,{},c)
        self.assertEqual(len(self.st.pending()),1); self.assertFalse(s.dele.called)
    def test_attachment_traversal(self):
        m=mail.EmailMessage(); m.set_content('text'); m.add_attachment(b'abc',maintype='text',subtype='plain',filename='../bad.txt'); data=mail.ingest(self.st,self.config(),'INBOX','1','1',m.as_bytes(),False)
        with self.assertRaises(ValueError): mail.handle(self.st,{'action':'attachments','messageId':data['id']})
    def test_cache_search(self):
        mail.ingest(self.st,self.config(),'INBOX','1','1',self.msg(),False); r=mail.handle(self.st,{'action':'search','query':'测试'}); self.assertEqual(len(r['messages']),1)
    def test_imap_starttls_auth_adapter(self):
        c=self.config(); c['incoming']['security']='starttls'; s=MagicMock(); s.capabilities=()
        with patch.dict(os.environ,{'MOCHI_TEST_PASS':'fixture-only'}),patch.object(mail.imaplib,'IMAP4',return_value=s) as factory:
            result=mail.connect(c,'incoming')
        self.assertIs(result,s); self.assertTrue(s.starttls.called); s.login.assert_called_once_with('demo@example.com','fixture-only'); self.assertEqual(factory.call_args.kwargs['timeout'],25)
    def test_smtp_starttls_auth_adapter(self):
        c=self.config(); c['smtp']['security']='starttls'; s=MagicMock()
        with patch.dict(os.environ,{'MOCHI_TEST_PASS':'fixture-only'}),patch.object(mail.smtplib,'SMTP',return_value=s): mail.connect(c,'smtp')
        self.assertTrue(s.starttls.called); self.assertEqual(s.ehlo.call_count,2); self.assertTrue(s.login.called)
    def test_pop_starttls_auth_adapter(self):
        c=self.config(); c['incoming'].update(protocol='pop3',security='starttls'); s=MagicMock()
        with patch.dict(os.environ,{'MOCHI_TEST_PASS':'fixture-only'}),patch.object(mail.poplib,'POP3',return_value=s): mail.connect(c,'incoming')
        self.assertTrue(s.stls.called); s.user.assert_called_once_with('demo@example.com'); s.pass_.assert_called_once_with('fixture-only')
    def test_imap_xoauth_adapter(self):
        c=self.config(); c.update(auth='oauth2',accessTokenEnv='MOCHI_TEST_TOKEN'); s=MagicMock(); s.capabilities=()
        with patch.dict(os.environ,{'MOCHI_TEST_TOKEN':'fixture-token'}),patch.object(mail.imaplib,'IMAP4_SSL',return_value=s): mail.connect(c,'incoming')
        self.assertEqual(s.authenticate.call_args.args[0],'XOAUTH2'); self.assertIn(b'auth=Bearer fixture-token',s.authenticate.call_args.args[1](b''))
    def test_tls_cannot_be_disabled(self):
        p=self.file('profile.json',json.dumps({**self.config(),'incoming':{'host':'example.com','port':143,'security':'none'}})); os.chmod(p,0o600)
        with self.assertRaises(ValueError): mail.profile({'profile':str(p)})
    def test_wrong_draft_hash(self):
        c=self.config(); mail.draft(self.st,{'draftId':'one','to':['to@example.com']},c)
        with self.assertRaises(ValueError): mail.send(self.st,{'draftId':'one','sha256':'wrong'},c)
    def test_remote_search_uses_literal(self):
        c=self.config(); s=MagicMock(); s.select.return_value=('OK',[]); s.response.return_value=('UIDVALIDITY',[b'10']); s.uid.return_value=('OK',[b'5 8 12'])
        with patch.object(mail,'profile',return_value=c),patch.object(mail,'connect',return_value=s): out=mail.handle(self.st,{'action':'remote-search','query':'账单','limit':2})
        self.assertEqual(out['uids'],['8','12']); self.assertTrue(out['limited']); self.assertEqual(s.literal,'账单'.encode()); s.uid.assert_called_once_with('SEARCH','CHARSET','UTF-8','TEXT')
    def test_remote_fetch_checks_validity(self):
        c=self.config(); s=MagicMock(); s.select.return_value=('OK',[]); s.response.return_value=('UIDVALIDITY',[b'10'])
        with patch.object(mail,'profile',return_value=c),patch.object(mail,'connect',return_value=s):
            with self.assertRaises(ValueError): mail.handle(self.st,{'action':'fetch','uid':'3','uidValidity':'old'})
        self.assertFalse(s.uid.called)

if __name__=="__main__": unittest.main(verbosity=2)
