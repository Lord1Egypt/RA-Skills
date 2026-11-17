"""Short real-process regressions; outputs a reproducible JSON evidence report."""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import unittest
import uuid

HERE = Path(__file__).resolve().parent
RUNNER = HERE / 'runner.py'
DEMO = HERE / 'demo_task.py'
ROOT = None
CALLS = []
specmod = importlib.util.spec_from_file_location('runner_under_test', RUNNER)
r = importlib.util.module_from_spec(specmod)
specmod.loader.exec_module(r)


def cli(*args):
    start = time.monotonic()
    p = subprocess.run([sys.executable, str(RUNNER), *map(str,args)], capture_output=True, timeout=60)
    CALLS.append({'action':args[0], 'bytes':len(p.stdout)+len(p.stderr), 'seconds':round(time.monotonic()-start,4)})
    try:
        return p.returncode, json.loads(p.stdout)
    except ValueError:
        raise AssertionError(p.stderr.decode('utf-8','replace')+p.stdout.decode('utf-8','replace'))


def eventually(job, predicate, seconds=12):
    end=time.monotonic()+seconds
    while time.monotonic()<end:
        try:
            state=r.read(job/'state.json')
            if predicate(state):
                return state
        except (FileNotFoundError,ValueError):
            pass
        time.sleep(.04)
    raise AssertionError('Deadline: '+str(r.read(job/'state.json')))


def terminal(job):
    return eventually(job, lambda s:s['status'] in r.TERMINAL and not r.held(job/'worker.lock'))


class Tests(unittest.TestCase):
    def setUp(self):
        self.d=ROOT/self._testMethodName
        self.d.mkdir()
        self.job=self.d/'job'
        self.started=[]

    def tearDown(self):
        for j in self.started:
            if (j/'state.json').exists() and r.held(j/'worker.lock'):
                cli('cancel','--job',j)
                terminal(j)

    def task(self, mode='ok', ident='one', seconds=.02, **extra):
        t={'id':ident,'argv':[sys.executable,str(DEMO),'--mode',mode,'--seconds',str(seconds),'--output',ident+'.json','--counter',ident+'.count'],
           'cwd':str(self.d),'timeout_s':6,'effect':'local','replay_safe':True,
           'artifacts':[{'kind':'json','path':ident+'.json','equals':{'ok':True}}]}
        t.update(extra)
        return t

    def start(self,tasks,job=None,**extra):
        job=job or self.job
        spec={'version':1,'name':'regression','total_timeout_s':15,'tasks':tasks}
        spec.update(extra)
        path=self.d/(job.name+'.spec.json')
        path.write_text(json.dumps(spec),encoding='utf-8')
        code,out=cli('start','--job',job,'--spec',path)
        self.assertEqual(code,0,out)
        self.started.append(job)
        return path

    def test_01_success_queue_and_wait(self):
        self.start([self.task(),self.task(ident='two')])
        code,out=cli('wait','--job',self.job,'--seconds',10)
        self.assertEqual(code,0,out)
        self.assertEqual(out['done'],2)
        s=terminal(self.job)
        self.assertGreaterEqual(s['tasks'][1]['started_at'],s['tasks'][0]['ended_at'])

    def test_02_failure_stops_queue(self):
        self.start([self.task('fail'),self.task(ident='two')])
        s=terminal(self.job)
        self.assertEqual(s['status'],'failed')
        self.assertEqual(s['tasks'][0]['failure']['code'],'E_EXIT')
        self.assertFalse((self.d/'two.count').exists())

    def test_03_silent_job_is_not_stalled_failure(self):
        self.start([self.task(seconds=.6,timeout_s=3)])
        self.assertEqual(terminal(self.job)['status'],'succeeded')

    def test_04_timeout(self):
        start=time.monotonic()
        self.start([self.task(seconds=20,timeout_s=.4)])
        s=terminal(self.job)
        self.assertEqual(s['status'],'timed_out')
        self.assertLess(time.monotonic()-start,5)
        self.assertFalse((self.d/'one.json').exists())

    def test_05_bad_json(self):
        self.start([self.task('badjson')])
        s=terminal(self.job)
        self.assertEqual(s['tasks'][0]['exit_code'],0)
        self.assertEqual(s['tasks'][0]['failure']['code'],'E_ARTIFACT_JSON')

    def test_06_empty_file(self):
        self.start([self.task('empty')])
        self.assertEqual(terminal(self.job)['tasks'][0]['failure']['code'],'E_ARTIFACT')

    def test_07_stale_file(self):
        (self.d/'one.json').write_text('{"ok":true}')
        self.start([self.task('noop')])
        self.assertEqual(terminal(self.job)['tasks'][0]['failure']['code'],'E_STALE_ARTIFACT')

    def test_08_wav(self):
        self.start([self.task('wav',artifacts=[{'kind':'wav','path':'one.json','min_duration_s':.9,'max_duration_s':1.1}])])
        self.assertEqual(terminal(self.job)['status'],'succeeded')

    def test_09_truncated_wav(self):
        self.start([self.task('badwav',artifacts=[{'kind':'wav','path':'one.json'}])])
        self.assertEqual(terminal(self.job)['tasks'][0]['failure']['code'],'E_ARTIFACT_WAV')

    def test_10_hash_mismatch(self):
        self.start([self.task(artifacts=[{'kind':'sha256','path':'one.json','sha256':'0'*64}])])
        self.assertEqual(terminal(self.job)['tasks'][0]['failure']['code'],'E_ARTIFACT_HASH')

    def test_11_custom_validator_failure(self):
        self.start([self.task(artifacts=[{'kind':'command','argv':[sys.executable,'-c','raise SystemExit(9)'],'timeout_s':2,'read_only':True}])])
        self.assertEqual(terminal(self.job)['tasks'][0]['failure']['code'],'E_VALIDATION')

    def test_12_custom_validator_timeout(self):
        self.start([self.task(artifacts=[{'kind':'command','argv':[sys.executable,'-c','import time; time.sleep(20)'],'timeout_s':.2,'read_only':True}])])
        self.assertEqual(terminal(self.job)['tasks'][0]['failure']['code'],'E_VALIDATION')

    def test_13_duplicate_start(self):
        path=self.start([self.task(seconds=.2)])
        terminal(self.job)
        for _ in range(2):
            code,out=cli('start','--spec',path,'--job',self.job)
            self.assertEqual(code,0,out)
        self.assertEqual((self.d/'one.count').read_text(),'1')

    def test_14_spec_conflict(self):
        path=self.start([self.task()])
        terminal(self.job)
        spec=json.loads(path.read_text())
        spec['name']='another job'
        path.write_text(json.dumps(spec))
        code,out=cli('start','--spec',path,'--job',self.job)
        self.assertEqual(out['error'],'E_ID_CONFLICT')
        self.assertEqual(code,2)

    def test_15_frozen_spec_edit(self):
        self.start([self.task()])
        terminal(self.job)
        sp=self.job/'spec.json'
        spec=json.loads(sp.read_text())
        spec['name']='changed'
        sp.write_text(json.dumps(spec))
        code,out=cli('resume','--job',self.job)
        self.assertEqual(out['error'],'E_SPEC_CHANGED')

    def test_16_safe_transient_retry(self):
        self.start([self.task('flaky',retry={'max_attempts':2,'exit_codes':[7],'delay_s':.05})])
        s=terminal(self.job)
        self.assertEqual(s['status'],'succeeded')
        self.assertEqual((self.d/'one.count').read_text(),'2')

    def test_17_nonallowlisted_exit_not_retried(self):
        self.start([self.task('fail',retry={'max_attempts':2,'exit_codes':[8],'delay_s':.05})])
        self.assertEqual(terminal(self.job)['status'],'failed')
        self.assertEqual((self.d/'one.count').read_text(),'1')

    def test_18_external_retry_rejected(self):
        spec={'version':1,'name':'unsafe','tasks':[self.task('fail',effect='external',replay_safe=False,retry={'max_attempts':2,'exit_codes':[7]})]}
        with self.assertRaises(r.Problem):
            r.validate_spec(spec)
        self.assertFalse((self.d/'one.count').exists())

    def test_19_cancel_and_resume(self):
        self.start([self.task(seconds=1)])
        eventually(self.job,lambda s:s['tasks'][0].get('pid') is not None)
        cli('cancel','--job',self.job)
        self.assertEqual(terminal(self.job)['status'],'cancelled')
        code,out=cli('resume','--job',self.job,'--replay-safe')
        self.assertEqual(code,0,out)
        self.assertEqual(terminal(self.job)['status'],'succeeded')

    def test_20_resume_skips_completed(self):
        self.start([self.task(),self.task('flaky',ident='two')])
        self.assertEqual(terminal(self.job)['status'],'failed')
        cli('resume','--job',self.job,'--replay-safe')
        self.assertEqual(terminal(self.job)['status'],'succeeded')
        self.assertEqual((self.d/'one.count').read_text(),'1')
        self.assertEqual((self.d/'two.count').read_text(),'2')

    def test_21_resume_external_blocked(self):
        self.start([self.task('fail',effect='external',replay_safe=False)])
        terminal(self.job)
        code,out=cli('resume','--job',self.job,'--replay-safe')
        self.assertEqual(out['error'],'E_REPLAY_UNSAFE')
        self.assertEqual((self.d/'one.count').read_text(),'1')

    def test_22_logs_bounded(self):
        self.start([self.task('noise')],log_bytes=1024)
        self.assertEqual(terminal(self.job)['status'],'succeeded')
        files=list(self.job.glob('process.log*'))
        self.assertLessEqual(len(files),3)
        self.assertLessEqual(sum(f.stat().st_size for f in files),3072)
        self.assertGreater(sum(f.stat().st_size for f in files),0)
        code,out=cli('status','--job',self.job)
        self.assertNotIn('tail',out)
        rev=out['revision']
        code,out=cli('status','--job',self.job,'--since',rev)
        self.assertFalse(out['changed'])

    def test_23_resource_serialization(self):
        path=self.start([self.task(seconds=.6)],resources=['test-gpu'],resource_dir=str(self.d/'resource-locks'))
        eventually(self.job,lambda s:s['tasks'][0].get('pid') is not None)
        j2=self.d/'job2'
        self.start([self.task(ident='two',seconds=.1)],job=j2,resources=['test-gpu'],resource_dir=str(self.d/'resource-locks'))
        s1,s2=terminal(self.job),terminal(j2)
        self.assertEqual(s2['status'],'succeeded')
        self.assertGreaterEqual(s2['tasks'][0]['started_at'],s1['tasks'][0]['ended_at'])

    def test_24_cancel_descendant_tree(self):
        self.start([self.task('tree',seconds=20,timeout_s=25)])
        end=time.monotonic()+5
        while not (self.d/'descendant-pid.txt').exists() and time.monotonic()<end:
            time.sleep(.05)
        self.assertTrue((self.d/'descendant-pid.txt').exists())
        cli('cancel','--job',self.job)
        self.assertEqual(terminal(self.job)['status'],'cancelled')
        time.sleep(4.2)
        self.assertFalse((self.d/'escaped-child.txt').exists())

    @unittest.skipUnless(os.name=='nt','Windows kill-on-job-close containment')
    def test_25_worker_crash_kills_descendants(self):
        self.start([self.task('tree',seconds=20,timeout_s=25)])
        end=time.monotonic()+5
        while not (self.d/'descendant-pid.txt').exists() and time.monotonic()<end:
            time.sleep(.05)
        self.assertTrue((self.d/'descendant-pid.txt').exists())
        state=r.read(self.job/'state.json')
        os.kill(state['worker_pid'],signal_number())
        time.sleep(4.2)
        self.assertFalse(r.held(self.job/'worker.lock'))
        self.assertFalse((self.d/'escaped-child.txt').exists())
        # Resume goes through kernel lock ownership, not a stale PID or heartbeat.
        code,out=cli('resume','--job',self.job,'--replay-safe')
        self.assertEqual(code,0,out)
        eventually(self.job,lambda s:s['generation']==2 and r.held(self.job/'worker.lock'))
        cli('cancel','--job',self.job)
        self.assertEqual(terminal(self.job)['status'],'cancelled')

    def test_26_completed_validation_on_resume(self):
        self.start([self.task(),self.task('flaky',ident='two')])
        terminal(self.job)
        (self.d/'one.json').write_text('invalid')
        cli('resume','--job',self.job,'--replay-safe')
        s=terminal(self.job)
        self.assertEqual(s['error']['code'],'E_COMPLETED_INVALID')
        self.assertEqual((self.d/'two.count').read_text(),'1')

    def test_27_concurrent_duplicate_launch(self):
        path=self.d/'spec.json'
        path.write_text(json.dumps({'version':1,'name':'duplicate','tasks':[self.task(seconds=.4)]}))
        args=[sys.executable,str(RUNNER),'start','--spec',str(path),'--job',str(self.job)]
        ps=[subprocess.Popen(args,stdout=subprocess.PIPE,stderr=subprocess.PIPE) for _ in range(3)]
        self.started.append(self.job)
        for proc in ps:
            stdout,stderr=proc.communicate(timeout=10)
            self.assertEqual(proc.returncode,0,stderr+stdout)
        self.assertEqual(terminal(self.job)['status'],'succeeded')
        self.assertEqual((self.d/'one.count').read_text(),'1')

    def test_28_total_timeout_while_waiting_resource(self):
        rd=self.d/'resources'
        with r.Lock(rd/'gpu.lock'):
            self.start([self.task()],resources=['gpu'],resource_dir=str(rd),total_timeout_s=.3)
            self.assertEqual(terminal(self.job)['status'],'timed_out')
        self.assertFalse((self.d/'one.count').exists())

    def test_29_cancel_during_retry_backoff(self):
        self.start([self.task('fail',retry={'max_attempts':2,'exit_codes':[7],'delay_s':5})])
        eventually(self.job,lambda s:s['tasks'][0]['status']=='retry_wait')
        cli('cancel','--job',self.job)
        self.assertEqual(terminal(self.job)['status'],'cancelled')
        self.assertEqual((self.d/'one.count').read_text(),'1')

    def test_30_disk_threshold(self):
        self.start([self.task()],min_free_bytes=10**16)
        self.assertEqual(terminal(self.job)['error']['code'],'E_DISK_SPACE')
        self.assertFalse((self.d/'one.count').exists())

    def test_31_launch_budget(self):
        self.start([self.task('fail',launch_limit=1)])
        terminal(self.job)
        code,out=cli('resume','--job',self.job,'--replay-safe')
        self.assertEqual(out['error'],'E_LAUNCH_LIMIT')

    def test_32_bounded_wait(self):
        self.start([self.task(seconds=1)])
        start=time.monotonic()
        code,out=cli('wait','--job',self.job,'--seconds',.1)
        self.assertEqual(code,3,out)
        self.assertLess(time.monotonic()-start,.9)
        self.assertEqual(terminal(self.job)['status'],'succeeded')

    def test_33_missing_null_json_key(self):
        self.start([self.task(artifacts=[{'kind':'json','path':'one.json','equals':{'not_present':None}}])])
        self.assertEqual(terminal(self.job)['tasks'][0]['failure']['code'],'E_ARTIFACT_JSON')

    def test_34_failure_history_survives_resume(self):
        self.start([self.task('flaky')])
        s=terminal(self.job)
        fid=s['tasks'][0]['failure']['id']
        cli('resume','--job',self.job,'--replay-safe')
        s=terminal(self.job)
        self.assertEqual(s['status'],'succeeded')
        self.assertTrue(any(f['id']==fid for f in s['failure_history']))

    def test_35_unicode_paths(self):
        self.d=self.d/'中文 空格 ☃'
        self.d.mkdir()
        self.job=self.d/'作业'
        self.start([self.task()])
        self.assertEqual(terminal(self.job)['status'],'succeeded')
        code,out=cli('status','--job',self.job)
        self.assertEqual(code,0,out)
        self.assertEqual(Path(out['artifacts'][0]),self.d/'one.json')

    def test_36_coalesced_changes(self):
        self.start([self.task('flaky',retry={'max_attempts':2,'exit_codes':[7],'delay_s':.05})])
        terminal(self.job)
        code,out=cli('status','--job',self.job,'--since',1)
        groups=out['delta']['groups']
        task=next(g for g in groups if g['task']=='one')
        self.assertEqual(task['phase'],'succeeded')
        self.assertGreaterEqual(task['events'],4)
        self.assertFalse(out['delta']['history_truncated'])
        code,same=cli('status','--job',self.job,'--since',out['revision'])
        self.assertNotIn('delta',same)
        self.assertFalse(same['changed'])


def signal_number():
    import signal
    return signal.SIGTERM


class EvidenceResult(unittest.TextTestResult):
    def startTest(self,test):
        self.test_start=time.monotonic()
        super().startTest(test)
    def stopTest(self,test):
        RECORDS.append({'test':test._testMethodName,'seconds':round(time.monotonic()-self.test_start,3)})
        super().stopTest(test)


RECORDS=[]
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root',type=Path,required=True)
    p.add_argument('--report',type=Path,required=True)
    args=p.parse_args()
    ROOT=args.root.resolve()/('qa-'+uuid.uuid4().hex[:10])
    ROOT.mkdir(parents=True)
    start=time.monotonic()
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(Tests)
    result=unittest.TextTestRunner(verbosity=1,resultclass=EvidenceResult).run(suite)
    report={'runner_version':r.VERSION,'python':sys.version,'platform':sys.platform,'root':str(ROOT),
            'tests_run':result.testsRun,'passed':result.testsRun-len(result.errors)-len(result.failures)-len(result.skipped),
            'failures':[(str(t),e) for t,e in result.failures+result.errors], 'skipped':[(str(t),why) for t,why in result.skipped],
            'seconds':round(time.monotonic()-start,3),'tests':RECORDS,'cli_calls':len(CALLS),
            'cli_return_bytes':sum(x['bytes'] for x in CALLS),'max_cli_return_bytes':max(x['bytes'] for x in CALLS),
            'measurement_note':'CLI calls executed inside one local test program, NOT model requests or token measurements. Setup/assertion disk reads also local.',
            'source_sha256':hashlib.sha256(RUNNER.read_bytes()).hexdigest()}
    args.report.parent.mkdir(parents=True,exist_ok=True)
    args.report.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:report[k] for k in ['tests_run','passed','seconds','cli_calls','cli_return_bytes','max_cli_return_bytes']},ensure_ascii=False))
    raise SystemExit(0 if result.wasSuccessful() else 1)
