import sys
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL_ROOT))

from novelforge_engine.skill_audit import audit_builtin_core


class SkillAuditTests(unittest.TestCase):
    def test_audit_builtin_core_rejects_author_and_project_specific_markers(self):
        result = audit_builtin_core(SKILL_ROOT)

        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["matches"], [])


if __name__ == "__main__":
    unittest.main()
