"""Pinned cross-run monitor policy store with history-only legacy import."""
from __future__ import annotations

import hashlib
import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path
import sqlite3
from uuid import uuid4

from run_journal import check_payload, digest, encoded


PROFILE='monitor-policy-store.json'
DATABASE='monitor-policies.sqlite'
METRICS={'structure_error_rate','handoff_rejection_rate','host_failure_rate',
         'human_correction_rate','disagreement_rate','latency_ms','cost'}


def require(condition,reason):
    if not condition: raise ValueError(reason)


def byte_hash(value): return hashlib.sha256(value).hexdigest()


def write_new(path,value):
    with Path(path).open('x',encoding='utf-8',newline='\n') as stream:
        stream.write(encoded(value)+'\n'); stream.flush(); os.fsync(stream.fileno())


def read_json(path):
    raw=Path(path).read_bytes()
    def pairs(items):
        value={}
        for key,item in items:
            require(key not in value,'monitor_policy_duplicate_json_key'); value[key]=item
        return value
    value=json.loads(raw.decode('utf-8-sig'),object_pairs_hook=pairs,
                     parse_constant=lambda x: (_ for _ in ()).throw(ValueError('monitor_policy_nonfinite_json')))
    check_payload(value); digest(value)
    require(isinstance(value,dict),'monitor_policy_json_invalid')
    return value,byte_hash(raw)


def timestamp(value):
    try:
        parsed=datetime.fromisoformat(str(value).replace('Z','+00:00'))
        require(parsed.tzinfo is not None,'monitor_policy_time_requires_timezone')
        return parsed.astimezone(timezone.utc)
    except (TypeError,ValueError) as exc: raise ValueError('monitor_policy_time_invalid') from exc


def validate_policy(policy):
    require(isinstance(policy,dict) and policy.get('schema_version')=='2.0' and
            all(isinstance(policy.get(k),str) and policy[k] for k in ('policy_id','revision')),
            'monitor_policy_identity_invalid')
    require(policy.get('automatic_model_override') is False,'monitor_policy_automatic_override_forbidden')
    for key in ('baseline_days','current_days','baseline_samples','current_samples'):
        require(type(policy.get(key)) is int and policy[key]>0,'monitor_policy_window_invalid')
    require(policy['baseline_days']>=14,'monitor_policy_baseline_too_short')
    thresholds=policy.get('thresholds')
    require(isinstance(thresholds,dict) and set(thresholds)==METRICS and
            all(type(v) in (int,float) and v>=0 for v in thresholds.values()),
            'monitor_policy_thresholds_invalid')
    calibration=policy.get('live_calibration')
    require(isinstance(calibration,dict) and calibration.get('manual_approval_required') is True and
            calibration.get('automatic_model_override') is False,
            'monitor_policy_calibration_boundary_invalid')
    return digest(policy)


class MonitorPolicyStore:
    @classmethod
    def create(cls,directory,client_scopes):
        require(isinstance(client_scopes,list) and client_scopes and len(client_scopes)==len(set(client_scopes)) and
                all(isinstance(x,str) and x.strip() for x in client_scopes),'monitor_policy_scopes_invalid')
        root=Path(directory).resolve(); root.mkdir(parents=False,exist_ok=False)
        profile=dict(schema_version='2.0',store_id=uuid4().hex,database=DATABASE,
                     client_scopes=sorted(client_scopes))
        write_new(root/PROFILE,profile)
        db=sqlite3.connect(root/DATABASE)
        try:
            db.executescript('''
              CREATE TABLE identity(singleton INTEGER PRIMARY KEY CHECK(singleton=1),store_id TEXT,root TEXT,profile_sha256 TEXT);
              CREATE TABLE policies(seq INTEGER PRIMARY KEY AUTOINCREMENT,client_scope TEXT,policy_id TEXT,revision TEXT,
                policy_sha256 TEXT,previous_sha256 TEXT,source_kind TEXT,current_authority INTEGER,
                source_sha256 TEXT,source_bytes BLOB,body TEXT,actor TEXT,source_reference TEXT,decided_at TEXT,
                UNIQUE(client_scope,policy_id,revision));
              CREATE TRIGGER identity_no_update BEFORE UPDATE ON identity BEGIN SELECT RAISE(ABORT,'immutable_identity'); END;
              CREATE TRIGGER identity_no_delete BEFORE DELETE ON identity BEGIN SELECT RAISE(ABORT,'immutable_identity'); END;
              CREATE TRIGGER policy_no_update BEFORE UPDATE ON policies BEGIN SELECT RAISE(ABORT,'immutable_policy'); END;
              CREATE TRIGGER policy_no_delete BEFORE DELETE ON policies BEGIN SELECT RAISE(ABORT,'immutable_policy'); END;
            ''')
            db.execute('INSERT INTO identity VALUES(1,?,?,?)',(profile['store_id'],str(root),byte_hash((root/PROFILE).read_bytes())))
            db.commit()
        finally: db.close()
        return cls.open(root/PROFILE)

    @classmethod
    def open(cls,profile_path):
        path=Path(profile_path).resolve(); require(path.name==PROFILE and path.is_file(),'monitor_policy_profile_missing')
        profile,fingerprint=read_json(path)
        require(set(profile)=={'schema_version','store_id','database','client_scopes'} and
                profile['schema_version']=='2.0' and profile['database']==DATABASE and
                isinstance(profile['client_scopes'],list) and profile['client_scopes'] and
                len(profile['client_scopes'])==len(set(profile['client_scopes'])) and
                all(isinstance(x,str) and x.strip() for x in profile['client_scopes']),
                'monitor_policy_profile_invalid')
        database=path.parent/DATABASE; require(database.is_file(),'monitor_policy_database_missing')
        instance=cls(); instance.profile_path=path; instance.profile=profile; instance.fingerprint=fingerprint
        instance.database=database; instance.file_identity=(database.stat().st_dev,database.stat().st_ino)
        instance.db=sqlite3.connect(database,timeout=20,isolation_level=None); instance.db.row_factory=sqlite3.Row
        try: instance.assert_store()
        except BaseException: instance.db.close(); raise
        return instance

    def close(self): self.db.close()

    def assert_store(self):
        profile,fingerprint=read_json(self.profile_path)
        require(profile==self.profile and fingerprint==self.fingerprint,'monitor_policy_profile_changed')
        require((self.database.stat().st_dev,self.database.stat().st_ino)==self.file_identity,
                'monitor_policy_database_replaced')
        row=self.db.execute('SELECT * FROM identity WHERE singleton=1').fetchone()
        require(row and row['store_id']==self.profile['store_id'] and Path(row['root']).resolve()==self.profile_path.parent and
                row['profile_sha256']==self.fingerprint,'monitor_policy_store_identity_mismatch')
        require(self.db.execute('PRAGMA integrity_check').fetchone()[0]=='ok','monitor_policy_store_integrity_failed')

    def _scope(self,client_scope):
        self.assert_store(); require(client_scope in self.profile['client_scopes'],'monitor_policy_client_scope_denied')

    def adopt(self,client_scope,policy,decision):
        self._scope(client_scope); policy_sha=validate_policy(policy)
        require(isinstance(decision,dict) and set(decision)=={'state','client_scope','policy_sha256','actor','source_reference','decided_at','previous_policy_sha256'} and
                decision['state']=='adopted' and decision['client_scope']==client_scope and
                decision['policy_sha256']==policy_sha and all(isinstance(decision[k],str) and decision[k].strip()
                for k in ('actor','source_reference','decided_at')),
                'monitor_policy_adoption_invalid')
        require(timestamp(decision['decided_at'])<=datetime.now(timezone.utc),'monitor_policy_decision_in_future')
        last=self.db.execute('SELECT * FROM policies WHERE client_scope=? AND policy_id=? AND current_authority=1 ORDER BY seq DESC LIMIT 1',
                             (client_scope,policy['policy_id'])).fetchone()
        expected=last['policy_sha256'] if last else None
        require(decision['previous_policy_sha256']==expected,'monitor_policy_previous_revision_mismatch')
        body=encoded(policy)
        try:
            self.db.execute('INSERT INTO policies(client_scope,policy_id,revision,policy_sha256,previous_sha256,source_kind,current_authority,source_sha256,source_bytes,body,actor,source_reference,decided_at) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)',
                (client_scope,policy['policy_id'],policy['revision'],policy_sha,expected,'native_v2',1,None,None,body,
                 decision['actor'],decision['source_reference'],decision['decided_at']))
        except sqlite3.IntegrityError as exc: raise ValueError('monitor_policy_revision_already_exists') from exc
        return self.reference(client_scope,policy['policy_id'],policy['revision'])

    def import_legacy(self,client_scope,path):
        self._scope(client_scope); source=Path(path).resolve(); require(source.is_file(),'monitor_policy_legacy_source_missing')
        raw=source.read_bytes(); policy,_=read_json(source)
        require(policy.get('schema_version')=='1.0' and policy.get('policy_id') and policy.get('revision'),
                'monitor_policy_legacy_identity_invalid')
        source_sha=byte_hash(raw); policy_sha=digest(policy)
        try:
            self.db.execute('INSERT INTO policies(client_scope,policy_id,revision,policy_sha256,previous_sha256,source_kind,current_authority,source_sha256,source_bytes,body,actor,source_reference,decided_at) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)',
                (client_scope,policy['policy_id'],policy['revision'],policy_sha,None,'legacy_v1',0,source_sha,raw,encoded(policy),
                 None,str(source),None))
        except sqlite3.IntegrityError as exc: raise ValueError('monitor_policy_revision_already_exists') from exc
        return self.reference(client_scope,policy['policy_id'],policy['revision'])

    def reference(self,client_scope,policy_id,revision):
        self._scope(client_scope)
        row=self.db.execute('SELECT * FROM policies WHERE client_scope=? AND policy_id=? AND revision=?',
                            (client_scope,policy_id,revision)).fetchone()
        require(row is not None,'monitor_policy_not_found')
        return dict(schema_version='2.0',store_id=self.profile['store_id'],profile_path=str(self.profile_path),
                    profile_sha256=self.fingerprint,client_scope=client_scope,policy_id=policy_id,revision=revision,
                    policy_sha256=row['policy_sha256'],source_kind=row['source_kind'],
                    current_authority=bool(row['current_authority']),legacy_permissions_inherited=False)

    def current(self,client_scope,policy_id):
        self._scope(client_scope)
        row=self.db.execute('SELECT * FROM policies WHERE client_scope=? AND policy_id=? AND current_authority=1 ORDER BY seq DESC LIMIT 1',
                            (client_scope,policy_id)).fetchone()
        require(row is not None,'monitor_policy_current_missing')
        policy=json.loads(row['body']); require(digest(policy)==row['policy_sha256'],'monitor_policy_body_changed')
        return policy,self.reference(client_scope,policy_id,row['revision'])

    def assert_current(self,client_scope,policy,reference):
        current,expected=self.current(client_scope,policy['policy_id'])
        require(current==policy and expected==reference,'monitor_policy_not_current')
        return expected

    def verify_legacy(self,client_scope,policy_id,revision):
        self._scope(client_scope)
        row=self.db.execute('SELECT * FROM policies WHERE client_scope=? AND policy_id=? AND revision=?',
                            (client_scope,policy_id,revision)).fetchone()
        require(row and row['source_kind']=='legacy_v1' and not row['current_authority'] and
                byte_hash(row['source_bytes'])==row['source_sha256'] and
                digest(json.loads(row['body']))==row['policy_sha256'],'monitor_policy_legacy_archive_invalid')
        return self.reference(client_scope,policy_id,revision)


def main():
    ap=argparse.ArgumentParser(description=__doc__); sub=ap.add_subparsers(dest='command',required=True)
    create=sub.add_parser('create'); create.add_argument('--directory',required=True); create.add_argument('--client-scope',action='append',required=True)
    for name in ('adopt','import-legacy','current'):
        p=sub.add_parser(name); p.add_argument('--profile',required=True); p.add_argument('--client-scope',required=True)
        if name=='adopt': p.add_argument('--policy',required=True); p.add_argument('--decision',required=True)
        elif name=='import-legacy': p.add_argument('--source',required=True)
        else: p.add_argument('--policy-id',required=True)
    args=ap.parse_args(); store=None
    try:
        if args.command=='create':
            store=MonitorPolicyStore.create(args.directory,args.client_scope)
            result=dict(status='monitor_policy_store_created',profile=str(store.profile_path))
        else:
            store=MonitorPolicyStore.open(args.profile)
            if args.command=='adopt':
                policy,_=read_json(args.policy); decision,_=read_json(args.decision)
                result=dict(status='monitor_policy_adopted',reference=store.adopt(args.client_scope,policy,decision))
            elif args.command=='import-legacy':
                result=dict(status='legacy_monitor_policy_archived',reference=store.import_legacy(args.client_scope,args.source))
            else:
                policy,reference=store.current(args.client_scope,args.policy_id)
                result=dict(status='current_monitor_policy',policy=policy,reference=reference)
        print(json.dumps(result,ensure_ascii=False,indent=2)); return 0
    except (ValueError,OSError,sqlite3.Error,json.JSONDecodeError) as exc:
        print(json.dumps({'status':'monitor_policy_store_blocked','reason':str(exc)},ensure_ascii=False)); return 2
    finally:
        if store is not None: store.close()


if __name__=='__main__': raise SystemExit(main())
