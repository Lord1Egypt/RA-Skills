import json
from pathlib import Path
import tempfile
import unittest
from runtime_timing import summarize, phase


class TimingTests(unittest.TestCase):
    def test_actual_timestamps_only(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'trace.jsonl'
            rows = [{'type':'function_call','callId':'a','name':'Read','timestamp':1000},
                    {'type':'function_call_result','callId':'a','timestamp':2500},
                    {'type':'function_call','callId':'b','name':'Bash','timestamp':3000}]
            path.write_text('\n'.join(json.dumps(row) for row in rows), encoding='utf-8')
            result = summarize(path)
            self.assertEqual(result['elapsed_seconds'], 2)
            self.assertEqual(result['tool_counts'], {'Read':1,'Bash':1})
            self.assertEqual(result['tool_spans'], [{'tool':'Read','seconds':1.5}])

    def test_missing_times_are_not_estimated(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'trace.jsonl'
            path.write_text('{"type":"function_call","name":"Read"}', encoding='utf-8')
            result = summarize(path)
            self.assertIsNone(result['elapsed_seconds'])
            self.assertEqual(result['tool_spans'], [])

    def test_phases_without_argument_disclosure(self):
        call = {'name':'Bash','arguments':json.dumps({'command':'python build_report_package.py --client PRIVATE_CLIENT'})}
        self.assertEqual(phase(call), 'report_and_pdf')
        self.assertEqual(phase({'name':'TaskOutput'}), 'expert_wait_or_control')
        self.assertEqual(phase({'name':'Bash','arguments':'not json'}), 'other')
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'trace.jsonl'
            call.update(type='function_call', timestamp=1000, callId='pdf')
            result = {'type':'function_call_result','timestamp':3000,'callId':'pdf'}
            path.write_text('\n'.join(json.dumps(row) for row in [call,result]), encoding='utf-8')
            diagnostic = summarize(path)
            self.assertEqual(diagnostic['tool_phase_seconds'], {'report_and_pdf':2.0})
            self.assertNotIn('PRIVATE_CLIENT', json.dumps(diagnostic))


if __name__ == '__main__': unittest.main()
