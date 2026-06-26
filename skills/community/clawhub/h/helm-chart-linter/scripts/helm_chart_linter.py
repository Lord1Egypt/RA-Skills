#!/usr/bin/env python3
"""
Helm Chart Linter — pure Python stdlib, no pip dependencies.
Commands: lint, security, dependencies, validate
Formats:  text, json, markdown
"""

import sys
import os
import re
import json
import glob
from pathlib import Path

# ---------------------------------------------------------------------------
# Minimal YAML parser (no PyYAML)
# Handles: key: value, lists (- item), nested maps (indented keys),
#          multiline strings, quoted strings, booleans, numbers, null.
# ---------------------------------------------------------------------------

def _yaml_parse_value(raw: str):
    """Parse a scalar YAML value string into a Python object."""
    s = raw.strip()
    if not s or s == '~' or s.lower() == 'null':
        return None
    if s.lower() == 'true':
        return True
    if s.lower() == 'false':
        return False
    # Quoted string
    if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
        return s[1:-1]
    # Int
    try:
        return int(s)
    except ValueError:
        pass
    # Float
    try:
        return float(s)
    except ValueError:
        pass
    return s


def _get_indent(line: str) -> int:
    return len(line) - len(line.lstrip(' '))


def yaml_loads(text: str):
    """
    Parse a YAML string into a Python dict/list/scalar.
    Supports: mappings, sequences, nested structures, comments, quoted strings.
    Does NOT support: anchors/aliases, multi-doc, flow style beyond simple scalars.
    """
    lines = text.splitlines()
    # Strip full-line comments and blank lines for structural parsing,
    # but keep originals for line-number references.
    # We build a filtered token list: (indent, key_or_dash, value_or_None)
    def parse_block(lines, base_indent):
        """Parse a YAML block starting at base_indent. Returns (object, consumed_count)."""
        result = None
        i = 0
        while i < len(lines):
            raw = lines[i]
            stripped = raw.strip()
            # Skip comments and blank lines
            if not stripped or stripped.startswith('#'):
                i += 1
                continue
            indent = _get_indent(raw)
            if indent < base_indent:
                break  # end of this block
            if indent > base_indent and result is not None:
                # continuation lines — shouldn't happen at top level if called correctly
                i += 1
                continue

            # Sequence item
            if stripped.startswith('- ') or stripped == '-':
                if result is None:
                    result = []
                if not isinstance(result, list):
                    break
                item_value_raw = stripped[1:].strip() if len(stripped) > 1 else ''
                # Check if item_value_raw is a key: value (inline mapping start)
                if item_value_raw and ':' in item_value_raw and not item_value_raw.startswith('"') and not item_value_raw.startswith("'"):
                    # Inline mapping as first field of an object item
                    # Collect all lines at indent+2 as sub-block
                    sub_lines = [' ' * (indent + 2) + item_value_raw]
                    j = i + 1
                    while j < len(lines):
                        sub_raw = lines[j]
                        sub_stripped = sub_raw.strip()
                        if not sub_stripped or sub_stripped.startswith('#'):
                            j += 1
                            continue
                        sub_indent = _get_indent(sub_raw)
                        if sub_indent <= indent:
                            break
                        sub_lines.append(sub_raw)
                        j += 1
                    obj, _ = parse_block(sub_lines, indent + 2)
                    result.append(obj)
                    i = j
                elif item_value_raw == '':
                    # Next lines form a mapping or sequence at higher indent
                    j = i + 1
                    sub_lines = []
                    child_indent = None
                    while j < len(lines):
                        sub_raw = lines[j]
                        sub_stripped = sub_raw.strip()
                        if not sub_stripped or sub_stripped.startswith('#'):
                            j += 1
                            continue
                        sub_indent = _get_indent(sub_raw)
                        if child_indent is None:
                            child_indent = sub_indent
                        if sub_indent < child_indent:
                            break
                        sub_lines.append(sub_raw)
                        j += 1
                    if sub_lines:
                        ci = child_indent if child_indent is not None else indent + 2
                        obj, _ = parse_block(sub_lines, ci)
                        result.append(obj)
                    else:
                        result.append(None)
                    i = j
                else:
                    result.append(_yaml_parse_value(item_value_raw))
                    i += 1
            elif ':' in stripped:
                # Key: value mapping
                if result is None:
                    result = {}
                if not isinstance(result, dict):
                    i += 1
                    continue
                # Handle quoted keys
                colon_pos = stripped.find(':')
                key_raw = stripped[:colon_pos].strip().strip('"').strip("'")
                val_raw = stripped[colon_pos + 1:].strip()

                # Strip inline comment from val_raw (but not inside quotes)
                if val_raw and not val_raw.startswith('"') and not val_raw.startswith("'"):
                    comment_match = re.search(r'\s+#', val_raw)
                    if comment_match:
                        val_raw = val_raw[:comment_match.start()].strip()

                if val_raw == '' or val_raw == '|' or val_raw == '>':
                    # Value is a nested block on the next lines
                    if val_raw in ('|', '>'):
                        # Literal/folded block scalar — collect as string
                        j = i + 1
                        block_lines = []
                        child_indent = None
                        while j < len(lines):
                            sub_raw = lines[j]
                            if not sub_raw.strip():
                                block_lines.append('')
                                j += 1
                                continue
                            sub_indent = _get_indent(sub_raw)
                            if child_indent is None:
                                child_indent = sub_indent
                            if sub_indent < child_indent:
                                break
                            block_lines.append(sub_raw[child_indent:])
                            j += 1
                        result[key_raw] = '\n'.join(block_lines)
                        i = j
                    else:
                        # Empty value: next indented lines are the child block
                        j = i + 1
                        sub_lines = []
                        child_indent = None
                        while j < len(lines):
                            sub_raw = lines[j]
                            sub_stripped = sub_raw.strip()
                            if not sub_stripped or sub_stripped.startswith('#'):
                                j += 1
                                continue
                            sub_indent = _get_indent(sub_raw)
                            if child_indent is None:
                                child_indent = sub_indent
                            if sub_indent < child_indent:
                                break
                            sub_lines.append(sub_raw)
                            j += 1
                        if sub_lines:
                            ci = child_indent if child_indent is not None else indent + 2
                            child_obj, _ = parse_block(sub_lines, ci)
                            result[key_raw] = child_obj
                        else:
                            result[key_raw] = None
                        i = j
                else:
                    result[key_raw] = _yaml_parse_value(val_raw)
                    i += 1
            else:
                i += 1

        return result, i

    obj, _ = parse_block(lines, 0)
    return obj


# ---------------------------------------------------------------------------
# Issue model
# ---------------------------------------------------------------------------

class Issue:
    LEVELS = ('error', 'warning', 'info')

    def __init__(self, rule: str, level: str, message: str, file: str = '', line: int = 0):
        self.rule = rule
        self.level = level
        self.message = message
        self.file = file
        self.line = line

    def to_dict(self):
        return {
            'rule': self.rule,
            'level': self.level,
            'message': self.message,
            'file': self.file,
            'line': self.line,
        }


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

SEMVER_RE = re.compile(
    r'^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)'
    r'(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?'
    r'(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$'
)

DEPRECATED_APIS = [
    'extensions/v1beta1',
    'apps/v1beta1',
    'apps/v1beta2',
    'batch/v1beta1',
    'networking.k8s.io/v1beta1',
    'rbac.authorization.k8s.io/v1alpha1',
    'rbac.authorization.k8s.io/v1beta1',
    'apiextensions.k8s.io/v1beta1',
    'admissionregistration.k8s.io/v1beta1',
    'policy/v1beta1',
]

SECRET_PATTERNS = [
    re.compile(r'\b(password|passwd|secret|token|api_key|apikey|private_key|access_key|secret_key)\s*:', re.I),
]

WILDCARD_VER_RE = re.compile(r'[*xX]')


def read_file(path: str) -> str:
    try:
        with open(path, 'r', encoding='utf-8', errors='replace') as f:
            return f.read()
    except OSError:
        return ''


def load_yaml_file(path: str):
    """Return parsed YAML or None on failure."""
    text = read_file(path)
    if not text:
        return None
    try:
        return yaml_loads(text)
    except Exception:
        return None


def find_template_files(chart_dir: str):
    templates_dir = os.path.join(chart_dir, 'templates')
    if not os.path.isdir(templates_dir):
        return []
    result = []
    for root, dirs, files in os.walk(templates_dir):
        for fname in files:
            if fname.endswith('.yaml') or fname.endswith('.yml'):
                result.append(os.path.join(root, fname))
    return result


# ---------------------------------------------------------------------------
# Rule implementations
# ---------------------------------------------------------------------------

def check_chart_yaml(chart_dir: str) -> list:
    issues = []
    chart_yaml_path = os.path.join(chart_dir, 'Chart.yaml')

    if not os.path.isfile(chart_yaml_path):
        issues.append(Issue('CHART001', 'error', 'Chart.yaml is missing', chart_yaml_path))
        return issues

    data = load_yaml_file(chart_yaml_path)
    if data is None or not isinstance(data, dict):
        issues.append(Issue('CHART001', 'error', 'Chart.yaml could not be parsed or is empty', chart_yaml_path))
        return issues

    required = ['apiVersion', 'name', 'version', 'description']
    for field in required:
        if field not in data or data[field] is None or str(data[field]).strip() == '':
            issues.append(Issue('CHART001', 'error', f'Chart.yaml missing required field: {field}', chart_yaml_path))

    # CHART002: semver
    version = str(data.get('version', '')).strip()
    if version and not SEMVER_RE.match(version):
        issues.append(Issue('CHART002', 'error', f'Chart.yaml version is not valid semver: "{version}"', chart_yaml_path))

    return issues


def check_values_yaml(chart_dir: str) -> list:
    issues = []
    values_path = os.path.join(chart_dir, 'values.yaml')
    if not os.path.isfile(values_path):
        issues.append(Issue('CHART003', 'error', 'values.yaml is missing', values_path))
    return issues


def check_templates_dir(chart_dir: str) -> list:
    issues = []
    templates_dir = os.path.join(chart_dir, 'templates')
    if not os.path.isdir(templates_dir):
        issues.append(Issue('CHART004', 'error', 'templates/ directory is missing', templates_dir))
        return issues

    notes_path = os.path.join(templates_dir, 'NOTES.txt')
    if not os.path.isfile(notes_path):
        issues.append(Issue('CHART005', 'warning', 'templates/NOTES.txt is missing (recommended for user guidance)', notes_path))

    return issues


def check_helmignore(chart_dir: str) -> list:
    issues = []
    helmignore_path = os.path.join(chart_dir, '.helmignore')
    if not os.path.isfile(helmignore_path):
        issues.append(Issue('CHART006', 'warning', '.helmignore is missing (recommended to exclude test/CI files)', helmignore_path))
    return issues


def check_secrets_in_values(chart_dir: str) -> list:
    issues = []
    values_path = os.path.join(chart_dir, 'values.yaml')
    if not os.path.isfile(values_path):
        return issues
    text = read_file(values_path)
    for lineno, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        if stripped.startswith('#'):
            continue
        for pattern in SECRET_PATTERNS:
            if pattern.search(stripped):
                # Check if the value looks like a real secret (non-empty, not a template)
                colon_pos = stripped.find(':')
                if colon_pos >= 0:
                    val = stripped[colon_pos + 1:].strip().strip('"').strip("'")
                    # Skip empty values, template placeholders, and documented examples
                    if val and not val.startswith('{{') and val.lower() not in ('', 'null', '~', 'changeme', 'your-secret-here', 'replace-me'):
                        issues.append(Issue(
                            'SEC001', 'warning',
                            f'Possible hardcoded secret on line {lineno}: "{stripped[:80]}"',
                            values_path, lineno
                        ))
                break
    return issues


def _search_in_templates(chart_dir: str, pattern_str: str, rule: str, level: str, message_tmpl: str) -> list:
    issues = []
    pattern = re.compile(pattern_str)
    for tpl_path in find_template_files(chart_dir):
        text = read_file(tpl_path)
        for lineno, line in enumerate(text.splitlines(), 1):
            if pattern.search(line):
                issues.append(Issue(rule, level, message_tmpl.format(file=os.path.basename(tpl_path)), tpl_path, lineno))
                break  # one issue per file
    return issues


def check_privileged_containers(chart_dir: str) -> list:
    issues = []
    pattern = re.compile(r'privileged\s*:\s*true', re.I)
    for tpl_path in find_template_files(chart_dir):
        text = read_file(tpl_path)
        for lineno, line in enumerate(text.splitlines(), 1):
            if pattern.search(line):
                issues.append(Issue('SEC002', 'error',
                    f'Privileged container detected in {os.path.basename(tpl_path)}', tpl_path, lineno))
    return issues


def check_host_namespace(chart_dir: str) -> list:
    issues = []
    pattern = re.compile(r'(hostNetwork|hostPID|hostIPC)\s*:\s*true', re.I)
    for tpl_path in find_template_files(chart_dir):
        text = read_file(tpl_path)
        for lineno, line in enumerate(text.splitlines(), 1):
            m = pattern.search(line)
            if m:
                issues.append(Issue('SEC003', 'error',
                    f'{m.group(1)} enabled in {os.path.basename(tpl_path)}', tpl_path, lineno))
    return issues


def check_resource_limits(chart_dir: str) -> list:
    issues = []
    for tpl_path in find_template_files(chart_dir):
        text = read_file(tpl_path)
        # Only check files that look like Deployment/StatefulSet/DaemonSet
        if not re.search(r'kind\s*:\s*(Deployment|StatefulSet|DaemonSet|Job|CronJob)', text):
            continue
        if 'limits:' not in text and 'resources:' not in text:
            issues.append(Issue('SEC004', 'warning',
                f'No resource limits defined in {os.path.basename(tpl_path)}', tpl_path))
    return issues


def check_run_as_root(chart_dir: str) -> list:
    issues = []
    for tpl_path in find_template_files(chart_dir):
        text = read_file(tpl_path)
        if not re.search(r'kind\s*:\s*(Deployment|StatefulSet|DaemonSet|Job)', text):
            continue
        has_security_context = 'securityContext' in text
        has_run_as_non_root = re.search(r'runAsNonRoot\s*:\s*true', text)
        has_run_as_user = re.search(r'runAsUser\s*:\s*\d+', text)
        if has_security_context and not has_run_as_non_root and not has_run_as_user:
            issues.append(Issue('SEC005', 'warning',
                f'securityContext present but runAsNonRoot/runAsUser not set in {os.path.basename(tpl_path)}',
                tpl_path))
    return issues


def check_latest_image_tag(chart_dir: str) -> list:
    issues = []
    # Check both values.yaml and templates
    values_path = os.path.join(chart_dir, 'values.yaml')
    if os.path.isfile(values_path):
        text = read_file(values_path)
        pattern = re.compile(r'tag\s*:\s*["\']?latest["\']?', re.I)
        for lineno, line in enumerate(text.splitlines(), 1):
            if pattern.search(line):
                issues.append(Issue('SEC006', 'warning',
                    f'Image tag "latest" used in values.yaml (line {lineno}) — pin to a specific version',
                    values_path, lineno))

    pattern = re.compile(r'image\s*:\s*\S+:latest', re.I)
    for tpl_path in find_template_files(chart_dir):
        text = read_file(tpl_path)
        for lineno, line in enumerate(text.splitlines(), 1):
            if pattern.search(line) and '{{' not in line:
                issues.append(Issue('SEC006', 'warning',
                    f'Hardcoded "latest" image tag in {os.path.basename(tpl_path)}', tpl_path, lineno))
    return issues


def _get_chart_deps(chart_dir: str):
    """Return list of dependency dicts from Chart.yaml, or []."""
    chart_yaml_path = os.path.join(chart_dir, 'Chart.yaml')
    data = load_yaml_file(chart_yaml_path)
    if not isinstance(data, dict):
        return []
    deps = data.get('dependencies') or data.get('requirements') or []
    return deps if isinstance(deps, list) else []


def check_chart_lock(chart_dir: str) -> list:
    issues = []
    chart_deps = _get_chart_deps(chart_dir)
    if not chart_deps:
        return issues  # no deps declared, nothing to check

    lock_path = os.path.join(chart_dir, 'Chart.lock')
    if not os.path.isfile(lock_path):
        issues.append(Issue('DEP001', 'warning',
            'Chart.lock is missing — run "helm dependency update" to generate it', lock_path))
        return issues

    lock_data = load_yaml_file(lock_path)
    if not isinstance(lock_data, dict):
        issues.append(Issue('DEP001', 'warning', 'Chart.lock could not be parsed', lock_path))
        return issues

    lock_deps = lock_data.get('dependencies') or []
    if not isinstance(lock_deps, list):
        lock_deps = []

    chart_names = sorted(d.get('name', '') for d in chart_deps if isinstance(d, dict))
    lock_names = sorted(d.get('name', '') for d in lock_deps if isinstance(d, dict))

    if chart_names != lock_names:
        issues.append(Issue('DEP001', 'warning',
            f'Chart.lock dependencies do not match Chart.yaml. Chart.yaml: {chart_names}, Chart.lock: {lock_names}',
            lock_path))
    return issues


def check_wildcard_versions(chart_dir: str) -> list:
    issues = []
    for dep in _get_chart_deps(chart_dir):
        if not isinstance(dep, dict):
            continue
        ver = str(dep.get('version', ''))
        if WILDCARD_VER_RE.search(ver):
            issues.append(Issue('DEP002', 'warning',
                f'Dependency "{dep.get("name", "?")}" uses wildcard version: "{ver}"',
                os.path.join(chart_dir, 'Chart.yaml')))
    return issues


def check_repo_https(chart_dir: str) -> list:
    issues = []
    for dep in _get_chart_deps(chart_dir):
        if not isinstance(dep, dict):
            continue
        repo = str(dep.get('repository', ''))
        if repo and not repo.startswith('https://') and not repo.startswith('oci://') and not repo.startswith('@'):
            issues.append(Issue('DEP003', 'warning',
                f'Dependency "{dep.get("name", "?")}" repository does not use HTTPS: "{repo}"',
                os.path.join(chart_dir, 'Chart.yaml')))
    return issues


def check_duplicate_deps(chart_dir: str) -> list:
    issues = []
    deps = _get_chart_deps(chart_dir)
    names = [d.get('name', '') for d in deps if isinstance(d, dict)]
    seen = set()
    for name in names:
        if name in seen:
            issues.append(Issue('DEP004', 'error',
                f'Duplicate dependency name: "{name}"',
                os.path.join(chart_dir, 'Chart.yaml')))
        seen.add(name)
    return issues


def check_standard_labels(chart_dir: str) -> list:
    issues = []
    required_labels = [
        'app.kubernetes.io/name',
        'app.kubernetes.io/version',
        'app.kubernetes.io/managed-by',
    ]
    for tpl_path in find_template_files(chart_dir):
        text = read_file(tpl_path)
        if not re.search(r'kind\s*:\s*(Deployment|StatefulSet|DaemonSet|Service)', text):
            continue
        missing = [lbl for lbl in required_labels if lbl not in text]
        if missing:
            issues.append(Issue('BP001', 'warning',
                f'{os.path.basename(tpl_path)} missing labels: {", ".join(missing)}', tpl_path))
    return issues


def check_probes(chart_dir: str) -> list:
    issues = []
    for tpl_path in find_template_files(chart_dir):
        text = read_file(tpl_path)
        if not re.search(r'kind\s*:\s*(Deployment|StatefulSet|DaemonSet)', text):
            continue
        has_liveness = 'livenessProbe' in text
        has_readiness = 'readinessProbe' in text
        if not has_liveness:
            issues.append(Issue('BP002', 'warning',
                f'livenessProbe not defined in {os.path.basename(tpl_path)}', tpl_path))
        if not has_readiness:
            issues.append(Issue('BP002', 'warning',
                f'readinessProbe not defined in {os.path.basename(tpl_path)}', tpl_path))
    return issues


def check_service_account(chart_dir: str) -> list:
    issues = []
    for tpl_path in find_template_files(chart_dir):
        text = read_file(tpl_path)
        if not re.search(r'kind\s*:\s*(Deployment|StatefulSet|DaemonSet)', text):
            continue
        if 'serviceAccountName' not in text:
            issues.append(Issue('BP003', 'warning',
                f'serviceAccountName not configured in {os.path.basename(tpl_path)}', tpl_path))
    return issues


def check_hardcoded_namespace(chart_dir: str) -> list:
    issues = []
    # namespace: hardcoded_value (not a template expression)
    pattern = re.compile(r'namespace\s*:\s*(?!\{\{)[a-zA-Z0-9][\w-]+', re.I)
    exclude = re.compile(r'namespace\s*:\s*(default|kube-system|kube-public)', re.I)
    for tpl_path in find_template_files(chart_dir):
        text = read_file(tpl_path)
        for lineno, line in enumerate(text.splitlines(), 1):
            stripped = line.strip()
            if stripped.startswith('#'):
                continue
            if pattern.search(stripped) and not exclude.search(stripped):
                issues.append(Issue('BP004', 'warning',
                    f'Hardcoded namespace in {os.path.basename(tpl_path)} line {lineno} — use .Release.Namespace',
                    tpl_path, lineno))
                break
    return issues


def check_deprecated_apis(chart_dir: str) -> list:
    issues = []
    for tpl_path in find_template_files(chart_dir):
        text = read_file(tpl_path)
        for dep_api in DEPRECATED_APIS:
            if dep_api in text:
                issues.append(Issue('BP005', 'error',
                    f'Deprecated apiVersion "{dep_api}" used in {os.path.basename(tpl_path)}', tpl_path))
    return issues


def check_values_documented(chart_dir: str) -> list:
    issues = []
    values_path = os.path.join(chart_dir, 'values.yaml')
    if not os.path.isfile(values_path):
        return issues
    text = read_file(values_path)
    lines = text.splitlines()
    if not lines:
        return issues
    # Count top-level keys and how many have a preceding comment
    top_keys = 0
    commented_keys = 0
    prev_was_comment = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('#'):
            prev_was_comment = True
            continue
        if stripped == '':
            prev_was_comment = False
            continue
        if not line.startswith(' ') and not line.startswith('\t') and ':' in stripped:
            top_keys += 1
            if prev_was_comment:
                commented_keys += 1
        prev_was_comment = False

    if top_keys > 3 and commented_keys == 0:
        issues.append(Issue('BP006', 'info',
            'values.yaml has no top-level comments — document keys for maintainability', values_path))
    elif top_keys > 5 and commented_keys / top_keys < 0.3:
        issues.append(Issue('BP006', 'info',
            f'Only {commented_keys}/{top_keys} top-level values.yaml keys have comments', values_path))
    return issues


# ---------------------------------------------------------------------------
# Command runners
# ---------------------------------------------------------------------------

def run_lint(chart_dir: str) -> list:
    """All 22 rules."""
    issues = []
    issues += check_chart_yaml(chart_dir)
    issues += check_values_yaml(chart_dir)
    issues += check_templates_dir(chart_dir)
    issues += check_helmignore(chart_dir)
    issues += check_secrets_in_values(chart_dir)
    issues += check_privileged_containers(chart_dir)
    issues += check_host_namespace(chart_dir)
    issues += check_resource_limits(chart_dir)
    issues += check_run_as_root(chart_dir)
    issues += check_latest_image_tag(chart_dir)
    issues += check_chart_lock(chart_dir)
    issues += check_wildcard_versions(chart_dir)
    issues += check_repo_https(chart_dir)
    issues += check_duplicate_deps(chart_dir)
    issues += check_standard_labels(chart_dir)
    issues += check_probes(chart_dir)
    issues += check_service_account(chart_dir)
    issues += check_hardcoded_namespace(chart_dir)
    issues += check_deprecated_apis(chart_dir)
    issues += check_values_documented(chart_dir)
    return issues


def run_security(chart_dir: str) -> list:
    issues = []
    issues += check_secrets_in_values(chart_dir)
    issues += check_privileged_containers(chart_dir)
    issues += check_host_namespace(chart_dir)
    issues += check_resource_limits(chart_dir)
    issues += check_run_as_root(chart_dir)
    issues += check_latest_image_tag(chart_dir)
    return issues


def run_dependencies(chart_dir: str) -> list:
    issues = []
    issues += check_chart_lock(chart_dir)
    issues += check_wildcard_versions(chart_dir)
    issues += check_repo_https(chart_dir)
    issues += check_duplicate_deps(chart_dir)
    return issues


def run_validate(chart_dir: str) -> list:
    return run_lint(chart_dir)


COMMANDS = {
    'lint': run_lint,
    'security': run_security,
    'dependencies': run_dependencies,
    'validate': run_validate,
}

# ---------------------------------------------------------------------------
# Output formatters
# ---------------------------------------------------------------------------

LEVEL_ICONS = {'error': '[ERROR]', 'warning': '[WARN] ', 'info': '[INFO] '}


def format_text(issues: list, chart_dir: str, command: str) -> str:
    lines = [f'Helm Chart Linter — {command} — {chart_dir}']
    lines.append('=' * 60)
    if not issues:
        lines.append('No issues found.')
        return '\n'.join(lines)
    for iss in issues:
        icon = LEVEL_ICONS.get(iss.level, '       ')
        loc = ''
        if iss.file:
            rel = os.path.relpath(iss.file, chart_dir)
            loc = f' ({rel}' + (f':{iss.line}' if iss.line else '') + ')'
        lines.append(f'{icon} [{iss.rule}] {iss.message}{loc}')
    lines.append('')
    counts = {'error': 0, 'warning': 0, 'info': 0}
    for iss in issues:
        counts[iss.level] = counts.get(iss.level, 0) + 1
    lines.append(f'Total: {len(issues)} issue(s) — {counts["error"]} error(s), {counts["warning"]} warning(s), {counts["info"]} info(s)')
    return '\n'.join(lines)


def format_json(issues: list, chart_dir: str, command: str) -> str:
    counts = {'error': 0, 'warning': 0, 'info': 0}
    for iss in issues:
        counts[iss.level] = counts.get(iss.level, 0) + 1
    payload = {
        'command': command,
        'chart_dir': chart_dir,
        'summary': {**counts, 'total': len(issues)},
        'issues': [iss.to_dict() for iss in issues],
    }
    return json.dumps(payload, indent=2)


def format_markdown(issues: list, chart_dir: str, command: str) -> str:
    lines = [f'# Helm Chart Linter Report', '']
    lines.append(f'**Command:** `{command}`  ')
    lines.append(f'**Chart:** `{chart_dir}`')
    lines.append('')
    counts = {'error': 0, 'warning': 0, 'info': 0}
    for iss in issues:
        counts[iss.level] = counts.get(iss.level, 0) + 1
    lines.append(f'**Summary:** {counts["error"]} error(s), {counts["warning"]} warning(s), {counts["info"]} info(s)')
    lines.append('')
    if not issues:
        lines.append('No issues found.')
        return '\n'.join(lines)
    lines.append('## Issues')
    lines.append('')
    for iss in issues:
        badge = {'error': '`ERROR`', 'warning': '`WARN`', 'info': '`INFO`'}.get(iss.level, '')
        loc = ''
        if iss.file:
            rel = os.path.relpath(iss.file, chart_dir)
            loc = f' — `{rel}' + (f':{iss.line}' if iss.line else '') + '`'
        lines.append(f'- {badge} **[{iss.rule}]** {iss.message}{loc}')
    return '\n'.join(lines)


FORMATTERS = {
    'text': format_text,
    'json': format_json,
    'markdown': format_markdown,
}

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    args = sys.argv[1:]

    if len(args) < 2 or args[0] in ('-h', '--help'):
        print('Usage: helm_chart_linter.py <command> <chart-dir> [--strict] [--format text|json|markdown]')
        print('Commands: lint, security, dependencies, validate')
        sys.exit(0 if args and args[0] in ('-h', '--help') else 2)

    command = args[0]
    chart_dir = args[1]
    rest = args[2:]

    if command not in COMMANDS:
        print(f'Unknown command: {command}. Valid: {", ".join(COMMANDS)}', file=sys.stderr)
        sys.exit(2)

    strict = '--strict' in rest
    fmt = 'text'
    for i, a in enumerate(rest):
        if a == '--format' and i + 1 < len(rest):
            fmt = rest[i + 1]

    if fmt not in FORMATTERS:
        print(f'Unknown format: {fmt}. Valid: text, json, markdown', file=sys.stderr)
        sys.exit(2)

    if not os.path.isdir(chart_dir):
        print(f'Chart directory not found: {chart_dir}', file=sys.stderr)
        sys.exit(2)

    issues = COMMANDS[command](chart_dir)
    output = FORMATTERS[fmt](issues, chart_dir, command)
    print(output)

    has_errors = any(iss.level == 'error' for iss in issues)
    has_warnings = any(iss.level == 'warning' for iss in issues)

    if has_errors:
        sys.exit(1)
    if strict and has_warnings:
        sys.exit(1)
    sys.exit(0)


if __name__ == '__main__':
    main()
