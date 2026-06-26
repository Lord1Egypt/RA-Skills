"""Tests for router.py — Main routing logic."""

import sys
import os
import unittest

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from router import ModelRouter, Route, route_request, TaskType


class TestRouterCoding(unittest.TestCase):
    """Tests for coding task routing."""

    def test_python_routes_to_coder(self):
        route = route_request("Write a Python function to sort a list")
        self.assertEqual(route.model_key, "qwen-coder")
        self.assertTrue(route.think)

    def test_debug_routes_to_coder(self):
        route = route_request("Debug this TypeError in my code")
        self.assertEqual(route.model_key, "qwen-coder")

    def test_api_routes_to_coder(self):
        route = route_request("Create a REST API endpoint for authentication")
        self.assertEqual(route.model_key, "qwen-coder")

    def test_docker_routes_to_coder(self):
        route = route_request("Build a Docker compose file for the microservices")
        self.assertEqual(route.model_key, "qwen-coder")


class TestRouterReasoning(unittest.TestCase):
    """Tests for reasoning task routing."""

    def test_analyze_routes_to_deepseek(self):
        route = route_request("Analyze the trade-offs between SQL and NoSQL databases")
        self.assertEqual(route.model_key, "deepseek-r1")
        self.assertTrue(route.think)

    def test_plan_routes_to_deepseek(self):
        route = route_request("Plan the architecture for a distributed system")
        self.assertEqual(route.model_key, "deepseek-r1")

    def test_compare_routes_to_deepseek(self):
        route = route_request("Compare the benefits of React vs Vue.js for our project")
        self.assertEqual(route.model_key, "deepseek-r1")


class TestRouterChat(unittest.TestCase):
    """Tests for chat task routing."""

    def test_hello_routes_to_qwen3(self):
        route = route_request("Hello, how are you doing today?")
        self.assertEqual(route.model_key, "qwen3-14b")
        self.assertFalse(route.think)

    def test_casual_routes_to_qwen3(self):
        route = route_request("That's a nice way to put it")
        self.assertEqual(route.model_key, "qwen3-14b")
        self.assertFalse(route.think)


class TestRouterLargeContext(unittest.TestCase):
    """Tests for large context override routing."""

    def test_large_context_routes_to_cloud(self):
        # Simulate a context > 120k tokens
        route = route_request("Summarize this", context_size=150000)
        self.assertEqual(route.model_key, "glm-5-1-cloud")
        self.assertTrue(route.context_overridden)

    def test_small_context_no_override(self):
        # Context under threshold should route normally
        route = route_request("Write a Python script", context_size=50000)
        self.assertEqual(route.model_key, "qwen-coder")
        self.assertFalse(route.context_overridden)

    def test_context_override_preserves_original_task(self):
        route = route_request("Debug this code issue", context_size=200000)
        self.assertTrue(route.context_overridden)
        self.assertEqual(route.original_task.value, "coding")

    def test_context_at_threshold_no_override(self):
        # Exactly at threshold should NOT override (needs > threshold)
        route = route_request("Write a function", context_size=120000)
        # The threshold is > 120000, so 120000 should not trigger override
        self.assertFalse(route.context_overridden)


class TestRouterContextMessages(unittest.TestCase):
    """Tests for context size estimation from messages."""

    def test_messages_context_estimation(self):
        # ~4 chars per token, so 500000 chars ≈ 125000 tokens > 120000 threshold
        messages = [{"role": "user", "content": "x" * 500000}]
        route = route_request("Hello", context_messages=messages)
        self.assertTrue(route.context_overridden)

    def test_small_messages_no_override(self):
        # Small messages should not trigger override
        messages = [{"role": "user", "content": "Hello"}]
        route = route_request("Hello", context_messages=messages)
        self.assertFalse(route.context_overridden)


class TestRouterRouteDataclass(unittest.TestCase):
    """Tests for Route dataclass fields."""

    def test_route_has_timestamp(self):
        route = route_request("Hello")
        self.assertTrue(route.timestamp)
        self.assertIn("T", route.timestamp)  # ISO format

    def test_route_has_reason(self):
        route = route_request("Write a Python function")
        self.assertTrue(route.reason)
        self.assertIn("coding", route.reason)

    def test_route_has_provider(self):
        route = route_request("Hello")
        self.assertEqual(route.provider, "ollama")

    def test_route_has_endpoint(self):
        route = route_request("Hello")
        self.assertIn("127.0.0.1", route.endpoint)

    def test_route_has_context_limit(self):
        route = route_request("Hello")
        self.assertGreater(route.context_limit, 0)


class TestRouterSummarize(unittest.TestCase):
    """Tests for summarize task routing."""

    def test_summarize_routes_to_qwen3(self):
        route = route_request("Summarize this article about machine learning")
        self.assertEqual(route.model_key, "qwen3-14b")
        self.assertFalse(route.think)


class TestRouterResearch(unittest.TestCase):
    """Tests for research task routing."""

    def test_research_routes_to_deepseek(self):
        route = route_request("Research the latest developments in quantum computing")
        self.assertEqual(route.model_key, "deepseek-r1")
        self.assertTrue(route.think)


class TestRouterVision(unittest.TestCase):
    """Tests for vision task routing."""

    def test_vision_routes_to_cloud(self):
        route = route_request("What does this screenshot show?")
        self.assertEqual(route.model_key, "glm-5-1-cloud")


class TestRouterFallback(unittest.TestCase):
    """Tests for default/fallback routing."""

    def test_unknown_routes_to_default(self):
        route = route_request("hi")
        self.assertEqual(route.model_key, "qwen3-14b")


if __name__ == "__main__":
    unittest.main()