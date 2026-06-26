#!/usr/bin/env python3
"""
Test suite for Cost Watchdog scripts.
Run with: python3 -m unittest tests.test_cost_watchdog
"""

import json
import os
import sys
import unittest
import subprocess
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

# Force the router to ignore network sources during tests so sentinel prices
# stay deterministic regardless of what LiteLLM reports today.
os.environ["CW_STATIC_ONLY"] = "1"

import _pricing   # noqa: E402
import _sources   # noqa: E402


class TestDocumentation(unittest.TestCase):
    """Test documentation completeness."""
    
    def test_readme_exists(self):
        """Test that README.md exists."""
        readme_path = Path(__file__).parent.parent / "README.md"
        self.assertTrue(readme_path.exists())
    
    def test_skill_md_exists(self):
        """Test that SKILL.md exists."""
        skill_path = Path(__file__).parent.parent / "SKILL.md"
        self.assertTrue(skill_path.exists())
    
    def test_license_exists(self):
        """Test that LICENSE exists."""
        license_path = Path(__file__).parent.parent / "LICENSE"
        self.assertTrue(license_path.exists())
    
    def test_scripts_exist(self):
        """Test that all scripts exist."""
        scripts_dir = Path(__file__).parent.parent / "scripts"
        self.assertTrue((scripts_dir / "cost-visualizer.py").exists())
        self.assertTrue((scripts_dir / "smart-budget.py").exists())
    
    def test_reference_files_exist(self):
        """Test that all reference files exist."""
        refs_dir = Path(__file__).parent.parent / "references"
        required_files = ["pricing.md", "optimization.md", "patterns.md", "calculators.md"]
        
        for filename in required_files:
            self.assertTrue((refs_dir / filename).exists(), f"{filename} not found")


class TestPricingData(unittest.TestCase):
    """Test pricing data integrity."""
    
    def test_pricing_file_exists(self):
        """Test that pricing.md exists."""
        pricing_path = Path(__file__).parent.parent / "references" / "pricing.md"
        self.assertTrue(pricing_path.exists())
    
    def test_pricing_file_not_empty(self):
        """Test that pricing.md has content."""
        pricing_path = Path(__file__).parent.parent / "references" / "pricing.md"
        content = pricing_path.read_text()
        self.assertGreater(len(content), 1000)
    
    def test_all_providers_documented(self):
        """The major providers we care about are present in pricing.md."""
        pricing_path = Path(__file__).parent.parent / "references" / "pricing.md"
        content = pricing_path.read_text()

        # Core set we always expect; regenerator may emit others too.
        must_have = ["Anthropic", "OpenAI", "Google", "OpenRouter"]
        for provider in must_have:
            self.assertIn(provider, content, f"{provider} not found in pricing.md")


class TestScriptsExecution(unittest.TestCase):
    """Test that scripts execute without errors."""
    
    def test_cost_visualizer_help(self):
        """Test cost-visualizer.py shows help."""
        result = subprocess.run(
            ["python3", "scripts/cost-visualizer.py"],
            capture_output=True,
            text=True,
            cwd=str(Path(__file__).parent.parent)
        )
        self.assertIn("Usage:", result.stdout)
        self.assertIn("Commands:", result.stdout)
    
    def test_smart_budget_help(self):
        """Test smart-budget.py shows help."""
        result = subprocess.run(
            ["python3", "scripts/smart-budget.py"],
            capture_output=True,
            text=True,
            cwd=str(Path(__file__).parent.parent)
        )
        self.assertIn("Usage:", result.stdout)
        self.assertIn("Commands:", result.stdout)
    
    def test_cost_visualizer_daily(self):
        """Test cost-visualizer.py daily command."""
        result = subprocess.run(
            ["python3", "scripts/cost-visualizer.py", "daily"],
            capture_output=True,
            text=True,
            cwd=str(Path(__file__).parent.parent)
        )
        self.assertIn("Daily Cost Report", result.stdout)
    
    def test_smart_budget_set(self):
        """Test smart-budget.py set command."""
        result = subprocess.run(
            ["python3", "scripts/smart-budget.py", "set", "10.00", "--priority=high"],
            capture_output=True,
            text=True,
            cwd=str(Path(__file__).parent.parent)
        )
        self.assertIn("Budget set", result.stdout)
    
    def test_smart_budget_alternatives(self):
        """Test smart-budget.py alternatives command."""
        result = subprocess.run(
            ["python3", "scripts/smart-budget.py", "alternatives", "claude-sonnet-4-6", "--savings=50"],
            capture_output=True,
            text=True,
            cwd=str(Path(__file__).parent.parent)
        )
        self.assertIn("Cheaper alternatives", result.stdout)


class TestPricingLoader(unittest.TestCase):
    """Tests for _pricing, the single source of truth for model pricing."""

    def test_load_pricing_populates_many_models(self):
        pricing = _pricing.load_pricing()
        # Multi-modal regenerated pricing.md has thousands of entries.
        self.assertGreater(len(pricing), 1000, "Expected >1000 models in pricing.md")

    def test_multiple_units_represented(self):
        """pricing.md should now contain non-token units too."""
        pricing = _pricing.load_pricing()
        units = {p.unit for p in pricing.values()}
        self.assertIn("token", units)
        self.assertIn("image", units, "image-generation models should be present")
        # Second and query are nice-to-haves; assert if present don't crash.
        self.assertGreater(len(units), 1, "Expected >1 billing unit in pricing.md")

    def test_multiple_modes_represented(self):
        pricing = _pricing.load_pricing()
        modes = {p.mode for p in pricing.values()}
        self.assertIn("chat", modes)
        self.assertIn("image_generation", modes, "expected image_generation models")
        self.assertIn("embedding", modes, "expected embedding models")

    def test_known_models_have_expected_prices(self):
        """Sentinel prices from the regenerated pricing.md (LiteLLM-aligned slugs)."""
        cases = {
            "claude-sonnet-4-6": (3.0, 15.0),
            "claude-opus-4-7":   (5.0, 25.0),
            "claude-haiku-4-5":  (1.0, 5.0),
            "gpt-4o":            (2.50, 10.00),
            "gpt-4o-mini":       (0.15, 0.60),
        }
        for slug, (want_in, want_out) in cases.items():
            price = _pricing.get_price(slug)
            self.assertIsNotNone(price, f"{slug} missing from pricing.md")
            self.assertAlmostEqual(price.input_per_1m, want_in, places=6, msg=slug)
            self.assertAlmostEqual(price.output_per_1m, want_out, places=6, msg=slug)

    def test_gpt4o_not_conflated_with_gpt4o_mini(self):
        """Regression: old substring lookup matched 'gpt-4o' inside 'gpt-4o-mini'."""
        full = _pricing.get_price("gpt-4o")
        mini = _pricing.get_price("gpt-4o-mini")
        self.assertIsNotNone(full)
        self.assertIsNotNone(mini)
        self.assertNotEqual(full.input_per_1m, mini.input_per_1m)
        self.assertGreater(full.input_per_1m, mini.input_per_1m)

    def test_unknown_model_returns_none(self):
        self.assertIsNone(_pricing.get_price("totally-fake-model-xyz"))

    def test_require_price_raises_for_unknown(self):
        with self.assertRaises(KeyError):
            _pricing.require_price("totally-fake-model-xyz")

    def test_canonical_slug_is_case_insensitive(self):
        a = _pricing.get_price("Claude-Sonnet-4-6")
        b = _pricing.get_price("claude-sonnet-4-6")
        self.assertIsNotNone(a)
        self.assertEqual(a, b)

    def test_find_cheaper_alternatives_exact_match(self):
        """Regression: substring match made every model look cheaper than itself."""
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "optimized_calculator", SCRIPTS_DIR / "optimized-calculator.py"
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

        alts = mod.find_cheaper_alternatives("claude-opus-4-7", 100_000, 20_000, min_savings=0.5)
        self.assertTrue(alts, "expected cheaper alternatives to Opus")
        slugs = [a["model"] for a in alts]
        self.assertNotIn("claude-opus-4-7", slugs, "alternatives must exclude the source model")


class TestTrackerWrappers(unittest.TestCase):
    """SDK wrappers log usage and enforce budgets."""

    def setUp(self):
        # Isolate each test to its own usage log.
        import tempfile, usage_log as ul
        self._tmp = tempfile.mkdtemp()
        self._orig = ul.USAGE_LOG
        ul.USAGE_LOG = Path(self._tmp) / "usage.jsonl"
        self._ul = ul

    def tearDown(self):
        import shutil
        self._ul.USAGE_LOG = self._orig
        shutil.rmtree(self._tmp, ignore_errors=True)

    def _fake_openai_response(self, model="gpt-4o", inp=100, out=50):
        """Construct an object shaped like an OpenAI chat.completions.create response."""
        import tracker
        return tracker._StubNamespace(
            model=model,
            usage=tracker._StubNamespace(
                prompt_tokens=inp,
                completion_tokens=out,
                prompt_tokens_details=tracker._StubNamespace(cached_tokens=0),
            ),
            system_fingerprint="fp_test",
        )

    def _fake_anthropic_response(self, model="claude-sonnet-4-6", inp=200, out=60):
        import tracker
        return tracker._StubNamespace(
            model=model,
            stop_reason="end_turn",
            usage=tracker._StubNamespace(
                input_tokens=inp,
                output_tokens=out,
                cache_read_input_tokens=0,
                cache_creation_input_tokens=0,
            ),
        )

    def test_openai_wrapper_logs_usage(self):
        import tracker
        resp = self._fake_openai_response(model="gpt-4o", inp=1_000_000, out=100_000)
        client = tracker._make_fake_openai_client(resp)
        client = tracker.track_openai(client, source="test-openai", session_id="s1")
        # Invoke as a user would
        returned = client.chat.completions.create(messages=[])
        self.assertIs(returned, resp)

        rows = self._ul.read_recent(limit=5)
        self.assertEqual(len(rows), 1)
        row = rows[0]
        self.assertEqual(row["source"], "test-openai")
        self.assertEqual(row["model"], "gpt-4o")
        self.assertEqual(row["input_tokens"], 1_000_000)
        self.assertEqual(row["output_tokens"], 100_000)
        self.assertGreater(row["cost_total"], 0, "should be priced from _pricing")
        self.assertEqual(row["session_id"], "s1")

    def test_anthropic_wrapper_logs_usage(self):
        import tracker
        resp = self._fake_anthropic_response(inp=10_000, out=2_000)
        client = tracker._make_fake_anthropic_client(resp)
        client = tracker.track_anthropic(client, source="test-anthropic", session_id="s2")
        client.messages.create(messages=[])

        rows = self._ul.read_recent(limit=5)
        self.assertEqual(len(rows), 1)
        row = rows[0]
        self.assertEqual(row["provider"], "anthropic")
        self.assertEqual(row["input_tokens"], 10_000)
        self.assertEqual(row["output_tokens"], 2_000)
        self.assertEqual(row["extra"]["stop_reason"], "end_turn")

    def test_budget_enforcement_raises(self):
        import tracker
        os.environ["CW_BUDGET_USD"] = "0.01"
        try:
            # Large GPT-4o call: 5M input tokens at $2.50/1M = $12.50 -> way over $0.01
            resp = self._fake_openai_response(model="gpt-4o", inp=5_000_000, out=100)
            client = tracker.track_openai(tracker._make_fake_openai_client(resp), session_id="budget-test")
            with self.assertRaises(tracker.BudgetExceeded):
                client.chat.completions.create(messages=[])
        finally:
            os.environ.pop("CW_BUDGET_USD", None)

    def test_logging_failure_does_not_break_call(self):
        """If pricing throws, the user's call must still return the response."""
        import tracker
        resp = self._fake_openai_response(model="some-model-we-dont-know", inp=1, out=1)
        client = tracker.track_openai(tracker._make_fake_openai_client(resp))
        returned = client.chat.completions.create(messages=[])
        self.assertIs(returned, resp)


class TestMultiModalAlternatives(unittest.TestCase):
    """find_cheaper_alternatives must respect billing units."""

    def test_alternatives_dont_mix_units(self):
        """A chat (token) model's alternatives must all be token-unit models."""
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "optimized_calculator", SCRIPTS_DIR / "optimized-calculator.py"
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

        alts = mod.find_cheaper_alternatives("claude-opus-4-7", 100_000, 20_000, min_savings=0.5)
        self.assertTrue(alts, "expected cheaper token-priced alternatives to Opus")
        for alt in alts:
            self.assertEqual(
                alt.get("unit"), "token",
                f"alt {alt['model']} has unit {alt.get('unit')!r}, expected 'token'",
            )


class TestOpenRouterPermissiveMatch(unittest.TestCase):
    """OpenRouter source should match fuzzy suffixes for cross-source fallback."""

    def test_normalize_dots_to_hyphens(self):
        n = _sources.OpenRouterSource._normalize
        self.assertEqual(n("Claude-Sonnet-4.6"), "claude-sonnet-4-6")
        self.assertEqual(n("openai/GPT-4.1"), "openai/gpt-4-1")

    def test_suffix_matching_requires_full_segment(self):
        """
        'gpt-4o' should NOT match 'openai/gpt-4o-long-name-variant' —
        suffix must align on '/' boundary.
        """
        src = _sources.OpenRouterSource()
        fake_data = {
            "data": [
                {"id": "openai/gpt-4o", "pricing": {"prompt": "0.0000025", "completion": "0.00001"}},
                {"id": "openai/gpt-4o-long-name-variant", "pricing": {"prompt": "0.1", "completion": "0.1"}},
            ]
        }
        # Directly exercise permissive matching via a stubbed _data.
        original_data = src._data
        src._data = lambda: (fake_data, 0.0)
        try:
            os.environ.pop("CW_STATIC_ONLY", None)
            sp = src.get_permissive("gpt-4o")
            self.assertIsNotNone(sp)
            self.assertEqual(sp.display_name, "openai/gpt-4o")
            self.assertAlmostEqual(sp.input_per_1m, 2.5, places=4)
        finally:
            src._data = original_data
            os.environ["CW_STATIC_ONLY"] = "1"


class TestRouter(unittest.TestCase):
    """Router picks the right source per model prefix."""

    def test_static_only_sources_return_static(self):
        """Under CW_STATIC_ONLY=1, all lookups should come from static."""
        price = _pricing.get_price("claude-sonnet-4-6")
        self.assertIsNotNone(price)
        self.assertEqual(price.source, "static")

    def test_openrouter_prefix_bypasses_litellm(self):
        """
        Swap the OpenRouter source with a fake one; the router must use it
        for openrouter/* models, not LiteLLM.
        """
        class FakeOR:
            called_with = []
            def get(self, model):
                FakeOR.called_with.append(model)
                return _sources.SourcedPrice(
                    input_per_1m=1.11, output_per_1m=2.22,
                    display_name="fake", provider="openrouter",
                    source="openrouter", fetched_at=123.0,
                )

        class FakeLL:
            def get(self, model):
                raise AssertionError("LiteLLM should not be consulted for openrouter/* models")

        original_or = _pricing._OPENROUTER
        original_ll = _pricing._LITELLM
        try:
            _pricing._OPENROUTER = FakeOR()
            _pricing._LITELLM = FakeLL()
            # Need to disable static-only so router doesn't short-circuit.
            os.environ.pop("CW_STATIC_ONLY", None)
            price = _pricing.get_price("openrouter/anthropic/claude-opus-4.7")
            self.assertIsNotNone(price)
            self.assertEqual(price.source, "openrouter")
            self.assertEqual(price.input_per_1m, 1.11)
            self.assertIn("openrouter/anthropic/claude-opus-4.7", FakeOR.called_with)
        finally:
            _pricing._OPENROUTER = original_or
            _pricing._LITELLM = original_ll
            os.environ["CW_STATIC_ONLY"] = "1"

    def test_non_openrouter_fallback_chain(self):
        """Non-openrouter: LiteLLM → OpenRouter (permissive) → static."""
        calls = {"litellm": 0, "openrouter": 0}

        class StubLL:
            def get(self, model):
                calls["litellm"] += 1
                return None

        class StubOR:
            def get(self, model):
                return None
            def get_permissive(self, model):
                calls["openrouter"] += 1
                return None  # miss → force fall-through to static

        original_ll = _pricing._LITELLM
        original_or = _pricing._OPENROUTER
        try:
            _pricing._LITELLM = StubLL()
            _pricing._OPENROUTER = StubOR()
            os.environ.pop("CW_STATIC_ONLY", None)
            price = _pricing.get_price("claude-sonnet-4-6")
            self.assertEqual(calls["litellm"], 1, "LiteLLM should have been consulted")
            self.assertEqual(calls["openrouter"], 1, "OpenRouter should be consulted next")
            self.assertIsNotNone(price, "should fall back to static")
            self.assertEqual(price.source, "static")
        finally:
            _pricing._LITELLM = original_ll
            _pricing._OPENROUTER = original_or
            os.environ["CW_STATIC_ONLY"] = "1"

    def test_offline_env_blocks_network(self):
        """CW_OFFLINE=1 prevents HTTP calls even when the cache is cold."""
        os.environ["CW_OFFLINE"] = "1"
        try:
            self.assertIsNone(_sources._http_get_json("http://example.invalid"))
        finally:
            os.environ.pop("CW_OFFLINE", None)


class TestAtomicIO(unittest.TestCase):
    """write_json_atomic never leaves a half-written file."""

    def test_atomic_roundtrip(self):
        import tempfile, io_utils as _io
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "data.json"
            _io.write_json_atomic(path, {"k": "v", "n": 3})
            self.assertEqual(_io.read_json(path), {"k": "v", "n": 3})

    def test_read_missing_returns_default(self):
        import tempfile, io_utils as _io
        with tempfile.TemporaryDirectory() as td:
            self.assertEqual(
                _io.read_json(Path(td) / "nope.json", default={"x": 1}),
                {"x": 1},
            )

    def test_read_corrupt_returns_default(self):
        import tempfile, io_utils as _io
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "broken.json"
            path.write_text("{ not valid json ")
            self.assertEqual(_io.read_json(path, default={"ok": True}), {"ok": True})


class TestCodeAudit(unittest.TestCase):
    """AST-based risk detection replaces the old regex."""

    def _audit(self, src: str):
        import code_audit
        return code_audit.audit_source(src)

    def test_while_true_with_llm_flags_critical(self):
        risks = self._audit("""
import openai
client = openai.OpenAI()
while True:
    r = client.chat.completions.create(model='gpt-4o', max_tokens=100, messages=[])
""")
        kinds = [r.kind for r in risks]
        self.assertIn("unbounded_while_true_api", kinds)

    def test_while_true_with_bound_is_not_flagged(self):
        risks = self._audit("""
import openai
client = openai.OpenAI()
max_iterations = 10
while True:
    if max_iterations <= 0: break
    client.chat.completions.create(model='gpt-4o', max_tokens=100, messages=[])
    max_iterations -= 1
""")
        self.assertNotIn("unbounded_while_true_api", [r.kind for r in risks])

    def test_recursion_with_llm_flags_critical(self):
        risks = self._audit("""
def agent_step(state):
    r = client.chat.completions.create(model='gpt-4o', max_tokens=100, messages=[])
    agent_step(state)
""")
        self.assertIn("unbounded_recursion_api", [r.kind for r in risks])

    def test_recursion_with_depth_param_is_allowed(self):
        risks = self._audit("""
def agent_step(state, max_depth):
    if max_depth <= 0: return
    client.chat.completions.create(model='gpt-4o', max_tokens=100, messages=[])
    agent_step(state, max_depth - 1)
""")
        self.assertNotIn("unbounded_recursion_api", [r.kind for r in risks])

    def test_missing_max_tokens_flags_medium(self):
        risks = self._audit("client.chat.completions.create(model='gpt-4o', messages=[])")
        self.assertIn("missing_max_tokens", [r.kind for r in risks])

    def test_has_max_tokens_not_flagged(self):
        risks = self._audit("client.chat.completions.create(model='gpt-4o', max_tokens=100, messages=[])")
        self.assertNotIn("missing_max_tokens", [r.kind for r in risks])

    def test_medium_class_is_not_flagged_as_recursion(self):
        """Regression: old regex flagged any class with >5 self. accesses as 'recursion'."""
        risks = self._audit("""
class Thing:
    def a(self): return self.b()
    def b(self): return self.c()
    def c(self): return self.d()
    def d(self): return self.x
    def x(self): self.y = self.z
""")
        self.assertNotIn("unbounded_recursion_api", [r.kind for r in risks])


class TestTokenizer(unittest.TestCase):
    """Provider-aware token counting doesn't lie about Claude/Gemini."""

    def test_method_openai_vs_claude_differs(self):
        import tokenizer
        text = "Hello world, how are you today?" * 10
        _, gpt_method = tokenizer.count_tokens(text, "gpt-4o")
        _, claude_method = tokenizer.count_tokens(text, "claude-sonnet-4-6")
        # Methods must be different — Claude should NOT go through tiktoken.
        self.assertNotEqual(gpt_method, claude_method)
        self.assertTrue(claude_method.startswith("heuristic-anthropic"))

    def test_gemini_uses_google_heuristic(self):
        import tokenizer
        _, method = tokenizer.count_tokens("some text", "gemini-2.5-pro")
        self.assertEqual(method, "heuristic-google")

    def test_empty_text_is_zero(self):
        import tokenizer
        self.assertEqual(tokenizer.count("", "gpt-4o"), 0)

    def test_provider_family_classification(self):
        import tokenizer
        cases = {
            "gpt-4o": "openai",
            "o3-mini": "openai",
            "claude-sonnet-4-6": "anthropic",
            "gemini-2.0-flash": "google",
            "mistral-large": "mistral",
            "llama-3.1-70b": "meta",
            "deepseek-v3": "deepseek",
            "made-up-name": "unknown",
        }
        for model, expected in cases.items():
            self.assertEqual(tokenizer._provider_family(model), expected, model)


class TestConfidenceFromSamples(unittest.TestCase):
    """smart-budget's confidence is variance-based, not a +0.05 ramp."""

    def _conf(self, samples):
        # Import via importlib because module has a hyphen.
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "smart_budget", SCRIPTS_DIR / "smart-budget.py"
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod.SmartBudgetManager._confidence_from_samples(samples)

    def test_one_sample_is_low_confidence(self):
        self.assertLess(self._conf([1.0]), 0.5)

    def test_many_consistent_samples_are_high_confidence(self):
        self.assertGreater(self._conf([1.0] * 20), 0.85)

    def test_high_variance_stays_low(self):
        conf = self._conf([0.1, 10.0, 0.5, 8.0, 0.2, 12.0, 0.1])
        self.assertLess(conf, 0.7)

    def test_zero_mean_samples_special_cased(self):
        """All-zero samples shouldn't divide-by-zero or lie about certainty."""
        conf = self._conf([0.0, 0.0, 0.0, 0.0])
        self.assertGreaterEqual(conf, 0.1)
        self.assertLessEqual(conf, 0.95)


class TestCassettes(unittest.TestCase):
    """Parse real-shaped JSON from LiteLLM + OpenRouter without hitting the network."""

    FIXTURES = Path(__file__).resolve().parent / "fixtures"

    def _load_litellm_source_with_fixture(self):
        import _sources
        src = _sources.LiteLLMSource()
        data = json.loads((self.FIXTURES / "litellm_sample.json").read_text())
        src._data = lambda: (data, 1_700_000_000.0)
        return src

    def _load_openrouter_source_with_fixture(self):
        import _sources
        src = _sources.OpenRouterSource()
        data = json.loads((self.FIXTURES / "openrouter_sample.json").read_text())
        src._data = lambda: (data, 1_700_000_000.0)
        return src

    def test_litellm_parses_chat(self):
        os.environ.pop("CW_STATIC_ONLY", None)
        try:
            src = self._load_litellm_source_with_fixture()
            p = src.get("gpt-4o")
            self.assertIsNotNone(p)
            self.assertEqual(p.mode, "chat")
            self.assertEqual(p.unit, "token")
            self.assertAlmostEqual(p.input_per_1m, 2.5, places=4)
            self.assertAlmostEqual(p.output_per_1m, 10.0, places=4)
        finally:
            os.environ["CW_STATIC_ONLY"] = "1"

    def test_litellm_parses_image_generation(self):
        os.environ.pop("CW_STATIC_ONLY", None)
        try:
            src = self._load_litellm_source_with_fixture()
            p = src.get("dall-e-3")
            self.assertIsNotNone(p)
            self.assertEqual(p.mode, "image_generation")
            self.assertEqual(p.unit, "image")
            # $0.04/image * 1M = $40,000/1M
            self.assertAlmostEqual(p.output_per_1m, 40000.0, places=1)
        finally:
            os.environ["CW_STATIC_ONLY"] = "1"

    def test_litellm_parses_audio_transcription(self):
        os.environ.pop("CW_STATIC_ONLY", None)
        try:
            src = self._load_litellm_source_with_fixture()
            p = src.get("whisper-1")
            self.assertIsNotNone(p)
            self.assertEqual(p.unit, "second")
            self.assertAlmostEqual(p.input_per_1m, 100.0, places=2)
        finally:
            os.environ["CW_STATIC_ONLY"] = "1"

    def test_litellm_skips_null_cost(self):
        os.environ.pop("CW_STATIC_ONLY", None)
        try:
            src = self._load_litellm_source_with_fixture()
            self.assertIsNone(src.get("model-with-null-cost"))
        finally:
            os.environ["CW_STATIC_ONLY"] = "1"

    def test_openrouter_parses_normal_and_filters_junk(self):
        os.environ.pop("CW_STATIC_ONLY", None)
        try:
            src = self._load_openrouter_source_with_fixture()
            p = src.get("openrouter/anthropic/claude-sonnet-4.6")
            self.assertIsNotNone(p)
            self.assertAlmostEqual(p.input_per_1m, 3.0, places=4)
            # Non-numeric pricing is swallowed gracefully.
            self.assertIsNone(src.get("openrouter/broken/model"))
        finally:
            os.environ["CW_STATIC_ONLY"] = "1"

    def test_openrouter_permissive_match_tolerates_dots(self):
        os.environ.pop("CW_STATIC_ONLY", None)
        try:
            src = self._load_openrouter_source_with_fixture()
            # user types hyphenated; OR has dotted form
            p = src.get_permissive("claude-sonnet-4-6")
            self.assertIsNotNone(p)
            self.assertAlmostEqual(p.input_per_1m, 3.0, places=4)
        finally:
            os.environ["CW_STATIC_ONLY"] = "1"


class TestCircuitBreaker(unittest.TestCase):
    """_http_get_json opens the breaker after N consecutive failures."""

    def setUp(self):
        import _sources
        _sources._BREAKER_STATE.clear()

    def test_opens_after_threshold(self):
        import _sources
        for _ in range(_sources._BREAKER_THRESHOLD):
            _sources._breaker_record_failure("https://example.invalid/data")
        self.assertTrue(_sources.breaker_open("https://example.invalid/data"))

    def test_closes_on_success(self):
        import _sources
        for _ in range(_sources._BREAKER_THRESHOLD):
            _sources._breaker_record_failure("https://example.invalid/data")
        _sources._breaker_record_success("https://example.invalid/data")
        self.assertFalse(_sources.breaker_open("https://example.invalid/data"))

    def test_http_get_returns_none_when_breaker_open(self):
        import _sources
        for _ in range(_sources._BREAKER_THRESHOLD):
            _sources._breaker_record_failure("https://example.invalid/data")
        self.assertIsNone(_sources._http_get_json("https://example.invalid/data"))


class TestModelCanon(unittest.TestCase):
    """Canonical family collapses variants for aggregation."""

    def test_strips_date_pins(self):
        from model_canon import canonical_family
        self.assertEqual(canonical_family("claude-haiku-4-5-20251001"), "claude-haiku-4-5")
        self.assertEqual(canonical_family("claude-sonnet-4-5-20250929"), "claude-sonnet-4-5")

    def test_collapses_dots_and_hyphens(self):
        from model_canon import canonical_family
        self.assertEqual(canonical_family("claude-sonnet-4.6"), "claude-sonnet-4-6")
        self.assertEqual(canonical_family("Claude-Sonnet-4.6"), "claude-sonnet-4-6")

    def test_strips_provider_prefix(self):
        from model_canon import canonical_family
        self.assertEqual(canonical_family("anthropic/claude-opus-4-7"), "claude-opus-4-7")

    def test_preserves_openrouter_tag(self):
        from model_canon import canonical_family
        self.assertEqual(
            canonical_family("openrouter/anthropic/claude-sonnet-4.6"),
            "openrouter/claude-sonnet-4-6",
        )

    def test_strips_thinking_and_hd(self):
        from model_canon import canonical_family
        self.assertEqual(canonical_family("claude-3.7-sonnet:thinking"), "claude-3-7-sonnet")
        self.assertEqual(canonical_family("dall-e-3-hd"), "dall-e-3")


class TestLogRotation(unittest.TestCase):
    """Usage log rotates on first write of a new day."""

    def setUp(self):
        import tempfile, usage_log as ul
        self._tmp = Path(tempfile.mkdtemp())
        self._orig_dir = ul.LOG_DIR
        self._orig_log = ul.USAGE_LOG
        ul.LOG_DIR = self._tmp
        ul.USAGE_LOG = self._tmp / "usage.jsonl"
        self._ul = ul

    def tearDown(self):
        import shutil
        self._ul.LOG_DIR = self._orig_dir
        self._ul.USAGE_LOG = self._orig_log
        shutil.rmtree(self._tmp, ignore_errors=True)

    def test_old_entries_rotate_on_new_day(self):
        from datetime import datetime, timezone, timedelta
        # Write an old entry directly to the file (ts = 2 days ago).
        old_ts = (datetime.now(timezone.utc) - timedelta(days=2)).timestamp()
        self._ul.USAGE_LOG.write_text(
            json.dumps({"ts": old_ts, "model": "gpt-4o", "cost_total": 1.0}) + "\n"
        )
        # Now append today — should trigger rotation.
        self._ul.append_usage({"model": "claude-sonnet-4-6", "cost_total": 0.5})
        # One rolled file + a fresh usage.jsonl should exist.
        rolled = list(self._tmp.glob("usage.????-??-??.jsonl"))
        self.assertEqual(len(rolled), 1)
        # Current file only has the new entry.
        current = self._ul.USAGE_LOG.read_text().splitlines()
        self.assertEqual(len(current), 1)
        self.assertIn("claude-sonnet-4-6", current[0])

    def test_iter_entries_since_skips_old_rolled_files(self):
        from datetime import datetime, timezone, timedelta
        # Drop a 30-day-old rolled file.
        old = self._tmp / "usage.2000-01-01.jsonl"
        old.write_text(json.dumps({"ts": 946684800.0, "model": "gpt-4o"}) + "\n")
        # One current entry.
        self._ul.append_usage({"model": "claude-sonnet-4-6", "cost_total": 0.1})
        since = (datetime.now(timezone.utc) - timedelta(days=7)).timestamp()
        entries = list(self._ul.iter_entries(since=since))
        # Old file shouldn't even be opened; result is only the new one.
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]["model"], "claude-sonnet-4-6")

    def test_aggregation_by_family_collapses_variants(self):
        self._ul.append_usage({"model": "claude-haiku-4-5-20251001", "cost_total": 1.0})
        self._ul.append_usage({"model": "claude-haiku-4-5", "cost_total": 2.0})
        self._ul.append_usage({"model": "claude-haiku-4.5", "cost_total": 3.0})
        totals = self._ul.session_total(by_family=True)
        self.assertEqual(len(totals["by_model"]), 1, "all three should collapse to one family")
        (fam, bucket), = totals["by_model"].items()
        self.assertEqual(fam, "claude-haiku-4-5")
        self.assertAlmostEqual(bucket["cost"], 6.0, places=4)


class TestDiskCache(unittest.TestCase):
    """Disk cache honors TTL and survives JSON corruption."""

    def test_cache_roundtrip(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            original = _sources.CACHE_DIR
            _sources.CACHE_DIR = Path(td)
            try:
                c = _sources._DiskCache("unit-test", ttl=60)
                payload, fetched_at, fresh = c.read()
                self.assertIsNone(payload)
                self.assertFalse(fresh)

                c.write({"hello": "world"})
                payload, _, fresh = c.read()
                self.assertEqual(payload, {"hello": "world"})
                self.assertTrue(fresh)
            finally:
                _sources.CACHE_DIR = original

    def test_cache_expires(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            original = _sources.CACHE_DIR
            _sources.CACHE_DIR = Path(td)
            try:
                c = _sources._DiskCache("unit-expire", ttl=0)  # immediately stale
                c.write({"x": 1})
                _, _, fresh = c.read()
                self.assertFalse(fresh, "ttl=0 cache should never be fresh")
            finally:
                _sources.CACHE_DIR = original


class TestFileStructure(unittest.TestCase):
    """Test repository structure."""
    
    def test_gitignore_exists(self):
        """Test that .gitignore exists."""
        gitignore_path = Path(__file__).parent.parent / ".gitignore"
        self.assertTrue(gitignore_path.exists())
    
    def test_env_example_exists(self):
        """Test that .env.example exists."""
        env_example_path = Path(__file__).parent.parent / ".env.example"
        self.assertTrue(env_example_path.exists())
    
    def test_scripts_executable(self):
        """Test that scripts are executable."""
        scripts_dir = Path(__file__).parent.parent / "scripts"
        
        for script in ["cost-visualizer.py", "smart-budget.py"]:
            script_path = scripts_dir / script
            self.assertTrue(script_path.exists(), f"{script} not found")
            # Check if file is readable
            with open(script_path, 'r') as f:
                content = f.read()
                self.assertGreater(len(content), 100, f"{script} is empty")


if __name__ == "__main__":
    unittest.main()
