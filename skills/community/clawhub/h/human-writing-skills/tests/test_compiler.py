import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory

from humanwriting.cli import main
from humanwriting.compiler import compile_audit_prompt, compile_humanize_prompt, compile_prompt
from humanwriting.detection import detect_audit_profiles
from humanwriting.pipeline import write_audit_pipeline
from humanwriting.skills import (
    default_skills_dir,
    list_module_skills,
    list_skills,
    list_style_skills,
    load_skill,
)


class CompilerTests(unittest.TestCase):
    def test_skill_metadata_covers_primary_discovery_queries(self):
        root = Path(__file__).resolve().parents[1]
        skill = root.joinpath("SKILL.md").read_text(encoding="utf-8")
        for term in (
            "AI humanizer",
            "humanize AI text",
            "de-AI writing",
            "fiction and novels",
            "story continuity",
            "去AI味",
            "小说续写",
            "长文一致性",
            "增强版去 AI 写作 Skill",
            "高级 AI 写作工具",
            "去AI写作",
            "humanize ai text",
            "natural rewriting",
            "novel writing assistant",
            "long-form audit",
            "chunked audit",
            "文风统一",
            "长篇审查",
            "人物设定统一",
            "scene ending audit",
            "AI式结尾",
            "生硬结尾审查",
        ):
            self.assertIn(term.lower(), skill.lower())

    def test_lists_builtin_skills(self):
        skills = list_skills()
        self.assertIn("fiction", skills)
        self.assertIn("webnovel", skills)

    def test_default_skills_resource_contains_core_files(self):
        root = default_skills_dir()
        self.assertTrue(root.joinpath("fiction.md").is_file())
        self.assertTrue(root.joinpath("relationship-stance-audit.md").is_file())
        self.assertTrue(root.joinpath("speech-register-continuity.md").is_file())
        self.assertTrue(root.joinpath("capability-state-audit.md").is_file())

    def test_lists_style_and_module_skills(self):
        self.assertIn("fiction", list_style_skills())
        self.assertIn("embodied-emotion", list_module_skills())
        self.assertIn("narrative-bridges", list_module_skills())
        self.assertIn("relationship-state", list_module_skills())
        self.assertIn("natural-measurement", list_module_skills())
        self.assertIn("forensic-physical-audit", list_module_skills())
        self.assertIn("occupancy-capacity", list_module_skills())
        self.assertIn("relationship-stance-audit", list_module_skills())
        self.assertIn("cliche-phrase-audit", list_module_skills())
        self.assertIn("formulaic-structure-audit", list_module_skills())
        self.assertIn("prose-progress-audit", list_module_skills())
        self.assertIn("logic-causality-audit", list_module_skills())
        self.assertIn("character-consistency-audit", list_module_skills())
        self.assertIn("proofreading-audit", list_module_skills())
        self.assertIn("reference-style-alignment", list_module_skills())
        self.assertIn("dialogue-voice-audit", list_module_skills())
        self.assertIn("speech-register-continuity", list_module_skills())
        self.assertIn("capability-state-audit", list_module_skills())
        self.assertIn("serial-reentry", list_module_skills())
        self.assertIn("narrative-distance-control", list_module_skills())
        self.assertIn("imagery-load-audit", list_module_skills())
        self.assertIn("paragraph-rhythm-audit", list_module_skills())
        self.assertIn("detail-disclosure-audit", list_module_skills())
        self.assertIn("scene-entry-audit", list_module_skills())
        self.assertIn("chapter-momentum-audit", list_module_skills())
        self.assertIn("world-ontology-audit", list_module_skills())
        self.assertIn("process-earnedness-audit", list_module_skills())
        self.assertIn("attention-budget-audit", list_module_skills())
        self.assertIn("chapter-pattern-audit", list_module_skills())
        self.assertIn("source-grounding", list_module_skills())
        self.assertIn("rewrite-fidelity", list_module_skills())
        self.assertIn("surface-pattern-audit", list_module_skills())
        self.assertIn("narrative-naturalness-audit", list_module_skills())
        self.assertIn("repetition-exposition-audit", list_module_skills())
        self.assertIn("voice-ambiguity-preservation", list_module_skills())
        self.assertIn("humanize-examples", list_module_skills())
        self.assertIn("long-form-style-consistency", list_module_skills())
        self.assertIn("earned-ending-audit", list_module_skills())
        self.assertIn("dialogue-performance-audit", list_module_skills())
        self.assertIn("translationese-audit", list_module_skills())

    def test_quick_humanize_loads_only_the_focused_rewrite_stack(self):
        with TemporaryDirectory() as directory:
            draft = Path(directory) / "draft.md"
            draft.write_text("她说不清。也许不是怕，只是不想开门。", encoding="utf-8")
            prompt = compile_humanize_prompt(str(draft), style="fiction")
        self.assertIn("Technique Module: surface-pattern-audit", prompt)
        self.assertIn("Technique Module: voice-ambiguity-preservation", prompt)
        self.assertIn("Technique Module: rewrite-fidelity", prompt)
        self.assertNotIn("Technique Module: humanize-examples", prompt)
        self.assertNotIn("Technique Module: formulaic-structure-audit", prompt)
        self.assertNotIn("Technique Module: cliche-phrase-audit", prompt)
        self.assertIn("same language and genre", prompt)
        self.assertIn("useful ambiguity", prompt)

    def test_deep_humanize_and_examples_are_independently_gated(self):
        with TemporaryDirectory() as directory:
            draft = Path(directory) / "draft.md"
            draft.write_text("这是一个值得注意的故事。", encoding="utf-8")
            deep = compile_humanize_prompt(str(draft), style="self-media", mode="deep")
            examples = compile_humanize_prompt(
                str(draft),
                style="self-media",
                with_examples=True,
            )
        self.assertIn("Technique Module: formulaic-structure-audit", deep)
        self.assertIn("Technique Module: prose-progress-audit", deep)
        self.assertIn("Technique Module: narrative-naturalness-audit", deep)
        self.assertNotIn("Technique Module: repetition-exposition-audit", deep)
        self.assertIn("Technique Module: imperfect-prose", deep)
        self.assertNotIn("Technique Module: earned-ending-audit", deep)
        self.assertNotIn("Technique Module: humanize-examples", deep)
        self.assertIn("Technique Module: humanize-examples", examples)
        self.assertNotIn("Technique Module: formulaic-structure-audit", examples)
        self.assertNotIn("Technique Module: earned-ending-audit", examples)

    def test_ending_profile_is_isolated_from_ai_trace_and_full_review(self):
        with TemporaryDirectory() as directory:
            draft = Path(directory) / "draft.md"
            draft.write_text(
                "她把钥匙放下。窗外暮色渐渐沉下，她不禁思考人生与未来。",
                encoding="utf-8",
            )
            ending = compile_audit_prompt(
                str(draft),
                profiles=["ending"],
                document_type="fiction",
            )
            ai_trace = compile_audit_prompt(
                str(draft),
                profiles=["ai-trace"],
                document_type="fiction",
            )
            full = compile_audit_prompt(
                str(draft),
                profiles=["full"],
                document_type="fiction",
            )
        self.assertIn("Selected profiles: ending", ending)
        self.assertIn("Audit Module: earned-ending-audit", ending)
        self.assertNotIn("Audit Module: formulaic-structure-audit", ending)
        self.assertNotIn("Audit Module: earned-ending-audit", ai_trace)
        self.assertIn("Audit Module: narrative-naturalness-audit", ai_trace)
        self.assertIn("Audit Module: repetition-exposition-audit", ai_trace)
        self.assertNotIn("Audit Module: earned-ending-audit", full)

    def test_repetition_profile_is_narrative_only_and_isolated(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            fiction = root / "fiction.md"
            news = root / "news.md"
            fiction.write_text("她把钥匙放回抽屉，又把钥匙放回抽屉。", encoding="utf-8")
            news.write_text("市交通局公布了新的封路安排。", encoding="utf-8")
            prompt = compile_audit_prompt(
                str(fiction),
                profiles=["repetition"],
                document_type="fiction",
            )
            with self.assertRaisesRegex(ValueError, "limited to fiction"):
                compile_audit_prompt(
                    str(news),
                    profiles=["repetition"],
                    document_type="news-report",
                )
        self.assertIn("Selected profiles: repetition", prompt)
        self.assertIn("Audit Module: repetition-exposition-audit", prompt)
        self.assertNotIn("Audit Module: formulaic-structure-audit", prompt)

    def test_serious_ending_profile_uses_same_module_without_narrative_naturalness(self):
        with TemporaryDirectory() as directory:
            draft = Path(directory) / "news.md"
            draft.write_text(
                "市交通局周二公布，东桥将于8月15日封闭两周。工程预计8月29日结束。",
                encoding="utf-8",
            )
            prompt = compile_audit_prompt(
                str(draft),
                profiles=["ending"],
                document_type="news-report",
            )
        self.assertIn("Audit Module: earned-ending-audit", prompt)
        self.assertNotIn("Audit Module: narrative-naturalness-audit", prompt)
        self.assertIn("Audit Module: protected-content", prompt)

    def test_humanize_prompt_budgets_keep_quick_materially_smaller(self):
        with TemporaryDirectory() as directory:
            draft = Path(directory) / "draft.md"
            draft.write_text("她停在门口，说不清自己在等什么。", encoding="utf-8")
            quick = compile_humanize_prompt(str(draft), style="fiction")
            deep = compile_humanize_prompt(str(draft), style="fiction", mode="deep")
        self.assertLess(len(quick), 15000)
        # Deep rewrite includes preservation plus the generation-time protocol.
        self.assertLess(len(deep), 34000)
        self.assertLess(len(quick), len(deep) * 0.6)

    def test_humanize_rejects_an_empty_draft(self):
        with TemporaryDirectory() as directory:
            draft = Path(directory) / "draft.md"
            draft.write_text("   ", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "non-empty --draft"):
                compile_humanize_prompt(str(draft), style="fiction")

    def test_preservation_profile_requires_original_and_stays_isolated(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            original = root / "original.md"
            revised = root / "revised.md"
            original.write_text("我没生气。算了，我不说了。", encoding="utf-8")
            revised.write_text("我没有生气，只是不想继续讨论。", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "requires --original"):
                compile_audit_prompt(str(revised), profiles=["preservation"])
            prompt = compile_audit_prompt(
                str(revised),
                profiles=["preservation"],
                original_path=str(original),
            )
        self.assertIn("Selected profiles: preservation", prompt)
        self.assertIn("Audit Module: voice-ambiguity-preservation", prompt)
        self.assertNotIn("Audit Module: rewrite-fidelity", prompt)
        self.assertIn("Original Text For Rewrite Comparison", prompt)

    def test_humanize_cli_builds_a_prompt(self):
        with TemporaryDirectory() as directory:
            draft = Path(directory) / "draft.md"
            draft.write_text("此外，这是一个重要的时刻。", encoding="utf-8")
            output = StringIO()
            with redirect_stdout(output):
                code = main(["humanize", "--draft", str(draft), "--style", "fiction"])
        self.assertEqual(code, 0)
        self.assertIn("Technique Module: voice-ambiguity-preservation", output.getvalue())

    def test_load_skill_content(self):
        skill = load_skill("news-report")
        self.assertEqual(skill.name, "news-report")
        self.assertEqual(skill.kind, "style")
        self.assertIn("News Report Skill", skill.content)

    def test_formal_document_is_a_serious_base_style(self):
        self.assertIn("formal-document", list_style_skills())
        prompt = compile_prompt("formal-document", "Draft an official notice.")
        self.assertIn("Selected Skill: formal-document", prompt)
        self.assertIn("Technique Module: protected-content", prompt)
        self.assertIn("Remove conversational fillers", prompt)

    def test_compile_prompt_contains_style_and_task(self):
        prompt = compile_prompt("fiction", "Write the next scene.")
        self.assertIn("Core Directive", prompt)
        self.assertIn("Beat bridge", prompt)
        self.assertIn("Relationship state", prompt)
        self.assertIn("Fiction Skill", prompt)
        self.assertIn("pressure-bearing line or action", prompt)
        self.assertIn("replace unrequested scene mini-headings or time cards", prompt)
        self.assertIn("prior residue", prompt)
        self.assertIn("Write the next scene.", prompt)
        self.assertNotIn("Technique Module: reference-style-alignment", prompt)

    def test_translationese_module_requires_an_explicit_translation_signal(self):
        ordinary = compile_prompt("fiction", "Escribe la siguiente escena en español.")
        translated = compile_prompt(
            "fiction",
            "Traduce esta escena al español y elimina los calcos de traducción.",
        )
        self.assertNotIn("Technique Module: translationese-audit", ordinary)
        self.assertIn("Technique Module: translationese-audit", translated)

    def test_dialogue_generation_activates_only_for_explicit_narrative_tasks(self):
        dialogue = compile_prompt("fiction", "写一场两位角色各有所求的谈判。")
        interaction = compile_prompt("fiction", "续写两人重逢后的试探场景。")
        narration = compile_prompt("fiction", "写一段独自穿过雨夜的场景。")
        excluded = compile_prompt("fiction", "只写动作，不要对话。")
        serious = compile_prompt("news-report", "Write an interview-based report.")
        self.assertIn("Technique Module: dialogue-voice-audit", dialogue)
        self.assertIn("Technique Module: dialogue-performance-audit", dialogue)
        self.assertIn("Scene Speech Contract", dialogue)
        self.assertIn("Response Obligation And Interaction Debt", dialogue)
        self.assertIn("Technique Module: dialogue-performance-audit", interaction)
        self.assertIn("Dialogue Performance And Landing", interaction)
        self.assertNotIn("Technique Module: dialogue-voice-audit", narration)
        self.assertNotIn("Technique Module: dialogue-performance-audit", narration)
        self.assertNotIn("Technique Module: dialogue-voice-audit", excluded)
        self.assertNotIn("Technique Module: dialogue-voice-audit", serious)

    def test_register_generation_requires_dialogue_and_explicit_language_evidence(self):
        with TemporaryDirectory() as directory:
            context = Path(directory) / "ledger.md"
            identity_context = Path(directory) / "identity-ledger.md"
            context.write_text(
                "人物来自广东，母语是粤语；与同事主要说普通话。",
                encoding="utf-8",
            )
            identity_context.write_text(
                "人物是美国人，未设定其他语言经历。",
                encoding="utf-8",
            )
            active = compile_prompt(
                "fiction", "写一段他与同事的对话。", context_path=str(context)
            )
            no_dialogue = compile_prompt(
                "fiction", "描写他走进办公室。", context_path=str(context)
            )
            no_evidence = compile_prompt("fiction", "写一段两人的对话。")
            identity_only = compile_prompt(
                "fiction", "写一段他的对话。", context_path=str(identity_context)
            )
            serious = compile_prompt("news-report", "写一篇包含采访引语的报道。")
        self.assertIn("Technique Module: speech-register-continuity", active)
        self.assertNotIn("Technique Module: speech-register-continuity", no_dialogue)
        self.assertNotIn("Technique Module: speech-register-continuity", no_evidence)
        self.assertIn("Technique Module: speech-register-continuity", identity_only)
        self.assertIn("does not by itself prove a dialect inventory", identity_only)
        self.assertNotIn("Technique Module: speech-register-continuity", serious)

    def test_capability_generation_is_current_task_gated(self):
        with TemporaryDirectory() as directory:
            context = Path(directory) / "ledger.md"
            context.write_text("主角当前为筑基后期，左臂受伤。", encoding="utf-8")
            active = compile_prompt(
                "webnovel",
                "续写突破场景，保持境界、伤势和代价连续。",
                context_path=str(context),
            )
            ordinary = compile_prompt(
                "webnovel", "续写两人在客栈吃饭的场景。", context_path=str(context)
            )
        self.assertIn("Technique Module: capability-state-audit", active)
        self.assertNotIn("Technique Module: capability-state-audit", ordinary)

    def test_world_and_process_generation_activate_only_on_matching_narrative_tasks(self):
        world = compile_prompt("fiction", "写一场民国背景下使用电报传讯的场景。")
        process = compile_prompt("webnovel", "详细写调查和取证过程，结果必须有代价。")
        plain = compile_prompt("fiction", "写一段河边散步。")
        serious = compile_prompt("news-report", "报道一次科研实验。")
        self.assertIn("Technique Module: world-ontology-audit", world)
        self.assertIn("Technique Module: process-earnedness-audit", process)
        self.assertNotIn("Technique Module: world-ontology-audit", plain)
        self.assertNotIn("Technique Module: process-earnedness-audit", plain)
        self.assertNotIn("Technique Module: process-earnedness-audit", serious)

    def test_reference_style_does_not_activate_without_explicit_signal(self):
        prompt = compile_prompt("fiction", "Write a quiet scene by the river.")
        self.assertNotIn("Technique Module: reference-style-alignment", prompt)
        self.assertNotIn("Reference Style Material", prompt)

    def test_original_activates_fidelity_without_style_or_source_contamination(self):
        with TemporaryDirectory() as directory:
            original = Path(directory) / "original.md"
            original.write_text("约有一半参与者表示不确定。", encoding="utf-8")
            prompt = compile_prompt(
                "self-media",
                "润色这段原文，不要增加事实。",
                original_path=str(original),
            )
            plain = compile_prompt("self-media", "写一篇新文章。")
        self.assertIn("Technique Module: rewrite-fidelity", prompt)
        self.assertIn("Original Text For Rewrite Comparison", prompt)
        self.assertIn("约有一半", prompt)
        self.assertNotIn("Reference Style Material", prompt)
        self.assertNotIn("Supplied Factual Sources", prompt)
        self.assertNotIn("Technique Module: rewrite-fidelity", plain)

    def test_explicit_task_style_request_activates_reference_module(self):
        prompt = compile_prompt("fiction", "参考冷峻克制的文风写下一场戏。")
        self.assertIn("Technique Module: reference-style-alignment", prompt)
        self.assertIn("Reference Style Material", prompt)
        self.assertIn("参考冷峻克制的文风", prompt)

    def test_reference_file_activates_and_respects_sampling_budget(self):
        with TemporaryDirectory() as directory:
            reference = Path(directory) / "reference.md"
            reference.write_text("甲" * 6000 + "中段标记" + "乙" * 6000, encoding="utf-8")
            prompt = compile_prompt(
                "fiction",
                "Write the next scene.",
                reference_paths=[str(reference)],
                reference_budget=1200,
            )
        self.assertIn("Technique Module: reference-style-alignment", prompt)
        self.assertIn("Reference: reference.md", prompt)
        self.assertIn("middle sample", prompt)
        self.assertLess(prompt.count("甲") + prompt.count("乙"), 1400)

    def test_many_reference_files_share_one_global_budget(self):
        with TemporaryDirectory() as directory:
            paths = []
            for index in range(12):
                path = Path(directory) / f"reference-{index}.md"
                path.write_text(str(index) * 2000, encoding="utf-8")
                paths.append(str(path))
            from humanwriting.reference import build_reference_pack

            pack = build_reference_pack(paths=paths, budget=1000)
        self.assertLessEqual(pack.sampled_characters, 1000)

    def test_audit_reference_automatically_adds_style_match(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            draft = root / "draft.md"
            reference = root / "reference.md"
            draft.write_text("她推开门，没有回头。", encoding="utf-8")
            reference.write_text("雨落得很慢。灯没有亮。", encoding="utf-8")
            prompt = compile_audit_prompt(
                str(draft),
                profiles=["character"],
                reference_paths=[str(reference)],
            )
        self.assertIn("Selected profiles: character, style-match", prompt)
        self.assertIn("Audit Module: reference-style-alignment", prompt)
        self.assertIn("Reference: reference.md", prompt)

    def test_style_match_profile_requires_explicit_reference(self):
        with TemporaryDirectory() as directory:
            draft = Path(directory) / "draft.md"
            draft.write_text("A short draft.", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "requires --reference"):
                compile_audit_prompt(str(draft), profiles=["style-match"])

    def test_fidelity_profile_requires_and_isolates_original(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            original = root / "original.md"
            candidate = root / "candidate.md"
            original.write_text("他可能在周五离开。", encoding="utf-8")
            candidate.write_text("他确定会在周五离开。", encoding="utf-8")
            prompt = compile_audit_prompt(
                str(candidate), profiles=["fidelity"], original_path=str(original)
            )
            with self.assertRaisesRegex(ValueError, "requires --original"):
                compile_audit_prompt(str(candidate), profiles=["fidelity"])
        self.assertIn("Audit Module: rewrite-fidelity", prompt)
        self.assertIn("Original Text For Rewrite Comparison", prompt)
        self.assertNotIn("Audit Module: ai-trace-rubric", prompt)

    def test_compile_prompt_can_add_modules(self):
        prompt = compile_prompt(
            "fiction",
            "Write the next scene.",
            modules=[
                "narrative-bridges",
                "relationship-state",
                "natural-measurement",
                "embodied-emotion",
                "vocal-rhythm",
            ],
            review=True,
        )
        self.assertIn("Technique Module: narrative-bridges", prompt)
        self.assertIn("Technique Module: relationship-state", prompt)
        self.assertIn("Technique Module: natural-measurement", prompt)
        self.assertIn("Technique Module: embodied-emotion", prompt)
        self.assertIn("Technique Module: vocal-rhythm", prompt)
        self.assertIn("Technique Module: editor-loop", prompt)
        self.assertIn("Technique Module: ai-trace-rubric", prompt)
        self.assertIn("Orphaned interaction", prompt)
        self.assertNotIn("Technique Module: relationship-stance-audit", prompt)
        self.assertNotIn("Technique Module: cliche-phrase-audit", prompt)
        self.assertNotIn("Technique Module: formulaic-structure-audit", prompt)
        self.assertNotIn("Technique Module: prose-progress-audit", prompt)

    def test_deep_review_adds_detailed_audits_and_is_larger(self):
        compact = compile_prompt("fiction", "Write the next scene.", review=True)
        deep = compile_prompt("fiction", "Write the next scene.", deep_review=True)
        self.assertIn("Technique Module: cliche-phrase-audit", deep)
        self.assertIn("Technique Module: formulaic-structure-audit", deep)
        self.assertIn("Technique Module: prose-progress-audit", deep)
        self.assertNotIn("Technique Module: attention-budget-audit", deep)
        self.assertIn("Technique Module: relationship-stance-audit", deep)
        self.assertIn("Technique Module: natural-measurement", deep)
        self.assertLess(len(compact), len(deep))
        self.assertNotIn("Technique Module: dialogue-voice-audit", deep)
        self.assertNotIn("Technique Module: serial-reentry", deep)
        self.assertNotIn("Technique Module: imagery-load-audit", deep)
        self.assertNotIn("Technique Module: chapter-momentum-audit", deep)

    def test_new_generation_modules_are_explicit_and_independent(self):
        prompt = compile_prompt(
            "fiction",
            "Write a dialogue scene.",
            modules=["dialogue-voice-audit", "paragraph-rhythm-audit"],
        )
        self.assertIn("Technique Module: dialogue-voice-audit", prompt)
        self.assertIn("Technique Module: paragraph-rhythm-audit", prompt)
        self.assertNotIn("Technique Module: serial-reentry", prompt)
        self.assertNotIn("Technique Module: imagery-load-audit", prompt)

    def test_attention_budget_generation_requires_explicit_long_form_signal(self):
        explicit = compile_prompt("fiction", "扩写这一章，并检查篇幅分配和灌水。")
        plain = compile_prompt("fiction", "写下一场戏。", deep_review=True)
        self.assertIn("Technique Module: attention-budget-audit", explicit)
        self.assertNotIn("Technique Module: attention-budget-audit", plain)

    def test_compact_review_stays_within_generation_prompt_budget(self):
        context = Path(__file__).resolve().parent.parent / "examples" / "story-ledger.md"
        prompt = compile_prompt(
            "webnovel",
            "Continue the next chapter.",
            context_path=str(context),
            review=True,
            strict_continuity=True,
        )
        # Includes the default generation protocol and genre brief, not full audits.
        self.assertLess(len(prompt), 26000)

    def test_duplicate_modules_are_loaded_once(self):
        prompt = compile_prompt(
            "fiction",
            "Write the next scene.",
            modules=["vocal-rhythm", "vocal-rhythm"],
        )
        self.assertEqual(prompt.count("# Technique Module: vocal-rhythm"), 1)

    def test_only_deep_review_adds_number_sense_for_narrative_styles(self):
        fiction_prompt = compile_prompt("fiction", "Write the next scene.", review=True)
        deep_fiction_prompt = compile_prompt("fiction", "Write the next scene.", deep_review=True)
        deep_news_prompt = compile_prompt("news-report", "Write the report.", deep_review=True)
        self.assertNotIn("Technique Module: natural-measurement", fiction_prompt)
        self.assertIn("Technique Module: natural-measurement", deep_fiction_prompt)
        self.assertNotIn("Technique Module: natural-measurement", deep_news_prompt)

    def test_number_sense_can_be_explicitly_added(self):
        prompt = compile_prompt("news-report", "Write the report.", number_sense=True)
        self.assertIn("Technique Module: natural-measurement", prompt)

    def test_compile_prompt_can_add_strict_continuity_modules(self):
        prompt = compile_prompt(
            "fiction",
            "Write a car scene.",
            strict_continuity=True,
        )
        self.assertIn("Technique Module: occupancy-capacity", prompt)
        self.assertIn("Technique Module: spatial-blocking", prompt)
        self.assertIn("Technique Module: appearance-prop-continuity", prompt)
        self.assertNotIn("Technique Module: physical-continuity-audit", prompt)

    def test_compile_audit_prompt_extracts_draft_and_modules(self):
        with TemporaryDirectory() as directory:
            draft = Path(directory) / "draft.md"
            draft.write_text(
                "Lao Gao looked from the front row toward Yanzi behind the glass. "
                "Later, he touched Yanzi in the rear seat. Yanzi wore flats, then heels.",
                encoding="utf-8",
            )
            prompt = compile_audit_prompt(str(draft), number_sense=True)
        self.assertIn("Audit Directive", prompt)
        self.assertIn("Audit Module: forensic-physical-audit", prompt)
        self.assertNotIn("Audit Module: occupancy-capacity", prompt)
        self.assertNotIn("Audit Module: spatial-blocking", prompt)
        self.assertNotIn("Audit Module: appearance-prop-continuity", prompt)
        self.assertNotIn("Audit Module: physical-continuity-audit", prompt)
        self.assertIn("Audit Module: relationship-stance-audit", prompt)
        self.assertIn("Audit Module: cliche-phrase-audit", prompt)
        self.assertIn("Audit Module: formulaic-structure-audit", prompt)
        self.assertIn("Audit Module: prose-progress-audit", prompt)
        self.assertIn("Audit Module: narrative-naturalness-audit", prompt)
        self.assertIn("Audit Module: natural-measurement", prompt)
        self.assertIn("Audit Module: logic-causality-audit", prompt)
        self.assertIn("Audit Module: character-consistency-audit", prompt)
        self.assertIn("Audit Module: proofreading-audit", prompt)
        self.assertIn("Draft To Audit", prompt)
        self.assertIn("behind the glass", prompt)
        self.assertIn("flats, then heels", prompt)

    def test_physical_profile_has_one_forensic_owner(self):
        with TemporaryDirectory() as directory:
            draft = Path(directory) / "draft.md"
            draft.write_text("她坐在后排，鞋跟碰到了地垫。", encoding="utf-8")
            prompt = compile_audit_prompt(str(draft), profiles=["physical"])
        self.assertIn("Audit Module: forensic-physical-audit", prompt)
        self.assertNotIn("Audit Module: occupancy-capacity", prompt)
        self.assertNotIn("Audit Module: spatial-blocking", prompt)
        self.assertNotIn("Audit Module: appearance-prop-continuity", prompt)
        self.assertNotIn("Audit Module: physical-continuity-audit", prompt)

    def test_light_physical_checklist_suppresses_default_forensic_profile(self):
        with TemporaryDirectory() as directory:
            draft = Path(directory) / "draft.md"
            draft.write_text("她坐在后排，鞋跟碰到了地垫。", encoding="utf-8")
            prompt = compile_audit_prompt(
                str(draft),
                modules=["physical-continuity-audit"],
            )
        self.assertIn("Audit Module: physical-continuity-audit", prompt)
        self.assertNotIn("Audit Module: forensic-physical-audit", prompt)

    def test_light_and_forensic_physical_audits_cannot_be_combined(self):
        with TemporaryDirectory() as directory:
            draft = Path(directory) / "draft.md"
            draft.write_text("她坐在后排。", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "do not combine"):
                compile_audit_prompt(
                    str(draft),
                    modules=["physical-continuity-audit"],
                    profiles=["physical"],
                )

    def test_no_strict_continuity_removes_all_physical_audits(self):
        with TemporaryDirectory() as directory:
            draft = Path(directory) / "draft.md"
            draft.write_text("A said B was trustworthy.", encoding="utf-8")
            prompt = compile_audit_prompt(str(draft), strict_continuity=False)
        self.assertNotIn("Audit Module: forensic-physical-audit", prompt)
        self.assertNotIn("Audit Module: physical-continuity-audit", prompt)
        self.assertNotIn("forensic physical continuity audit", prompt)
        self.assertIn("Audit Module: relationship-stance-audit", prompt)
        self.assertIn("Audit Module: ai-trace-rubric", prompt)

    def test_full_audit_does_not_load_optional_high_cost_profiles(self):
        with TemporaryDirectory() as directory:
            draft = Path(directory) / "draft.md"
            draft.write_text("她说：\u201c回来。\u201d他答：\u201c不。\u201d", encoding="utf-8")
            prompt = compile_audit_prompt(str(draft))
        self.assertNotIn("Audit Module: dialogue-voice-audit", prompt)
        self.assertNotIn("Audit Module: serial-reentry", prompt)
        self.assertNotIn("Audit Module: imagery-load-audit", prompt)
        self.assertNotIn("Audit Module: chapter-momentum-audit", prompt)
        self.assertNotIn("Audit Module: world-ontology-audit", prompt)
        self.assertNotIn("Audit Module: process-earnedness-audit", prompt)
        self.assertNotIn("Audit Module: attention-budget-audit", prompt)
        self.assertNotIn("Audit Module: chapter-pattern-audit", prompt)
        self.assertNotIn("Audit Module: source-grounding", prompt)
        self.assertNotIn("Audit Module: earned-ending-audit", prompt)

    def test_narrative_naturalness_audit_is_gated_for_serious_documents(self):
        with TemporaryDirectory() as directory:
            draft = Path(directory) / "draft.md"
            draft.write_text("The report presents the revised findings and limitations.", encoding="utf-8")
            fiction = compile_audit_prompt(str(draft), document_type="fiction")
            serious_prompts = [
                compile_audit_prompt(str(draft), document_type=document_type)
                for document_type in ("academic-paper", "formal-document", "news-report")
            ]
        self.assertIn("Audit Module: narrative-naturalness-audit", fiction)
        for prompt in serious_prompts:
            self.assertIn("Audit Module: ai-trace-rubric", prompt)
            self.assertNotIn("Audit Module: narrative-naturalness-audit", prompt)

    def test_relationship_profile_does_not_load_unrelated_audits(self):
        with TemporaryDirectory() as directory:
            draft = Path(directory) / "draft.md"
            draft.write_text("A praised C in front of B.", encoding="utf-8")
            prompt = compile_audit_prompt(str(draft), profiles=["relationship"])
        self.assertIn("Audit Module: relationship-state", prompt)
        self.assertIn("Audit Module: relationship-stance-audit", prompt)
        self.assertNotIn("Audit Module: forensic-physical-audit", prompt)
        self.assertNotIn("Audit Module: ai-trace-rubric", prompt)

    def test_numbers_profile_only_loads_number_audit(self):
        with TemporaryDirectory() as directory:
            draft = Path(directory) / "draft.md"
            draft.write_text("Her hand moved three centimeters.", encoding="utf-8")
            prompt = compile_audit_prompt(str(draft), profiles=["numbers"])
        self.assertIn("Audit Module: natural-measurement", prompt)
        self.assertNotIn("Audit Module: forensic-physical-audit", prompt)
        self.assertNotIn("Audit Module: ai-trace-rubric", prompt)

    def test_ai_trace_profile_catches_orphaned_interactions_without_voice_cost(self):
        with TemporaryDirectory() as directory:
            draft = Path(directory) / "draft.md"
            draft.write_text(
                "她只说了一句重要的话，随后叙述直接转向了窗外的天气。",
                encoding="utf-8",
            )
            prompt = compile_audit_prompt(str(draft), profiles=["ai-trace"])
        self.assertIn("Audit Module: prose-progress-audit", prompt)
        self.assertIn("Interaction Progress Test", prompt)
        self.assertIn("orphaned pressure-bearing interactions", prompt)
        self.assertNotIn("Audit Module: dialogue-voice-audit", prompt)

    def test_ai_trace_modules_keep_one_owner_per_pattern_family(self):
        with TemporaryDirectory() as directory:
            draft = Path(directory) / "draft.md"
            draft.write_text("这不是雨，是命运。比夜更黑，比梦更冷。", encoding="utf-8")
            prompt = compile_audit_prompt(
                str(draft),
                profiles=["ai-trace"],
                document_type="fiction",
            )
        self.assertIn("One span, one owner", prompt)
        self.assertIn("formulaic-structure-audit", prompt)
        self.assertIn("Do not report them again here", prompt)
        self.assertNotIn("Comparison ladders:", load_skill("cliche-phrase-audit").content)
        self.assertNotIn(
            "repeated contrast, comparison, rhetorical setup",
            load_skill("surface-pattern-audit").content,
        )

    def test_dialogue_performance_consumes_voice_response_map(self):
        voice = load_skill("dialogue-voice-audit").content
        performance = load_skill("dialogue-performance-audit").content
        self.assertIn("Response Obligation And Interaction Debt", voice)
        self.assertIn("owns response obligation and interaction debt", performance)
        self.assertIn("Use the listener uptake already established", performance)
        self.assertNotIn("Required uptake: none / immediate", performance)

    def test_ending_module_is_explicitly_gated_in_its_own_contract(self):
        ending = load_skill("earned-ending-audit").content
        self.assertIn("selects the `ending` audit profile", ending)
        self.assertIn("do not load this full tail audit automatically", ending)

    def test_logic_character_and_proofread_profiles_are_isolated(self):
        with TemporaryDirectory() as directory:
            draft = Path(directory) / "draft.md"
            draft.write_text("A decision caused a later consequence.", encoding="utf-8")
            logic = compile_audit_prompt(str(draft), profiles=["logic"])
            character = compile_audit_prompt(str(draft), profiles=["character"])
            proofread = compile_audit_prompt(str(draft), profiles=["proofread"])
        self.assertIn("Audit Module: logic-causality-audit", logic)
        self.assertNotIn("Audit Module: character-consistency-audit", logic)
        self.assertIn("Audit Module: character-consistency-audit", character)
        self.assertNotIn("Audit Module: logic-causality-audit", character)
        self.assertIn("Audit Module: proofreading-audit", proofread)
        self.assertIn("Missing-Word And Sentence-Skeleton Pass", proofread)
        self.assertNotIn("Audit Module: ai-trace-rubric", proofread)

    def test_generation_uses_light_omission_guard_without_full_proofread_module(self):
        prompt = compile_prompt("fiction", "Continue the scene.")
        self.assertIn("subjects, objects, complements", prompt)
        self.assertNotIn("Audit Module: proofreading-audit", prompt)

    def test_voice_serial_momentum_and_texture_profiles_are_isolated(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            draft = root / "draft.md"
            context = root / "ledger.md"
            draft.write_text("她说：\u201c别问。\u201d他答：\u201c我必须问。\u201d", encoding="utf-8")
            context.write_text("上一章结束时，两人仍在车站。", encoding="utf-8")
            voice = compile_audit_prompt(str(draft), profiles=["voice"])
            serial = compile_audit_prompt(
                str(draft),
                context_path=str(context),
                profiles=["serial"],
            )
            texture = compile_audit_prompt(str(draft), profiles=["texture"])
            momentum = compile_audit_prompt(str(draft), profiles=["momentum"])
        self.assertIn("Audit Module: dialogue-voice-audit", voice)
        self.assertIn("Audit Module: dialogue-performance-audit", voice)
        self.assertIn("Scene Speech Contract", voice)
        self.assertIn("Dialogue Performance Audit", voice)
        self.assertIn("Response Obligation And Interaction Debt", voice)
        self.assertIn("Common Ground And Subtext", voice)
        self.assertIn("occupational stereotype", voice)
        self.assertNotIn("Audit Module: serial-reentry", voice)
        self.assertIn("Audit Module: serial-reentry", serial)
        self.assertNotIn("Audit Module: dialogue-voice-audit", serial)
        self.assertIn("Audit Module: imagery-load-audit", texture)
        self.assertIn("Audit Module: paragraph-rhythm-audit", texture)
        self.assertIn("Audit Module: scene-entry-audit", texture)
        self.assertNotIn("Audit Module: dialogue-voice-audit", texture)
        self.assertIn("Audit Module: chapter-momentum-audit", momentum)
        self.assertNotIn("Audit Module: serial-reentry", momentum)

    def test_register_and_capability_profiles_are_isolated(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            draft = root / "draft.md"
            context = root / "ledger.md"
            draft.write_text("他说：\u201c俺也去。\u201d她答：\u201c好。\u201d", encoding="utf-8")
            context.write_text(
                "他说普通话，从未接触东北方言。当前为筑基后期，左臂受伤。",
                encoding="utf-8",
            )
            register = compile_audit_prompt(str(draft), profiles=["register"])
            capability = compile_audit_prompt(
                str(draft), context_path=str(context), profiles=["capability"]
            )
            with self.assertRaisesRegex(ValueError, "requires --context"):
                compile_audit_prompt(str(draft), profiles=["capability"])
        self.assertIn("Audit Module: speech-register-continuity", register)
        self.assertNotIn("Audit Module: dialogue-voice-audit", register)
        self.assertIn("Audit Module: capability-state-audit", capability)
        self.assertNotIn("Audit Module: world-ontology-audit", capability)

    def test_auto_detection_gates_register_and_capability_on_evidence(self):
        draft = "他说：\u201c俺也去。\u201d她问：\u201c你学的东北话？\u201d"
        context = "人物只说普通话，没有东北方言经历；当前战力为三级。"
        decisions = detect_audit_profiles(
            draft, context_active=True, context=context
        )
        selected = {item.profile for item in decisions if item.selected}
        self.assertTrue({"register", "capability"} <= selected)

        without_context = detect_audit_profiles(draft)
        without_selected = {item.profile for item in without_context if item.selected}
        self.assertIn("register", without_selected)
        self.assertNotIn("capability", without_selected)

    def test_new_deep_profiles_are_isolated(self):
        with TemporaryDirectory() as directory:
            draft = Path(directory) / "draft.md"
            draft.write_text("民国调查终于完成。", encoding="utf-8")
            world = compile_audit_prompt(str(draft), profiles=["world"])
            process = compile_audit_prompt(str(draft), profiles=["process"])
            salience = compile_audit_prompt(str(draft), profiles=["salience"])
            recurrence = compile_audit_prompt(str(draft), profiles=["recurrence"])
        self.assertIn("Audit Module: world-ontology-audit", world)
        self.assertNotIn("Audit Module: process-earnedness-audit", world)
        self.assertIn("Audit Module: process-earnedness-audit", process)
        self.assertIn("Audit Module: attention-budget-audit", salience)
        self.assertIn("Audit Module: chapter-pattern-audit", recurrence)

    def test_serial_profile_requires_prior_context(self):
        with TemporaryDirectory() as directory:
            draft = Path(directory) / "draft.md"
            draft.write_text("第二章开始了。", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "requires --context"):
                compile_audit_prompt(str(draft), profiles=["serial"])

    def test_auto_detection_keeps_core_and_skips_irrelevant_optional_stages(self):
        decisions = detect_audit_profiles(
            "This report evaluates policy outcomes and presents a cautious conclusion."
        )
        selected = {decision.profile for decision in decisions if decision.selected}
        self.assertEqual(selected, {"logic", "ai-trace", "proofread"})

    def test_auto_detection_selects_scene_specific_stages(self):
        decisions = detect_audit_profiles("她坐在后排说：董事长已经等了七秒。")
        selected = {decision.profile for decision in decisions if decision.selected}
        self.assertEqual(
            selected,
            {"logic", "character", "relationship", "physical", "ai-trace", "numbers", "proofread"},
        )

    def test_auto_detection_adds_new_profiles_only_on_matching_cues(self):
        draft = (
            "第二章。\n\n"
            "她说：\u201c你又迟到了。\u201d\n\n"
            "他低声答：\u201c路上出了事。\u201d\n\n"
            "她问：\u201c什么事？\u201d\n\n"
            "他说：\u201c现在不能讲。\u201d\n\n"
            "灯像一只眼睛，雨像旧胶片，门仿佛在喘气，走廊如同一条空船，夜色好似潮水。"
        )
        decisions = detect_audit_profiles(draft, context_active=True)
        selected = {decision.profile for decision in decisions if decision.selected}
        self.assertTrue({"voice", "serial", "texture"} <= selected)

    def test_auto_detection_uses_context_for_short_dialogue_review(self):
        draft = "她说：\u201c我只答应这一回。\u201d他问：\u201c条件呢？\u201d"
        without_context = detect_audit_profiles(draft)
        with_context = detect_audit_profiles(draft, context_active=True)
        self.assertIn("voice", {item.profile for item in without_context if item.selected})
        self.assertIn("voice", {item.profile for item in with_context if item.selected})

    def test_auto_detection_skips_serial_without_context(self):
        decisions = detect_audit_profiles("第二章，他想起上一章的争执。")
        selected = {decision.profile for decision in decisions if decision.selected}
        self.assertNotIn("serial", selected)

    def test_auto_detection_selects_momentum_only_for_multi_chapter_text(self):
        one = detect_audit_profiles("第一章 夜雨\n她推门进来。")
        many = detect_audit_profiles(
            "第一章 夜雨\n她推门进来。\n\n第二章 余波\n他还握着那封信。"
        )
        self.assertNotIn("momentum", {item.profile for item in one if item.selected})
        self.assertIn("momentum", {item.profile for item in many if item.selected})

    def test_auto_detection_selects_world_process_salience_and_recurrence_conservatively(self):
        short = detect_audit_profiles("她沿河走了一会儿。")
        short_selected = {item.profile for item in short if item.selected}
        self.assertFalse({"world", "process", "salience", "recurrence"} & short_selected)

        world_process = detect_audit_profiles("民国背景下，他们调查线索，最终查明了结果。")
        selected = {item.profile for item in world_process if item.selected}
        self.assertTrue({"world", "process"} <= selected)

        chapters = "\n\n".join(
            f"第{index}章 标题\n她说完后离开。" for index in ("一", "二", "三")
        )
        recurrence = {item.profile for item in detect_audit_profiles(chapters) if item.selected}
        self.assertTrue({"momentum", "recurrence"} <= recurrence)

        long_draft = "\n\n".join(["她看着门，想起上一章的争执。" * 30] * 12)
        salience = {item.profile for item in detect_audit_profiles(long_draft) if item.selected}
        self.assertIn("salience", salience)

    def test_auto_detection_gates_repetition_to_long_narrative_evidence(self):
        short = {item.profile for item in detect_audit_profiles("她知道他不想再谈。") if item.selected}
        dense = "\n\n".join(
            [
                "她知道对方不想再谈，一边收拾文件，一边等门锁响。"
                for _ in range(64)
            ]
        )
        selected = {item.profile for item in detect_audit_profiles(dense) if item.selected}
        serious = {
            item.profile
            for item in detect_audit_profiles(dense, serious_document=True)
            if item.selected
        }
        self.assertNotIn("repetition", short)
        self.assertIn("repetition", selected)
        self.assertNotIn("repetition", serious)

    def test_source_grounding_requires_sources_and_serious_document(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            draft = root / "draft.md"
            source = root / "source.md"
            draft.write_text("研究方法和结果见文献[1]。", encoding="utf-8")
            source.write_text("研究样本为120人，结果仅适用于本地区。", encoding="utf-8")
            prompt = compile_audit_prompt(
                str(draft),
                profiles=["sources"],
                source_paths=[str(source)],
                document_type="academic-paper",
                source_budget=1000,
            )
            with self.assertRaisesRegex(ValueError, "requires one or more --source"):
                compile_audit_prompt(
                    str(draft),
                    profiles=["sources"],
                    document_type="academic-paper",
                )
            with self.assertRaisesRegex(ValueError, "limited to serious"):
                compile_audit_prompt(
                    str(draft),
                    profiles=["sources"],
                    source_paths=[str(source)],
                    document_type="fiction",
                )
        self.assertIn("Audit Module: source-grounding", prompt)
        self.assertIn("Supplied Factual Sources", prompt)
        self.assertIn("Source: source.md", prompt)

    def test_source_grounding_auto_activates_only_for_serious_generation(self):
        with TemporaryDirectory() as directory:
            source = Path(directory) / "source.md"
            source.write_text("The measured result was 18 percent.", encoding="utf-8")
            academic = compile_prompt(
                "academic-paper",
                "Write the results section.",
                source_paths=[str(source)],
            )
            fiction = compile_prompt(
                "fiction",
                "Write the next scene.",
                source_paths=[str(source)],
            )
        self.assertIn("Technique Module: source-grounding", academic)
        self.assertIn("Supplied Factual Sources", academic)
        self.assertNotIn("Technique Module: source-grounding", fiction)
        self.assertNotIn("Supplied Factual Sources", fiction)

    def test_auto_detection_sends_cinematic_opening_stack_to_texture(self):
        decisions = detect_audit_profiles(
            "第一章 抵达\n傍晚六点半，临港机场二号航站楼，落日照着玻璃。"
            "她身穿深色制服，心里莫名有一股说不清的感觉。"
        )
        self.assertIn("texture", {item.profile for item in decisions if item.selected})

    def test_pipeline_writes_independent_stage_prompts_and_manifest(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            draft = root / "draft.md"
            output = root / "pipeline"
            draft.write_text("她坐在后排说：董事长已经等了七秒。", encoding="utf-8")
            written, stages = write_audit_pipeline(
                str(draft),
                str(output),
                auto=True,
            )
            logic_prompt = (written / "01-logic.md").read_text(encoding="utf-8")
            manifest = (written / "README.md").read_text(encoding="utf-8")
            lint_report = (written / "00-pattern-lint.json").read_text(encoding="utf-8")
        self.assertEqual(len(stages), 7)
        self.assertIn("Audit Module: logic-causality-audit", logic_prompt)
        self.assertNotIn("Audit Module: character-consistency-audit", logic_prompt)
        self.assertIn("fresh model conversation", manifest)
        self.assertIn("Detected exact-number cue", manifest)
        self.assertIn("Pattern lint style", manifest)
        self.assertIn('"disclaimer"', lint_report)

    def test_pipeline_adds_style_match_only_with_reference(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            draft = root / "draft.md"
            reference = root / "reference.md"
            draft.write_text("一份没有人物动作的说明文本。", encoding="utf-8")
            reference.write_text("句子很短。偶尔很长，但不解释。", encoding="utf-8")
            without_reference, _ = write_audit_pipeline(
                str(draft),
                str(root / "without-reference"),
                auto=True,
            )
            with_reference, stages = write_audit_pipeline(
                str(draft),
                str(root / "with-reference"),
                auto=True,
                reference_paths=[str(reference)],
            )
            without_manifest = (without_reference / "README.md").read_text(encoding="utf-8")
            with_manifest = (with_reference / "README.md").read_text(encoding="utf-8")
        self.assertNotIn("| `style-match` | yes |", without_manifest)
        self.assertIn("| `style-match` | yes |", with_manifest)
        self.assertIn("style-match", [stage.profile for stage in stages])

    def test_pipeline_adds_one_fidelity_stage_only_with_original(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            original = root / "original.md"
            draft = root / "draft.md"
            original.write_text("约有一半用户表示不确定。", encoding="utf-8")
            draft.write_text("80%的用户表示满意。", encoding="utf-8")
            _, stages = write_audit_pipeline(
                str(draft),
                str(root / "pipeline"),
                auto=True,
                original_path=str(original),
            )
            fidelity = [stage for stage in stages if stage.profile == "fidelity"]
            self.assertEqual(len(fidelity), 1)
            self.assertIn("约有一半", fidelity[0].prompt)
            self.assertTrue(
                all("约有一半" not in stage.prompt for stage in stages if stage.profile != "fidelity")
            )

    def test_pipeline_preservation_is_explicit_and_original_gated(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            original = root / "original.md"
            draft = root / "draft.md"
            original.write_text("我没生气。算了，我不说了。", encoding="utf-8")
            draft.write_text("我没有生气，只是不想讨论。", encoding="utf-8")
            _, automatic = write_audit_pipeline(
                str(draft),
                str(root / "auto"),
                auto=True,
                original_path=str(original),
            )
            _, explicit = write_audit_pipeline(
                str(draft),
                str(root / "explicit"),
                stages=["preservation"],
                original_path=str(original),
            )
            with self.assertRaisesRegex(ValueError, "requires --original"):
                write_audit_pipeline(
                    str(draft),
                    str(root / "missing"),
                    stages=["preservation"],
                )
        self.assertNotIn("preservation", [stage.profile for stage in automatic])
        self.assertEqual([stage.profile for stage in explicit], ["preservation"])
        self.assertIn("Audit Module: voice-ambiguity-preservation", explicit[0].prompt)

    def test_pipeline_writes_statistics_only_when_requested(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            draft = root / "draft.md"
            draft.write_text("第一句很短。第二句也很短。第三句仍然很短。" * 4, encoding="utf-8")
            plain, _ = write_audit_pipeline(str(draft), str(root / "plain"), stages=["ai-trace"])
            measured, _ = write_audit_pipeline(
                str(draft),
                str(root / "measured"),
                stages=["ai-trace"],
                with_stats=True,
            )
            self.assertFalse((plain / "00-style-stats.json").exists())
            self.assertTrue((measured / "00-style-stats.json").exists())

    def test_pipeline_sources_are_serious_only_and_isolated(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            draft = root / "paper.md"
            source = root / "study.md"
            draft.write_text("研究方法和结果见文献[1]。", encoding="utf-8")
            source.write_text("SOURCE_ONLY_MARKER: 样本为120人。", encoding="utf-8")
            written, stages = write_audit_pipeline(
                str(draft),
                str(root / "pipeline"),
                auto=True,
                source_paths=[str(source)],
                document_type="academic-paper",
            )
            source_stage = next(stage for stage in stages if stage.profile == "sources")
            logic_stage = next(stage for stage in stages if stage.profile == "logic")
            source_prompt = (written / f"{source_stage.order:02d}-sources.md").read_text(
                encoding="utf-8"
            )
            logic_prompt = (written / f"{logic_stage.order:02d}-logic.md").read_text(
                encoding="utf-8"
            )
        self.assertIn("SOURCE_ONLY_MARKER", source_prompt)
        self.assertNotIn("SOURCE_ONLY_MARKER", logic_prompt)
        self.assertEqual([stage.profile for stage in stages].count("sources"), 1)

    def test_cli_reports_missing_draft_without_traceback(self):
        stderr = StringIO()
        with redirect_stderr(stderr), self.assertRaises(SystemExit) as raised:
            main(["audit", "--draft", "missing-draft.md"])
        self.assertEqual(raised.exception.code, 2)
        self.assertIn("missing-draft.md", stderr.getvalue())
        self.assertNotIn("Traceback", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
