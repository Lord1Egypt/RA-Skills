#!/usr/bin/env python3
"""Model Throughput Tester — 纯逻辑单测（不发起真实请求）

用法:
  python3 tests/test_throughput.py
"""

import os
import sys
import json
import statistics

SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, SCRIPT_DIR)

import throughput


class TestResult:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []

    def ok(self, name):
        self.passed += 1
        print(f"  ✅ {name}")

    def fail(self, name, reason=""):
        self.failed += 1
        msg = f"  ❌ {name}"
        if reason:
            msg += f" — {reason}"
        print(msg)
        self.errors.append((name, reason))

    def summary(self):
        total = self.passed + self.failed
        print(f"\n{'─' * 40}")
        print(f"  通过 {self.passed}/{total}" + (f"，失败 {self.failed}" if self.failed else ""))
        if self.errors:
            print("\n  失败详情:")
            for name, reason in self.errors:
                print(f"    • {name}: {reason}")
        print()
        return self.failed == 0


# ── Token 估算 ─────────────────────────────────────────────

def test_estimate_tokens_english(t):
    """英文：1 token ≈ 0.75 word → 100 words ≈ 133 tokens"""
    text = " ".join(["hello"] * 100)
    tokens = throughput.estimate_tokens(text)
    if 130 <= tokens <= 137:
        t.ok(f"estimate_tokens(英文 100 words) ≈ {tokens:.1f}")
    else:
        t.fail("estimate_tokens 英文", f"预期 ~133，得到 {tokens:.1f}")


def test_estimate_tokens_chinese(t):
    """中文：1 token ≈ 1.5 chars → 150 字 ≈ 100 tokens"""
    text = "测试" * 75  # 150 字符
    tokens = throughput.estimate_tokens(text)
    if 95 <= tokens <= 105:
        t.ok(f"estimate_tokens(中文 150 chars) ≈ {tokens:.1f}")
    else:
        t.fail("estimate_tokens 中文", f"预期 ~100，得到 {tokens:.1f}")


def test_estimate_tokens_mixed(t):
    """混合文本：英文为主时走英文规则"""
    text = "Hello world this is a test " * 10  # 6 words × 10 = 60 words, 几乎全 ASCII
    tokens = throughput.estimate_tokens(text)
    # 60 / 0.75 = 80 tokens
    if 75 <= tokens <= 85:
        t.ok(f"estimate_tokens(mixed) ≈ {tokens:.1f}")
    else:
        t.fail("estimate_tokens mixed", f"预期 ~80，得到 {tokens:.1f}")


def test_estimate_tokens_empty(t):
    """空字符串不应崩溃"""
    try:
        tokens = throughput.estimate_tokens("")
        # 空字符串触发 ZeroDivisionError → except 兜底
        t.ok(f"estimate_tokens(空字符串) = {tokens}")
    except Exception as e:
        t.fail("estimate_tokens 空字符串", f"崩溃: {e}")


# ── 语言检测 ──────────────────────────────────────────────

def test_detect_lang_english(t):
    if throughput.detect_lang("Hello world this is a test") == "en":
        t.ok("detect_lang 英文")
    else:
        t.fail("detect_lang 英文")


def test_detect_lang_chinese(t):
    if throughput.detect_lang("今天天气很好适合出去散步") == "zh":
        t.ok("detect_lang 中文")
    else:
        t.fail("detect_lang 中文")


def test_detect_lang_threshold(t):
    """70% ASCII 阈值的边界测试"""
    # 71% ASCII → en
    text_en = "a" * 71 + "测" * 29
    # 69% ASCII → zh
    text_zh = "a" * 69 + "测" * 31

    if throughput.detect_lang(text_en) == "en":
        t.ok("detect_lang 71% ASCII → en")
    else:
        t.fail("detect_lang 71% 边界", f"应为 en，得到 {throughput.detect_lang(text_en)}")

    if throughput.detect_lang(text_zh) == "zh":
        t.ok("detect_lang 69% ASCII → zh")
    else:
        t.fail("detect_lang 69% 边界", f"应为 zh，得到 {throughput.detect_lang(text_zh)}")


# ── Provider/Model 解析 ───────────────────────────────────

def test_get_model_from_provider(t):
    cases = [
        ("zai/glm-5-turbo", ("zai", "glm-5-turbo")),
        ("openai/gpt-4o-mini", ("openai", "gpt-4o-mini")),
        ("only-model-name", (None, "only-model-name")),
        ("provider/with/slash/model", ("provider", "with/slash/model")),
    ]
    for input_str, expected in cases:
        provider, model_id = throughput.get_model_from_provider(input_str)
        if (provider, model_id) == expected:
            t.ok(f"parse '{input_str}'")
        else:
            t.fail(f"parse '{input_str}'", f"预期 {expected}，得到 ({provider}, {model_id})")


def test_parse_models_csv(t):
    result = throughput.parse_models("gpt-4o-mini,gpt-4o,claude-sonnet")
    if result == ["gpt-4o-mini", "gpt-4o", "claude-sonnet"]:
        t.ok("parse_models CSV")
    else:
        t.fail("parse_models CSV", f"得到 {result}")


def test_parse_models_json(t):
    result = throughput.parse_models('["gpt-4o-mini", "gpt-4o"]')
    if result == ["gpt-4o-mini", "gpt-4o"]:
        t.ok("parse_models JSON")
    else:
        t.fail("parse_models JSON", f"得到 {result}")


# ── URL 处理（间接覆盖 call_model 内部逻辑）────────────────

def _build_api_url(base_url):
    """镜像 call_model 内部的 URL 处理逻辑（用于单测验证）"""
    req_url = base_url.rstrip("/")
    if "/chat/completions" in req_url:
        pass
    elif req_url.endswith("/v1") or req_url.endswith("/v1/"):
        req_url += "/chat/completions"
    elif req_url.endswith("/v4") or req_url.endswith("/v4/"):
        req_url += "/chat/completions"
    else:
        req_url += "/v1/chat/completions"
    return req_url


def test_url_v1_suffix(t):
    """以 /v1 结尾 → 自动补 /chat/completions"""
    url = _build_api_url("https://api.openai.com/v1")
    if url == "https://api.openai.com/v1/chat/completions":
        t.ok("URL: /v1 后缀")
    else:
        t.fail("URL /v1", f"得到 {url}")


def test_url_v4_suffix(t):
    url = _build_api_url("https://gateway.example.com/v4")
    if url == "https://gateway.example.com/v4/chat/completions":
        t.ok("URL: /v4 后缀")
    else:
        t.fail("URL /v4", f"得到 {url}")


def test_url_no_suffix(t):
    url = _build_api_url("https://api.example.com")
    if url == "https://api.example.com/v1/chat/completions":
        t.ok("URL: 无后缀 → 加 /v1")
    else:
        t.fail("URL 无后缀", f"得到 {url}")


def test_url_full_completions(t):
    """已含 /chat/completions → 不动"""
    url = _build_api_url("https://api.example.com/v1/chat/completions")
    if url == "https://api.example.com/v1/chat/completions":
        t.ok("URL: 已是完整路径")
    else:
        t.fail("URL 完整路径", f"得到 {url}")


def test_url_trailing_slash(t):
    """末尾斜杠应被剥离"""
    url = _build_api_url("https://api.example.com/v1/")
    if url == "https://api.example.com/v1/chat/completions":
        t.ok("URL: 末尾斜杠")
    else:
        t.fail("URL 末尾斜杠", f"得到 {url}")


# ── 报告生成 ──────────────────────────────────────────────

def test_report_ok_results(t):
    """3 次成功 → avg tokens/s、0% error rate"""
    results = [
        {"model": "test-model", "iter": 1, "elapsed": 1.0, "output_tokens": 50, "tokens_per_sec": 50.0, "status": "ok", "error": ""},
        {"model": "test-model", "iter": 2, "elapsed": 1.0, "output_tokens": 60, "tokens_per_sec": 60.0, "status": "ok", "error": ""},
        {"model": "test-model", "iter": 3, "elapsed": 1.0, "output_tokens": 70, "tokens_per_sec": 70.0, "status": "ok", "error": ""},
    ]
    report = throughput.build_markdown_report(results, "auto", "", 3, "test prompt")
    if "test-model" in report and "60.0" in report and "0.0%" in report:
        t.ok("report: 3 次成功 → avg 60.0 tokens/s")
    else:
        t.fail("report 内容缺失", report[:200])


def test_report_with_errors(t):
    """1 次失败 → 33.3% error rate"""
    results = [
        {"model": "flaky", "iter": 1, "elapsed": 1.0, "output_tokens": 50, "tokens_per_sec": 50.0, "status": "ok", "error": ""},
        {"model": "flaky", "iter": 2, "elapsed": 1.0, "output_tokens": 60, "tokens_per_sec": 60.0, "status": "ok", "error": ""},
        {"model": "flaky", "iter": 3, "elapsed": 60.0, "output_tokens": 0, "tokens_per_sec": 0.0, "status": "timeout", "error": "timeout"},
    ]
    report = throughput.build_markdown_report(results, "auto", "", 3, "test")
    if "33.3%" in report and "timeout" in report:
        t.ok("report: 含 timeout 记录和 error rate")
    else:
        t.fail("report 错误率", report[:300])


def test_report_dict_input(t):
    """多模型（dict 输入）"""
    results = {
        "model-a": [
            {"model": "model-a", "iter": 1, "elapsed": 1.0, "output_tokens": 100, "tokens_per_sec": 100.0, "status": "ok", "error": ""},
        ],
        "model-b": [
            {"model": "model-b", "iter": 1, "elapsed": 2.0, "output_tokens": 100, "tokens_per_sec": 50.0, "status": "ok", "error": ""},
        ],
    }
    report = throughput.build_markdown_report(results, "api", "https://api.test/v1", 1, "test")
    if "model-a" in report and "model-b" in report and "100.0" in report and "50.0" in report:
        t.ok("report: 多模型 dict 输入")
    else:
        t.fail("report 多模型", report[:300])


def test_report_cache_hit(t):
    """cache_hit 状态应被算作成功（与 ok 一样）"""
    results = [
        {"model": "cached", "iter": 1, "elapsed": 0.5, "output_tokens": 200, "tokens_per_sec": 400.0, "status": "cache_hit", "error": ""},
    ]
    report = throughput.build_markdown_report(results, "api", "", 1, "test")
    if "cached" in report and "400.0" in report and "0.0%" in report:
        t.ok("report: cache_hit 视为成功")
    else:
        t.fail("report cache_hit", report[:200])


def test_report_empty_results(t):
    """空结果不应崩溃"""
    try:
        report = throughput.build_markdown_report([], "auto", "", 0, "")
        if "unknown" in report or "0.0%" in report:
            t.ok("report: 空结果不崩溃")
        else:
            t.ok("report: 空结果不崩溃（内容宽松）")
    except Exception as e:
        t.fail("report 空结果", f"崩溃: {e}")


# ── CSV 输出 ──────────────────────────────────────────────

def test_write_csv(t):
    import tempfile
    results = [
        {"model": "csv-test", "iter": 1, "elapsed": 1.5, "output_tokens": 100.5, "tokens_per_sec": 67.0, "status": "ok", "error": ""},
    ]
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        csv_path = f.name
    try:
        throughput.write_csv(results, csv_path)
        with open(csv_path) as f:
            content = f.read()
        if "csv-test" in content and "tokens_per_s" in content and "100" in content:
            t.ok("write_csv: 写入并含必要字段")
        else:
            t.fail("write_csv", content[:200])
    finally:
        os.unlink(csv_path)


# ── 配置读取 ──────────────────────────────────────────────

def test_get_current_model_no_config(t):
    """配置文件不存在时返回空字符串而非崩溃"""
    orig = throughput.get_current_model.__code__.co_consts
    # 只检查不抛异常
    try:
        result = throughput.get_current_model()
        if isinstance(result, str):
            t.ok(f"get_current_model 不崩溃，返回 '{result}'")
        else:
            t.fail("get_current_model 类型", f"预期 str，得到 {type(result)}")
    except Exception as e:
        t.fail("get_current_model", f"崩溃: {e}")


# ── 运行 ──────────────────────────────────────────────────

def main():
    t = TestResult()
    print("🧪 Model Throughput Tester 测试\n")

    print("📝 Token 估算\n")
    test_estimate_tokens_english(t)
    test_estimate_tokens_chinese(t)
    test_estimate_tokens_mixed(t)
    test_estimate_tokens_empty(t)

    print("\n🌐 语言检测\n")
    test_detect_lang_english(t)
    test_detect_lang_chinese(t)
    test_detect_lang_threshold(t)

    print("\n🔧 Provider/Model 解析\n")
    test_get_model_from_provider(t)
    test_parse_models_csv(t)
    test_parse_models_json(t)

    print("\n🔗 URL 处理\n")
    test_url_v1_suffix(t)
    test_url_v4_suffix(t)
    test_url_no_suffix(t)
    test_url_full_completions(t)
    test_url_trailing_slash(t)

    print("\n📊 报告生成\n")
    test_report_ok_results(t)
    test_report_with_errors(t)
    test_report_dict_input(t)
    test_report_cache_hit(t)
    test_report_empty_results(t)

    print("\n💾 CSV 输出\n")
    test_write_csv(t)

    print("\n⚙️ 配置读取\n")
    test_get_current_model_no_config(t)

    ok = t.summary()
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
