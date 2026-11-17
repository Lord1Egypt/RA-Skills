import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from types import SimpleNamespace
import finish_agent_handoff


class FinishEncodingTests(unittest.TestCase):
    def test_member_guidance_does_not_repeat_successful_return(self):
        root = Path(__file__).resolve().parents[1]
        for role in ('data-analyst','platform-ops','content-live-growth','ad-profit-optimizer'):
            text = (root/'agents'/(role+'.md')).read_text(encoding='utf-8')
            self.assertIn('仅任务卡没有 `finish_command` 时', text)
            self.assertIn('不得再执行 `validation_commands`', text)

    def test_bad_numeric_fact_cannot_commit_return(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            raw = root/'raw.json'
            raw.write_text(json.dumps({'facts':[{'claim':'推广花费500元。'}]},ensure_ascii=False),encoding='utf-8')
            inventory = root/'inventory.json'
            inventory.write_text('{"report_count":1}',encoding='utf-8')
            (root/'claim-ledger.json').write_text('{"claims":[]}',encoding='utf-8')
            card = root/'card.json'
            card.write_text(json.dumps(dict(client_scope='runtime-acceptance-no-client-data',
                paths=dict(raw_handoff=str(raw),baseline='baseline.json',run_dir=str(root),report_inventory=str(inventory)),
                agent_id='data-analyst',attempt_id='a1',required_result=dict(minimum_depth='L2'))),encoding='utf-8')
            with patch.object(sys,'argv',['finish','--task-card',str(card)]), patch.object(
                    finish_agent_handoff.subprocess,'run',return_value=SimpleNamespace(returncode=0,stdout='',stderr='')) as invoked:
                self.assertEqual(finish_agent_handoff.main(),1)
                self.assertEqual(invoked.call_count,2)
                self.assertFalse(any('write_agent_return.py' in str(call.args) for call in invoked.call_args_list))

    def test_ordinary_business_scope_does_not_use_mechanism_exemption(self):
        finish_agent_handoff.verify_mechanism_facts({'client_scope':'customer'}, Path('not-read.json'))

    def test_gbk_parent_can_print_unicode_after_return(self):
        with tempfile.TemporaryDirectory() as folder:
            card = Path(folder)/'card.json'
            card.write_text(json.dumps(dict(paths=dict(raw_handoff='raw.json',baseline='baseline.json'),agent_id='data-analyst',attempt_id='a1',required_result=dict(minimum_depth='L2'))),encoding='utf-8')
            code = '''import sys
from unittest.mock import patch
from types import SimpleNamespace
import finish_agent_handoff as module
sys.argv=['finish','--task-card',sys.argv[1]]
with patch.object(module.subprocess,'run',return_value=SimpleNamespace(returncode=0,stdout='专家已回传 ✓',stderr='')) as invoked:
    result=module.main()
    assert invoked.call_count==3
    assert all(item.kwargs['env']['PYTHONIOENCODING']=='utf-8' for item in invoked.call_args_list)
sys.exit(result)
'''
            result = subprocess.run([sys.executable,'-B','-c',code,str(card)],cwd=Path(__file__).parent,capture_output=True,env=dict(os.environ,PYTHONIOENCODING='gbk',PYTHONDONTWRITEBYTECODE='1'))
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertIn('专家已回传 ✓',result.stdout.decode('utf-8'))


if __name__ == '__main__': unittest.main()
