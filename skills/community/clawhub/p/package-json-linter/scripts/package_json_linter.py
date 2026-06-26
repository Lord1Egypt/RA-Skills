#!/usr/bin/env python3
"""Package.json Linter — lint, validate, and audit package.json files.

Pure Python stdlib. No dependencies.
"""
import sys, os, re, json, argparse
from pathlib import Path


# ---------------------------------------------------------------------------
# Issue model
# ---------------------------------------------------------------------------

class Issue:
    def __init__(self, rule, severity, message, field=''):
        self.rule = rule
        self.severity = severity  # error, warning, info
        self.message = message
        self.field = field

    def to_dict(self):
        return {
            'rule': self.rule,
            'severity': self.severity,
            'message': self.message,
            'field': self.field,
        }


# ---------------------------------------------------------------------------
# Known data
# ---------------------------------------------------------------------------

DEPRECATED_PACKAGES = {
    'request': 'Use `node-fetch`, `undici`, or `got` instead',
    'moment': 'Use `dayjs`, `date-fns`, or `luxon` instead',
    'nomnom': 'Use `commander` or `yargs` instead',
    'istanbul': 'Use `nyc` or `c8` instead',
    'gulp-util': 'Use individual modules instead',
    'left-pad': 'Use `String.prototype.padStart()` instead',
    'tslint': 'Use `eslint` with `@typescript-eslint` instead',
    'popper.js': 'Use `@popperjs/core` instead',
    'node-uuid': 'Use `uuid` instead',
    'querystring': 'Use `URLSearchParams` or `qs` instead',
    'colors': 'Use `chalk`, `picocolors`, or `kleur` instead',
    'node-sass': 'Use `sass` (Dart Sass) instead',
    'merge': 'Use `deepmerge` or spread operator instead',
    'jade': 'Use `pug` instead',
    'coffee-script': 'Use `coffeescript` instead',
    'uglify-js': 'Use `terser` instead (for ES6+ support)',
    'mkdirp': 'Use `fs.mkdirSync(path, { recursive: true })` instead (Node 10+)',
    'rimraf': 'Use `fs.rmSync(path, { recursive: true })` instead (Node 14+)',
    'which': 'Use `node:child_process` execSync with `which`/`where` instead',
    'axios': None,  # not deprecated but often flagged; skip — actually remove this
}
# Remove axios, it's not deprecated
DEPRECATED_PACKAGES.pop('axios', None)

SUSPICIOUS_SCRIPT_PATTERNS = [
    (r'\bcurl\b', 'curl'),
    (r'\bwget\b', 'wget'),
    (r'\beval\b', 'eval'),
    (r'\|\s*sh\b', 'pipe to sh'),
    (r'\|\s*bash\b', 'pipe to bash'),
    (r'\|\s*/bin/sh\b', 'pipe to /bin/sh'),
    (r'\|\s*/bin/bash\b', 'pipe to /bin/bash'),
]

SEMVER_RE = re.compile(
    r'^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)'
    r'(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?'
    r'(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$'
)

NPM_NAME_RE = re.compile(r'^(@[a-z0-9-~][a-z0-9-._~]*/)?[a-z0-9-~][a-z0-9-._~]*$')


# ---------------------------------------------------------------------------
# Linters
# ---------------------------------------------------------------------------

def lint_required_fields(pkg):
    """Check required fields (rules 1-5)."""
    issues = []

    # 1. missing-name
    if 'name' not in pkg:
        issues.append(Issue('missing-name', 'error', 'Missing required `name` field', 'name'))
    else:
        name = pkg['name']
        # 3. invalid-name
        if isinstance(name, str):
            if len(name) > 214:
                issues.append(Issue('invalid-name', 'error',
                    f'Package name exceeds 214 characters ({len(name)} chars)', 'name'))
            elif not NPM_NAME_RE.match(name):
                issues.append(Issue('invalid-name', 'error',
                    f'Package name `{name}` does not match npm naming rules (lowercase, no spaces)', 'name'))
        else:
            issues.append(Issue('invalid-name', 'error', '`name` field must be a string', 'name'))

    # 2. missing-version
    if 'version' not in pkg:
        issues.append(Issue('missing-version', 'error', 'Missing required `version` field', 'version'))
    else:
        version = pkg['version']
        # 4. invalid-version
        if isinstance(version, str):
            if not SEMVER_RE.match(version):
                issues.append(Issue('invalid-version', 'error',
                    f'Version `{version}` is not valid semver', 'version'))
        else:
            issues.append(Issue('invalid-version', 'error', '`version` field must be a string', 'version'))

    # 5. missing-description
    if 'description' not in pkg:
        issues.append(Issue('missing-description', 'warning', 'Missing `description` field', 'description'))

    return issues


def lint_dependencies(pkg):
    """Check dependency issues (rules 6-11)."""
    issues = []

    deps = pkg.get('dependencies', {}) or {}
    dev_deps = pkg.get('devDependencies', {}) or {}
    peer_deps = pkg.get('peerDependencies', {}) or {}
    optional_deps = pkg.get('optionalDependencies', {}) or {}

    all_dep_sections = [
        ('dependencies', deps),
        ('devDependencies', dev_deps),
        ('peerDependencies', peer_deps),
        ('optionalDependencies', optional_deps),
    ]

    for section_name, section in all_dep_sections:
        if not isinstance(section, dict):
            continue
        for pkg_name, version in section.items():
            if not isinstance(version, str):
                continue

            # 6. wildcard-dependency
            if version in ('*', '', 'latest'):
                issues.append(Issue('wildcard-dependency', 'error',
                    f'`{pkg_name}` in `{section_name}` uses wildcard/empty version `{version}`',
                    f'{section_name}.{pkg_name}'))

            # 7. git-dependency
            if version.startswith('git://') or version.startswith('git+') or \
               version.startswith('github:') or re.match(r'^[a-zA-Z0-9_-]+/[a-zA-Z0-9_-]+', version):
                # heuristic: user/repo pattern (but skip semver ranges)
                if version.startswith(('git://', 'git+', 'github:')):
                    issues.append(Issue('git-dependency', 'warning',
                        f'`{pkg_name}` in `{section_name}` points to a git URL (fragile)',
                        f'{section_name}.{pkg_name}'))

            # 8. file-dependency
            if version.startswith('file:'):
                issues.append(Issue('file-dependency', 'warning',
                    f'`{pkg_name}` in `{section_name}` uses `file:` protocol',
                    f'{section_name}.{pkg_name}'))

            # 11. deprecated-package
            if pkg_name in DEPRECATED_PACKAGES:
                hint = DEPRECATED_PACKAGES[pkg_name]
                msg = f'`{pkg_name}` is deprecated'
                if hint:
                    msg += f' -- {hint}'
                issues.append(Issue('deprecated-package', 'warning', msg,
                    f'{section_name}.{pkg_name}'))

    # 9. pinned-dependency — all deps pinned to exact version
    if deps and isinstance(deps, dict):
        all_pinned = True
        for version in deps.values():
            if isinstance(version, str) and (version.startswith('^') or version.startswith('~') or version.startswith('>') or version.startswith('<')):
                all_pinned = False
                break
        if all_pinned and len(deps) > 0:
            issues.append(Issue('pinned-dependency', 'info',
                'All dependencies are pinned to exact versions (no `^` or `~` ranges)',
                'dependencies'))

    # 10. duplicate-dependency
    if isinstance(deps, dict) and isinstance(dev_deps, dict):
        dupes = set(deps.keys()) & set(dev_deps.keys())
        for d in sorted(dupes):
            issues.append(Issue('duplicate-dependency', 'warning',
                f'`{d}` appears in both `dependencies` and `devDependencies`',
                f'dependencies.{d}'))

    return issues


def lint_security(pkg):
    """Check security issues (rules 12-15)."""
    issues = []

    scripts = pkg.get('scripts', {})
    if not isinstance(scripts, dict):
        return issues

    # 12. postinstall-script
    if 'postinstall' in scripts:
        issues.append(Issue('postinstall-script', 'warning',
            '`postinstall` script detected -- supply chain risk',
            'scripts.postinstall'))

    # 13. preinstall-script
    if 'preinstall' in scripts:
        issues.append(Issue('preinstall-script', 'warning',
            '`preinstall` script detected -- supply chain risk',
            'scripts.preinstall'))

    # 14. install-script
    if 'install' in scripts:
        issues.append(Issue('install-script', 'warning',
            '`install` script detected -- supply chain risk',
            'scripts.install'))

    # 15. suspicious-script
    for script_name, script_val in scripts.items():
        if not isinstance(script_val, str):
            continue
        for pattern, label in SUSPICIOUS_SCRIPT_PATTERNS:
            if re.search(pattern, script_val):
                issues.append(Issue('suspicious-script', 'warning',
                    f'Script `{script_name}` contains `{label}` -- potential security risk',
                    f'scripts.{script_name}'))
                break  # one finding per script

    return issues


def lint_best_practices(pkg):
    """Check best practices (rules 16-22)."""
    issues = []

    # 16. missing-license
    if 'license' not in pkg:
        issues.append(Issue('missing-license', 'warning', 'Missing `license` field', 'license'))

    # 17. missing-repository
    if 'repository' not in pkg:
        issues.append(Issue('missing-repository', 'info', 'Missing `repository` field', 'repository'))

    # 18. missing-engines
    if 'engines' not in pkg:
        issues.append(Issue('missing-engines', 'info', 'Missing `engines` field -- specify Node.js version requirements', 'engines'))

    # 19. missing-keywords
    if 'keywords' not in pkg:
        issues.append(Issue('missing-keywords', 'info', 'Missing `keywords` field', 'keywords'))

    # 20. missing-main
    if 'main' not in pkg and 'exports' not in pkg:
        issues.append(Issue('missing-main', 'info', 'Missing `main` or `exports` field', 'main'))

    # 21. missing-scripts
    if 'scripts' not in pkg:
        issues.append(Issue('missing-scripts', 'info', 'No `scripts` section defined', 'scripts'))

    # 22. non-https-url
    url_fields = ['homepage', 'bugs']
    for field in url_fields:
        val = pkg.get(field)
        if isinstance(val, str) and val.startswith('http://'):
            issues.append(Issue('non-https-url', 'warning',
                f'`{field}` uses HTTP instead of HTTPS: `{val}`', field))
        elif isinstance(val, dict):
            url = val.get('url', '')
            if isinstance(url, str) and url.startswith('http://'):
                issues.append(Issue('non-https-url', 'warning',
                    f'`{field}.url` uses HTTP instead of HTTPS: `{url}`', f'{field}.url'))

    repo = pkg.get('repository')
    if isinstance(repo, str) and repo.startswith('http://'):
        issues.append(Issue('non-https-url', 'warning',
            f'`repository` uses HTTP instead of HTTPS: `{repo}`', 'repository'))
    elif isinstance(repo, dict):
        url = repo.get('url', '')
        if isinstance(url, str) and url.startswith('http://'):
            issues.append(Issue('non-https-url', 'warning',
                f'`repository.url` uses HTTP instead of HTTPS: `{url}`', 'repository.url'))

    return issues


def lint_scripts_analysis(pkg):
    """Analyze scripts section in detail."""
    issues = []
    scripts = pkg.get('scripts', {})
    if not isinstance(scripts, dict):
        return issues

    # Check for common missing scripts
    common_scripts = ['test', 'start', 'build']
    for s in common_scripts:
        if s not in scripts:
            issues.append(Issue(f'missing-script-{s}', 'info',
                f'No `{s}` script defined', f'scripts.{s}'))

    # Check for placeholder test script
    test_val = scripts.get('test', '')
    if isinstance(test_val, str) and 'no test specified' in test_val.lower():
        issues.append(Issue('placeholder-test', 'warning',
            'Test script is a placeholder (`no test specified`)', 'scripts.test'))

    return issues


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------

def load_package_json(filepath):
    """Load and parse a package.json file. Returns (dict, error_string)."""
    try:
        raw = Path(filepath).read_text(encoding='utf-8', errors='replace')
    except OSError as e:
        return None, f'Cannot read file: {e}'

    try:
        pkg = json.loads(raw)
    except json.JSONDecodeError as e:
        return None, f'Invalid JSON: {e}'

    if not isinstance(pkg, dict):
        return None, 'package.json root must be an object'

    return pkg, None


def lint_file(filepath, command='lint', strict=False):
    """Lint a single package.json file. Returns list of Issues."""
    pkg, err = load_package_json(filepath)
    if err:
        return [Issue('parse-error', 'error', err, '')]

    issues = []

    if command in ('lint', 'validate'):
        issues.extend(lint_required_fields(pkg))

    if command in ('lint', 'validate', 'scripts'):
        issues.extend(lint_dependencies(pkg))

    if command in ('lint', 'security'):
        issues.extend(lint_security(pkg))

    if command in ('lint', 'validate'):
        issues.extend(lint_best_practices(pkg))

    if command in ('lint', 'scripts'):
        issues.extend(lint_scripts_analysis(pkg))

    return issues


def find_package_files(path):
    """Find package.json files in path."""
    p = Path(path)
    if p.is_file():
        return [p]
    files = list(p.rglob('package.json'))
    # Exclude node_modules
    files = [f for f in files if 'node_modules' not in f.parts]
    return sorted(files)


# ---------------------------------------------------------------------------
# Formatters
# ---------------------------------------------------------------------------

def format_text(filepath, issues):
    lines = []
    for iss in issues:
        field_str = f' ({iss.field})' if iss.field else ''
        lines.append(f'{filepath}:{field_str} {iss.severity} [{iss.rule}] {iss.message}')
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
    lines = [f'## {filepath}', '', '| Severity | Rule | Field | Message |', '|----------|------|-------|---------|']
    for iss in issues:
        sev = {'error': ':red_circle:', 'warning': ':warning:', 'info': ':information_source:'}.get(iss.severity, iss.severity)
        lines.append(f'| {sev} {iss.severity} | `{iss.rule}` | `{iss.field}` | {iss.message} |')
    errs = sum(1 for i in issues if i.severity == 'error')
    warns = sum(1 for i in issues if i.severity == 'warning')
    infos = sum(1 for i in issues if i.severity == 'info')
    lines.append(f'\n**{len(issues)} issues** ({errs} errors, {warns} warnings, {infos} info)')
    return '\n'.join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description='Package.json Linter')
    sub = parser.add_subparsers(dest='command', required=True)

    # lint
    p_lint = sub.add_parser('lint', help='Lint package.json (all rules)')
    p_lint.add_argument('path', help='package.json file or directory')
    p_lint.add_argument('--strict', action='store_true', help='Exit 1 on warnings too')
    p_lint.add_argument('--format', choices=['text', 'json', 'markdown'], default='text')

    # security
    p_sec = sub.add_parser('security', help='Security-focused audit')
    p_sec.add_argument('path', help='package.json file or directory')
    p_sec.add_argument('--format', choices=['text', 'json', 'markdown'], default='text')

    # scripts
    p_scr = sub.add_parser('scripts', help='Analyze scripts section')
    p_scr.add_argument('path', help='package.json file or directory')
    p_scr.add_argument('--format', choices=['text', 'json', 'markdown'], default='text')

    # validate
    p_val = sub.add_parser('validate', help='Validate required fields and structure')
    p_val.add_argument('path', help='package.json file or directory')
    p_val.add_argument('--strict', action='store_true', help='Exit 1 on warnings too')
    p_val.add_argument('--format', choices=['text', 'json', 'markdown'], default='text')

    args = parser.parse_args()

    files = find_package_files(args.path)
    if not files:
        print(f'No package.json files found in: {args.path}', file=sys.stderr)
        sys.exit(1)

    fmt = getattr(args, 'format', 'text')
    strict = getattr(args, 'strict', False)
    total_errors = 0
    total_warnings = 0
    total_infos = 0
    all_results = []

    for f in files:
        issues = lint_file(str(f), args.command, strict)
        errs = sum(1 for i in issues if i.severity == 'error')
        warns = sum(1 for i in issues if i.severity == 'warning')
        infos = sum(1 for i in issues if i.severity == 'info')
        total_errors += errs
        total_warnings += warns
        total_infos += infos

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
        total = total_errors + total_warnings + total_infos
        print(f'\n{total} issues ({total_errors} errors, {total_warnings} warnings, {total_infos} info) in {len(files)} file(s)')

    if total_errors > 0:
        sys.exit(1)
    if strict and total_warnings > 0:
        sys.exit(1)
    sys.exit(0)


if __name__ == '__main__':
    main()
