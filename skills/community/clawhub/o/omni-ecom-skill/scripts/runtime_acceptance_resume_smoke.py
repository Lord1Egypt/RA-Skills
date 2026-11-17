import json
from pathlib import Path
import tempfile
import unittest

from runtime_acceptance import build_resume_prompt


class MaintenanceResumeTests(unittest.TestCase):
    def prepare(self, folder):
        root = Path(folder)
        scaffold = {'run_id': 'existing-run', 'after_binding_commands': ['one', 'two', 'three', 'four', 'exact-report-command'], 'review_prepare_command': 'exact-review-command'}
        binding = {'run_id': 'existing-run', 'status': 'analysis_returns_bound'}
        (root / 'acceptance-scaffold-receipt.json').write_text(json.dumps(scaffold), encoding='utf-8')
        (root / 'analysis-binding-receipt.json').write_text(json.dumps(binding), encoding='utf-8')
        return root

    def test_fixed_report_command_and_existing_roles(self):
        with tempfile.TemporaryDirectory() as folder:
            root = self.prepare(folder)
            prompt = build_resume_prompt('2.0.3-candidate.2', root, after_maintenance=True)
            self.assertIn('第一执行动作必须原样执行报告构建命令：exact-report-command', prompt)
            self.assertIn('exact-review-command', prompt)
            self.assertIn('禁止重新派工', prompt)
            self.assertIn('candidate_pipeline_complete', prompt)
            self.assertIn('不得 TeamCreate', prompt)

    def test_does_not_overwrite_report_or_reviewer(self):
        for name in ('report.json', 'review-launch-manifest.json'):
            with self.subTest(name=name), tempfile.TemporaryDirectory() as folder:
                root = self.prepare(folder)
                (root / name).write_text('{}', encoding='utf-8')
                with self.assertRaisesRegex(ValueError, 'maintenance_resume_requires_report_pending'):
                    build_resume_prompt('2.0.3-candidate.2', root, after_maintenance=True)

    def test_wrong_binding_rejected(self):
        for binding in ({'run_id':'other-run','status':'analysis_returns_bound'}, {'run_id':'existing-run','status':'waiting'}):
            with self.subTest(binding=binding), tempfile.TemporaryDirectory() as folder:
                root = self.prepare(folder)
                (root / 'analysis-binding-receipt.json').write_text(json.dumps(binding), encoding='utf-8')
                with self.assertRaisesRegex(ValueError, 'maintenance_resume_binding_invalid'):
                    build_resume_prompt('2.0.3-candidate.2', root, after_maintenance=True)

    def test_formal_receipt_mode(self):
        with tempfile.TemporaryDirectory() as folder:
            root = self.prepare(folder)
            prompt = build_resume_prompt('2.0.3', root, after_maintenance=True)
            self.assertIn('formal_delivery_complete', prompt)
            self.assertNotIn('candidate_pipeline_complete', prompt)



if __name__ == '__main__':
    unittest.main()
