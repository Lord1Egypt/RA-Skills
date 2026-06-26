#!/usr/bin/env python3
"""
Quick validation script for skills - minimal version (no external dependencies)
"""

import sys
import re
from pathlib import Path

# Allowed frontmatter properties
ALLOWED_PROPERTIES = {'name', 'description', 'license', 'allowed-tools', 'metadata'}


def parse_simple_yaml(text):
    """
    Parse simple YAML frontmatter without external dependencies.
    Only handles top-level key: value pairs (sufficient for skill frontmatter).
    """
    result = {}
    current_key = None
    current_value_lines = []

    for line in text.split('\n'):
        # Check if line starts a new key (not indented, has colon)
        key_match = re.match(r'^([a-z][a-z0-9-]*)\s*:\s*(.*)', line)
        if key_match:
            # Save previous key if exists
            if current_key:
                result[current_key] = '\n'.join(current_value_lines).strip()
            current_key = key_match.group(1)
            current_value_lines = [key_match.group(2)]
        elif current_key and (line.startswith('  ') or line.startswith('\t') or not line.strip()):
            # Continuation of multi-line value
            current_value_lines.append(line)

    # Save last key
    if current_key:
        result[current_key] = '\n'.join(current_value_lines).strip()

    return result


def validate_skill(skill_path):
    """Basic validation of a skill"""
    skill_path = Path(skill_path)

    # Check SKILL.md exists
    skill_md = skill_path / 'SKILL.md'
    if not skill_md.exists():
        return False, "SKILL.md not found"

    # Read and validate frontmatter
    content = skill_md.read_text()
    if not content.startswith('---'):
        return False, "No YAML frontmatter found"

    # Extract frontmatter
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return False, "Invalid frontmatter format"

    frontmatter_text = match.group(1)

    # Parse YAML frontmatter (simple parser, no external deps)
    try:
        frontmatter = parse_simple_yaml(frontmatter_text)
    except Exception as e:
        return False, f"Failed to parse frontmatter: {e}"

    # Check for unexpected properties
    unexpected_keys = set(frontmatter.keys()) - ALLOWED_PROPERTIES
    if unexpected_keys:
        return False, (
            f"Unexpected key(s) in SKILL.md frontmatter: {', '.join(sorted(unexpected_keys))}. "
            f"Allowed properties are: {', '.join(sorted(ALLOWED_PROPERTIES))}"
        )

    # Check required fields
    if 'name' not in frontmatter:
        return False, "Missing 'name' in frontmatter"
    if 'description' not in frontmatter:
        return False, "Missing 'description' in frontmatter"

    # Extract name for validation
    name = frontmatter.get('name', '').strip()
    if name:
        # Check naming convention (hyphen-case: lowercase with hyphens)
        if not re.match(r'^[a-z0-9-]+$', name):
            return False, f"Name '{name}' should be hyphen-case (lowercase letters, digits, and hyphens only)"
        if name.startswith('-') or name.endswith('-') or '--' in name:
            return False, f"Name '{name}' cannot start/end with hyphen or contain consecutive hyphens"
        # Check name length (max 64 characters per spec)
        if len(name) > 64:
            return False, f"Name is too long ({len(name)} characters). Maximum is 64 characters."

    # Extract and validate description
    description = frontmatter.get('description', '').strip()
    if description:
        # Check for angle brackets
        if '<' in description or '>' in description:
            return False, "Description cannot contain angle brackets (< or >)"
        # Check description length (max 1024 characters per spec)
        if len(description) > 1024:
            return False, f"Description is too long ({len(description)} characters). Maximum is 1024 characters."

    return True, "Skill is valid!"

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python quick_validate.py <skill_directory>")
        sys.exit(1)

    valid, message = validate_skill(sys.argv[1])
    print(message)
    sys.exit(0 if valid else 1)
