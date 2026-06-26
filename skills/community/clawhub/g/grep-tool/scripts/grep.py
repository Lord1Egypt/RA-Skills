#!/usr/bin/env python3
"""Grep Tool - Text search."""

import argparse
import os
import re
import sys
from typing import List, Tuple


def search_file(
    filepath: str,
    pattern: str,
    ignore_case: bool = False,
    line_numbers: bool = False,
    invert: bool = False,
    count_only: bool = False,
    files_only: bool = False,
    word_regexp: bool = False,
    after: int = 0,
    before: int = 0,
    color: bool = False
) -> List[str]:
    """Search for pattern in file."""
    results = []
    
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
    except Exception as e:
        return [f"Error: {e}"]
    
    # Compile regex
    flags = re.IGNORECASE if ignore_case else 0
    if word_regexp:
        pattern = r'\b' + pattern + r'\b'
    
    try:
        regex = re.compile(pattern, flags)
    except re.error as e:
        return [f"Invalid pattern: {e}"]
    
    matches = []
    for i, line in enumerate(lines):
        line_match = regex.search(line)
        if invert:
            line_match = not line_match
        
        if line_match:
            matches.append(i)
    
    # Output
    if count_only:
        return [f"{filepath}: {len(matches)}"]
    
    if files_only:
        if matches:
            return [filepath]
        return []
    
    for idx in matches:
        # Get context
        start = max(0, idx - before)
        end = min(len(lines), idx + after + 1)
        
        for j in range(start, end):
            line = lines[j]
            is_match = (j == idx)
            
            # Highlight
            if color and is_match:
                highlighted = regex.sub(lambda m: f"\033[31m{m.group()}\033[0m", line.rstrip())
                line = highlighted
            else:
                line = line.rstrip()
            
            if line_numbers:
                results.append(f"{filepath}:{j+1}:{line}")
            else:
                results.append(f"{filepath}:{line}")
    
    return results


def search_directory(
    dirpath: str,
    pattern: str,
    recursive: bool = True,
    **kwargs
) -> List[str]:
    """Search in directory."""
    results = []
    
    for root, dirs, files in os.walk(dirpath):
        for filename in files:
            filepath = os.path.join(root, filename)
            file_results = search_file(filepath, pattern, **kwargs)
            results.extend(file_results)
        
        if not recursive:
            break
    
    return results


def main():
    parser = argparse.ArgumentParser(description='Text search tool')
    parser.add_argument('pattern', help='Search pattern')
    parser.add_argument('path', nargs='?', help='File or directory to search')
    parser.add_argument('-r', '--recursive', action='store_true', help='Recursive search')
    parser.add_argument('-i', '--ignore-case', action='store_true', help='Case insensitive')
    parser.add_argument('-n', '--line-number', action='store_true', help='Line numbers')
    parser.add_argument('-v', '--invert', action='store_true', help='Invert match')
    parser.add_argument('-c', '--count', action='store_true', help='Count only')
    parser.add_argument('-l', '--files-with-matches', action='store_true', help='Files only')
    parser.add_argument('-w', '--word', action='store_true', help='Whole word')
    parser.add_argument('-A', '--after', type=int, default=0, help='Lines after')
    parser.add_argument('-B', '--before', type=int, default=0, help='Lines before')
    parser.add_argument('--color', action='store_true', help='Highlight matches')
    
    args = parser.parse_args()
    
    if not args.path:
        # Read from stdin
        content = sys.stdin.read()
        pattern = args.pattern
        flags = re.IGNORECASE if args.ignore_case else 0
        if args.word:
            pattern = r'\b' + pattern + r'\b'
        
        try:
            regex = re.compile(pattern, flags)
        except re.error as e:
            print(f"Invalid pattern: {e}", file=sys.stderr)
            sys.exit(1)
        
        for i, line in enumerate(content.splitlines()):
            match = regex.search(line)
            if args.invert:
                match = not match
            if match:
                if args.line_numbers:
                    print(f"{i+1}:{line}")
                else:
                    print(line)
        return
    
    # Check if path is file or directory
    if os.path.isfile(args.path):
        results = search_file(
            args.path,
            args.pattern,
            ignore_case=args.ignore_case,
            line_numbers=args.line_number,
            invert=args.invert,
            count_only=args.count,
            files_only=args.files_with_matches,
            word_regexp=args.word,
            after=args.after,
            before=args.before,
            color=args.color
        )
    elif os.path.isdir(args.path):
        results = search_directory(
            args.path,
            args.pattern,
            recursive=args.recursive,
            ignore_case=args.ignore_case,
            line_numbers=args.line_number,
            invert=args.invert,
            count_only=args.count,
            files_only=args.files_with_matches,
            word_regexp=args.word,
            after=args.after,
            before=args.before,
            color=args.color
        )
    else:
        print(f"Error: {args.path} not found", file=sys.stderr)
        sys.exit(1)
    
    for result in results:
        print(result)


if __name__ == '__main__':
    main()
