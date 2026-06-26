#!/usr/bin/env python3
"""Parse notebooklm ask JSON output and extract SKILL.md content."""
import json
import re
import sys


def extract_skill_content(answer: str) -> str:
    """Extract SKILL.md markdown from a notebooklm answer string."""
    # Try to find a ```markdown code block
    md_pattern = r'```markdown\s*\n(.*?)```'
    match = re.search(md_pattern, answer, re.DOTALL)
    if match:
        content = match.group(1).strip()
        if content.startswith('---'):
            return content

    # Try any ``` code block
    any_pattern = r'```\s*\n(.*?)```'
    match = re.search(any_pattern, answer, re.DOTALL)
    if match:
        content = match.group(1).strip()
        if content.startswith('---'):
            return content

    # Try to find YAML frontmatter directly in the text
    fm_pattern = r'^---\s*\n.*?^---\s*\n'
    match = re.search(fm_pattern, answer, re.DOTALL | re.MULTILINE)
    if match:
        start = match.start()
        return answer[start:].strip()

    # Fallback: return raw answer
    return answer.strip()


def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            data = json.load(f)
    else:
        data = json.load(sys.stdin)

    answer = data.get('answer', '')
    if not answer:
        print("Error: no 'answer' field in JSON input", file=sys.stderr)
        sys.exit(1)

    skill_content = extract_skill_content(answer)

    # Basic validation
    if not skill_content.startswith('---'):
        print("Warning: extracted content doesn't start with YAML frontmatter", file=sys.stderr)

    print(skill_content)


if __name__ == '__main__':
    main()
