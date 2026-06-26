#!/usr/bin/env python3
import argparse
import json
import re
import glob
import sys
import os
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
import datetime

@dataclass
class LintIssue:
    line: int
    column: int
    rule: str
    severity: str  # 'error', 'warning', 'info'
    message: str
    fix: Optional[str] = None

class MarkdownLinter:
    def __init__(self, max_line_length: int = 80, check_external_links: bool = False):
        self.max_line_length = max_line_length
        self.check_external_links = check_external_links
        self.issues: List[LintIssue] = []
        
    def lint_file(self, filepath: str) -> Dict[str, Any]:
        """Lint a single markdown file."""
        self.issues = []
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except Exception as e:
            return {
                "file": filepath,
                "error": str(e),
                "issues": [],
                "summary": {"total_issues": 0, "errors": 0, "warnings": 0}
            }
        
        # Apply each rule
        self.check_header_hierarchy(lines)
        self.check_image_alt_text(lines)
        self.check_line_length(lines)
        self.check_trailing_whitespace(lines)
        self.check_list_consistency(lines)
        self.check_code_block_language(lines)
        self.check_empty_links(lines)
        self.check_duplicate_headers(lines)
        
        # Internal link checking requires parsing the whole file
        self.check_internal_links(lines, filepath)
        
        # External link checking (optional, slow)
        if self.check_external_links:
            self.check_external_links_func(lines)
        
        # Categorize issues
        errors = sum(1 for i in self.issues if i.severity == 'error')
        warnings = sum(1 for i in self.issues if i.severity == 'warning')
        
        return {
            "file": filepath,
            "issues": [asdict(i) for i in self.issues],
            "summary": {
                "total_issues": len(self.issues),
                "errors": errors,
                "warnings": warnings
            }
        }
    
    def add_issue(self, line_num: int, column: int, rule: str, severity: str, message: str, fix: str = None):
        """Add a linting issue."""
        # Convert to 1-indexed for user display
        self.issues.append(LintIssue(
            line=line_num + 1,
            column=column + 1,
            rule=rule,
            severity=severity,
            message=message,
            fix=fix
        ))
    
    # Rule implementations
    def check_header_hierarchy(self, lines: List[str]):
        """MD001: Header hierarchy should only increment by one level at a time."""
        prev_level = 0
        for i, line in enumerate(lines):
            match = re.match(r'^(#+)\s', line)
            if match:
                level = len(match.group(1))
                if level > prev_level + 1 and prev_level > 0:
                    self.add_issue(
                        i, 0, "MD001", "warning",
                        f"Header levels should only increment by one level at a time (jumped from h{prev_level} to h{level})",
                        f"Change {'#' * level} to {'#' * (prev_level + 1)}"
                    )
                prev_level = level
    
    def check_image_alt_text(self, lines: List[str]):
        """MD002: Images should have descriptive alt text."""
        img_pattern = r'!\[(.*?)\]\(.*?\)'
        for i, line in enumerate(lines):
            # Find all image markdown in line
            for match in re.finditer(img_pattern, line):
                alt_text = match.group(1).strip()
                if not alt_text or alt_text == '':
                    col = match.start()
                    self.add_issue(
                        i, col, "MD002", "warning",
                        "Image missing descriptive alt text",
                        "Add descriptive text between brackets: ![description](url)"
                    )
    
    def check_line_length(self, lines: List[str]):
        """MD004: Lines should not exceed maximum length."""
        for i, line in enumerate(lines):
            # Don't count newline
            line_len = len(line.rstrip('\n\r'))
            if line_len > self.max_line_length:
                self.add_issue(
                    i, self.max_line_length, "MD004", "warning",
                    f"Line exceeds maximum length ({line_len} > {self.max_line_length})",
                    "Split the line or reduce content"
                )
    
    def check_trailing_whitespace(self, lines: List[str]):
        """MD005: Lines should not have trailing whitespace."""
        for i, line in enumerate(lines):
            if line.rstrip('\n\r') != line.rstrip():
                # Find the trailing whitespace
                stripped = line.rstrip('\n\r')
                trailing = line[len(stripped):-1] if line.endswith('\n') else line[len(stripped):]
                col = len(stripped)
                self.add_issue(
                    i, col, "MD005", "warning",
                    "Line has trailing whitespace",
                    "Remove trailing spaces/tabs"
                )
    
    def check_list_consistency(self, lines: List[str]):
        """MD006: List markers should be consistent within the same list."""
        # Simplified: check that each list uses consistent markers
        list_markers = []
        current_list_start = -1
        current_marker = None
        
        for i, line in enumerate(lines):
            match = re.match(r'^(\s*)([-*+]|\d+\.)\s', line)
            if match:
                marker = match.group(2)
                if current_list_start == -1:
                    current_list_start = i
                    current_marker = marker
                elif marker != current_marker:
                    self.add_issue(
                        i, match.start(2), "MD006", "warning",
                        f"Inconsistent list marker (using '{marker}' in list started with '{current_marker}')",
                        f"Change to '{current_marker}' for consistency"
                    )
            else:
                # Blank line or non-list line ends the current list
                if line.strip() == '':
                    continue
                else:
                    current_list_start = -1
                    current_marker = None
    
    def check_code_block_language(self, lines: List[str]):
        """MD007: Code blocks should specify language when possible."""
        in_code_block = False
        code_block_start = -1
        
        for i, line in enumerate(lines):
            if line.strip().startswith('```'):
                if not in_code_block:
                    # Starting a code block
                    in_code_block = True
                    code_block_start = i
                    # Check if language is specified
                    lang = line.strip()[3:].strip()
                    if not lang:
                        self.add_issue(
                            i, 0, "MD007", "info",
                            "Code block missing language specification",
                            "Add language after ```: ```python"
                        )
                else:
                    # Ending a code block
                    in_code_block = False
    
    def check_empty_links(self, lines: List[str]):
        """MD008: Links should not have empty text or URLs."""
        link_pattern = r'\[(.*?)\]\((.*?)\)'
        for i, line in enumerate(lines):
            for match in re.finditer(link_pattern, line):
                # Skip image links (already handled by MD002)
                start_pos = match.start()
                if start_pos > 0 and line[start_pos - 1] == '!':
                    continue
                
                link_text = match.group(1).strip()
                link_url = match.group(2).strip()
                col = start_pos
                
                if not link_text:
                    self.add_issue(
                        i, col, "MD008", "warning",
                        "Link has empty text",
                        "Add descriptive text between brackets: [text](url)"
                    )
                if not link_url:
                    self.add_issue(
                        i, col, "MD008", "error",
                        "Link has empty URL",
                        "Add URL between parentheses: [text](url)"
                    )
    
    def check_duplicate_headers(self, lines: List[str]):
        """MD009: Headers with duplicate text within the same file."""
        headers = {}
        for i, line in enumerate(lines):
            match = re.match(r'^#+\s+(.+)$', line)
            if match:
                header_text = match.group(1).strip().lower()
                if header_text in headers:
                    prev_line = headers[header_text]
                    self.add_issue(
                        i, 0, "MD009", "warning",
                        f"Duplicate header text (previously on line {prev_line + 1})",
                        "Consider using different header text or adding disambiguating content"
                    )
                else:
                    headers[header_text] = i
    
    def check_internal_links(self, lines: List[str], filepath: str):
        """MD003: Check internal links point to existing anchors in the same file."""
        # Extract all headers as potential anchors
        anchors = set()
        for line in lines:
            match = re.match(r'^#+\s+(.+)$', line)
            if match:
                header_text = match.group(1).strip()
                # Generate anchor: lowercase, replace spaces with hyphens, remove punctuation
                anchor = re.sub(r'[^\w\s-]', '', header_text.lower())
                anchor = re.sub(r'[-\s]+', '-', anchor)
                anchors.add('#' + anchor)
        
        # Check internal links
        for i, line in enumerate(lines):
            # Find links that start with #
            for match in re.finditer(r'\[.*?\]\((#.*?)\)', line):
                anchor = match.group(1)
                if anchor not in anchors:
                    col = match.start(1)
                    self.add_issue(
                        i, col, "MD003", "warning",
                        f"Internal link points to non-existent anchor: {anchor}",
                        f"Create a header that generates anchor {anchor} or fix the link"
                    )
    
    def check_external_links_func(self, lines: List[str]):
        """MD010: Check external URLs (requires requests)."""
        try:
            import requests
            from urllib.parse import urlparse
        except ImportError:
            # If requests not available, skip
            return
        
        url_pattern = r'\[.*?\]\((https?://[^\s)]+)\)'
        for i, line in enumerate(lines):
            for match in re.finditer(url_pattern, line):
                url = match.group(1)
                col = match.start(1)
                try:
                    response = requests.head(url, timeout=5, allow_redirects=True)
                    if response.status_code >= 400:
                        self.add_issue(
                            i, col, "MD010", "warning",
                            f"External link returns error status {response.status_code}: {url}",
                            "Check URL or remove link"
                        )
                except requests.exceptions.RequestException:
                    self.add_issue(
                        i, col, "MD010", "warning",
                        f"External link cannot be reached: {url}",
                        "Check URL or remove link"
                    )

def run(args):
    """Main linting function."""
    results = []
    
    # Expand glob patterns
    filepaths = []
    for pattern in args.input.split(','):
        pattern = pattern.strip()
        if '*' in pattern or '?' in pattern:
            filepaths.extend(glob.glob(pattern, recursive=True))
        else:
            filepaths.append(pattern)
    
    # Remove duplicates and ensure files exist
    filepaths = list(set(filepaths))
    filepaths = [f for f in filepaths if os.path.exists(f)]
    
    if not filepaths:
        return {"status": "error", "message": "No valid files found"}
    
    linter = MarkdownLinter(
        max_line_length=args.max_line_length,
        check_external_links=args.check_external_links
    )
    
    for filepath in filepaths:
        result = linter.lint_file(filepath)
        results.append(result)
    
    return {
        "status": "success",
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "results": results,
        "summary": {
            "files_processed": len(results),
            "total_issues": sum(r['summary']['total_issues'] for r in results),
            "total_errors": sum(r['summary']['errors'] for r in results),
            "total_warnings": sum(r['summary']['warnings'] for r in results)
        }
    }

def main():
    parser = argparse.ArgumentParser(description='Markdown Linter')
    parser.add_argument('command', choices=['run', 'help'])
    parser.add_argument('--input', help='Input file(s) (supports glob patterns, comma-separated)')
    parser.add_argument('--max-line-length', type=int, default=80, help='Maximum line length (default: 80)')
    parser.add_argument('--check-external-links', action='store_true', help='Validate external URLs (slow)')
    
    args = parser.parse_args()
    
    if args.command == 'run':
        if not args.input:
            print('Error: --input is required')
            parser.print_help()
            sys.exit(1)
        result = run(args)
        print(json.dumps(result, indent=2))
    else:
        parser.print_help()

if __name__ == '__main__':
    main()