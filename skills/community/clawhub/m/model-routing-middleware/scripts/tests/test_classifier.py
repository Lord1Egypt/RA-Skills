"""Tests for classifiers.py — Task type detection."""

import sys
import os
import unittest

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from classifiers import TaskType, classify_task, classify_task_simple, ClassificationResult


class TestClassifyCoding(unittest.TestCase):
    """Tests for coding task classification."""

    def test_python_keyword(self):
        result = classify_task("Write a Python function to sort a list")
        self.assertEqual(result.task_type, TaskType.CODING)
        self.assertGreater(result.confidence, 0.5)
        self.assertIn("python", result.matched_keywords)

    def test_debug_keyword(self):
        result = classify_task("Debug this error: TypeError at line 42")
        self.assertEqual(result.task_type, TaskType.CODING)

    def test_api_endpoint(self):
        result = classify_task("Create an API endpoint for user authentication")
        self.assertEqual(result.task_type, TaskType.CODING)

    def test_docker_keyword(self):
        result = classify_task("Build a Docker container for the service")
        self.assertEqual(result.task_type, TaskType.CODING)

    def test_refactor_keyword(self):
        result = classify_task("Refactor the authentication module")
        self.assertEqual(result.task_type, TaskType.CODING)

    def test_git_keyword(self):
        result = classify_task("Create a git branch for the feature")
        self.assertEqual(result.task_type, TaskType.CODING)

    def test_javascript_keyword(self):
        result = classify_task("Write a JavaScript function to validate forms")
        self.assertEqual(result.task_type, TaskType.CODING)

    def test_yaml_keyword(self):
        result = classify_task("Create a YAML config for Kubernetes deployment")
        self.assertEqual(result.task_type, TaskType.CODING)

    def test_syntax_error(self):
        result = classify_task("Fix the syntax error in my code")
        self.assertEqual(result.task_type, TaskType.CODING)


class TestClassifyReasoning(unittest.TestCase):
    """Tests for reasoning task classification."""

    def test_analyze_keyword(self):
        result = classify_task("Analyze the pros and cons of microservices")
        self.assertEqual(result.task_type, TaskType.REASONING)

    def test_plan_keyword(self):
        result = classify_task("Plan the architecture for the new system")
        self.assertEqual(result.task_type, TaskType.REASONING)

    def test_compare_keyword(self):
        result = classify_task("Compare React vs Vue for our next project")
        self.assertEqual(result.task_type, TaskType.REASONING)

    def test_strategy_keyword(self):
        result = classify_task("Design a strategy for market expansion")
        self.assertEqual(result.task_type, TaskType.REASONING)

    def test_why_question(self):
        result = classify_task("Why does this approach work better?")
        self.assertEqual(result.task_type, TaskType.REASONING)

    def test_step_by_step(self):
        result = classify_task("Give me a step-by-step explanation of how DNS works")
        self.assertEqual(result.task_type, TaskType.REASONING)


class TestClassifySummarize(unittest.TestCase):
    """Tests for summarize task classification."""

    def test_summarize_keyword(self):
        result = classify_task("Summarize this article about AI safety")
        self.assertEqual(result.task_type, TaskType.SUMMARIZE)

    def test_tldr_keyword(self):
        result = classify_task("TLDR this meeting notes")
        self.assertEqual(result.task_type, TaskType.SUMMARIZE)

    def test_key_points(self):
        result = classify_task("What are the key points of this document?")
        self.assertEqual(result.task_type, TaskType.SUMMARIZE)


class TestClassifyResearch(unittest.TestCase):
    """Tests for research task classification."""

    def test_research_keyword(self):
        result = classify_task("Research the latest developments in quantum computing")
        self.assertEqual(result.task_type, TaskType.RESEARCH)

    def test_investigate_keyword(self):
        result = classify_task("Investigate the root cause of the outage")
        self.assertEqual(result.task_type, TaskType.RESEARCH)

    def test_explore_keyword(self):
        result = classify_task("Explore options for database migration")
        self.assertEqual(result.task_type, TaskType.RESEARCH)


class TestClassifyTools(unittest.TestCase):
    """Tests for tools task classification."""

    def test_cli_keyword(self):
        result = classify_task("Run the CLI command to deploy the service")
        self.assertEqual(result.task_type, TaskType.TOOLS)

    def test_install_keyword(self):
        # "package" matches coding — this is a coding/tools overlap
        result = classify_task("Install the new package for monitoring")
        self.assertIn(result.task_type, [TaskType.TOOLS, TaskType.CODING])

    def test_status_keyword(self):
        result = classify_task("Check the status of the Docker containers")
        # Could be CODING (docker) or TOOLS (status) — priority decides
        self.assertIn(result.task_type, [TaskType.TOOLS, TaskType.CODING])


class TestClassifyVision(unittest.TestCase):
    """Tests for vision task classification."""

    def test_screenshot_keyword(self):
        result = classify_task("What does this screenshot show?")
        self.assertEqual(result.task_type, TaskType.VISION)

    def test_image_keyword(self):
        result = classify_task("Describe the image I sent you")
        self.assertEqual(result.task_type, TaskType.VISION)

    def test_photo_keyword(self):
        result = classify_task("Can you see what's in this photo?")
        self.assertEqual(result.task_type, TaskType.VISION)


class TestClassifyChat(unittest.TestCase):
    """Tests for chat (default) classification."""

    def test_simple_greeting(self):
        result = classify_task("Hello, how are you?")
        self.assertEqual(result.task_type, TaskType.CHAT)

    def test_casual_question(self):
        result = classify_task("What's the weather like today?")
        # "What" doesn't strongly match any category, could default to chat or reasoning
        self.assertIn(result.task_type, [TaskType.CHAT, TaskType.REASONING])

    def test_empty_prompt(self):
        result = classify_task("")
        self.assertEqual(result.task_type, TaskType.CHAT)
        self.assertLess(result.confidence, 0.5)

    def test_whitespace_only(self):
        result = classify_task("   ")
        self.assertEqual(result.task_type, TaskType.CHAT)

    def test_simple_statement(self):
        result = classify_task("That's interesting")
        self.assertEqual(result.task_type, TaskType.CHAT)


class TestClassifySimple(unittest.TestCase):
    """Tests for the convenience function."""

    def test_returns_string(self):
        result = classify_task_simple("Write a Python script")
        self.assertIsInstance(result, str)
        self.assertEqual(result, "coding")

    def test_chat_default(self):
        result = classify_task_simple("Hello there")
        self.assertEqual(result, "chat")


class TestClassificationConfidence(unittest.TestCase):
    """Tests for confidence scoring."""

    def test_strong_match_has_high_confidence(self):
        result = classify_task("Write a Python function to debug the API endpoint")
        self.assertGreater(result.confidence, 0.7)

    def test_weak_match_has_lower_confidence(self):
        result = classify_task("Hello there, I need some help")
        # Weak/ambiguous matches should have lower confidence
        self.assertLess(result.confidence, 0.8)

    def test_no_match_has_low_confidence(self):
        result = classify_task("hi")
        self.assertLessEqual(result.confidence, 0.5)


if __name__ == "__main__":
    unittest.main()