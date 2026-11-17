"""Synthetic fixtures only: no learner records or private answers."""
import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts' / 'grade_mcq.py'
spec = importlib.util.spec_from_file_location('grade_mcq', SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def fixture():
    return {'exam_id': 'synthetic-demo', 'version': 'v1', 'questions': [
        {'id': i, 'answer': 'ABCD'[(i-1) % 4], 'options': list('ABCD'),
         'topic': 'concept' if i <= 2 else 'application'} for i in range(1, 6)]}


class GradeTests(unittest.TestCase):
    def test_partial_range_not_full_exam(self):
        out = module.grade(fixture(), 2, 4, 'B C D', 'v1')
        self.assertEqual((out['correct'], out['possible']), (3, 3))
        self.assertEqual(out['not_submitted_ids'], [1, 5])

    def test_grouped_case_insensitive(self):
        out = module.grade(fixture(), 1, 5, 'ab;cd，a', 'v1')
        self.assertEqual(out['correct'], 5)

    def test_mismatch_refuses_shift(self):
        with self.assertRaisesRegex(ValueError, 'requires 4 answers'):
            module.grade(fixture(), 1, 4, 'BCD', 'v1')

    def test_numbered_input_not_silently_stripped(self):
        with self.assertRaises(ValueError):
            module.grade(fixture(), 1, 2, '1A 2B', 'v1')

    def test_version_mismatch(self):
        with self.assertRaises(ValueError):
            module.grade(fixture(), 1, 1, 'A', 'v2')

    def test_skipped_and_wrong_separate(self):
        out = module.grade(fixture(), 1, 3, 'A?A', 'v1')
        self.assertEqual((out['correct'], out['answered'], out['skipped']), (1, 2, 1))
        self.assertEqual(out['accuracy_percent_answered'], 50)
        self.assertEqual(out['score_percent_in_range'], 33.33)

    def test_all_skipped_accuracy_unknown(self):
        out = module.grade(fixture(), 1, 2, '??', 'v1')
        self.assertIsNone(out['accuracy_percent_answered'])

    def test_duplicate_key_ids(self):
        key = fixture()
        key['questions'].append(copy.deepcopy(key['questions'][0]))
        with self.assertRaises(ValueError):
            module.validate_key(key)

    def test_missing_key_question(self):
        key = fixture()
        key['questions'] = [q for q in key['questions'] if q['id'] != 2]
        with self.assertRaisesRegex(ValueError, 'absent'):
            module.grade(key, 1, 3, 'ABC', 'v1')

    def test_invalid_answer_letter(self):
        with self.assertRaises(ValueError):
            module.grade(fixture(), 1, 1, 'E', 'v1')

    def test_invalid_key_answer(self):
        key = fixture()
        key['questions'][0]['answer'] = 'E'
        with self.assertRaises(ValueError):
            module.validate_key(key)

    def test_points_validation(self):
        for bad in [0, -1, True, float('nan'), float('inf'), '1']:
            key = fixture()
            key['questions'][0]['points'] = bad
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                module.validate_key(key)

    def test_weighted_score_and_topic(self):
        key = fixture()
        key['questions'][0]['points'] = 2
        out = module.grade(key, 1, 2, 'AA', 'v1')
        self.assertEqual((out['earned'], out['possible']), (2, 3))
        self.assertEqual(out['by_topic']['concept']['answered'], 2)

    def test_invalid_range(self):
        for start, end in [(0, 2), (3, 2), (1, 10**9)]:
            with self.subTest(start=start), self.assertRaises(ValueError):
                module.grade(fixture(), start, end, 'A', 'v1')

    def test_no_mutation(self):
        key = fixture()
        before = copy.deepcopy(key)
        module.grade(key, 1, 2, 'AB', 'v1')
        self.assertEqual(key, before)

    def test_cli_and_no_file_write(self):
        with tempfile.TemporaryDirectory() as directory:
            keyfile = Path(directory) / 'key.json'
            keyfile.write_text(json.dumps(fixture()), encoding='utf-8')
            before = keyfile.read_bytes()
            proc = subprocess.run([sys.executable, str(SCRIPT), '--key', str(keyfile),
                '--start', '1', '--end', '2', '--answers', 'AB', '--exam-version', 'v1'],
                capture_output=True, text=True, cwd=directory, check=False)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertEqual(json.loads(proc.stdout)['correct'], 2)
            self.assertEqual(keyfile.read_bytes(), before)
            self.assertEqual([p.name for p in Path(directory).iterdir()], ['key.json'])

    def test_cli_malformed_key_nonzero(self):
        with tempfile.TemporaryDirectory() as directory:
            keyfile = Path(directory) / 'key.json'
            keyfile.write_text('{', encoding='utf-8')
            proc = subprocess.run([sys.executable, str(SCRIPT), '--key', str(keyfile),
                '--start', '1', '--end', '1', '--answers', 'A', '--exam-version', 'v1'],
                capture_output=True, text=True, check=False)
            self.assertEqual(proc.returncode, 2)
            self.assertIn('error', json.loads(proc.stderr))


if __name__ == '__main__':
    unittest.main()
