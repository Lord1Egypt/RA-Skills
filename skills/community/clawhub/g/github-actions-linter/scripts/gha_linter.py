#!/usr/bin/env python3
"""GitHub Actions Workflow Linter — lint, validate, and audit .yml workflow files.

Pure Python stdlib. No dependencies.
"""
import sys, os, re, json, argparse
from pathlib import Path

# ---------------------------------------------------------------------------
# Minimal YAML parser (good enough for GitHub Actions workflows)
# ---------------------------------------------------------------------------

class YAMLParser:
    """Minimal YAML parser that handles the subset used by GitHub Actions."""

    def __init__(self, text):
        self.lines = text.splitlines()
        self.pos = 0

    def parse(self):
        return self._parse_mapping(0)

    def _current_indent(self, line):
        return len(line) - len(line.lstrip())

    def _strip_comment(self, line):
        in_sq = in_dq = False
        for i, c in enumerate(line):
            if c == "'" and not in_dq:
                in_sq = not in_sq
            elif c == '"' and not in_sq:
                in_dq = not in_dq
            elif c == '#' and not in_sq and not in_dq:
                return line[:i].rstrip()
        return line.rstrip()

    def _parse_value(self, val, base_indent):
        val = val.strip()
        if val == '' or val == '~' or val == 'null':
            return None
        if val == 'true' or val == 'True' or val == 'on' or val == 'On' or val == 'yes' or val == 'Yes':
            return True
        if val == 'false' or val == 'False' or val == 'off' or val == 'Off' or val == 'no' or val == 'No':
            return False
        if val.startswith('[') and val.endswith(']'):
            inner = val[1:-1].strip()
            if not inner:
                return []
            return [self._parse_scalar(x.strip()) for x in self._split_flow(inner)]
        if val.startswith('{') and val.endswith('}'):
            inner = val[1:-1].strip()
            if not inner:
                return {}
            result = {}
            for pair in self._split_flow(inner):
                if ':' in pair:
                    k, v = pair.split(':', 1)
                    result[k.strip().strip('"').strip("'")] = self._parse_scalar(v.strip())
            return result
        if val.startswith('|') or val.startswith('>'):
            return self._parse_block_scalar(base_indent)
        return self._parse_scalar(val)

    def _split_flow(self, s):
        parts = []
        depth = 0
        current = []
        for c in s:
            if c in '[{':
                depth += 1
            elif c in ']}':
                depth -= 1
            elif c == ',' and depth == 0:
                parts.append(''.join(current).strip())
                current = []
                continue
            current.append(c)
        if current:
            parts.append(''.join(current).strip())
        return parts

    def _parse_scalar(self, val):
        if not val or val == '~' or val == 'null':
            return None
        if val == 'true' or val == 'True':
            return True
        if val == 'false' or val == 'False':
            return False
        for q in ('"', "'"):
            if val.startswith(q) and val.endswith(q) and len(val) >= 2:
                return val[1:-1]
        try:
            return int(val)
        except ValueError:
            pass
        try:
            return float(val)
        except ValueError:
            pass
        return val

    def _parse_block_scalar(self, base_indent):
        lines = []
        while self.pos < len(self.lines):
            line = self.lines[self.pos]
            if not line.strip():
                lines.append('')
                self.pos += 1
                continue
            indent = self._current_indent(line)
            if indent <= base_indent:
                break
            lines.append(line.rstrip())
            self.pos += 1
        return '\n'.join(lines)

    def _parse_mapping(self, expected_indent):
        result = {}
        while self.pos < len(self.lines):
            line = self.lines[self.pos]
            if not line.strip() or line.strip().startswith('#'):
                self.pos += 1
                continue
            indent = self._current_indent(line)
            if indent < expected_indent:
                break
            if indent > expected_indent:
                self.pos += 1
                continue
            stripped = self._strip_comment(line).strip()
            if stripped.startswith('- '):
                break  # list context
            if ':' not in stripped:
                self.pos += 1
                continue
            # find key:value
            colon_pos = stripped.find(':')
            key = stripped[:colon_pos].strip().strip('"').strip("'")
            val_part = stripped[colon_pos + 1:].strip()
            self.pos += 1
            if val_part:
                result[key] = self._parse_value(val_part, indent)
            else:
                # check next line
                if self.pos < len(self.lines):
                    next_line = self.lines[self.pos]
                    if next_line.strip() and not next_line.strip().startswith('#'):
                        next_indent = self._current_indent(next_line)
                        if next_indent > indent:
                            next_stripped = self._strip_comment(next_line).strip()
                            if next_stripped.startswith('- '):
                                result[key] = self._parse_list(next_indent)
                            else:
                                result[key] = self._parse_mapping(next_indent)
                        else:
                            result[key] = None
                    else:
                        result[key] = None
                else:
                    result[key] = None
        return result

    def _parse_list(self, expected_indent):
        result = []
        while self.pos < len(self.lines):
            line = self.lines[self.pos]
            if not line.strip() or line.strip().startswith('#'):
                self.pos += 1
                continue
            indent = self._current_indent(line)
            if indent < expected_indent:
                break
            stripped = self._strip_comment(line).strip()
            if not stripped.startswith('- '):
                if indent > expected_indent:
                    self.pos += 1
                    continue
                break
            if indent != expected_indent:
                if indent > expected_indent:
                    self.pos += 1
                    continue
                break
            item_val = stripped[2:].strip()
            self.pos += 1
            if not item_val:
                # next lines are mapping under this list item
                if self.pos < len(self.lines):
                    nxt = self.lines[self.pos]
                    if nxt.strip() and self._current_indent(nxt) > indent:
                        result.append(self._parse_mapping(self._current_indent(nxt)))
                    else:
                        result.append(None)
                else:
                    result.append(None)
            elif ':' in item_val and not item_val.startswith('{'):
                # inline mapping in list item: "- key: val"
                m = {}
                colon = item_val.find(':')
                k = item_val[:colon].strip().strip('"').strip("'")
                v = item_val[colon + 1:].strip()
                m[k] = self._parse_value(v, indent + 2) if v else None
                # continue reading indented keys
                if self.pos < len(self.lines):
                    nxt = self.lines[self.pos]
                    if nxt.strip() and self._current_indent(nxt) > indent:
                        extra = self._parse_mapping(self._current_indent(nxt))
                        m.update(extra)
                if not v and m[k] is None:
                    if self.pos < len(self.lines):
                        nxt = self.lines[self.pos]
                        if nxt.strip() and self._current_indent(nxt) > indent + 2:
                            nxt_stripped = self._strip_comment(nxt).strip()
                            if nxt_stripped.startswith('- '):
                                m[k] = self._parse_list(self._current_indent(nxt))
                            else:
                                m[k] = self._parse_mapping(self._current_indent(nxt))
                result.append(m)
            else:
                result.append(self._parse_value(item_val, indent + 2))
        return result


def parse_yaml(text):
    parser = YAMLParser(text)
    return parser.parse()


# ---------------------------------------------------------------------------
# Issue model
# ---------------------------------------------------------------------------

class Issue:
    def __init__(self, rule, severity, message, line=0, col=0):
        self.rule = rule
        self.severity = severity  # error, warning, info
        self.message = message
        self.line = line
        self.col = col

    def to_dict(self):
        return {
            'rule': self.rule,
            'severity': self.severity,
            'message': self.message,
            'line': self.line,
            'col': self.col,
        }


# ---------------------------------------------------------------------------
# Known data
# ---------------------------------------------------------------------------

VALID_TRIGGERS = {
    'push', 'pull_request', 'pull_request_target', 'pull_request_review',
    'pull_request_review_comment', 'issues', 'issue_comment', 'create', 'delete',
    'deployment', 'deployment_status', 'fork', 'gollum', 'label', 'milestone',
    'page_build', 'project', 'project_card', 'project_column', 'public',
    'registry_package', 'release', 'status', 'watch', 'workflow_call',
    'workflow_dispatch', 'workflow_run', 'repository_dispatch', 'schedule',
    'check_run', 'check_suite', 'discussion', 'discussion_comment',
    'merge_group', 'branch_protection_rule',
}

DEPRECATED_RUNNERS = {
    'ubuntu-16.04', 'ubuntu-18.04', 'macos-10.15', 'macos-11',
    'windows-2016', 'windows-2019',
}

# action -> current recommended major version
KNOWN_ACTIONS = {
    'actions/checkout': 4,
    'actions/setup-node': 4,
    'actions/setup-python': 5,
    'actions/setup-java': 4,
    'actions/setup-go': 5,
    'actions/upload-artifact': 4,
    'actions/download-artifact': 4,
    'actions/cache': 4,
    'actions/github-script': 7,
    'actions/setup-dotnet': 4,
    'actions/labeler': 5,
    'actions/stale': 9,
    'actions/create-release': 1,  # archived but still used
    'docker/build-push-action': 6,
    'docker/setup-buildx-action': 3,
    'docker/login-action': 3,
    'docker/setup-qemu-action': 3,
    'peaceiris/actions-gh-pages': 4,
    'codecov/codecov-action': 4,
    'coverallsapp/github-action': 2,
}

UNTRUSTED_CONTEXTS = [
    'github.event.issue.title',
    'github.event.issue.body',
    'github.event.pull_request.title',
    'github.event.pull_request.body',
    'github.event.comment.body',
    'github.event.review.body',
    'github.event.review_comment.body',
    'github.event.discussion.title',
    'github.event.discussion.body',
    'github.event.pages.*.page_name',
    'github.event.commits.*.message',
    'github.event.commits.*.author.email',
    'github.event.commits.*.author.name',
    'github.event.head_commit.message',
    'github.event.head_commit.author.email',
    'github.event.head_commit.author.name',
    'github.head_ref',
    'github.event.workflow_run.head_branch',
    'github.event.workflow_run.head_commit.message',
]

VALID_PERMISSIONS = {
    'actions', 'checks', 'contents', 'deployments', 'id-token',
    'issues', 'discussions', 'packages', 'pages', 'pull-requests',
    'repository-projects', 'security-events', 'statuses', 'attestations',
}

SECRET_PATTERNS = [
    r'(?i)(password|passwd|pwd)\s*[:=]\s*["\']?[^\s"\']+',
    r'(?i)(api[_-]?key|apikey)\s*[:=]\s*["\']?[^\s"\']+',
    r'(?i)(secret|token)\s*[:=]\s*["\']?[A-Za-z0-9+/=_-]{16,}',
    r'(?i)ghp_[A-Za-z0-9]{36}',
    r'(?i)gho_[A-Za-z0-9]{36}',
    r'(?i)github_pat_[A-Za-z0-9_]{22,}',
    r'AKIA[0-9A-Z]{16}',
    r'(?i)sk-[A-Za-z0-9]{20,}',
]


# ---------------------------------------------------------------------------
# Linters
# ---------------------------------------------------------------------------

def find_line(lines, pattern, start=0):
    """Find line number (1-based) containing pattern."""
    for i in range(start, len(lines)):
        if pattern in lines[i]:
            return i + 1
    return 0


def lint_structure(workflow, lines):
    """Check workflow structure (rules 1-8)."""
    issues = []

    if 'on' not in workflow and True not in workflow:
        issues.append(Issue('missing-on', 'error', 'Workflow missing required `on` trigger', find_line(lines, 'name:') or 1))

    if 'jobs' not in workflow:
        issues.append(Issue('missing-jobs', 'error', 'Workflow missing required `jobs` section', find_line(lines, 'name:') or 1))
        return issues

    jobs = workflow.get('jobs')
    if not jobs or not isinstance(jobs, dict):
        issues.append(Issue('empty-jobs', 'error', '`jobs` section is empty', find_line(lines, 'jobs:')))
        return issues

    # validate triggers
    on_val = workflow.get('on') or workflow.get(True)
    if on_val:
        triggers = []
        if isinstance(on_val, str):
            triggers = [on_val]
        elif isinstance(on_val, list):
            triggers = on_val
        elif isinstance(on_val, dict):
            triggers = list(on_val.keys())
        for t in triggers:
            if isinstance(t, str) and t not in VALID_TRIGGERS:
                issues.append(Issue('invalid-trigger', 'error', f'Unknown trigger event: `{t}`', find_line(lines, t)))

    # check each job
    job_names = set(jobs.keys())
    for job_name, job in jobs.items():
        if not isinstance(job, dict):
            continue
        jline = find_line(lines, f'{job_name}:')

        if 'runs-on' not in job and 'uses' not in job:
            issues.append(Issue('missing-runs-on', 'error', f'Job `{job_name}` missing `runs-on`', jline))

        steps = job.get('steps')
        if 'uses' not in job:  # reusable workflows don't need steps
            if steps is None:
                issues.append(Issue('missing-steps', 'error', f'Job `{job_name}` missing `steps`', jline))
            elif isinstance(steps, list) and len(steps) == 0:
                issues.append(Issue('empty-steps', 'warning', f'Job `{job_name}` has empty steps', jline))

        # circular deps
        needs = job.get('needs')
        if needs:
            if isinstance(needs, str):
                needs = [needs]
            if isinstance(needs, list):
                for n in needs:
                    if n not in job_names:
                        issues.append(Issue('circular-deps', 'error', f'Job `{job_name}` needs `{n}` which does not exist', jline))

    # deeper circular dep check
    if isinstance(jobs, dict):
        issues.extend(_check_circular_deps(jobs, lines))

    return issues


def _check_circular_deps(jobs, lines):
    """Detect circular dependencies in job `needs`."""
    graph = {}
    for name, job in jobs.items():
        if not isinstance(job, dict):
            continue
        needs = job.get('needs', [])
        if isinstance(needs, str):
            needs = [needs]
        if isinstance(needs, list):
            graph[name] = [n for n in needs if isinstance(n, str)]
        else:
            graph[name] = []

    visited = set()
    path = set()
    issues = []

    def dfs(node):
        if node in path:
            issues.append(Issue('circular-deps', 'error',
                f'Circular dependency detected involving job `{node}`',
                find_line(lines, f'{node}:')))
            return
        if node in visited:
            return
        path.add(node)
        for dep in graph.get(node, []):
            dfs(dep)
        path.remove(node)
        visited.add(node)

    for name in graph:
        dfs(name)
    return issues


def lint_security(workflow, lines, raw_text):
    """Check security issues (rules 9-16)."""
    issues = []
    jobs = workflow.get('jobs', {})
    if not isinstance(jobs, dict):
        return issues

    # shell injection: ${{ }} in run blocks
    expr_pattern = re.compile(r'\$\{\{.*?\}\}')
    for i, line in enumerate(lines):
        stripped = line.strip()
        # only flag in run: blocks or env values
        if 'run:' in line or (stripped.startswith('run:') or stripped.startswith('- run:')):
            exprs = expr_pattern.findall(line)
            for expr in exprs:
                inner = expr[3:-2].strip()
                # check for untrusted contexts
                for ctx in UNTRUSTED_CONTEXTS:
                    ctx_plain = ctx.replace('*', '')
                    if ctx_plain in inner or (ctx in inner):
                        issues.append(Issue('shell-injection', 'error',
                            f'Expression `{expr}` in run: may be vulnerable to injection via `{ctx}`',
                            i + 1))
                        break
                else:
                    # general warning for any expression in run
                    if 'secrets.' not in inner and 'env.' not in inner and 'needs.' not in inner and 'steps.' not in inner and 'matrix.' not in inner and 'inputs.' not in inner:
                        if 'github.event' in inner:
                            issues.append(Issue('untrusted-context', 'warning',
                                f'Expression `{expr}` in run: uses event context — verify it is safe',
                                i + 1))

    # hardcoded secrets
    for pattern in SECRET_PATTERNS:
        for i, line in enumerate(lines):
            if re.search(pattern, line):
                # skip if it's a ${{ secrets.* }} reference
                if '${{ secrets.' in line:
                    continue
                issues.append(Issue('hardcoded-secret', 'error',
                    f'Possible hardcoded secret/credential on line {i+1}',
                    i + 1))
                break  # one per pattern

    # permissions check
    perms = workflow.get('permissions')
    if perms is None:
        issues.append(Issue('permissive-permissions', 'info',
            'No top-level `permissions` block — defaults to read-write for all scopes',
            1))
    elif perms == 'write-all':
        issues.append(Issue('permissive-permissions', 'warning',
            '`permissions: write-all` grants unnecessary broad access',
            find_line(lines, 'permissions:')))

    # pull_request_target
    on_val = workflow.get('on') or workflow.get(True)
    has_prt = False
    if isinstance(on_val, dict) and 'pull_request_target' in on_val:
        has_prt = True
    elif isinstance(on_val, list) and 'pull_request_target' in on_val:
        has_prt = True
    elif isinstance(on_val, str) and on_val == 'pull_request_target':
        has_prt = True

    if has_prt:
        # check if any job checks out PR head
        if 'ref: ${{ github.event.pull_request.head' in raw_text or "ref: ${{ github.event.pull_request.head" in raw_text:
            issues.append(Issue('pull-request-target', 'error',
                '`pull_request_target` with checkout of PR head ref is a known security vulnerability',
                find_line(lines, 'pull_request_target')))
        else:
            issues.append(Issue('pull-request-target', 'warning',
                '`pull_request_target` trigger requires careful security review',
                find_line(lines, 'pull_request_target')))

    # third-party actions without SHA pinning
    for i, line in enumerate(lines):
        m = re.match(r'\s*uses:\s*([^\s@]+)@(.+)', line.strip())
        if m:
            action = m.group(1)
            version = m.group(2).strip()
            # skip official actions/* and docker://
            if action.startswith('actions/') or action.startswith('docker://') or action.startswith('./'):
                continue
            # check if pinned to SHA (40 hex chars)
            if not re.match(r'^[0-9a-f]{40}$', version):
                issues.append(Issue('third-party-action', 'warning',
                    f'Third-party action `{action}@{version}` not pinned to SHA — supply chain risk',
                    i + 1))

    # secrets directly in run: instead of env:
    for i, line in enumerate(lines):
        if 'run:' in line or line.strip().startswith('run:'):
            if '${{ secrets.' in line:
                issues.append(Issue('env-in-run', 'warning',
                    f'Secret used directly in `run:` — prefer passing via `env:` for security',
                    i + 1))

    return issues


def lint_deprecated(workflow, lines):
    """Check for deprecated actions and runners (rules 17-20)."""
    issues = []
    jobs = workflow.get('jobs', {})
    if not isinstance(jobs, dict):
        return issues

    # deprecated actions
    for i, line in enumerate(lines):
        m = re.match(r'\s*uses:\s*([^\s@]+)@v?(\d+)', line.strip())
        if m:
            action = m.group(1)
            version = int(m.group(2))
            if action in KNOWN_ACTIONS:
                current = KNOWN_ACTIONS[action]
                if version < current:
                    issues.append(Issue('deprecated-action', 'warning',
                        f'`{action}@v{version}` is outdated — current is v{current}',
                        i + 1))

    # deprecated runners
    for job_name, job in jobs.items():
        if not isinstance(job, dict):
            continue
        runs_on = job.get('runs-on', '')
        if isinstance(runs_on, str):
            runners = [runs_on]
        elif isinstance(runs_on, list):
            runners = runs_on
        else:
            continue
        for r in runners:
            if isinstance(r, str) and r in DEPRECATED_RUNNERS:
                issues.append(Issue('deprecated-runner', 'warning',
                    f'Job `{job_name}` uses deprecated runner `{r}`',
                    find_line(lines, r)))

    # deprecated set-output and save-state
    for i, line in enumerate(lines):
        if '::set-output ' in line or '::set-output::' in line:
            issues.append(Issue('set-output-deprecated', 'warning',
                '`::set-output::` is deprecated — use `$GITHUB_OUTPUT` instead',
                i + 1))
        if '::save-state ' in line or '::save-state::' in line:
            issues.append(Issue('save-state-deprecated', 'warning',
                '`::save-state::` is deprecated — use `$GITHUB_STATE` instead',
                i + 1))

    return issues


def lint_best_practices(workflow, lines, raw_text):
    """Check best practices (rules 21-28)."""
    issues = []
    jobs = workflow.get('jobs', {})
    if not isinstance(jobs, dict):
        return issues

    for job_name, job in jobs.items():
        if not isinstance(job, dict):
            continue
        jline = find_line(lines, f'{job_name}:')

        # missing timeout
        if 'timeout-minutes' not in job:
            issues.append(Issue('missing-timeout', 'warning',
                f'Job `{job_name}` has no `timeout-minutes` (default: 360 min)',
                jline))

        # check steps
        steps = job.get('steps', [])
        if not isinstance(steps, list):
            continue

        step_ids = []
        for idx, step in enumerate(steps):
            if not isinstance(step, dict):
                continue

            # missing name
            if 'name' not in step:
                issues.append(Issue('missing-name', 'info',
                    f'Step {idx+1} in job `{job_name}` has no `name`',
                    jline))

            # duplicate step id
            sid = step.get('id')
            if sid:
                if sid in step_ids:
                    issues.append(Issue('duplicate-step-id', 'error',
                        f'Duplicate step id `{sid}` in job `{job_name}`',
                        jline))
                step_ids.append(sid)

            # latest tag
            uses = step.get('uses', '')
            if isinstance(uses, str):
                if uses.endswith('@main') or uses.endswith('@master'):
                    issues.append(Issue('latest-tag', 'warning',
                        f'Action `{uses}` pinned to branch — use a version tag or SHA',
                        find_line(lines, uses) or jline))

    # no concurrency
    if 'concurrency' not in workflow:
        issues.append(Issue('no-concurrency', 'info',
            'No `concurrency` block — parallel runs may waste resources',
            1))

    # long run commands
    in_run = False
    run_start = 0
    run_lines = 0
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith('run:') or stripped.startswith('- run:'):
            if '|' in stripped:
                in_run = True
                run_start = i + 1
                run_lines = 0
        elif in_run:
            indent = len(line) - len(line.lstrip())
            if stripped and indent <= (len(lines[run_start - 1]) - len(lines[run_start - 1].lstrip())):
                in_run = False
                if run_lines > 50:
                    issues.append(Issue('long-run-command', 'info',
                        f'`run:` block starting at line {run_start} has {run_lines} lines — consider a script',
                        run_start))
            else:
                if stripped:
                    run_lines += 1

    return issues


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------

def lint_file(filepath, rules='all'):
    """Lint a single workflow file. Returns list of Issues."""
    raw = Path(filepath).read_text(encoding='utf-8', errors='replace')
    lines = raw.splitlines()

    try:
        workflow = parse_yaml(raw)
    except Exception as e:
        return [Issue('parse-error', 'error', f'Failed to parse YAML: {e}', 1)]

    if not isinstance(workflow, dict):
        return [Issue('parse-error', 'error', 'Workflow root is not a mapping', 1)]

    issues = []
    if rules in ('all', 'structure', 'validate'):
        issues.extend(lint_structure(workflow, lines))
    if rules in ('all', 'security'):
        issues.extend(lint_security(workflow, lines, raw))
    if rules in ('all', 'deprecated'):
        issues.extend(lint_deprecated(workflow, lines))
    if rules in ('all', 'practices'):
        issues.extend(lint_best_practices(workflow, lines, raw))

    return issues


def find_workflow_files(path):
    """Find .yml/.yaml files in path."""
    p = Path(path)
    if p.is_file():
        return [p]
    files = []
    for ext in ('*.yml', '*.yaml'):
        files.extend(p.rglob(ext))
    return sorted(files)


# ---------------------------------------------------------------------------
# Formatters
# ---------------------------------------------------------------------------

def format_text(filepath, issues):
    lines = []
    for iss in sorted(issues, key=lambda x: x.line):
        lines.append(f'{filepath}:{iss.line} {iss.severity} [{iss.rule}] {iss.message}')
    return '\n'.join(lines)


def format_json(filepath, issues):
    return json.dumps({
        'file': str(filepath),
        'issues': [i.to_dict() for i in issues],
        'summary': {
            'errors': sum(1 for i in issues if i.severity == 'error'),
            'warnings': sum(1 for i in issues if i.severity == 'warning'),
            'info': sum(1 for i in issues if i.severity == 'info'),
        }
    }, indent=2)


def format_markdown(filepath, issues):
    lines = [f'## {filepath}', '', '| Severity | Rule | Line | Message |', '|----------|------|------|---------|']
    for iss in sorted(issues, key=lambda x: x.line):
        sev = {'error': ':red_circle:', 'warning': ':warning:', 'info': ':information_source:'}.get(iss.severity, iss.severity)
        lines.append(f'| {sev} {iss.severity} | `{iss.rule}` | {iss.line} | {iss.message} |')
    errs = sum(1 for i in issues if i.severity == 'error')
    warns = sum(1 for i in issues if i.severity == 'warning')
    infos = sum(1 for i in issues if i.severity == 'info')
    lines.append(f'\n**{len(issues)} issues** ({errs} errors, {warns} warnings, {infos} info)')
    return '\n'.join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description='GitHub Actions Workflow Linter')
    sub = parser.add_subparsers(dest='command', required=True)

    # lint
    p_lint = sub.add_parser('lint', help='Lint workflow files (all rules)')
    p_lint.add_argument('path', help='Workflow file or directory')
    p_lint.add_argument('--strict', action='store_true', help='Exit 1 on warnings too')
    p_lint.add_argument('--format', choices=['text', 'json', 'markdown'], default='text')

    # security
    p_sec = sub.add_parser('security', help='Security-focused audit')
    p_sec.add_argument('path', help='Workflow file')
    p_sec.add_argument('--format', choices=['text', 'json', 'markdown'], default='text')

    # deprecated
    p_dep = sub.add_parser('deprecated', help='Check for deprecated actions/runners')
    p_dep.add_argument('path', help='Workflow file')
    p_dep.add_argument('--format', choices=['text', 'json', 'markdown'], default='text')

    # validate
    p_val = sub.add_parser('validate', help='Validate workflow structure')
    p_val.add_argument('path', help='Workflow file')
    p_val.add_argument('--format', choices=['text', 'json', 'markdown'], default='text')

    args = parser.parse_args()

    rule_map = {
        'lint': 'all',
        'security': 'security',
        'deprecated': 'deprecated',
        'validate': 'validate',
    }
    rules = rule_map[args.command]

    files = find_workflow_files(args.path)
    if not files:
        print(f'No workflow files found in: {args.path}', file=sys.stderr)
        sys.exit(1)

    fmt = getattr(args, 'format', 'text')
    strict = getattr(args, 'strict', False)
    total_errors = 0
    total_warnings = 0
    all_results = []

    for f in files:
        issues = lint_file(str(f), rules)
        errs = sum(1 for i in issues if i.severity == 'error')
        warns = sum(1 for i in issues if i.severity == 'warning')
        total_errors += errs
        total_warnings += warns

        if fmt == 'text':
            if issues:
                print(format_text(f, issues))
        elif fmt == 'json':
            all_results.append(json.loads(format_json(f, issues)))
        elif fmt == 'markdown':
            if issues:
                print(format_markdown(f, issues))

    if fmt == 'json':
        if len(all_results) == 1:
            print(json.dumps(all_results[0], indent=2))
        else:
            print(json.dumps(all_results, indent=2))

    if fmt == 'text':
        total = total_errors + total_warnings
        print(f'\n{total} issues ({total_errors} errors, {total_warnings} warnings) in {len(files)} file(s)')

    if total_errors > 0:
        sys.exit(1)
    if strict and total_warnings > 0:
        sys.exit(1)
    sys.exit(0)


if __name__ == '__main__':
    main()
