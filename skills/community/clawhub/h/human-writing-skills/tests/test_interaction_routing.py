import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from humanwriting.compiler import compile_humanize_prompt_text, compile_prompt
from humanwriting.detection import detect_audit_profiles
from humanwriting.longform import write_long_form_audit


class InteractionRoutingTests(unittest.TestCase):
    def test_wordless_generation_and_rewriting_load_response_owner_once(self):
        prompts = [
            compile_prompt("fiction", "只写动作，不要对话：她把信递给对方。"),
            compile_prompt("webnovel", "Write her missing reaction as I approach her."),
            compile_humanize_prompt_text("Mara handed him the envelope.", "fiction"),
        ]
        for prompt in prompts:
            with self.subTest(prompt=prompt[:60]):
                for module in ("dialogue-voice-audit", "dialogue-performance-audit"):
                    self.assertEqual(prompt.count(f"Technique Module: {module}"), 1)
                self.assertNotIn("Technique Module: speech-register-continuity", prompt)

    def test_ordinary_and_serious_generation_stay_small(self):
        for style, task in [
            ("fiction", "只写独行者在河岸看风景，不要对话。"),
            ("news-report", "报道工作人员把资料递给记者的经过。"),
            ("academic-paper", "Participants handed them the consent form."),
        ]:
            with self.subTest(style=style):
                prompt = compile_prompt(style, task)
                self.assertNotIn("Technique Module: dialogue-voice-audit", prompt)
                self.assertNotIn("Technique Module: dialogue-performance-audit", prompt)

    def test_auto_route_detects_actions_but_does_not_judge_responses(self):
        for text in [
            "她把信递给他。叙述转向多年前的往事。",
            "她把信递给他。他没有接，手仍压着那张车票。",
            "She handed him the parcel. He tucked it under his arm.",
            "I approached her. She stepped aside.",
        ]:
            with self.subTest(text=text):
                decisions = {d.profile: d for d in detect_audit_profiles(text)}
                self.assertTrue(decisions["voice"].selected)
                serious = {d.profile: d for d in detect_audit_profiles(text, serious_document=True)}
                self.assertFalse(serious["voice"].selected)

    def test_deep_chunk_tasks_include_wordless_actions_only_in_fiction(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            draft = root / "draft.md"
            draft.write_text("她把信递给对方。\n\n" + "河水沿着石阶慢慢涨上来。" * 210, encoding="utf-8")
            for style in ("fiction", "news-report"):
                output, _ = write_long_form_audit(
                    str(draft), str(root / style), style=style,
                    agent_mode="deep", chunk_size=2000,
                )
                plan = json.loads((output / "agent-plan.json").read_text(encoding="utf-8"))
                tasks = [t for t in plan["tasks"] if t["kind"] == "deep-dialogue-audit"]
                self.assertEqual(len(tasks), 1 if style == "fiction" else 0)
                if tasks:
                    prompt = (output / tasks[0]["prompt"]).read_text(encoding="utf-8")
                    self.assertIn("wordless", prompt)
                    self.assertIn("pending boundary check", prompt)


if __name__ == "__main__":
    unittest.main()
