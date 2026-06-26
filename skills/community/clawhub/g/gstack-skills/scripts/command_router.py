#!/usr/bin/env python3
"""
Command Router for gstack-skills

This script routes user commands to the appropriate specialized skill.
It parses user input and determines which skill should be invoked.

Usage:
    python command_router.py "<user_input>"
"""

import re
import json
import sys
from pathlib import Path
from typing import Dict, Optional, Tuple

# Command to skill mapping
COMMAND_TO_SKILL = {
    "/gstack": "gstack-skills",
    "/office-hours": "office-hours",
    "/plan-ceo-review": "plan-ceo-review",
    "/plan-eng-review": "plan-eng-review",
    "/plan-design-review": "plan-design-review",
    "/design-consultation": "design-consultation",
    "/review": "review",
    "/investigate": "investigate",
    "/design-review": "design-review",
    "/qa": "qa",
    "/qa-only": "qa-only",
    "/ship": "ship",
    "/document-release": "document-release",
    "/retro": "retro",
    "/codex": "codex",
    "/careful": "careful",
    "/freeze": "freeze",
    "/guard": "guard",
}

# Keyword patterns for skill detection
KEYWORD_PATTERNS = {
    "office-hours": [
        r"brainstorm",
        r"i have an idea",
        r"help me think through",
        r"validate my.*idea",
        r"product idea",
        r"startup.*idea",
    ],
    "plan-ceo-review": [
        r"think bigger",
        r"expand scope",
        r"strategic review",
        r"rethink",
        r"ceo.*perspective",
        r"ambition",
    ],
    "plan-eng-review": [
        r"engineering review",
        r"architecture review",
        r"technical.*review",
        r"implementation.*approach",
        r"tech.*decision",
    ],
    "review": [
        r"review.*pr",
        r"code review",
        r"pre-landing review",
        r"check.*diff",
        r"review.*branch",
        r"review.*changes",
    ],
    "investigate": [
        r"debug.*this",
        r"investigate",
        r"root cause",
        r"why.*fail",
        r"troubleshoot",
        r"bug.*investigation",
    ],
    "qa": [
        r"run qa",
        r"test.*this",
        r"check.*bug",
        r"quality check",
        r"qa.*test",
        r"test.*application",
    ],
    "ship": [
        r"ship",
        r"deploy",
        r"push.*main",
        r"create.*pr",
        r"merge.*push",
        r"release.*code",
        r"prepare.*deploy",
    ],
}


class CommandRouter:
    """Routes user commands to appropriate skills."""

    def __init__(self, skills_base_path: str):
        """
        Initialize the command router.

        Args:
            skills_base_path: Base path to the skills directory
        """
        self.skills_base_path = Path(skills_base_path)
        self.command_to_skill = COMMAND_TO_SKILL
        self.keyword_patterns = KEYWORD_PATTERNS

    def parse_command(self, user_input: str) -> Tuple[Optional[str], str]:
        """
        Parse user input and determine the appropriate skill.

        Args:
            user_input: Raw user input string

        Returns:
            Tuple of (skill_name, command_arguments)
            Returns (None, user_input) if no specific skill is identified
        """
        user_input = user_input.strip()

        # Check for explicit commands (e.g., "/review", "/ship")
        for command, skill_name in self.command_to_skill.items():
            if user_input.startswith(command):
                # Extract arguments after the command
                args = user_input[len(command):].strip()
                return skill_name, args

        # Check for keyword patterns
        for skill_name, patterns in self.keyword_patterns.items():
            for pattern in patterns:
                if re.search(pattern, user_input, re.IGNORECASE):
                    return skill_name, user_input

        # No specific skill identified
        return None, user_input

    def get_skill_path(self, skill_name: str) -> Path:
        """
        Get the file path to a skill's SKILL.md file.

        Args:
            skill_name: Name of the skill

        Returns:
            Path to the skill directory
        """
        return self.skills_base_path / skill_name / "SKILL.md"

    def skill_exists(self, skill_name: str) -> bool:
        """
        Check if a skill exists.

        Args:
            skill_name: Name of the skill

        Returns:
            True if skill exists, False otherwise
        """
        skill_path = self.get_skill_path(skill_name)
        return skill_path.exists()

    def route(self, user_input: str) -> Dict:
        """
        Route user input to the appropriate skill.

        Args:
            user_input: Raw user input string

        Returns:
            Dictionary with routing information
        """
        skill_name, args = self.parse_command(user_input)

        if skill_name is None:
            return {
                "status": "no_skill",
                "message": "No specific gstack skill identified for this input",
                "suggestion": "Use /gstack to see available commands",
                "original_input": user_input,
            }

        if not self.skill_exists(skill_name):
            return {
                "status": "skill_not_found",
                "message": f"Skill '{skill_name}' not found",
                "suggestion": "Install the missing skill or use /gstack for help",
                "requested_skill": skill_name,
                "original_input": user_input,
            }

        skill_path = self.get_skill_path(skill_name)

        return {
            "status": "routed",
            "skill_name": skill_name,
            "skill_path": str(skill_path),
            "arguments": args,
            "original_input": user_input,
        }

    def list_available_skills(self) -> list:
        """
        List all available skills.

        Returns:
            List of skill names
        """
        available = []
        for skill_name in self.command_to_skill.values():
            if self.skill_exists(skill_name):
                available.append(skill_name)
        return available


def main():
    """Main entry point for command line usage."""
    if len(sys.argv) < 2:
        print("Usage: python command_router.py '<user_input>'")
        print("Example: python command_router.py '/review my changes'")
        sys.exit(1)

    user_input = sys.argv[1]
    
    # Get the skills base path (relative to this script)
    script_dir = Path(__file__).parent
    skills_base_path = script_dir.parent

    router = CommandRouter(skills_base_path)
    result = router.route(user_input)

    # Output as JSON for programmatic use
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
