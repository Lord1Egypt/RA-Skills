"""Property-based test: Prompt template 正確載入.

Feature: llm-booster-skill, Property 3: Prompt template 正確載入
Validates: Requirements 1.3
"""

from __future__ import annotations

import os
import sys
import tempfile

from hypothesis import given, settings, strategies as st

# Ensure the skill package is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from prompt_loader import PromptNotFoundError, PromptTemplateLoader

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

VALID_STEPS = ["plan", "draft", "self_critique", "refine"]

STEP_FILE_MAPPING: dict[str, str] = {
    "plan": "plan.md",
    "draft": "draft.md",
    "self_critique": "self_critique.md",
    "refine": "refine.md",
}

# ---------------------------------------------------------------------------
# Strategies
# ---------------------------------------------------------------------------

# Valid step names
valid_step_names = st.sampled_from(VALID_STEPS)

# Random template content (non-empty strings).
# Exclude bare \r since Python text-mode I/O normalises \r → \n,
# which is expected behaviour for text files, not a bug.
# Also exclude surrogates (\ud800-\udfff) which can't be encoded to UTF-8.
template_content = st.text(
    alphabet=st.characters(
        blacklist_characters="\r",
        blacklist_categories=("Cs",),
    ),
    min_size=1,
    max_size=500,
)

# Invalid step names: arbitrary text that is NOT one of the valid steps
invalid_step_names = st.text(min_size=0, max_size=100).filter(
    lambda s: s not in VALID_STEPS
)


# ---------------------------------------------------------------------------
# Property 3: Prompt template 正確載入
# ---------------------------------------------------------------------------


class TestPromptTemplateLoadingProperty:
    """**Validates: Requirements 1.3**"""

    @settings(max_examples=100)
    @given(step_name=valid_step_names, content=template_content)
    def test_valid_step_loads_correct_file(
        self, step_name: str, content: str
    ) -> None:
        """For any valid step name, load_template returns the content of the
        corresponding file from the prompts/ directory, verifying the mapping:
        plan→plan.md, draft→draft.md, self_critique→self_critique.md,
        refine→refine.md."""

        tmpdir = tempfile.mkdtemp()
        try:
            # Write only the file for this step with the random content
            expected_filename = STEP_FILE_MAPPING[step_name]
            filepath = os.path.join(tmpdir, expected_filename)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)

            loader = PromptTemplateLoader(tmpdir)
            result = loader.load_template(step_name)

            assert result == content, (
                f"Step '{step_name}' should load from '{expected_filename}' "
                f"with exact content, got different content"
            )
        finally:
            # Cleanup
            for fname in os.listdir(tmpdir):
                os.remove(os.path.join(tmpdir, fname))
            os.rmdir(tmpdir)

    @settings(max_examples=100)
    @given(step_name=invalid_step_names)
    def test_invalid_step_raises_prompt_not_found_error(
        self, step_name: str
    ) -> None:
        """For any step name that is NOT one of the valid steps (plan, draft,
        self_critique, refine), load_template raises PromptNotFoundError."""

        tmpdir = tempfile.mkdtemp()
        try:
            loader = PromptTemplateLoader(tmpdir)
            try:
                loader.load_template(step_name)
                assert False, (
                    f"Expected PromptNotFoundError for invalid step name "
                    f"'{step_name!r}', but no exception was raised"
                )
            except PromptNotFoundError:
                pass  # Expected
        finally:
            os.rmdir(tmpdir)
