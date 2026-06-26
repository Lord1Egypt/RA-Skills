#!/usr/bin/env python3
"""
Fetch a problem from NCCUOJ and output formatted Markdown.

Usage:
  python get_problem.py <problem_id>                                              # public problem
  python get_problem.py <problem_id> --username <user> --password <pass>           # with login
  python get_problem.py <problem_id> --contest <contest_id> --username <u> --password <p>
  python get_problem.py <problem_id> --raw                                        # raw JSON output

Output: Markdown-formatted problem statement to stdout.
"""

import argparse
import json
import sys
import os
import re
from urllib.parse import unquote

sys.path.insert(0, os.path.dirname(__file__))
from session import get_session, api_get, api_post, API_URL


def html_to_markdown(html):
    """Simple HTML to Markdown conversion for OJ problem descriptions."""
    if not html:
        return ""
    text = html
    # <br> / <br/> → newline
    text = re.sub(r'<br\s*/?>', '\n', text)
    # <p>...</p> → paragraph
    text = re.sub(r'<p>(.*?)</p>', r'\1\n', text, flags=re.DOTALL)
    # <strong>/<b> → bold
    text = re.sub(r'<(?:strong|b)>(.*?)</(?:strong|b)>', r'**\1**', text, flags=re.DOTALL)
    # <em>/<i> → italic
    text = re.sub(r'<(?:em|i)>(.*?)</(?:em|i)>', r'*\1*', text, flags=re.DOTALL)
    # <code> → inline code
    text = re.sub(r'<code>(.*?)</code>', r'`\1`', text, flags=re.DOTALL)
    # <pre> → code block
    text = re.sub(r'<pre>(.*?)</pre>', r'```\n\1\n```', text, flags=re.DOTALL)
    # <ul>/<ol>/<li>
    text = re.sub(r'<li>(.*?)</li>', r'- \1', text, flags=re.DOTALL)
    text = re.sub(r'</?(?:ul|ol)>', '', text)
    # <sub>/<sup> for math
    text = re.sub(r'<sup>(.*?)</sup>', r'^{\1}', text, flags=re.DOTALL)
    text = re.sub(r'<sub>(.*?)</sub>', r'_{\1}', text, flags=re.DOTALL)
    # Strip remaining tags
    text = re.sub(r'<[^>]+>', '', text)
    # Collapse multiple blank lines
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def decode_field(value):
    """URL-decode a field and convert HTML to Markdown."""
    if not value:
        return ""
    decoded = unquote(value)
    return html_to_markdown(decoded)


def format_problem(data):
    """Format problem JSON into Markdown."""
    lines = []
    display_id = data.get("_id", "")
    title = data.get("title", "")
    lines.append(f"# {display_id}. {title}")
    lines.append("")

    # Metadata
    difficulty = data.get("difficulty", "")
    rule_type = data.get("rule_type", "")
    time_limit = data.get("time_limit", "")
    memory_limit = data.get("memory_limit", "")
    internal_id = data.get("id", "")
    tags = data.get("tags", [])

    lines.append(f"- **Internal ID**: {internal_id}")
    lines.append(f"- **Difficulty**: {difficulty}")
    lines.append(f"- **Rule**: {rule_type}")
    lines.append(f"- **Time Limit**: {time_limit} ms")
    lines.append(f"- **Memory Limit**: {memory_limit} MB")
    if tags:
        lines.append(f"- **Tags**: {', '.join(tags)}")
    lines.append("")

    # Description
    desc = decode_field(data.get("description", ""))
    if desc:
        lines.append("## Description")
        lines.append("")
        lines.append(desc)
        lines.append("")

    # Input
    inp = decode_field(data.get("input_description", ""))
    if inp:
        lines.append("## Input")
        lines.append("")
        lines.append(inp)
        lines.append("")

    # Output
    out = decode_field(data.get("output_description", ""))
    if out:
        lines.append("## Output")
        lines.append("")
        lines.append(out)
        lines.append("")

    # Samples
    samples = data.get("samples", [])
    if samples:
        lines.append("## Samples")
        lines.append("")
        for i, s in enumerate(samples, 1):
            lines.append(f"### Sample {i}")
            lines.append("")
            lines.append("**Input**")
            lines.append("```")
            lines.append(s.get("input", "").strip())
            lines.append("```")
            lines.append("")
            lines.append("**Output**")
            lines.append("```")
            lines.append(s.get("output", "").strip())
            lines.append("```")
            lines.append("")

    # Hint
    hint = decode_field(data.get("hint", ""))
    if hint:
        lines.append("## Hint")
        lines.append("")
        lines.append(hint)
        lines.append("")

    # Allowed Languages
    languages = data.get("languages", [])
    if languages:
        lines.append("## Allowed Languages")
        lines.append("")
        lines.append(", ".join(f"`{l}`" for l in languages))
        lines.append("")

    # Statistics
    submission_number = data.get("submission_number", 0)
    accepted_number = data.get("accepted_number", 0)
    if submission_number:
        ac_rate = f"{accepted_number / submission_number * 100:.1f}%" if submission_number else "N/A"
        lines.append("## Statistics")
        lines.append("")
        lines.append(f"- **Submissions**: {submission_number}")
        lines.append(f"- **Accepted**: {accepted_number}")
        lines.append(f"- **AC Rate**: {ac_rate}")
        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Fetch an NCCUOJ problem")
    parser.add_argument("problem_id", help="Problem display ID")
    parser.add_argument("--contest", type=int, help="Contest ID (for contest problems)")
    parser.add_argument("--username", help="NCCUOJ username (required for some problems)")
    parser.add_argument("--password", help="NCCUOJ password (required for some problems)")
    parser.add_argument("--raw", action="store_true", help="Output raw JSON instead of Markdown")
    args = parser.parse_args()

    opener, cookie_jar, csrf = get_session()

    if args.username and args.password:
        api_post(opener, cookie_jar, f"{API_URL}/login", {
            "username": args.username,
            "password": args.password,
        })

    if args.contest:
        url = f"{API_URL}/contest/problem?contest_id={args.contest}&problem_id={args.problem_id}"
    else:
        url = f"{API_URL}/problem?problem_id={args.problem_id}"

    data = api_get(opener, url)

    if args.raw:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print(format_problem(data))


if __name__ == "__main__":
    main()
