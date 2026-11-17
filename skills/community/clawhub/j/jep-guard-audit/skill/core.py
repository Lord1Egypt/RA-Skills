"""Authenticated, tenant-scoped audit storage. Security profile v1; see SECURITY.md."""
import hashlib
import json
import os
import sqlite3
import threading
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4
from .types import FriendlyEvent, AuditChain, AuditChainLink, ComplianceStandard, ComplianceReport, Verb
from .adapter import JEPAdapter
from .codec import JEPCodec
from .security import canonical, plain, verify_event
from .capacity import capacity_policy

class AuditEngine:
    def __init__(self, database=None, trusted_keys=None, *, tenant_quotas=None):
        self.keys=trusted_keys
        self.lock=threading.RLock()
        self._tenant_quotas,self._capacity_policy=capacity_policy(tenant_quotas)
        database=database or os.environ.get('JEP_AUDIT_DB',str(Path.home()/'.jep-audit/events.sqlite3'))
        if database != ':memory:':
            path=Path(database).expanduser().absolute()
            path.parent.mkdir(mode=0o700,parents=True,exist_ok=True)
            if path.is_symlink() or path.parent.is_symlink(): raise ValueError('Symlink database paths are not allowed')
            if path.parent.stat().st_mode & 0o077: raise ValueError('Database directory must be private (0700)')
            fd=os.open(path,os.O_CREAT|os.O_RDWR|os.O_NOFOLLOW,0o600)
            os.close(fd)
            if path.stat().st_mode & 0o077: raise ValueError('Database must be private (0600)')
            database=str(path)
        self.db=sqlite3.connect(database,check_same_thread=False)
        self.db.execute('CREATE TABLE IF NOT EXISTS events (seq INTEGER PRIMARY KEY, tenant TEXT, session TEXT, issuer TEXT, nonce TEXT, body TEXT, digest TEXT, UNIQUE(tenant,issuer,nonce))')
        self.db.execute('CREATE INDEX IF NOT EXISTS session_index ON events(tenant,session,seq)')
        try:
            self._initialize_capacity_policy()
        except Exception:
            self.db.close()
            raise

    def _initialize_capacity_policy(self):
        with self.db:
            self.db.execute('BEGIN IMMEDIATE')
            self.db.execute('CREATE TABLE IF NOT EXISTS audit_capacity_policy (id INTEGER PRIMARY KEY CHECK(id=1), policy TEXT NOT NULL)')
            saved=self.db.execute('SELECT policy FROM audit_capacity_policy WHERE id=1').fetchone()
            if saved is not None and saved[0]!=self._capacity_policy:
                raise ValueError('Storage quota policy differs from this database; use a reviewed offline migration')
            usage=self.db.execute('SELECT tenant,COUNT(*),SUM(LENGTH(CAST(body AS BLOB))) FROM events GROUP BY tenant')
            for tenant,count,size in usage:
                limits=self._tenant_quotas.get(tenant)
                if limits is None or count>limits['max_events'] or size>limits['max_bytes']:
                    raise ValueError('Existing audit data exceeds or lacks a tenant reservation; preserve data and migrate offline')
            if saved is None:
                self.db.execute('INSERT INTO audit_capacity_policy(id,policy) VALUES(1,?)',(self._capacity_policy,))

    def _reserved_capacity(self,tenant,batch_size):
        limits=self._tenant_quotas.get(tenant)
        if limits is None:
            raise ValueError('No storage reservation configured for this tenant')
        saved=self.db.execute('SELECT policy FROM audit_capacity_policy WHERE id=1').fetchone()
        if saved is None or saved[0]!=self._capacity_policy:
            raise ValueError('Storage quota policy changed; restart with the operator-approved policy')
        count,size=self.db.execute('SELECT COUNT(*),COALESCE(SUM(LENGTH(CAST(body AS BLOB))),0) FROM events WHERE tenant=?',(tenant,)).fetchone()
        if count+batch_size>limits['max_events']:
            raise OverflowError('Tenant event capacity')
        return limits['max_bytes']-size

    def _rows(self,session_id,tenant):
        return self.db.execute('SELECT body,digest FROM events WHERE tenant=? AND session=? ORDER BY seq LIMIT 1001',(tenant,session_id)).fetchall()

    def ingest(self,session_id,friendly,tenant='local'):
        self.ingest_batch(session_id,[friendly],tenant)

    def ingest_batch(self,session_id,friendlies,tenant='local'):
        if not isinstance(session_id,str) or not 1<=len(session_id)<=128: raise ValueError('Invalid session ID')
        if not isinstance(tenant,str) or not 1<=len(tenant)<=128: raise ValueError('Invalid tenant')
        if not 1<=len(friendlies)<=128: raise ValueError('Batch size must be 1 to 128')
        context={'purpose':'audit','tenant':tenant,'session':session_id}
        with self.lock, self.db:
            # BEGIN IMMEDIATE makes quota/replay checks atomic across worker processes too.
            self.db.execute('BEGIN IMMEDIATE')
            rows=self._rows(session_id,tenant)
            if len(rows)+len(friendlies)>1000: raise OverflowError('Session capacity')
            remaining_bytes=self._reserved_capacity(tenant,len(friendlies))
            seen={json.loads(b)['event_id'] for b,_ in rows}
            for friendly in friendlies:
                body=plain(friendly)
                evt=JEPAdapter.to_jep04(friendly)
                if evt.nonce in seen: raise ValueError('Duplicate event ID')
                if not verify_event(body,context,self.keys): raise ValueError('Untrusted or invalid signature')
                if not JEPCodec.verify_timestamp_window(evt.when): raise ValueError('Timestamp outside acceptance window')
                encoded=JEPCodec.encode(evt)
                digest=hashlib.sha256(encoded.encode()).hexdigest()
                stored=canonical(body)
                remaining_bytes-=len(stored)
                if remaining_bytes<0: raise OverflowError('Tenant byte capacity')
                try:
                    self.db.execute('INSERT INTO events(tenant,session,issuer,nonce,body,digest) VALUES(?,?,?,?,?,?)',
                        (tenant,session_id,evt.who,evt.nonce,stored.decode(),digest))
                except sqlite3.IntegrityError as exc: raise ValueError('Replayed event') from exc
                seen.add(evt.nonce)

    def build_chain(self,session_id,tenant='local'):
        with self.lock: rows=self._rows(session_id,tenant)
        context={'purpose':'audit','tenant':tenant,'session':session_id}
        records=[(FriendlyEvent(**json.loads(b)),digest) for b,digest in rows]
        events=[JEPAdapter.to_jep04(f) for f,_ in records]
        index={}; hashes={}; links=[]; violations=0; warnings=0
        signatures=[verify_event(f,context,self.keys) for f,_ in records]
        for i,((friendly,stored_hash),evt) in enumerate(zip(records,events)):
            digest=hashlib.sha256(JEPCodec.encode(evt).encode()).hexdigest()
            findings=[]
            hash_valid=digest==stored_hash
            sig_valid=signatures[i]
            if not hash_valid: findings.append('[critical] Stored event digest mismatch')
            if not sig_valid: findings.append('[critical] Signature or trusted key mismatch')
            # References must resolve to earlier records, never future/self references.
            refs=list(friendly.verify_of or [])
            if friendly.terminate_of: refs.append(friendly.terminate_of)
            if friendly.prev_event_id: refs.append(friendly.prev_event_id)
            if evt.verb!=Verb.JUDGE and not refs: findings.append('[violation] Missing predecessor reference')
            if len(refs)!=len(set(refs)) and len(friendly.verify_of or [])!=len(set(friendly.verify_of or [])):
                findings.append('[violation] Duplicate verification reference')
            if any(ref not in index or index[ref].when>evt.when for ref in refs): findings.append('[critical] Dangling, future, or self reference')
            if evt.task_based_on and evt.task_based_on not in hashes: findings.append('[violation] Unknown prior parent digest')
            if evt.verb==Verb.VERIFY:
                if friendly.verification_result not in ("confirmed","rejected","partial"): findings.append("[violation] Missing or invalid verification result")
                if not friendly.verify_of or any(r not in index or index[r].verb!=Verb.JUDGE or index[r].aud!=evt.aud for r in friendly.verify_of):
                    findings.append('[violation] Verification must refer to prior judgments for the same target')
            if evt.verb in (Verb.TERMINATE,Verb.DELEGATE):
                ref=friendly.terminate_of if evt.verb==Verb.TERMINATE else friendly.prev_event_id
                parent=index.get(ref)
                if parent is None or parent.verb!=Verb.JUDGE or parent.who!=evt.who or parent.aud!=evt.aud:
                    findings.append('[violation] Issuer lacks authority over the referenced judgment')
            chain_ok=not findings
            if evt.verb==Verb.JUDGE:
                later=any(signatures[j] and events[j].verb==Verb.VERIFY and evt.nonce in (records[j][0].verify_of or []) and events[j].when>=evt.when and events[j].aud==evt.aud for j in range(i+1,len(events)))
                if not later:
                    findings.append('[warning] R001: Judgment has no subsequent signed verification')
                    warnings+=1
            violations+=sum(not f.startswith('[warning]') for f in findings)
            links.append(AuditChainLink(evt,digest,hash_valid,sig_valid,chain_ok,findings))
            index[evt.nonce]=evt
            hashes['sha256:'+digest]=evt
        return AuditChain(session_id,links,bool(links) and violations==0,violations,warnings,
            min((datetime.fromtimestamp(e.when,timezone.utc) for e in events),default=None),
            max((datetime.fromtimestamp(e.when,timezone.utc) for e in events),default=None))

    def export_compliance(self,session_id,standard=ComplianceStandard.GENERIC,tenant='local'):
        chain=self.build_chain(session_id,tenant)
        findings=[{'event_nonce':l.event.nonce,'finding':v} for l in chain.links for v in l.violations]
        summary={'total_events':len(chain.links),'chain_valid':chain.chain_valid,'violation_count':chain.violation_count,'warning_count':chain.warning_count}
        raw=canonical({'profile':'jep-audit-security-v1','session_id':session_id,'summary':summary,'findings':findings}).decode()
        return ComplianceReport(report_id=str(uuid4()),standard=standard,session_id=session_id,generated_at=datetime.now(timezone.utc),chain_summary=summary,findings=findings,
            recommendations=['Technical evidence only. Regulatory labels are legacy export categories, not legal compliance certification.','Anchor exported digests externally if deletion/truncation detection is required.'],export_format='json',raw_data=raw)
