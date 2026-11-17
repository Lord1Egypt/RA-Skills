import unittest

from optimize_prompt_v1 import OptimizerConfig, PromptOptimizer, PromptIR
from optimize_prompt_v1.model import ModelOptimization, RetryableModelError


LONG_PREFIX = "这是为了下游执行而准备的详细请求，请在完全保留约束的情况下整理内容。"


class FakeModel:
    def __init__(self, response):
        self.response = response
        self.calls = 0

    def optimize(self, prompt):
        self.calls += 1
        return self.response


class SequenceModel:
    def __init__(self, outcomes):
        self.outcomes = list(outcomes)
        self.calls = 0

    def optimize(self, prompt):
        outcome = self.outcomes[self.calls]
        self.calls += 1
        if isinstance(outcome, Exception):
            raise outcome
        return outcome


def configured(model=None):
    return PromptOptimizer(
        config=OptimizerConfig(min_chars_for_model=30, min_tokens_for_model=10),
        model=model,
    )


class OptimizerTests(unittest.TestCase):
    def test_retryable_model_error_retries_then_succeeds(self):
        original = LONG_PREFIX + "总结 notes.txt 并输出英文。"
        response = ModelOptimization("passthrough", original, PromptIR(actions=["总结"], entities=["notes.txt"], outputs=["输出英文"]), 0.9, 88, None, ["目标明确"], [])
        model = SequenceModel([RetryableModelError("rate limited"), response])
        result = configured(model).optimize(original)
        self.assertEqual(model.calls, 2)
        self.assertEqual(result.fallback_reason, "")

    def test_retry_exhaustion_safely_passes_original(self):
        original = LONG_PREFIX + "总结 notes.txt 并输出英文。"
        model = SequenceModel([RetryableModelError("timeout")] * 3)
        result = configured(model).optimize(original)
        self.assertEqual(model.calls, 3)
        self.assertEqual(result.optimized_prompt, original)
        self.assertEqual(result.fallback_reason, "model_error")

    def test_invalid_model_response_does_not_retry(self):
        original = LONG_PREFIX + "总结 notes.txt 并输出英文。"
        response = ModelOptimization("optimized", "", PromptIR(), 0.9)
        model = FakeModel(response)
        result = configured(model).optimize(original)
        self.assertEqual(model.calls, 1)
        self.assertEqual(result.optimized_prompt, original)
        self.assertEqual(result.fallback_reason, "invalid_model_response")

    def test_invalid_confidence_does_not_change_route(self):
        original = LONG_PREFIX + "总结 notes.txt 并输出英文。"
        response = ModelOptimization("passthrough", original, PromptIR(actions=["总结"], entities=["notes.txt"], outputs=["输出英文"]), "high", 80)  # type: ignore[arg-type]
        result = configured(FakeModel(response)).optimize(original)
        self.assertEqual(result.mode, "passthrough")
        self.assertEqual(result.confidence, 0)
        self.assertEqual(result.confidence_status, "invalid")

    def test_score_feedback_separates_learning_feedback(self):
        original = LONG_PREFIX + "你好，麻烦总结 notes.txt 并输出英文，谢谢。"
        response = ModelOptimization("optimized", "总结 notes.txt；输出英文。", PromptIR(actions=["总结"], entities=["notes.txt"], outputs=["输出英文"]), 0.9, 70, None, ["目标明确"], ["删除礼貌性填充"])
        result = configured(FakeModel(response)).optimize(original)
        self.assertEqual(result.score_feedback["strengths"], ["目标明确"])
        self.assertEqual(result.score_feedback["improvements"], ["删除礼貌性填充"])

    def test_negation_scope_swap_is_rejected(self):
        original = LONG_PREFIX + "不要删除 A，可以删除 B。"
        response = ModelOptimization("optimized", "可以删除 A，不要删除 B。", PromptIR(actions=["删除 A", "删除 B"], constraints=["不要删除"], entities=["A", "B"]), 0.9, 60)
        result = configured(FakeModel(response)).optimize(original)
        self.assertTrue(result.validation_failed)
        self.assertIn("不要删除 A", result.validation["negation_scope_mismatches"])

    def test_pre_gate_passthrough_is_not_scored(self):
        result = configured(FakeModel(None)).optimize("将 README.md 翻译成中文。")
        self.assertIsNone(result.original_prompt_score)
        self.assertEqual(result.score_status, "not_scored")
        self.assertEqual(result.score_reasons, [])

    def test_model_score_is_exposed_for_ui(self):
        original = LONG_PREFIX + "你好，麻烦帮我总结 notes.txt，谢谢。"
        response = ModelOptimization(
            "optimized",
            "总结 notes.txt。",
            PromptIR(actions=["总结"], entities=["notes.txt"]),
            0.95,
            68,
            ["目标明确", "存在礼貌用语和口语填充"],
        )
        result = configured(FakeModel(response)).optimize(original)
        self.assertEqual(result.original_prompt_score, 68)
        self.assertEqual(result.score_status, "scored")
        self.assertEqual(result.score_reasons, ["目标明确", "存在礼貌用语和口语填充"])

    def test_high_score_does_not_override_model_route(self):
        original = LONG_PREFIX + "整理 report.pdf 的内容并输出中文摘要。"
        response = ModelOptimization(
            "optimized",
            "整理 report.pdf；输出中文摘要。",
            PromptIR(actions=["整理"], entities=["report.pdf"], outputs=["输出中文摘要"]),
            0.95,
            96,
            ["意图清晰", "输出要求明确"],
        )
        result = configured(FakeModel(response)).optimize(original)
        self.assertEqual(result.original_prompt_score, 96)
        self.assertEqual(result.mode, "optimized")

    def test_low_score_does_not_override_model_passthrough(self):
        original = LONG_PREFIX + "总结 notes.txt 并输出英文。"
        response = ModelOptimization(
            "passthrough",
            original,
            PromptIR(actions=["总结"], entities=["notes.txt"], outputs=["输出英文"]),
            0.9,
            45,
            ["表达可以更简洁"],
        )
        result = configured(FakeModel(response)).optimize(original)
        self.assertEqual(result.original_prompt_score, 45)
        self.assertEqual(result.mode, "passthrough")

    def test_invalid_score_is_ignored_without_changing_route(self):
        original = LONG_PREFIX + "总结 notes.txt 并输出英文。"
        response = ModelOptimization(
            "passthrough",
            original,
            PromptIR(actions=["总结"], entities=["notes.txt"], outputs=["输出英文"]),
            0.9,
            120,
            ["目标清晰"],
        )
        result = configured(FakeModel(response)).optimize(original)
        self.assertIsNone(result.original_prompt_score)
        self.assertEqual(result.score_status, "invalid")
        self.assertEqual(result.mode, "passthrough")
        self.assertTrue(any("invalid original_prompt_score" in warning for warning in result.warnings))

    def test_data_uri_is_pre_gate_passthrough(self):
        model = FakeModel(None)
        text = "请分析图片：data:image/jpeg;base64," + ("A" * 300)
        result = configured(model).optimize(text)
        self.assertEqual(result.mode, "passthrough")
        self.assertEqual(result.gate_reason, "contains_base64_data")
        self.assertEqual(result.fallback_reason, "")
        self.assertEqual(model.calls, 0)

    def test_long_bare_base64_is_pre_gate_passthrough(self):
        model = FakeModel(None)
        text = "处理以下编码：" + ("QUJD" * 70)
        result = configured(model).optimize(text)
        self.assertEqual(result.gate_reason, "contains_base64_data")
        self.assertEqual(model.calls, 0)

    def test_code_block_dominant_prompt_is_passthrough(self):
        model = FakeModel(None)
        code = "\n".join(f"value_{i} = {i}" for i in range(80))
        text = f"帮我重构这段代码：\n```python\n{code}\n```"
        result = configured(model).optimize(text)
        self.assertEqual(result.gate_reason, "code_block_dominant")
        self.assertEqual(model.calls, 0)

    def test_short_code_example_does_not_trigger_code_gate(self):
        original = LONG_PREFIX + "解释下面示例并给出改进建议：\n```python\nprint('ok')\n```"
        response = ModelOptimization("passthrough", original, PromptIR(actions=["解释", "给出改进建议"]), 0.9)
        model = FakeModel(response)
        result = configured(model).optimize(original)
        self.assertNotEqual(result.gate_reason, "code_block_dominant")
        self.assertEqual(model.calls, 1)

    def test_structured_xml_is_pre_gate_passthrough(self):
        model = FakeModel(None)
        text = "<context>项目 Alpha 的发布资料</context><user_query>生成发布检查表</user_query>"
        result = configured(model).optimize(text)
        self.assertEqual(result.gate_reason, "structured_xml_tags")
        self.assertEqual(model.calls, 0)

    def test_arbitrary_html_tag_does_not_trigger_xml_gate(self):
        original = LONG_PREFIX + "请解释 HTML 中的 <div>内容</div> 标签，并输出中文说明。"
        response = ModelOptimization("passthrough", original, PromptIR(actions=["解释"], entities=["<div>内容</div>"], outputs=["输出中文说明"]), 0.9)
        model = FakeModel(response)
        result = configured(model).optimize(original)
        self.assertNotEqual(result.gate_reason, "structured_xml_tags")
        self.assertEqual(model.calls, 1)

    def test_filler_heavy_prompt_is_optimized_by_model(self):
        original = "你好，麻烦帮我一下，就是请帮我生成一份本周工作周报，非常感谢。"
        response = ModelOptimization(
            "optimized",
            "生成一份本周工作周报。",
            PromptIR(actions=["生成"], entities=["本周工作周报"]),
            0.96,
        )
        model = FakeModel(response)
        optimizer = PromptOptimizer(
            config=OptimizerConfig(min_chars_for_model=20, min_tokens_for_model=12),
            model=model,
        )
        result = optimizer.optimize(original)
        self.assertEqual(model.calls, 1)
        self.assertEqual(result.mode, "optimized")
        self.assertEqual(result.optimized_prompt, "生成一份本周工作周报。")
        self.assertNotIn("麻烦", result.optimized_prompt)
        self.assertNotIn("感谢", result.optimized_prompt)
        self.assertGreater(result.compression_ratio, 0)

    def test_short_prompt_is_pre_gate_passthrough_without_model(self):
        model = FakeModel(None)
        result = configured(model).optimize("将 README.md 翻译成中文。")
        self.assertEqual(result.mode, "passthrough")
        self.assertEqual(result.gate_reason, "too_short")
        self.assertEqual(model.calls, 0)

    def test_json_is_pre_gate_passthrough(self):
        model = FakeModel(None)
        text = '{"tool":"search","query":"a sufficiently long machine request that must remain exact"}'
        result = configured(model).optimize(text)
        self.assertEqual(result.gate_reason, "json_input")
        self.assertEqual(model.calls, 0)

    def test_tool_call_is_pre_gate_passthrough(self):
        model = FakeModel(None)
        text = "send_email(recipient='a@example.com', draft=true, body='this is deliberately long')"
        result = configured(model).optimize(text)
        self.assertEqual(result.gate_reason, "machine_instruction")
        self.assertEqual(model.calls, 0)

    def test_regular_natural_language_reaches_model(self):
        original = LONG_PREFIX + "总结 notes.txt，输出英文。"
        response = ModelOptimization("passthrough", original, PromptIR(actions=["总结"], entities=["notes.txt"], outputs=["输出英文"]), 0.99)
        model = FakeModel(response)
        result = configured(model).optimize(original)
        self.assertEqual(result.mode, "passthrough")
        self.assertEqual(model.calls, 1)

    def test_valid_one_shot_optimization(self):
        original = LONG_PREFIX + "分析 report.pdf 中 2026-01-01 至 2026-03-31 的数据，不要修改文件，输出 JSON。"
        response = ModelOptimization(
            "optimized",
            "分析 report.pdf 中 2026-01-01 至 2026-03-31 的数据；不要修改文件；输出 JSON。",
            PromptIR(actions=["分析"], entities=["report.pdf", "2026-01-01", "2026-03-31"], constraints=["不要修改文件"], outputs=["输出 JSON"]),
            0.96,
        )
        result = configured(FakeModel(response)).optimize(original)
        self.assertEqual(result.mode, "optimized")
        self.assertFalse(result.validation_failed)
        self.assertEqual(result.prompt_ir["actions"], ["分析"])

    def test_missing_number_falls_back_to_original(self):
        original = LONG_PREFIX + "统计 3 个项目，预算 ¥50,000，输出 JSON。"
        response = ModelOptimization("optimized", "统计项目，预算 ¥50,000，输出 JSON。", PromptIR(actions=["统计"], entities=["¥50,000"], outputs=["输出 JSON"]), 0.9)
        result = configured(FakeModel(response)).optimize(original)
        self.assertTrue(result.validation_failed)
        self.assertEqual(result.optimized_prompt, original)
        self.assertIn("3", result.validation["missing_literals"])

    def test_missing_negation_falls_back(self):
        original = LONG_PREFIX + "分析 app.py，但不要修改文件，输出中文。"
        response = ModelOptimization("optimized", "分析 app.py 并修改文件，输出中文。", PromptIR(actions=["分析"], entities=["app.py"], outputs=["输出中文"]), 0.9)
        result = configured(FakeModel(response)).optimize(original)
        self.assertTrue(result.validation_failed)
        self.assertIn("不要", result.validation["missing_literals"])

    def test_unsupported_parameter_falls_back(self):
        original = LONG_PREFIX + "总结 report.pdf 并输出列表。"
        response = ModelOptimization("optimized", "总结 report.pdf 的 10 页内容并输出列表。", PromptIR(actions=["总结"], entities=["report.pdf"], outputs=["输出列表"]), 0.9)
        result = configured(FakeModel(response)).optimize(original)
        self.assertTrue(result.validation_failed)
        self.assertIn("10", result.validation["unsupported_additions"])

    def test_url_percentage_date_function_and_filename_are_preserved(self):
        original = LONG_PREFIX + "读取 https://example.com/a 和 app.py，调用 run_job()，检查 25% 与 2026/07/11，输出 JSON。"
        response = ModelOptimization(
            "optimized", "读取 https://example.com/a、app.py；调用 run_job()；检查 25%、2026/07/11；输出 JSON。",
            PromptIR(actions=["读取", "调用 run_job()", "检查"], entities=["https://example.com/a", "app.py", "25%", "2026/07/11"], outputs=["输出 JSON"]), 0.95,
        )
        result = configured(FakeModel(response)).optimize(original)
        self.assertFalse(result.validation_failed)

    def test_ir_item_must_trace_to_original(self):
        original = LONG_PREFIX + "总结 report.pdf，输出中文。"
        response = ModelOptimization("optimized", "总结 report.pdf，输出中文。", PromptIR(actions=["总结"], entities=["report.pdf", "客户机密"], outputs=["输出中文"]), 0.9)
        result = configured(FakeModel(response)).optimize(original)
        self.assertTrue(result.validation_failed)
        self.assertIn("客户机密", result.validation["ir_untraceable_items"])

    def test_optimized_literals_must_exist_in_ir(self):
        original = LONG_PREFIX + "总结 report.pdf，输出中文。"
        response = ModelOptimization("optimized", "总结 report.pdf，输出中文。", PromptIR(actions=["总结"], outputs=["输出中文"]), 0.9)
        result = configured(FakeModel(response)).optimize(original)
        self.assertTrue(result.validation_failed)
        self.assertIn("report.pdf", result.validation["prompt_ir_mismatches"])

    def test_model_conservative_mode_is_retained_when_valid(self):
        original = LONG_PREFIX + "考虑删除 old.csv，但可能只生成方案，不要执行删除。"
        response = ModelOptimization("conservative", original, PromptIR(actions=["考虑删除"], entities=["old.csv"], constraints=["可能只生成方案", "不要执行删除"], ambiguities=["可能只生成方案"], risk_flags=["删除"]), 0.7)
        result = configured(FakeModel(response)).optimize(original)
        self.assertEqual(result.mode, "conservative")
        self.assertFalse(result.validation_failed)
        self.assertEqual(result.optimized_prompt, original)

    def test_high_risk_conservative_rewrite_never_reaches_downstream(self):
        original = LONG_PREFIX + "删除 production 数据库中的用户表。"
        response = ModelOptimization(
            "conservative",
            "立即删除 production 数据库中的用户表。",
            PromptIR(actions=["删除"], entities=["production 数据库", "用户表"], risk_flags=["删除"]),
            0.8,
        )
        result = configured(FakeModel(response)).optimize(original)
        self.assertEqual(result.mode, "conservative")
        self.assertEqual(result.optimized_prompt, original)
        self.assertNotIn("立即删除", result.optimized_prompt)
        self.assertIn("删除", result.prompt_ir["risk_flags"])

    def test_metrics_only_describe_optimization_quality(self):
        original = LONG_PREFIX + "总结 notes.txt，输出英文。"
        response = ModelOptimization("passthrough", original, PromptIR(actions=["总结"], entities=["notes.txt"], outputs=["输出英文"]), 0.99)
        optimizer = configured(FakeModel(response))
        result = optimizer.optimize(original)
        snapshot = optimizer.metrics.snapshot()
        self.assertEqual(result.compression_ratio, 0)
        self.assertEqual(snapshot["average_compression_ratio"], 0)
        self.assertEqual(snapshot["average_confidence"], 0.99)
        self.assertNotIn("estimated_net_saving", snapshot)


if __name__ == "__main__":
    unittest.main()
