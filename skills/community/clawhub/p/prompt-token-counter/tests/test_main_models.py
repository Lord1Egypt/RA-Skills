"""
Tests for main models with benchmark data.

Uses fuzzy model name matching (e.g. anthropic/claude-sonnet-4-6 -> claude-sonnet-4-6).
Benchmark: 8927 chars -> expected token counts per model.
Tolerance: ±30% for approximation-based models (formula-based estimates vary with text).
OpenAI (tiktoken): skip when tiktoken not installed.
"""

import pytest

from scripts.core import TokenCounter, count_tokens
from scripts.registry.models import get_model_info as registry_get_model_info

try:
    import tiktoken
    TIKTOKEN_AVAILABLE = True
except ImportError:
    TIKTOKEN_AVAILABLE = False


# Benchmark: 8927 chars, expected tokens per model
# 1 token ≈ chars/token from user's table
MAIN_MODELS_BENCHMARK = [
    ("anthropic/claude-sonnet-4-6", 8927, 2763),
    ("anthropic/claude-sonnet-4-5", 8927, 2763),
    ("anthropic/claude-opus-4.6", 8927, 2763),
    ("openai/gpt-5.2-codex", 8927, 2459),
    ("google/gemini-3.1-pro-preview", 8927, 2627),
    ("z-ai/glm-5", 8927, 2457),
    ("volcengine/doubao-seed-2-0-pro", 8927, 2702),
    ("moonshot/kimi-k2.5", 8927, 2402),
    ("minimax/MiniMax-M2.5", 8927, 2428),
    ("deepseek-v3.2", 8927, 2578),
]

# Also test canonical names (no provider prefix)
CANONICAL_BENCHMARK = [
    ("claude-sonnet-4-6", 8927, 2763),
    ("gpt-5.2-codex", 8927, 2459),  # OpenAI, requires tiktoken
    ("glm-5", 8927, 2457),
    ("deepseek-v3.2", 8927, 2578),
]

# OpenAI models that need tiktoken
OPENAI_MODELS = {"gpt-5.2-codex", "openai/gpt-5.2-codex"}

# Benchmark: 3050 chars, Chinese-mixed content (混杂中文)
# 1 token ≈ 1.5–2.4 chars (CJK tokenizes to fewer chars/token)
MAIN_MODELS_BENCHMARK_ZH = [
    ("anthropic/claude-sonnet-4-6", 3050, 1913),
    ("anthropic/claude-sonnet-4-5", 3050, 1913),
    ("anthropic/claude-opus-4.6", 3050, 1913),
    ("openai/gpt-5.2-codex", 3050, 1564),
    ("google/gemini-3.1-pro-preview", 3050, 1473),
    ("z-ai/glm-5", 3050, 1318),
    ("volcengine/doubao-seed-2-0-pro", 3050, 1494),
    ("moonshot/kimi-k2.5", 3050, 1257),
    ("minimax/MiniMax-M2.5", 3050, 1289),
    ("deepseek-v3.2", 3050, 1361),
]


def _make_test_text(length: int) -> str:
    """Generate test text of given length (mixed content for realistic tokenization)."""
    base = (
        "Token counting benchmark. 这是一段混合中英文的测试文本。"
        "Code: def hello(): return 42\n"
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
    )
    if length <= len(base):
        return base[:length]
    repeat = (length // len(base)) + 1
    return (base * repeat)[:length]


def _make_chinese_mixed_text(length: int) -> str:
    """Generate Chinese-heavy mixed text (混杂中文) for CJK tokenization benchmark.
    ~90% CJK to match user benchmark (3050 chars -> ~1.6-2.4 chars/token)."""
    base = (
        "大语言模型token计数基准测试。这是一段混杂了中文与英文的测试文本，"
        "用于验证不同模型对CJK字符的tokenization表现。"
        "大语言模型在处理中文时通常每个汉字约一至两个token。"
        "测试数据包含中英混合内容。"
    )
    if length <= len(base):
        return base[:length]
    repeat = (length // len(base)) + 1
    return (base * repeat)[:length]


@pytest.fixture
def benchmark_text():
    return _make_test_text(8927)


@pytest.fixture
def benchmark_text_zh():
    return _make_chinese_mixed_text(3050)


class TestFuzzyModelMatching:
    """Test fuzzy model name matching."""

    @pytest.mark.parametrize(
        "input_name,expected_canonical",
        [
            ("anthropic/claude-sonnet-4-6", "claude-sonnet-4-6"),
            ("openai/gpt-5.2-codex", "gpt-5.2-codex"),
            ("z-ai/glm-5", "glm-5"),
            ("minimax/MiniMax-M2.5", "minimax-m2.5"),
            ("deepseek-v3.2", "deepseek-v3.2"),
        ],
    )
    def test_fuzzy_match_resolves(self, input_name, expected_canonical):
        info = registry_get_model_info(input_name)
        assert info is not None, f"Model '{input_name}' should resolve via fuzzy match"
        assert info.name.lower() == expected_canonical.lower()

    def test_exact_match_unchanged(self):
        assert registry_get_model_info("gpt-4") is not None
        assert registry_get_model_info("claude-3-opus") is not None


class TestMainModelsTokenCount:
    """Test token counts for main models against benchmark data."""

    @pytest.mark.parametrize("model_name,char_count,expected_tokens", MAIN_MODELS_BENCHMARK)
    def test_main_models_with_fuzzy_name(self, benchmark_text, model_name, char_count, expected_tokens):
        if model_name in OPENAI_MODELS and not TIKTOKEN_AVAILABLE:
            pytest.skip("tiktoken required for OpenAI models")
        assert len(benchmark_text) == char_count
        counter = TokenCounter(model_name)
        tokens = counter.count(benchmark_text)
        # ±30% tolerance for approximation-based models
        tolerance = 0.30
        low = int(expected_tokens * (1 - tolerance))
        high = int(expected_tokens * (1 + tolerance))
        assert low <= tokens <= high, (
            f"{model_name}: got {tokens} tokens, expected ~{expected_tokens} (range {low}-{high})"
        )

    @pytest.mark.parametrize("model_name,char_count,expected_tokens", CANONICAL_BENCHMARK)
    def test_canonical_names(self, benchmark_text, model_name, char_count, expected_tokens):
        if model_name in OPENAI_MODELS and not TIKTOKEN_AVAILABLE:
            pytest.skip("tiktoken required for OpenAI models")
        assert len(benchmark_text) == char_count
        tokens = count_tokens(benchmark_text, model_name)
        tolerance = 0.30
        low = int(expected_tokens * (1 - tolerance))
        high = int(expected_tokens * (1 + tolerance))
        assert low <= tokens <= high, (
            f"{model_name}: got {tokens} tokens, expected ~{expected_tokens} (range {low}-{high})"
        )

    @pytest.mark.parametrize("model_name,char_count,expected_tokens", MAIN_MODELS_BENCHMARK_ZH)
    def test_main_models_chinese_mixed(self, benchmark_text_zh, model_name, char_count, expected_tokens):
        """Test token counts for Chinese-mixed text (混杂中文). CJK chars ≈ 1–2 chars/token."""
        if model_name in OPENAI_MODELS and not TIKTOKEN_AVAILABLE:
            pytest.skip("tiktoken required for OpenAI models")
        assert len(benchmark_text_zh) == char_count
        counter = TokenCounter(model_name)
        tokens = counter.count(benchmark_text_zh)
        tolerance = 0.30
        low = int(expected_tokens * (1 - tolerance))
        high = int(expected_tokens * (1 + tolerance))
        assert low <= tokens <= high, (
            f"{model_name} (ZH): got {tokens} tokens, expected ~{expected_tokens} (range {low}-{high})"
        )
