"""Unit tests for PromptTemplateLoader."""

import os
import tempfile

import pytest

from prompt_loader import PromptNotFoundError, PromptTemplateLoader


class TestPromptTemplateLoader:
    """Tests for PromptTemplateLoader.load_template()."""

    def setup_method(self):
        """Create a temporary prompts directory with template files."""
        self.tmpdir = tempfile.mkdtemp()
        self.loader = PromptTemplateLoader(self.tmpdir)

        # Create all 4 prompt files with content
        self.templates = {
            "plan.md": "Plan template: {{context}}",
            "draft.md": "Draft template: {{context}}",
            "self_critique.md": "Self-critique template: {{context}}",
            "refine.md": "Refine template: {{context}}",
        }
        for filename, content in self.templates.items():
            with open(os.path.join(self.tmpdir, filename), "w", encoding="utf-8") as f:
                f.write(content)

    def test_load_plan_template(self):
        result = self.loader.load_template("plan")
        assert result == "Plan template: {{context}}"

    def test_load_draft_template(self):
        result = self.loader.load_template("draft")
        assert result == "Draft template: {{context}}"

    def test_load_self_critique_template(self):
        result = self.loader.load_template("self_critique")
        assert result == "Self-critique template: {{context}}"

    def test_load_refine_template(self):
        result = self.loader.load_template("refine")
        assert result == "Refine template: {{context}}"

    def test_unknown_step_name_raises_error(self):
        with pytest.raises(PromptNotFoundError, match="Unknown step name"):
            self.loader.load_template("unknown_step")

    def test_empty_step_name_raises_error(self):
        with pytest.raises(PromptNotFoundError, match="Unknown step name"):
            self.loader.load_template("")

    def test_file_not_found_raises_error(self):
        # Use an empty directory with no prompt files
        empty_dir = tempfile.mkdtemp()
        loader = PromptTemplateLoader(empty_dir)
        with pytest.raises(PromptNotFoundError, match="Prompt template file not found"):
            loader.load_template("plan")

    def test_step_files_mapping(self):
        assert PromptTemplateLoader.STEP_FILES == {
            "plan": "plan.md",
            "draft": "draft.md",
            "self_critique": "self_critique.md",
            "refine": "refine.md",
        }

    def test_error_message_lists_valid_steps(self):
        with pytest.raises(PromptNotFoundError) as exc_info:
            self.loader.load_template("invalid")
        msg = str(exc_info.value)
        for step in ["draft", "plan", "refine", "self_critique"]:
            assert step in msg
