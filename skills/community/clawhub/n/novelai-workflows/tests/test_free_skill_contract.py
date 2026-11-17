from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FREE_SKILL = ROOT / "variants" / "openclaw-novelai-free" / "SKILL.md"


class FreeSkillContractTests(unittest.TestCase):
    def test_free_skill_has_valid_frontmatter(self) -> None:
        content = FREE_SKILL.read_text(encoding="utf-8")
        self.assertTrue(content.startswith("---\n"))
        self.assertIn("name: openclaw-novelai-free", content)
        self.assertIn("version: 0.1.2", content)
        self.assertRegex(content, r"(?m)^description: .+")
        self.assertRegex(content, r"(?m)^description: '.+: .+'$")
        self.assertIn('"primaryEnv":"NOVELAI_TOKEN"', content)

        frontmatter_end = content.find("\n---\n", 4)
        self.assertGreater(frontmatter_end, 0)
        frontmatter = content[4:frontmatter_end]
        name = re.search(r"(?m)^name: ([a-z0-9][a-z0-9-]{0,63})$", frontmatter)
        description = re.search(r"(?m)^description: (.+)$", frontmatter)
        self.assertIsNotNone(name)
        self.assertIsNotNone(description)
        self.assertLessEqual(len(description.group(1)), 1024)

    def test_free_skill_requires_explicit_zero_estimate(self) -> None:
        content = FREE_SKILL.read_text(encoding="utf-8")
        self.assertIn("estimate_anlas_cost", content)
        self.assertIn("explicit numeric cost of exactly `0` Anlas", content)
        self.assertIn("missing estimator: block every image generation", content)
        self.assertIn("Never use Subscription Anlas or Paid Anlas", content)

    def test_free_skill_blocks_paid_image_capabilities(self) -> None:
        content = FREE_SKILL.read_text(encoding="utf-8")
        for operation in (
            "image_to_image",
            "encode_vibe",
            "director_tool",
            "enhance",
            "upscale_image",
        ):
            self.assertIn(operation, content)
        self.assertIn("These operations are blocked", content)

    def test_free_skill_contains_no_token_like_literal(self) -> None:
        content = FREE_SKILL.read_text(encoding="utf-8")
        self.assertIsNone(re.search(r"(?i)\bpst-[A-Za-z0-9_-]{20,}\b", content))
        self.assertIsNone(re.search(r"(?i)\bsk-[A-Za-z0-9_-]{20,}\b", content))

    def test_free_skill_reuses_profile_and_retries_transient_failures(self) -> None:
        content = FREE_SKILL.read_text(encoding="utf-8")
        self.assertIn("Session-scoped zero-cost verification lease", content)
        self.assertIn("reuse the verified profile indefinitely", content)
        self.assertIn("up to 3 sequential retries after the initial attempt", content)
        self.assertIn("Do not retry parameter errors, authentication/billing errors", content)
        self.assertIn("ambiguous", content)


if __name__ == "__main__":
    unittest.main()
