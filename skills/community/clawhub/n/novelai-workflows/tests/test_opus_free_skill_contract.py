from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "variants" / "openclaw-novelai-opus-free" / "SKILL.md"


class OpusFreeSkillContractTests(unittest.TestCase):
    def test_skill_has_valid_frontmatter(self) -> None:
        content = SKILL.read_text(encoding="utf-8")
        self.assertTrue(content.startswith("---\n"))
        self.assertIn("name: openclaw-novelai-opus-free", content)
        self.assertIn("version: 0.2.3", content)
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

    def test_skill_requires_opus_and_exact_zero_estimate(self) -> None:
        content = SKILL.read_text(encoding="utf-8")
        self.assertIn("tier=3", content)
        self.assertIn("estimate_anlas_cost", content)
        self.assertIn("explicit numeric cost of exactly `0` Anlas", content)
        self.assertIn("opus_free_sample=true", content)
        self.assertIn("account balance decreases", content)

    def test_skill_reuses_verified_profile_for_same_session(self) -> None:
        content = SKILL.read_text(encoding="utf-8")
        self.assertIn("Session-scoped zero-cost verification lease", content)
        self.assertIn("no time limit and no reuse-count limit", content)
        self.assertIn("same conversation", content)
        self.assertIn("all billing-affecting fields must remain unchanged", content)
        self.assertIn("OpenClaw or MCP restarts", content)
        self.assertIn("do not narrate another account check or estimator call", content)

    def test_skill_retries_only_transient_failures(self) -> None:
        content = SKILL.read_text(encoding="utf-8")
        self.assertIn("up to 3 times after the initial attempt", content)
        self.assertIn("Retry the exact same operation and parameters", content)
        self.assertIn("transient `5xx`", content)
        self.assertIn("do not retry automatically", content)
        self.assertIn("ambiguous", content)

    def test_skill_allows_tested_free_enhancements(self) -> None:
        content = SKILL.read_text(encoding="utf-8")
        for operation in (
            "image_to_image",
            "inpaint",
            "annotate_image",
            "lineart",
            "sketch",
            "declutter",
            "colorize",
            "emotion",
        ):
            self.assertIn(operation, content)
        self.assertIn("already encoded V4/V4.5 Vibes", content)

    def test_skill_blocks_known_paid_or_unsupported_operations(self) -> None:
        content = SKILL.read_text(encoding="utf-8")
        for phrase in (
            "encode_vibe",
            "Precise Reference",
            "bg-removal",
            "enhance",
            "upscale_image",
        ):
            self.assertIn(phrase, content)
        self.assertIn("any batch, multi-sample, or parallel image generation", content)

    def test_skill_contains_no_token_like_literal(self) -> None:
        content = SKILL.read_text(encoding="utf-8")
        self.assertIsNone(re.search(r"(?i)\bpst-[A-Za-z0-9_-]{20,}\b", content))
        self.assertIsNone(re.search(r"(?i)\bsk-[A-Za-z0-9_-]{20,}\b", content))


if __name__ == "__main__":
    unittest.main()
