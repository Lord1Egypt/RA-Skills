#!/usr/bin/env python3
"""Validate commit message format against conventional commits standard."""

import re
import sys


def validate_commit_message(message: str) -> tuple[bool, list[str]]:
    """
    Validate a commit message against the conventional commits format.

    Args:
        message: The commit message to validate

    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    lines = message.strip().split('\n')

    if not lines:
        return False, ["Commit message is empty"]

    subject = lines[0]

    # Check subject line format: type(scope): description
    # Scope is optional
    pattern = r'^(feat|fix|refactor|docs|test|chore)(\([a-z0-9-]+\))?: .+'
    if not re.match(pattern, subject):
        errors.append(
            "Subject line must follow format: type(scope): description\n"
            "Valid types: feat, fix, refactor, docs, test, chore\n"
            "Scope is optional but must be lowercase with hyphens if present"
        )

    # Check subject line length
    if len(subject) > 72:
        errors.append(f"Subject line too long ({len(subject)} chars). Keep under 72 characters.")

    # Check for imperative mood (basic check)
    description_match = re.search(r': (.+)$', subject)
    if description_match:
        description = description_match.group(1)
        # Common mistakes: past tense verbs
        past_tense_patterns = [
            r'^added ', r'^fixed ', r'^updated ', r'^removed ',
            r'^changed ', r'^implemented ', r'^refactored '
        ]
        for pattern in past_tense_patterns:
            if re.match(pattern, description, re.IGNORECASE):
                suggestion = (description
                    .replace('added', 'add').replace('fixed', 'fix')
                    .replace('updated', 'update').replace('removed', 'remove')
                    .replace('changed', 'change').replace('implemented', 'implement')
                    .replace('refactored', 'refactor'))
                errors.append(
                    f"Use imperative mood: '{description}' -> '{suggestion}'"
                )
                break

    # Check for forbidden AI markers
    forbidden_patterns = [
        r'Generated with.*Claude',
        r'Co-Authored-By:.*Claude',
        r'🤖.*Generated',
        r'AI[- ]generated',
    ]
    full_message = '\n'.join(lines)
    for pattern in forbidden_patterns:
        if re.search(pattern, full_message, re.IGNORECASE):
            errors.append(
                "Commit message must not contain Claude Code signatures, "
                "co-author attributions, or AI-generated markers"
            )
            break

    # Check body format if present
    if len(lines) > 1:
        # Should have blank line after subject
        if lines[1].strip() != '':
            errors.append("Include blank line between subject and body")

        # Count bullet points
        bullet_count = sum(1 for line in lines[2:] if line.strip().startswith('-'))
        if bullet_count > 4:
            errors.append(f"Body has {bullet_count} bullet points. Keep to maximum 3-4.")

    return len(errors) == 0, errors


def main():
    """Main entry point for CLI usage."""
    if len(sys.argv) < 2:
        print("Usage: validate_commit.py <commit_message>")
        print("   or: validate_commit.py --file <message_file>")
        sys.exit(1)

    if sys.argv[1] == '--file':
        if len(sys.argv) < 3:
            print("Error: --file requires a filename")
            sys.exit(1)
        with open(sys.argv[2], 'r') as f:
            message = f.read()
    else:
        message = ' '.join(sys.argv[1:])

    is_valid, errors = validate_commit_message(message)

    if is_valid:
        print("✅ Commit message is valid")
        sys.exit(0)
    else:
        print("❌ Commit message validation failed:\n")
        for error in errors:
            print(f"  • {error}")
        sys.exit(1)


if __name__ == '__main__':
    main()
