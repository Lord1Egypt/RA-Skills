#!/usr/bin/env python3
"""GitLab CI/CD Pipeline Linter — lint, validate, and audit .gitlab-ci.yml files.

Pure Python stdlib. No dependencies.
"""
import sys, os, re, json, argparse
from pathlib import Path

# ---------------------------------------------------------------------------
# Minimal YAML parser (good enough for GitLab CI pipelines)
# ---------------------------------------------------------------------------

class YAMLParser:
    """Minimal YAML parser that handles the subset used by GitLab CI."""

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
        if val in ('true', 'True', 'on', 'On', 'yes', 'Yes'):
            return True
        if val in ('false', 'False', 'off', 'Off', 'no', 'No'):
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
        if val in ('true', 'True'):
            return True
        if val in ('false', 'False'):
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
            colon_pos = stripped.find(':')
            key = stripped[:colon_pos].strip().strip('"').strip("'")
            val_part = stripped[colon_pos + 1:].strip()
            self.pos += 1
            if val_part:
                result[key] = self._parse_value(val_part, indent)
            else:
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
                if self.pos < len(self.lines):
                    nxt = self.lines[self.pos]
                    if nxt.strip() and self._current_indent(nxt) > indent:
                        result.append(self._parse_mapping(self._current_indent(nxt)))
                    else:
                        result.append(None)
                else:
                    result.append(None)
            elif ':' in item_val and not item_val.startswith('{'):
                m = {}
                colon = item_val.find(':')
                k = item_val[:colon].strip().strip('"').strip("'")
                v = item_val[colon + 1:].strip()
                m[k] = self._parse_value(v, indent + 2) if v else None
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
    def __init__(self, rule, severity, message, line=0):
        self.rule = rule
        self.severity = severity  # error, warning, info
        self.message = message
        self.line = line

    def to_dict(self):
        return {
            'rule': self.rule,
            'severity': self.severity,
            'message': self.message,
            'line': self.line,
        }


# ---------------------------------------------------------------------------
# Known data
# ---------------------------------------------------------------------------

# GitLab CI top-level keywords
GITLAB_TOP_LEVEL_KEYWORDS = {
    'stages', 'variables', 'image', 'services', 'before_script',
    'after_script', 'cache', 'default', 'include', 'workflow',
    'pages',
}

# GitLab CI job-level keywords
GITLAB_JOB_KEYWORDS = {
    'script', 'before_script', 'after_script', 'stage', 'image',
    'services', 'variables', 'cache', 'artifacts', 'only', 'except',
    'rules', 'tags', 'allow_failure', 'when', 'environment', 'retry',
    'timeout', 'needs', 'dependencies', 'extends', 'trigger',
    'resource_group', 'interruptible', 'coverage', 'parallel',
    'release', 'secrets', 'pages', 'inherit', 'id_tokens',
    'identity', 'hooks',
}

# Default stages in GitLab CI
DEFAULT_STAGES = ['build', 'test', 'deploy']

# Sensitive variable name patterns
SENSITIVE_VAR_PATTERNS = [
    r'(?i)(password|passwd|pwd|secret|token|api[_-]?key|apikey|'
    r'private[_-]?key|access[_-]?key|auth|credential|ssh[_-]?key)',
]

# Hardcoded secret patterns
SECRET_PATTERNS = [
    r'(?i)(password|passwd|pwd)\s*[:=]\s*["\']?[^\s"\'$]{8,}',
    r'(?i)(api[_-]?key|apikey)\s*[:=]\s*["\']?[^\s"\'$]{8,}',
    r'(?i)(secret|token)\s*[:=]\s*["\']?[A-Za-z0-9+/=_-]{16,}',
    r'AKIA[0-9A-Z]{16}',
    r'(?i)sk-[A-Za-z0-9]{20,}',
    r'(?i)glpat-[A-Za-z0-9_-]{20,}',
    r'(?i)ghp_[A-Za-z0-9]{36}',
]

# Security-related job name patterns
SECURITY_JOB_PATTERNS = [
    r'(?i)(sast|dast|secret[_-]?detect|dependency[_-]?scan|container[_-]?scan|'
    r'license[_-]?scan|security|vulnerability|pentest|trivy|snyk|sonar)',
]

# Long-running job name patterns (for missing-interruptible)
LONG_RUNNING_PATTERNS = [
    r'(?i)(deploy|build|e2e|integration|performance|load[_-]?test|stress)',
]

# Test job name patterns (for no-coverage-regex)
TEST_JOB_PATTERNS = [
    r'(?i)(test|spec|unit|coverage|pytest|rspec|jest|mocha)',
]

# Deploy/test job patterns (for missing-retry)
FLAKY_JOB_PATTERNS = [
    r'(?i)(deploy|test|e2e|integration|publish|release|upload)',
]

# Privileged runner tag patterns
PRIVILEGED_PATTERNS = [
    r'(?i)(privileged|dind|docker-in-docker)',
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def find_line(lines, pattern, start=0):
    """Find line number (1-based) containing pattern."""
    for i in range(start, len(lines)):
        if pattern in lines[i]:
            return i + 1
    return 0


def is_hidden_job(name):
    """Check if job name starts with a dot (hidden job / template)."""
    return name.startswith('.')


def is_gitlab_keyword(name):
    """Check if name is a GitLab CI top-level keyword (not a job)."""
    return name in GITLAB_TOP_LEVEL_KEYWORDS


def get_jobs(pipeline):
    """Extract job definitions from pipeline (exclude top-level keywords)."""
    if not isinstance(pipeline, dict):
        return {}
    jobs = {}
    for key, val in pipeline.items():
        if not is_gitlab_keyword(key) and isinstance(val, dict):
            jobs[key] = val
    return jobs


# ---------------------------------------------------------------------------
# Linters
# ---------------------------------------------------------------------------

def lint_structure(pipeline, lines, raw_text):
    """Check pipeline structure (rules 1-8)."""
    issues = []

    # Rule 1: missing-stages
    stages_defined = pipeline.get('stages')
    if stages_defined is None:
        issues.append(Issue('missing-stages', 'warning',
            'No `stages:` definition — using default stages (build, test, deploy)',
            1))
        effective_stages = DEFAULT_STAGES
    elif isinstance(stages_defined, list):
        effective_stages = [s for s in stages_defined if isinstance(s, str)]
    else:
        effective_stages = DEFAULT_STAGES

    jobs = get_jobs(pipeline)

    # Rule 7: duplicate-job — detect via raw text (YAML parser collapses dupes)
    job_name_lines = {}
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith('#'):
            continue
        indent = len(line) - len(line.lstrip())
        if indent == 0 and ':' in stripped and not stripped.startswith('-'):
            colon = stripped.find(':')
            name = stripped[:colon].strip().strip('"').strip("'")
            if not is_gitlab_keyword(name) and name:
                if name in job_name_lines:
                    issues.append(Issue('duplicate-job', 'error',
                        f'Duplicate job name `{name}` (first at line {job_name_lines[name]}, again at line {i+1})',
                        i + 1))
                else:
                    job_name_lines[name] = i + 1

    # Track which hidden jobs are referenced via extends
    extended_jobs = set()
    for job_name, job in jobs.items():
        if not isinstance(job, dict):
            continue
        ext = job.get('extends')
        if isinstance(ext, str):
            extended_jobs.add(ext)
        elif isinstance(ext, list):
            for e in ext:
                if isinstance(e, str):
                    extended_jobs.add(e)

    for job_name, job in jobs.items():
        if not isinstance(job, dict):
            continue
        jline = find_line(lines, f'{job_name}:')

        # Rule 2: undefined-stage
        job_stage = job.get('stage')
        if isinstance(job_stage, str) and job_stage not in effective_stages and not is_hidden_job(job_name):
            issues.append(Issue('undefined-stage', 'error',
                f'Job `{job_name}` uses stage `{job_stage}` not defined in `stages:`',
                jline))

        # Rule 3 & 5: empty-job / missing-script
        has_script = 'script' in job
        has_before_script = 'before_script' in job
        has_trigger = 'trigger' in job
        has_extends = 'extends' in job

        if not is_hidden_job(job_name) and not has_extends:
            if not has_script and not has_before_script and not has_trigger:
                issues.append(Issue('missing-script', 'error',
                    f'Job `{job_name}` has no `script:`, `before_script:`, or `trigger:`',
                    jline))
            elif has_script:
                script_val = job.get('script')
                if script_val is not None and isinstance(script_val, list) and len(script_val) == 0:
                    issues.append(Issue('empty-job', 'warning',
                        f'Job `{job_name}` has empty `script:` list',
                        jline))

        # Rule 4: invalid-job-name — hidden job not used as template
        if is_hidden_job(job_name) and job_name not in extended_jobs:
            issues.append(Issue('invalid-job-name', 'info',
                f'Hidden job `{job_name}` is never referenced via `extends:` — is it intentional?',
                jline))

        # Rule 8: invalid-keyword
        for key in job:
            if key not in GITLAB_JOB_KEYWORDS:
                issues.append(Issue('invalid-keyword', 'warning',
                    f'Unknown job-level keyword `{key}` in job `{job_name}`',
                    find_line(lines, f'{key}:', jline - 1 if jline > 0 else 0) or jline))

    # Rule 6: circular-needs
    issues.extend(_check_circular_needs(jobs, lines))

    return issues


def _check_circular_needs(jobs, lines):
    """Detect circular dependencies in job `needs`."""
    graph = {}
    for name, job in jobs.items():
        if not isinstance(job, dict):
            continue
        needs = job.get('needs', [])
        if isinstance(needs, str):
            needs = [needs]
        if isinstance(needs, list):
            deps = []
            for n in needs:
                if isinstance(n, str):
                    deps.append(n)
                elif isinstance(n, dict) and 'job' in n:
                    deps.append(n['job'])
            graph[name] = deps
        else:
            graph[name] = []

    visited = set()
    path = set()
    issues = []

    def dfs(node):
        if node in path:
            issues.append(Issue('circular-needs', 'error',
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


def lint_security(pipeline, lines, raw_text):
    """Check security issues (rules 9-14)."""
    issues = []
    jobs = get_jobs(pipeline)

    # Rule 9: hardcoded-secret
    for pattern in SECRET_PATTERNS:
        for i, line in enumerate(lines):
            if re.search(pattern, line):
                # skip CI variable references
                if '$CI_' in line or '${CI_' in line or '${{' in line:
                    continue
                # skip comments
                if line.strip().startswith('#'):
                    continue
                issues.append(Issue('hardcoded-secret', 'error',
                    f'Possible hardcoded secret/credential on line {i+1}',
                    i + 1))
                break  # one per pattern

    # Rule 10: unprotected-variable
    top_vars = pipeline.get('variables', {})
    if isinstance(top_vars, dict):
        for var_name, var_val in top_vars.items():
            if not isinstance(var_name, str):
                continue
            for pat in SENSITIVE_VAR_PATTERNS:
                if re.search(pat, var_name):
                    # check if value is a CI variable reference
                    val_str = str(var_val) if var_val is not None else ''
                    if not re.search(r'\$CI_|\$\{CI_', val_str):
                        issues.append(Issue('unprotected-variable', 'warning',
                            f'Variable `{var_name}` looks sensitive — consider using CI/CD masked variables instead',
                            find_line(lines, var_name)))
                    break

    # Also check job-level variables
    for job_name, job in jobs.items():
        if not isinstance(job, dict):
            continue
        job_vars = job.get('variables', {})
        if isinstance(job_vars, dict):
            for var_name, var_val in job_vars.items():
                if not isinstance(var_name, str):
                    continue
                for pat in SENSITIVE_VAR_PATTERNS:
                    if re.search(pat, var_name):
                        val_str = str(var_val) if var_val is not None else ''
                        if not re.search(r'\$CI_|\$\{CI_', val_str):
                            issues.append(Issue('unprotected-variable', 'warning',
                                f'Variable `{var_name}` in job `{job_name}` looks sensitive — use CI/CD masked variables',
                                find_line(lines, var_name)))
                        break

    # Rule 11: allow-failure-security
    for job_name, job in jobs.items():
        if not isinstance(job, dict):
            continue
        allow_fail = job.get('allow_failure')
        if allow_fail is True:
            for pat in SECURITY_JOB_PATTERNS:
                if re.search(pat, job_name):
                    issues.append(Issue('allow-failure-security', 'error',
                        f'Security job `{job_name}` has `allow_failure: true` — security checks should block the pipeline',
                        find_line(lines, f'{job_name}:')))
                    break

    # Rule 12: privileged-runner
    for job_name, job in jobs.items():
        if not isinstance(job, dict):
            continue
        tags = job.get('tags', [])
        if isinstance(tags, list):
            for tag in tags:
                if isinstance(tag, str):
                    for pat in PRIVILEGED_PATTERNS:
                        if re.search(pat, tag):
                            issues.append(Issue('privileged-runner', 'warning',
                                f'Job `{job_name}` requests privileged runner tag `{tag}` — ensure this is necessary',
                                find_line(lines, tag)))
                            break

    # Rule 13: unmasked-variable — sensitive var name without [masked] hint
    for i, line in enumerate(lines):
        stripped = line.strip()
        if ':' in stripped and not stripped.startswith('#') and not stripped.startswith('-'):
            colon = stripped.find(':')
            key = stripped[:colon].strip()
            for pat in SENSITIVE_VAR_PATTERNS:
                if re.search(pat, key):
                    # check if line or surrounding context mentions masked
                    context_start = max(0, i - 2)
                    context_end = min(len(lines), i + 3)
                    context = ' '.join(lines[context_start:context_end]).lower()
                    if 'masked' not in context and '$ci_' not in stripped.lower() and '${ci_' not in stripped.lower():
                        val_part = stripped[colon + 1:].strip()
                        if val_part and not val_part.startswith('$') and val_part not in ('""', "''", '~', 'null', ''):
                            issues.append(Issue('unmasked-variable', 'info',
                                f'Variable `{key}` looks sensitive but is not marked as masked',
                                i + 1))
                    break

    # Rule 14: insecure-image
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith('#'):
            continue
        # match image: or - name: with :latest
        m = re.match(r'(?:image|name)\s*:\s*["\']?(\S+?)["\']?\s*$', stripped)
        if m:
            image = m.group(1)
            if image.endswith(':latest'):
                issues.append(Issue('insecure-image', 'warning',
                    f'Image `{image}` uses `:latest` tag — pin to a specific version for reproducibility',
                    i + 1))
            elif ':' not in image and '/' in image:
                # no tag at all implies :latest
                issues.append(Issue('insecure-image', 'info',
                    f'Image `{image}` has no tag — defaults to `:latest`',
                    i + 1))

    return issues


def lint_best_practices(pipeline, lines, raw_text):
    """Check best practices (rules 15-24)."""
    issues = []
    jobs = get_jobs(pipeline)

    for job_name, job in jobs.items():
        if not isinstance(job, dict):
            continue
        if is_hidden_job(job_name):
            continue  # skip templates

        jline = find_line(lines, f'{job_name}:')

        # Rule 15: missing-retry
        if 'retry' not in job:
            for pat in FLAKY_JOB_PATTERNS:
                if re.search(pat, job_name):
                    issues.append(Issue('missing-retry', 'info',
                        f'Job `{job_name}` has no `retry:` — consider adding retry for reliability',
                        jline))
                    break

        # Rule 16: missing-timeout
        if 'timeout' not in job:
            issues.append(Issue('missing-timeout', 'warning',
                f'Job `{job_name}` has no `timeout:` — default is 1 hour, which may be too long',
                jline))

        # Rule 17: no-cache-key
        cache = job.get('cache')
        if cache is not None:
            if isinstance(cache, dict) and 'key' not in cache:
                issues.append(Issue('no-cache-key', 'warning',
                    f'Job `{job_name}` has `cache:` without explicit `key:` — cache may collide',
                    jline))
            elif isinstance(cache, list):
                for idx, c in enumerate(cache):
                    if isinstance(c, dict) and 'key' not in c:
                        issues.append(Issue('no-cache-key', 'warning',
                            f'Job `{job_name}` cache entry {idx+1} has no explicit `key:`',
                            jline))

        # Rule 18: broad-artifacts
        artifacts = job.get('artifacts')
        if isinstance(artifacts, dict):
            paths = artifacts.get('paths', [])
            if isinstance(paths, list):
                for p in paths:
                    if isinstance(p, str) and p in ('.', './', '*', '**/*', '**'):
                        issues.append(Issue('broad-artifacts', 'warning',
                            f'Job `{job_name}` has overly broad artifact path `{p}`',
                            jline))

        # Rule 19: missing-rules
        has_rules = 'rules' in job
        has_only = 'only' in job
        has_except = 'except' in job
        has_trigger = 'trigger' in job
        if not has_rules and not has_only and not has_except and not has_trigger:
            issues.append(Issue('missing-rules', 'info',
                f'Job `{job_name}` has no `rules:`, `only:`, or `except:` — runs on all pipelines',
                jline))

        # Rule 20: deprecated-only-except
        if has_only or has_except:
            issues.append(Issue('deprecated-only-except', 'info',
                f'Job `{job_name}` uses `only:`/`except:` — prefer `rules:` (more flexible)',
                jline))

        # Rule 21: long-script
        script = job.get('script')
        if isinstance(script, list) and len(script) > 30:
            issues.append(Issue('long-script', 'info',
                f'Job `{job_name}` has {len(script)} script lines — consider moving to a separate script file',
                jline))
        elif isinstance(script, str):
            script_lines = script.strip().splitlines()
            if len(script_lines) > 30:
                issues.append(Issue('long-script', 'info',
                    f'Job `{job_name}` has {len(script_lines)} script lines — consider a separate file',
                    jline))

        # Rule 22: missing-interruptible
        if 'interruptible' not in job:
            for pat in LONG_RUNNING_PATTERNS:
                if re.search(pat, job_name):
                    issues.append(Issue('missing-interruptible', 'info',
                        f'Long-running job `{job_name}` has no `interruptible:` flag',
                        jline))
                    break

        # Rule 23: no-coverage-regex
        if 'coverage' not in job:
            for pat in TEST_JOB_PATTERNS:
                if re.search(pat, job_name):
                    issues.append(Issue('no-coverage-regex', 'info',
                        f'Test job `{job_name}` has no `coverage:` regex defined',
                        jline))
                    break

        # Rule 24: missing-when in rules entries
        rules_list = job.get('rules')
        if isinstance(rules_list, list):
            for idx, rule in enumerate(rules_list):
                if isinstance(rule, dict) and 'when' not in rule:
                    issues.append(Issue('missing-when', 'info',
                        f'Job `{job_name}` rule entry {idx+1} has no `when:` — defaults to `on_success`',
                        jline))

    return issues


def lint_stages_info(pipeline, lines):
    """Analyze stages and job-to-stage mapping."""
    issues = []
    stages_defined = pipeline.get('stages')
    jobs = get_jobs(pipeline)

    if isinstance(stages_defined, list):
        effective_stages = [s for s in stages_defined if isinstance(s, str)]
    else:
        effective_stages = DEFAULT_STAGES

    # Map jobs to stages
    stage_jobs = {s: [] for s in effective_stages}
    for job_name, job in jobs.items():
        if not isinstance(job, dict) or is_hidden_job(job_name):
            continue
        job_stage = job.get('stage', 'test')  # default stage is 'test'
        if job_stage in stage_jobs:
            stage_jobs[job_stage].append(job_name)
        else:
            issues.append(Issue('undefined-stage', 'error',
                f'Job `{job_name}` uses stage `{job_stage}` not defined in `stages:`',
                find_line(lines, f'{job_name}:')))

    # Check for unused stages
    for stage in effective_stages:
        if not stage_jobs.get(stage):
            issues.append(Issue('unused-stage', 'info',
                f'Stage `{stage}` is defined but no jobs use it',
                find_line(lines, stage)))

    return issues, stage_jobs, effective_stages


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------

def lint_file(filepath, rules='all'):
    """Lint a single pipeline file. Returns list of Issues."""
    raw = Path(filepath).read_text(encoding='utf-8', errors='replace')
    lines = raw.splitlines()

    try:
        pipeline = parse_yaml(raw)
    except Exception as e:
        return [Issue('parse-error', 'error', f'Failed to parse YAML: {e}', 1)]

    if not isinstance(pipeline, dict):
        return [Issue('parse-error', 'error', 'Pipeline root is not a mapping', 1)]

    issues = []
    if rules in ('all', 'structure', 'validate'):
        issues.extend(lint_structure(pipeline, lines, raw))
    if rules in ('all', 'security'):
        issues.extend(lint_security(pipeline, lines, raw))
    if rules in ('all', 'practices'):
        issues.extend(lint_best_practices(pipeline, lines, raw))
    if rules in ('all', 'stages'):
        stage_issues, _, _ = lint_stages_info(pipeline, lines)
        issues.extend(stage_issues)

    return issues


def stages_report(filepath):
    """Generate stages report for a pipeline file."""
    raw = Path(filepath).read_text(encoding='utf-8', errors='replace')
    lines = raw.splitlines()

    try:
        pipeline = parse_yaml(raw)
    except Exception as e:
        return [Issue('parse-error', 'error', f'Failed to parse YAML: {e}', 1)], {}, []

    if not isinstance(pipeline, dict):
        return [Issue('parse-error', 'error', 'Pipeline root is not a mapping', 1)], {}, []

    return lint_stages_info(pipeline, lines)


def find_pipeline_files(path):
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


def format_stages_text(filepath, stage_jobs, stages, issues):
    lines = [f'Stages for {filepath}:', '']
    for stage in stages:
        jobs = stage_jobs.get(stage, [])
        if jobs:
            lines.append(f'  {stage}: {", ".join(jobs)}')
        else:
            lines.append(f'  {stage}: (no jobs)')
    if issues:
        lines.append('')
        lines.append(format_text(filepath, issues))
    return '\n'.join(lines)


def format_stages_json(filepath, stage_jobs, stages, issues):
    return json.dumps({
        'file': str(filepath),
        'stages': {s: stage_jobs.get(s, []) for s in stages},
        'issues': [i.to_dict() for i in issues],
    }, indent=2)


def format_stages_markdown(filepath, stage_jobs, stages, issues):
    lines = [f'## Stages — {filepath}', '']
    for stage in stages:
        jobs = stage_jobs.get(stage, [])
        if jobs:
            lines.append(f'- **{stage}**: {", ".join(jobs)}')
        else:
            lines.append(f'- **{stage}**: _(no jobs)_')
    if issues:
        lines.append('')
        lines.append(format_markdown(filepath, issues))
    return '\n'.join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description='GitLab CI/CD Pipeline Linter')
    sub = parser.add_subparsers(dest='command', required=True)

    # lint
    p_lint = sub.add_parser('lint', help='Lint pipeline files (all rules)')
    p_lint.add_argument('path', help='Pipeline file or directory')
    p_lint.add_argument('--strict', action='store_true', help='Exit 1 on warnings too')
    p_lint.add_argument('--format', choices=['text', 'json', 'markdown'], default='text')

    # security
    p_sec = sub.add_parser('security', help='Security-focused audit')
    p_sec.add_argument('path', help='Pipeline file')
    p_sec.add_argument('--format', choices=['text', 'json', 'markdown'], default='text')

    # stages
    p_stg = sub.add_parser('stages', help='Show stages and job mapping')
    p_stg.add_argument('path', help='Pipeline file')
    p_stg.add_argument('--format', choices=['text', 'json', 'markdown'], default='text')

    # validate
    p_val = sub.add_parser('validate', help='Validate pipeline structure')
    p_val.add_argument('path', help='Pipeline file')
    p_val.add_argument('--format', choices=['text', 'json', 'markdown'], default='text')

    args = parser.parse_args()
    fmt = getattr(args, 'format', 'text')
    strict = getattr(args, 'strict', False)

    # Handle stages command separately
    if args.command == 'stages':
        files = find_pipeline_files(args.path)
        if not files:
            print(f'No pipeline files found in: {args.path}', file=sys.stderr)
            sys.exit(1)
        has_issues = False
        for f in files:
            stage_issues, stage_jobs, stages = stages_report(str(f))
            if any(i.severity == 'error' for i in stage_issues):
                has_issues = True
            if fmt == 'text':
                print(format_stages_text(f, stage_jobs, stages, stage_issues))
            elif fmt == 'json':
                print(format_stages_json(f, stage_jobs, stages, stage_issues))
            elif fmt == 'markdown':
                print(format_stages_markdown(f, stage_jobs, stages, stage_issues))
        sys.exit(1 if has_issues else 0)

    rule_map = {
        'lint': 'all',
        'security': 'security',
        'validate': 'validate',
    }
    rules = rule_map[args.command]

    files = find_pipeline_files(args.path)
    if not files:
        print(f'No pipeline files found in: {args.path}', file=sys.stderr)
        sys.exit(1)

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
