from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"


class SkillContractTests(unittest.TestCase):
    def test_skill_has_required_frontmatter(self) -> None:
        content = SKILL.read_text(encoding="utf-8")
        self.assertTrue(content.startswith("---\n"))
        self.assertIn("name: openclaw-novelai", content)
        self.assertIn("version: 0.1.3", content)
        self.assertRegex(content, r"(?m)^description: .+")
        self.assertRegex(content, r"(?m)^description: '.+: .+'$")
        self.assertIn('metadata: {"openclaw"', content)
        self.assertIn('"NOVELAI_TOKEN"', content)
        self.assertIn('"primaryEnv":"NOVELAI_TOKEN"', content)

        frontmatter_end = content.find("\n---\n", 4)
        self.assertGreater(frontmatter_end, 0)
        frontmatter = content[4:frontmatter_end]
        name = re.search(r"(?m)^name: ([a-z0-9][a-z0-9-]{0,63})$", frontmatter)
        description = re.search(r"(?m)^description: (.+)$", frontmatter)
        self.assertIsNotNone(name)
        self.assertIsNotNone(description)
        self.assertLessEqual(len(description.group(1)), 1024)

    def test_skill_mentions_required_workflow_tools(self) -> None:
        content = SKILL.read_text(encoding="utf-8")
        for tool in (
            "generate_image",
            "image_to_image",
            "inpaint",
            "upscale_image",
            "director_tool",
            "annotate_image",
            "suggest_tags",
            "encode_vibe",
            "estimate_anlas_cost",
        ):
            self.assertIn(tool, content)

    def test_skill_contains_no_token_like_literal(self) -> None:
        content = SKILL.read_text(encoding="utf-8")
        self.assertIsNone(re.search(r"(?i)\bpst-[A-Za-z0-9_-]{20,}\b", content))
        self.assertIsNone(re.search(r"(?i)\bsk-[A-Za-z0-9_-]{20,}\b", content))

    def test_skill_reuses_profile_and_retries_transient_failures(self) -> None:
        content = SKILL.read_text(encoding="utf-8")
        self.assertIn("Session-scoped billing profile and retry policy", content)
        self.assertIn("Reuse the profile indefinitely in the same conversation", content)
        self.assertIn("up to 3 sequential retries after the initial attempt", content)
        self.assertIn("Do not retry `400`, `401`, `402`", content)
        self.assertIn("ambiguous", content)
        self.assertIn("Never ask the user to paste a NovelAI token", content)

    def test_skill_pins_reference_server_version(self) -> None:
        content = SKILL.read_text(encoding="utf-8")
        example = (ROOT / "examples/openclaw.config.example.json5").read_text(
            encoding="utf-8"
        )
        self.assertIn("novelai-image-mcp==0.4.0", content)
        self.assertIn("novelai-image-mcp==0.4.0", example)


if __name__ == "__main__":
    unittest.main()
