#!/usr/bin/env python3
"""
Assertion-based grading for skill benchmark results.

Usage:
    python3 grade-assertions.py --workspace /path/to/results
    python3 grade-assertions.py --workspace /path/to/results --verbose

This script reads benchmark execution results from a workspace directory
and grades them against defined assertions.

Workspace structure expected:
    /path/to/results/
        grading-config.json      # Assertion definitions
        iteration-1/
            test-name/
                with_skill/outputs/
                    result.md
                without_skill/outputs/
                    result.md

Output:
    grading.json with pass/fail per assertion and summary statistics.
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path


# --- Assertion Types ---

class AssertionResult:
    def __init__(self, assertion_type, text, passed, evidence="", category=""):
        self.type = assertion_type
        self.text = text
        self.passed = passed
        self.evidence = evidence
        self.category = category

    def to_dict(self):
        return {
            "type": self.type,
            "text": self.text,
            "passed": self.passed,
            "evidence": self.evidence,
            "category": self.category,
        }


def check_keyword_absent(content, keyword, case_sensitive=False):
    """Assertion: a banned keyword should NOT appear in output."""
    if case_sensitive:
        found = keyword in content
    else:
        found = keyword.lower() in content.lower()
    return not found


def check_keyword_present(content, keyword, case_sensitive=False):
    """Assertion: a required keyword MUST appear in output."""
    if case_sensitive:
        found = keyword in content
    else:
        found = keyword.lower() in content.lower()
    return found


def check_required_section(content, section_marker):
    """Assertion: a required section header must appear in output."""
    # Match markdown headers like "## Section Name" or "### Section"
    pattern = rf"^#+\s+{re.escape(section_marker)}"
    return bool(re.search(pattern, content, re.MULTILINE))


def check_file_exists(filepath):
    """Assertion: a file must exist."""
    return os.path.isfile(filepath)


def check_format_json(content):
    """Assertion: content must be valid JSON."""
    try:
        json.loads(content)
        return True
    except (json.JSONDecodeError, TypeError):
        return False


def check_format_markdown(content, min_lines=5):
    """Assertion: content must be valid markdown with minimum lines."""
    lines = content.strip().split("\n")
    has_headers = any(re.match(r"^#+ ", line) for line in lines)
    return len(lines) >= min_lines and has_headers


def check_bilingual_keywords(content, zh_keyword, en_keyword):
    """Assertion: at least one language variant of a keyword must appear."""
    has_zh = zh_keyword in content
    has_en = en_keyword.lower() in content.lower()
    return has_zh or has_en


def check_no_hardcoded_credentials(content):
    """Assertion: no API keys, tokens, or credentials in content."""
    patterns = [
        r'sk-[a-zA-Z0-9]{20,}',  # OpenAI key
        r'ghp_[a-zA-Z0-9]{36}',  # GitHub PAT
        r'api[_-]?key["\']?\s*[=:]\s*["\'][^"\']{8,}',
        r'token["\']?\s*[=:]\s*["\'][^"\']{8,}',
    ]
    for pattern in patterns:
        if re.search(pattern, content, re.IGNORECASE):
            return False
    return True


def check_mention_count(content, keyword, min_count=1):
    """Assertion: a keyword must appear at least min_count times."""
    return content.lower().count(keyword.lower()) >= min_count


# --- Grading Engine ---

AVAILABLE_CHECKS = {
    "keyword_absent": check_keyword_absent,
    "keyword_present": check_keyword_present,
    "required_section": check_required_section,
    "file_exists": check_file_exists,
    "format_json": check_format_json,
    "format_markdown": check_format_markdown,
    "bilingual_keywords": check_bilingual_keywords,
    "no_hardcoded_credentials": check_no_hardcoded_credentials,
    "mention_count": check_mention_count,
}


def load_grading_config(workspace):
    """Load grading configuration from grading-config.json or generate defaults."""
    config_path = os.path.join(workspace, "grading-config.json")
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    
    # Default: grade all output files for basic quality
    return {
        "Assertions": [],
        "default_checks": {
            "format_markdown": True,
            "no_hardcoded_credentials": True,
        }
    }


def find_output_files(workspace):
    """Find all output files in the workspace."""
    outputs = []
    for root, dirs, files in os.walk(workspace):
        # Skip the workspace root and non-output directories
        if "outputs" in root:
            for f in files:
                if f.endswith((".md", ".txt", ".json", ".html")):
                    outputs.append(os.path.join(root, f))
    return outputs


def grade_file(filepath, assertions):
    """Grade a single output file against assertions."""
    results = []
    
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except (IOError, UnicodeDecodeError):
        return [AssertionResult(
            "file_exists", f"File: {filepath}", False,
            f"Could not read file", "file"
        )]
    
    # Check each assertion
    for assertion in assertions:
        check_type = assertion.get("type", "")
        params = assertion.get("params", {})
        category = assertion.get("category", "general")
        description = assertion.get("description", f"{check_type} check")
        
        if check_type not in AVAILABLE_CHECKS:
            results.append(AssertionResult(
                check_type, description, False,
                f"Unknown assertion type: {check_type}", category
            ))
            continue
        
        check_fn = AVAILABLE_CHECKS[check_type]
        
        try:
            # Handle different check signatures
            if check_type == "keyword_absent":
                passed = check_fn(content, params.get("keyword"), params.get("case_sensitive", False))
                evidence = f"'{params.get('keyword')}' {'found' if not passed else 'not found'}"
            elif check_type == "keyword_present":
                passed = check_fn(content, params.get("keyword"), params.get("case_sensitive", False))
                evidence = f"'{params.get('keyword')}' {'found' if passed else 'not found'}"
            elif check_type == "required_section":
                passed = check_fn(content, params.get("section"))
                evidence = f"Section '{params.get('section')}' {'found' if passed else 'not found'}"
            elif check_type == "file_exists":
                passed = check_fn(filepath)
                evidence = f"File exists: {passed}"
            elif check_type == "format_json":
                passed = check_fn(content)
                evidence = f"Valid JSON: {passed}"
            elif check_type == "format_markdown":
                passed = check_fn(content, params.get("min_lines", 5))
                evidence = f"Valid markdown with {len(content.split())} lines: {passed}"
            elif check_type == "bilingual_keywords":
                passed = check_fn(content, params.get("zh"), params.get("en"))
                evidence = f"Keywords '{params.get('zh')}' or '{params.get('en')}' found: {passed}"
            elif check_type == "no_hardcoded_credentials":
                passed = check_fn(content)
                evidence = f"No credentials found: {passed}"
            elif check_type == "mention_count":
                passed = check_fn(content, params.get("keyword"), params.get("min_count", 1))
                evidence = f"'{params.get('keyword')}' appears {content.lower().count(params.get('keyword').lower())} times (min: {params.get('min_count', 1)})"
            else:
                passed = False
                evidence = "Unknown check type"
            
            results.append(AssertionResult(
                check_type, description, passed, evidence, category
            ))
        except Exception as e:
            results.append(AssertionResult(
                check_type, description, False, f"Check error: {e}", category
            ))
    
    return results


def grade_workspace(workspace, verbose=False):
    """Grade all outputs in a workspace against assertions."""
    workspace = os.path.abspath(workspace)
    
    if not os.path.exists(workspace):
        return {
            "error": f"Workspace not found: {workspace}",
            "expectations": [],
            "summary": {"passed": 0, "failed": 0, "total": 0, "pass_rate": 0}
        }
    
    config = load_grading_config(workspace)
    assertions = config.get("Assertions", [])
    
    # If no assertions defined, use default checks
    if not assertions:
        assertions = _get_default_assertions()
    
    output_files = find_output_files(workspace)
    
    if verbose:
        print(f"Grading workspace: {workspace}")
        print(f"Found {len(output_files)} output files")
        print(f"Running {len(assertions)} assertions per file")
    
    all_results = []
    
    for filepath in output_files:
        if verbose:
            print(f"  Grading: {os.path.relpath(filepath, workspace)}")
        results = grade_file(filepath, assertions)
        all_results.extend(results)
    
    # Deduplicate by text
    seen = set()
    unique_results = []
    for r in all_results:
        if r.text not in seen:
            seen.add(r.text)
            unique_results.append(r)
    
    return {
        "workspace": workspace,
        "files_checked": len(output_files),
        "assertions": [r.to_dict() for r in unique_results],
        "expectations": [r.to_dict() for r in unique_results],
        "summary": {
            "passed": sum(1 for r in unique_results if r.passed),
            "failed": sum(1 for r in unique_results if not r.passed),
            "total": len(unique_results),
            "pass_rate": sum(1 for r in unique_results if r.passed) / max(len(unique_results), 1),
        }
    }


def _get_default_assertions():
    """Get default assertions for markdown-based outputs."""
    return [
        {
            "type": "format_markdown",
            "description": "Output should be valid markdown with headers",
            "category": "format",
            "params": {"min_lines": 5}
        },
        {
            "type": "no_hardcoded_credentials",
            "description": "Output should not contain hardcoded credentials",
            "category": "security",
            "params": {}
        },
        {
            "type": "keyword_present",
            "description": "Output should contain substantive content",
            "category": "quality",
            "params": {"keyword": "##", "case_sensitive": False}
        },
    ]


def main():
    parser = argparse.ArgumentParser(
        description="Grade benchmark results against assertions"
    )
    parser.add_argument(
        "--workspace", "-w", required=True,
        help="Path to benchmark results workspace"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true",
        help="Show detailed grading output"
    )
    parser.add_argument(
        "--json", action="store_true",
        help="Output JSON format"
    )
    args = parser.parse_args()
    
    result = grade_workspace(args.workspace, verbose=args.verbose)
    
    # Save grading.json
    grading_path = os.path.join(args.workspace, "grading.json")
    with open(grading_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        summary = result["summary"]
        total = summary["total"]
        passed = summary["passed"]
        failed = summary["failed"]
        rate = summary["pass_rate"]
        
        print(f"\n📊 Grading Results")
        print(f"{'=' * 50}")
        print(f"Files checked: {result.get('files_checked', 0)}")
        print(f"Total assertions: {total}")
        print(f"  ✅ Passed: {passed}")
        print(f"  ❌ Failed: {failed}")
        print(f"  Pass rate: {rate:.1%}")
        print(f"{'=' * 50}")
        
        if failed > 0 and verbose:
            print("\nFailed assertions:")
            for a in result["assertions"]:
                if not a["passed"]:
                    print(f"  ❌ {a['text']}")
                    print(f"     Evidence: {a['evidence']}")
        
        print(f"\n📁 Results saved to: {grading_path}")


if __name__ == "__main__":
    main()
