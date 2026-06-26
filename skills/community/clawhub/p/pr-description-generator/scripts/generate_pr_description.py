#!/usr/bin/env python3
"""
PR Description Generator — Auto-generate pull request descriptions from git diffs.

Analyzes git changes to produce structured PR descriptions with:
- Summary of changes by category (features, fixes, refactoring, tests, docs)
- File-level change breakdown
- Impact analysis (high/medium/low)
- Reviewer hints
- Conventional commit parsing

No external dependencies — pure Python stdlib + git CLI.
"""

import argparse
import json
import os
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path


def run_git(args, cwd=None):
    """Run a git command and return stdout."""
    cmd = ['git'] + args
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd, timeout=30)
        return result.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return ''


def get_diff_stats(base='main', cwd=None):
    """Get file-level diff statistics."""
    output = run_git(['diff', '--stat', '--numstat', f'{base}...HEAD'], cwd=cwd)
    if not output:
        output = run_git(['diff', '--stat', '--numstat', base], cwd=cwd)
    return output


def get_diff(base='main', cwd=None):
    """Get full diff."""
    output = run_git(['diff', f'{base}...HEAD'], cwd=cwd)
    if not output:
        output = run_git(['diff', base], cwd=cwd)
    return output


def get_commits(base='main', cwd=None):
    """Get commit messages since base branch."""
    output = run_git(['log', '--oneline', '--no-merges', f'{base}...HEAD'], cwd=cwd)
    if not output:
        output = run_git(['log', '--oneline', '--no-merges', f'{base}..HEAD'], cwd=cwd)
    return output


def get_changed_files(base='main', cwd=None):
    """Get list of changed files with status."""
    output = run_git(['diff', '--name-status', f'{base}...HEAD'], cwd=cwd)
    if not output:
        output = run_git(['diff', '--name-status', base], cwd=cwd)
    files = []
    for line in output.split('\n'):
        if not line.strip():
            continue
        parts = line.split('\t')
        if len(parts) >= 2:
            status = parts[0][0]  # A, M, D, R
            fname = parts[-1]
            files.append((status, fname))
    return files


def categorize_file(filepath):
    """Categorize a file by its type/purpose."""
    fp = filepath.lower()
    name = Path(filepath).name.lower()

    if any(p in fp for p in ['test', 'spec', '__tests__', 'fixtures']):
        return 'tests'
    if any(p in fp for p in ['.md', 'readme', 'changelog', 'license', 'docs/', 'doc/']):
        return 'docs'
    if any(p in fp for p in ['dockerfile', 'docker-compose', '.github/', 'ci/', '.gitlab-ci',
                              'jenkinsfile', 'terraform', '.tf', 'helm/', 'k8s/']):
        return 'infra'
    if any(p in fp for p in ['package.json', 'requirements.txt', 'go.mod', 'cargo.toml',
                              'gemfile', 'pom.xml', 'build.gradle', 'pyproject.toml',
                              'package-lock.json', 'yarn.lock', 'poetry.lock']):
        return 'deps'
    if any(p in fp for p in ['.env', 'config/', 'settings', '.yml', '.yaml', '.toml', '.ini',
                              '.conf']):
        return 'config'
    if any(p in fp for p in ['migration', 'migrate', 'schema', '.sql']):
        return 'database'
    if any(fp.endswith(ext) for ext in ['.css', '.scss', '.less', '.styled']):
        return 'styles'

    return 'code'


def parse_conventional_commits(commits_text):
    """Parse conventional commit messages."""
    categories = defaultdict(list)
    pattern = re.compile(r'^[a-f0-9]+\s+(feat|fix|refactor|docs|test|chore|perf|style|ci|build|revert)(?:\(([^)]+)\))?[!]?:\s*(.+)$', re.IGNORECASE)

    for line in commits_text.split('\n'):
        line = line.strip()
        if not line:
            continue
        match = pattern.match(line)
        if match:
            ctype = match.group(1).lower()
            scope = match.group(2) or ''
            msg = match.group(3).strip()
            categories[ctype].append({'scope': scope, 'message': msg})
        else:
            # Non-conventional commit
            parts = line.split(' ', 1)
            if len(parts) > 1:
                categories['other'].append({'scope': '', 'message': parts[1]})

    return categories


def estimate_impact(changed_files, diff_text):
    """Estimate change impact level."""
    high_risk = [
        'migration', '.sql', 'schema', 'auth', 'security', 'payment',
        'database', 'api/', 'routes', 'middleware', 'dockerfile', '.env',
        'package.json', 'requirements.txt',
    ]
    medium_risk = [
        'model', 'service', 'controller', 'handler', 'util', 'helper',
        'config', 'hook',
    ]

    score = 0
    reasons = []

    # File count
    file_count = len(changed_files)
    if file_count > 20:
        score += 3
        reasons.append(f'{file_count} files changed')
    elif file_count > 10:
        score += 2

    # Diff size
    diff_lines = diff_text.count('\n')
    additions = diff_text.count('\n+')
    deletions = diff_text.count('\n-')

    if additions + deletions > 500:
        score += 3
        reasons.append(f'{additions}+ / {deletions}- lines')
    elif additions + deletions > 200:
        score += 2

    # High-risk files
    for status, fname in changed_files:
        fl = fname.lower()
        if any(hr in fl for hr in high_risk):
            score += 2
            reasons.append(f'touches {fname}')
            break
        if any(mr in fl for mr in medium_risk):
            score += 1
            break

    # Deleted files
    deleted = sum(1 for s, f in changed_files if s == 'D')
    if deleted > 0:
        score += 1
        reasons.append(f'{deleted} files deleted')

    if score >= 5:
        return 'high', reasons
    elif score >= 3:
        return 'medium', reasons
    return 'low', reasons


def generate_file_breakdown(changed_files):
    """Group files by category."""
    groups = defaultdict(list)
    for status, fname in changed_files:
        cat = categorize_file(fname)
        status_icon = {'A': '+', 'M': '~', 'D': '-', 'R': '>'}.get(status, '?')
        groups[cat].append(f'{status_icon} {fname}')
    return groups


def generate_description(base='main', cwd=None, template='standard', output_format='markdown'):
    """Generate the PR description."""
    commits_text = get_commits(base, cwd)
    changed_files = get_changed_files(base, cwd)
    diff_text = get_diff(base, cwd)

    if not changed_files and not commits_text:
        return "No changes found between current branch and base."

    # Parse
    commit_categories = parse_conventional_commits(commits_text)
    file_groups = generate_file_breakdown(changed_files)
    impact, impact_reasons = estimate_impact(changed_files, diff_text)

    # Count stats
    total_files = len(changed_files)
    added = sum(1 for s, _ in changed_files if s == 'A')
    modified = sum(1 for s, _ in changed_files if s == 'M')
    deleted = sum(1 for s, _ in changed_files if s == 'D')

    # Generate summary
    summary_parts = []

    type_labels = {
        'feat': 'Features',
        'fix': 'Bug Fixes',
        'refactor': 'Refactoring',
        'docs': 'Documentation',
        'test': 'Tests',
        'chore': 'Chores',
        'perf': 'Performance',
        'style': 'Style',
        'ci': 'CI/CD',
        'build': 'Build',
        'revert': 'Reverts',
        'other': 'Other Changes',
    }

    if output_format == 'json':
        return json.dumps({
            'summary': {
                'total_files': total_files,
                'added': added,
                'modified': modified,
                'deleted': deleted,
            },
            'impact': impact,
            'impact_reasons': impact_reasons,
            'commits': dict(commit_categories),
            'file_groups': dict(file_groups),
        }, indent=2)

    # Markdown output
    lines = []

    if template == 'minimal':
        # Minimal template
        lines.append('## Summary\n')
        for ctype, commits in commit_categories.items():
            label = type_labels.get(ctype, ctype.capitalize())
            for c in commits:
                scope = f'**{c["scope"]}**: ' if c['scope'] else ''
                lines.append(f'- {scope}{c["message"]}')
        if not commit_categories:
            lines.append(f'- {total_files} files changed ({added} added, {modified} modified, {deleted} deleted)')
        return '\n'.join(lines)

    # Standard template
    lines.append('## Summary\n')

    for ctype in ['feat', 'fix', 'refactor', 'perf', 'docs', 'test', 'chore', 'ci', 'build', 'revert', 'other']:
        commits = commit_categories.get(ctype)
        if commits:
            label = type_labels[ctype]
            lines.append(f'### {label}\n')
            for c in commits:
                scope = f'**{c["scope"]}**: ' if c['scope'] else ''
                lines.append(f'- {scope}{c["message"]}')
            lines.append('')

    if not commit_categories:
        lines.append(f'{total_files} files changed ({added} added, {modified} modified, {deleted} deleted)\n')

    # Impact
    impact_icon = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}[impact]
    lines.append(f'## Impact: {impact_icon} {impact.capitalize()}\n')
    if impact_reasons:
        for reason in impact_reasons[:5]:
            lines.append(f'- {reason}')
        lines.append('')

    # File breakdown
    if template == 'detailed' and file_groups:
        lines.append('## Changed Files\n')
        cat_labels = {
            'code': 'Source Code',
            'tests': 'Tests',
            'docs': 'Documentation',
            'infra': 'Infrastructure',
            'deps': 'Dependencies',
            'config': 'Configuration',
            'database': 'Database',
            'styles': 'Styles',
        }
        for cat in ['code', 'database', 'infra', 'deps', 'config', 'tests', 'docs', 'styles']:
            files = file_groups.get(cat)
            if files:
                lines.append(f'### {cat_labels.get(cat, cat.capitalize())}')
                lines.append('```')
                for f in files:
                    lines.append(f)
                lines.append('```')
                lines.append('')

    # Reviewer hints
    if template == 'detailed':
        lines.append('## Reviewer Hints\n')
        if any(categorize_file(f) == 'database' for _, f in changed_files):
            lines.append('- ⚠️ Database changes — verify migration is reversible')
        if any(categorize_file(f) == 'infra' for _, f in changed_files):
            lines.append('- ⚠️ Infrastructure changes — review deployment impact')
        if any(categorize_file(f) == 'deps' for _, f in changed_files):
            lines.append('- ⚠️ Dependency changes — check for breaking updates')
        if deleted > 3:
            lines.append(f'- ⚠️ {deleted} files deleted — verify nothing breaks')
        if impact == 'high':
            lines.append('- ⚠️ High impact — consider staging deployment first')
        if not any(categorize_file(f) == 'tests' for _, f in changed_files) and \
           any(categorize_file(f) == 'code' for _, f in changed_files):
            lines.append('- 💡 No test changes — consider adding tests for new code')

    # Test plan placeholder
    lines.append('\n## Test Plan\n')
    lines.append('- [ ] Unit tests pass')
    lines.append('- [ ] Integration tests pass')
    if any(categorize_file(f) == 'database' for _, f in changed_files):
        lines.append('- [ ] Migration tested (up and down)')
    if any(categorize_file(f) == 'infra' for _, f in changed_files):
        lines.append('- [ ] Deployment tested in staging')
    lines.append('- [ ] Manual verification')

    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='PR Description Generator — auto-generate PR descriptions from git diffs'
    )
    parser.add_argument('--base', '-b', default='main',
                        help='Base branch to compare against (default: main)')
    parser.add_argument('--repo', '-r', default='.',
                        help='Path to git repository (default: current directory)')
    parser.add_argument('--template', '-t', choices=['minimal', 'standard', 'detailed'],
                        default='standard', help='Template style (default: standard)')
    parser.add_argument('--format', '-f', choices=['markdown', 'json'],
                        default='markdown', help='Output format (default: markdown)')
    parser.add_argument('--output', '-o', help='Write description to file')
    parser.add_argument('--copy', action='store_true',
                        help='Also copy to clipboard (requires xclip/pbcopy)')

    args = parser.parse_args()

    # Verify it's a git repo
    if not run_git(['rev-parse', '--is-inside-work-tree'], cwd=args.repo):
        print("Error: Not a git repository", file=sys.stderr)
        sys.exit(1)

    # Auto-detect base branch
    base = args.base
    if base == 'main':
        branches = run_git(['branch', '-a'], cwd=args.repo)
        if 'main' not in branches and 'master' in branches:
            base = 'master'

    description = generate_description(
        base=base,
        cwd=args.repo,
        template=args.template,
        output_format=args.format,
    )

    if args.output:
        with open(args.output, 'w') as f:
            f.write(description)
        print(f"PR description written to {args.output}")
    else:
        print(description)

    if args.copy:
        try:
            proc = subprocess.Popen(['xclip', '-selection', 'clipboard'],
                                    stdin=subprocess.PIPE)
            proc.communicate(description.encode())
        except FileNotFoundError:
            try:
                proc = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
                proc.communicate(description.encode())
            except FileNotFoundError:
                print("(clipboard copy failed — install xclip or pbcopy)", file=sys.stderr)


if __name__ == '__main__':
    main()
