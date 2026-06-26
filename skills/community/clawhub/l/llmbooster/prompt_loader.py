"""Prompt Template Loader for LLMBooster skill."""

from __future__ import annotations

import os


class PromptNotFoundError(Exception):
    """Raised when a prompt template file cannot be found or step name is unknown."""


class PromptTemplateLoader:
    """
    Reads prompt template files from prompts/ directory.
    Each thinking step corresponds to one file: plan.md, draft.md, self_critique.md, refine.md.
    """

    STEP_FILES: dict[str, str] = {
        "plan": "plan.md",
        "draft": "draft.md",
        "self_critique": "self_critique.md",
        "refine": "refine.md",
    }

    def __init__(self, prompts_dir: str) -> None:
        self.prompts_dir = prompts_dir

    def load_template(self, step_name: str) -> str:
        """Load prompt template for specified step.

        Args:
            step_name: The thinking step name (plan, draft, self_critique, refine).

        Returns:
            The prompt template content as a string.

        Raises:
            PromptNotFoundError: If step_name is unknown or the file doesn't exist.
        """
        if step_name not in self.STEP_FILES:
            raise PromptNotFoundError(
                f"Unknown step name: '{step_name}'. "
                f"Valid steps: {', '.join(sorted(self.STEP_FILES))}"
            )

        filename = self.STEP_FILES[step_name]
        filepath = os.path.join(self.prompts_dir, filename)

        if not os.path.isfile(filepath):
            raise PromptNotFoundError(
                f"Prompt template file not found: {filepath}"
            )

        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
