#!/usr/bin/env python3
"""Prettier Config Validator — validate .prettierrc for structure, options, deprecated fields, best practices."""

import sys
import os
import json
import re
from dataclasses import dataclass
from enum import Enum


class Severity(Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass
class Issue:
    file: str
    path: str
    rule: str
    severity: Severity
    message: str
    category: str


VALID_OPTIONS = {
    'printWidth', 'tabWidth', 'useTabs', 'semi', 'singleQuote',
    'quoteProps', 'jsxSingleQuote', 'trailingComma', 'bracketSpacing',
    'bracketSameLine', 'arrowParens', 'rangeStart', 'rangeEnd',
    'parser', 'filepath', 'requirePragma', 'insertPragma', 'proseWrap',
    'htmlWhitespaceSensitivity', 'vueIndentScriptAndStyle', 'endOfLine',
    'embeddedLanguageFormatting', 'singleAttributePerLine',
    'experimentalTernaries', 'overrides', 'plugins', '$schema',
    'experimentalOperatorPosition', 'objectWrap',
}

BOOLEAN_OPTIONS = {
    'useTabs', 'semi', 'singleQuote', 'jsxSingleQuote', 'bracketSpacing',
    'bracketSameLine', 'requirePragma', 'insertPragma',
    'vueIndentScriptAndStyle', 'singleAttributePerLine',
    'experimentalTernaries',
}

INT_OPTIONS = {'printWidth', 'tabWidth', 'rangeStart', 'rangeEnd'}

STRING_OPTIONS = {
    'quoteProps', 'trailingComma', 'arrowParens', 'parser', 'filepath',
    'proseWrap', 'htmlWhitespaceSensitivity', 'endOfLine',
    'embeddedLanguageFormatting', '$schema',
}

ARRAY_OPTIONS = {'overrides', 'plugins'}

ENUM_VALUES = {
    'quoteProps': {'as-needed', 'consistent', 'preserve'},
    'trailingComma': {'all', 'es5', 'none'},
    'arrowParens': {'always', 'avoid'},
    'proseWrap': {'always', 'never', 'preserve'},
    'htmlWhitespaceSensitivity': {'css', 'strict', 'ignore'},
    'endOfLine': {'lf', 'crlf', 'cr', 'auto'},
    'embeddedLanguageFormatting': {'auto', 'off'},
    'objectWrap': {'preserve', 'collapse'},
    'experimentalOperatorPosition': {'start', 'end'},
}

KNOWN_PARSERS = {
    'babel', 'babel-flow', 'babel-ts', 'flow', 'typescript', 'acorn',
    'espree', 'meriyah', 'css', 'less', 'scss', 'json', 'json5',
    'json-stringify', 'graphql', 'markdown', 'mdx', 'vue', 'yaml',
    'glimmer', 'html', 'angular', 'lwc',
}

DEPRECATED_OPTIONS = {
    'jsxBracketSameLine': 'bracketSameLine (in Prettier v2.4+)',
}

REMOVED_OPTIONS = {
    'useFlowParser': 'set parser to "flow" instead',
    'tabs': 'use useTabs (boolean)',
}


def load_config(filepath):
    """Load a prettier config file. Returns (config_dict, format_str, error)."""
    if not os.path.exists(filepath):
        return None, None, f"File not found: {filepath}"

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return None, None, f"Failed to read file: {e}"

    if not content.strip():
        return {}, 'empty', None

    basename = os.path.basename(filepath).lower()

    if basename == 'package.json':
        try:
            pkg = json.loads(content)
            if not isinstance(pkg, dict):
                return None, 'package.json', "package.json root must be an object"
            if 'prettier' not in pkg:
                return None, 'package.json', "No 'prettier' field in package.json"
            cfg = pkg['prettier']
            if isinstance(cfg, str):
                return {'__extends__': cfg}, 'package.json', None
            if not isinstance(cfg, dict):
                return None, 'package.json', "package.json 'prettier' field must be an object or string"
            return cfg, 'package.json', None
        except json.JSONDecodeError as e:
            return None, 'package.json', f"Invalid JSON: {e.msg} at line {e.lineno}"

    if basename.endswith('.js') or basename.endswith('.mjs') or basename.endswith('.cjs'):
        return None, 'js', "JS config files cannot be statically validated (use .prettierrc.json for full validation)"

    if basename.endswith('.toml'):
        try:
            try:
                import tomllib
            except ImportError:
                try:
                    import tomli as tomllib
                except ImportError:
                    return None, 'toml', "TOML support requires Python 3.11+ or tomli package"
            cfg = tomllib.loads(content)
            return cfg, 'toml', None
        except Exception as e:
            return None, 'toml', f"Invalid TOML: {e}"

    if basename.endswith('.yaml') or basename.endswith('.yml'):
        try:
            import yaml
            cfg = yaml.safe_load(content)
            if cfg is None:
                return {}, 'yaml', None
            if not isinstance(cfg, dict):
                return None, 'yaml', "YAML root must be a mapping/object"
            return cfg, 'yaml', None
        except ImportError:
            return parse_simple_yaml(content), 'yaml-simple', None
        except Exception as e:
            return None, 'yaml', f"Invalid YAML: {e}"

    try:
        cfg = json.loads(content)
        if not isinstance(cfg, dict):
            return None, 'json', "Config root must be an object"
        return cfg, 'json', None
    except json.JSONDecodeError as je:
        try:
            import yaml
            cfg = yaml.safe_load(content)
            if isinstance(cfg, dict):
                return cfg, 'yaml', None
        except Exception:
            pass
        return None, 'json', f"Invalid JSON: {je.msg} at line {je.lineno}"


def parse_simple_yaml(content):
    """Minimal YAML parser for simple key:value configs (fallback when PyYAML missing)."""
    cfg = {}
    for line in content.splitlines():
        s = line.strip()
        if not s or s.startswith('#'):
            continue
        if ':' not in s:
            continue
        k, _, v = s.partition(':')
        k = k.strip()
        v = v.strip().strip('"').strip("'")
        if v.lower() == 'true':
            cfg[k] = True
        elif v.lower() == 'false':
            cfg[k] = False
        elif v.lower() in ('null', '~', ''):
            cfg[k] = None
        else:
            try:
                cfg[k] = int(v)
            except ValueError:
                cfg[k] = v
    return cfg


def check_type(filepath, path_prefix, key, value, issues, in_override=False):
    """Check a single option's type. Appends issues to list."""
    category = "options"
    full_path = f"{path_prefix}.{key}" if path_prefix else key

    if key in BOOLEAN_OPTIONS:
        if not isinstance(value, bool):
            issues.append(Issue(filepath, full_path, "wrong-type", Severity.ERROR,
                                f"'{key}' must be a boolean, got {type(value).__name__}", category))
    elif key in INT_OPTIONS:
        if not isinstance(value, int) or isinstance(value, bool):
            issues.append(Issue(filepath, full_path, "wrong-type", Severity.ERROR,
                                f"'{key}' must be an integer, got {type(value).__name__}", category))
    elif key in STRING_OPTIONS:
        if not isinstance(value, str):
            issues.append(Issue(filepath, full_path, "wrong-type", Severity.ERROR,
                                f"'{key}' must be a string, got {type(value).__name__}", category))
    elif key in ARRAY_OPTIONS:
        if not isinstance(value, list):
            issues.append(Issue(filepath, full_path, "wrong-type", Severity.ERROR,
                                f"'{key}' must be an array, got {type(value).__name__}", category))


def lint_structure(filepath, config):
    issues = []

    if not config:
        issues.append(Issue(filepath, '', "empty-config", Severity.INFO,
                            "Config is empty — all Prettier defaults will apply", "structure"))
        return issues

    if '__extends__' in config:
        issues.append(Issue(filepath, 'prettier', "string-extends", Severity.INFO,
                            f"package.json 'prettier' field is a string (extends '{config['__extends__']}') — "
                            "cannot validate inherited options", "structure"))
        return issues

    for key in config.keys():
        if key in DEPRECATED_OPTIONS:
            continue
        if key in REMOVED_OPTIONS:
            continue
        if key not in VALID_OPTIONS:
            issues.append(Issue(filepath, key, "unknown-option", Severity.WARNING,
                                f"Unknown Prettier option '{key}' — check spelling or plugin docs",
                                "structure"))
            continue
        check_type(filepath, '', key, config[key], issues)

    return issues


def lint_options(filepath, config):
    issues = []

    for key, allowed in ENUM_VALUES.items():
        if key in config:
            value = config[key]
            if isinstance(value, str) and value not in allowed:
                issues.append(Issue(filepath, key, "invalid-enum-value", Severity.ERROR,
                                    f"'{key}' has invalid value '{value}' (valid: {', '.join(sorted(allowed))})",
                                    "options"))

    if 'parser' in config and isinstance(config['parser'], str):
        parser = config['parser']
        if parser and parser not in KNOWN_PARSERS:
            issues.append(Issue(filepath, 'parser', "unknown-parser", Severity.INFO,
                                f"Parser '{parser}' is not a built-in — assumed to come from a plugin",
                                "options"))

    if 'printWidth' in config and isinstance(config['printWidth'], int):
        pw = config['printWidth']
        if pw < 20:
            issues.append(Issue(filepath, 'printWidth', "print-width-too-small", Severity.WARNING,
                                f"printWidth {pw} is unusually small (< 20)", "options"))
        elif pw > 320:
            issues.append(Issue(filepath, 'printWidth', "print-width-too-large", Severity.WARNING,
                                f"printWidth {pw} is unusually large (> 320)", "options"))

    if 'tabWidth' in config and isinstance(config['tabWidth'], int):
        tw = config['tabWidth']
        if tw < 1:
            issues.append(Issue(filepath, 'tabWidth', "tab-width-invalid", Severity.ERROR,
                                f"tabWidth {tw} must be >= 1", "options"))
        elif tw > 16:
            issues.append(Issue(filepath, 'tabWidth', "tab-width-too-large", Severity.WARNING,
                                f"tabWidth {tw} is unusually large (> 16)", "options"))

    if config.get('requirePragma') is True and config.get('insertPragma') is True:
        issues.append(Issue(filepath, '', "pragma-conflict", Severity.WARNING,
                            "requirePragma and insertPragma both true — only files with pragmas "
                            "will be formatted, and pragmas will be inserted when missing (usually redundant)",
                            "options"))

    if 'rangeStart' in config and 'rangeEnd' in config:
        rs, re_ = config['rangeStart'], config['rangeEnd']
        if isinstance(rs, int) and isinstance(re_, int) and rs > re_:
            issues.append(Issue(filepath, 'rangeStart', "range-inverted", Severity.ERROR,
                                f"rangeStart ({rs}) must be <= rangeEnd ({re_})", "options"))

    return issues


def lint_deprecated(filepath, config):
    issues = []
    for key, replacement in DEPRECATED_OPTIONS.items():
        if key in config:
            issues.append(Issue(filepath, key, "deprecated-option", Severity.WARNING,
                                f"'{key}' is deprecated — use '{replacement}'", "deprecated"))
    for key, note in REMOVED_OPTIONS.items():
        if key in config:
            issues.append(Issue(filepath, key, "removed-option", Severity.ERROR,
                                f"'{key}' is removed — {note}", "deprecated"))
    return issues


def lint_overrides(filepath, config):
    issues = []
    overrides = config.get('overrides')
    if overrides is None:
        return issues
    if not isinstance(overrides, list):
        return issues

    seen_patterns = []
    for idx, ov in enumerate(overrides):
        base = f"overrides[{idx}]"
        if not isinstance(ov, dict):
            issues.append(Issue(filepath, base, "override-not-object", Severity.ERROR,
                                "Each override must be an object", "overrides"))
            continue

        if 'files' not in ov:
            issues.append(Issue(filepath, base, "override-missing-files", Severity.ERROR,
                                "Override must have 'files' field", "overrides"))
        else:
            files = ov['files']
            if isinstance(files, list):
                if len(files) == 0:
                    issues.append(Issue(filepath, f"{base}.files", "override-empty-files",
                                        Severity.ERROR, "Override 'files' array is empty", "overrides"))
                for f in files:
                    if not isinstance(f, str):
                        issues.append(Issue(filepath, f"{base}.files", "override-bad-file-type",
                                            Severity.ERROR, "'files' entries must be strings", "overrides"))
                    elif f in seen_patterns:
                        issues.append(Issue(filepath, f"{base}.files", "override-duplicate-pattern",
                                            Severity.WARNING,
                                            f"Duplicate glob pattern '{f}' — earlier override takes precedence",
                                            "overrides"))
                    else:
                        seen_patterns.append(f)
            elif isinstance(files, str):
                if not files:
                    issues.append(Issue(filepath, f"{base}.files", "override-empty-files",
                                        Severity.ERROR, "Override 'files' is empty", "overrides"))
                elif files in seen_patterns:
                    issues.append(Issue(filepath, f"{base}.files", "override-duplicate-pattern",
                                        Severity.WARNING,
                                        f"Duplicate glob pattern '{files}'", "overrides"))
                else:
                    seen_patterns.append(files)
            else:
                issues.append(Issue(filepath, f"{base}.files", "override-bad-files-type",
                                    Severity.ERROR,
                                    "'files' must be a string or array of strings", "overrides"))

        if 'options' not in ov:
            issues.append(Issue(filepath, base, "override-missing-options", Severity.WARNING,
                                "Override has no 'options' — it has no effect", "overrides"))
        else:
            opts = ov['options']
            if not isinstance(opts, dict):
                issues.append(Issue(filepath, f"{base}.options", "override-bad-options-type",
                                    Severity.ERROR, "'options' must be an object", "overrides"))
            else:
                for k in opts.keys():
                    if k in DEPRECATED_OPTIONS:
                        issues.append(Issue(filepath, f"{base}.options.{k}", "override-deprecated-option",
                                            Severity.WARNING,
                                            f"Deprecated option '{k}' in override — use '{DEPRECATED_OPTIONS[k]}'",
                                            "overrides"))
                    elif k in REMOVED_OPTIONS:
                        issues.append(Issue(filepath, f"{base}.options.{k}", "override-removed-option",
                                            Severity.ERROR,
                                            f"Removed option '{k}' in override", "overrides"))
                    elif k not in VALID_OPTIONS:
                        issues.append(Issue(filepath, f"{base}.options.{k}", "override-unknown-option",
                                            Severity.WARNING,
                                            f"Unknown option '{k}' in override", "overrides"))
                    else:
                        check_type(filepath, f"{base}.options", k, opts[k], issues, in_override=True)
                for key, allowed in ENUM_VALUES.items():
                    if key in opts and isinstance(opts[key], str) and opts[key] not in allowed:
                        issues.append(Issue(filepath, f"{base}.options.{key}", "override-invalid-enum",
                                            Severity.ERROR,
                                            f"'{key}' override has invalid value '{opts[key]}'",
                                            "overrides"))

        extra_keys = set(ov.keys()) - {'files', 'excludeFiles', 'options'}
        if extra_keys:
            issues.append(Issue(filepath, base, "override-extra-keys", Severity.WARNING,
                                f"Override has unknown keys: {', '.join(sorted(extra_keys))}",
                                "overrides"))

    return issues


def lint_best_practices(filepath, config):
    issues = []
    if not config or '__extends__' in config:
        return issues

    if 'endOfLine' not in config:
        issues.append(Issue(filepath, '', "missing-end-of-line", Severity.INFO,
                            "No 'endOfLine' set — default is 'lf', consider explicit value for cross-platform teams",
                            "best-practices"))

    if 'trailingComma' not in config:
        issues.append(Issue(filepath, '', "missing-trailing-comma", Severity.INFO,
                            "No 'trailingComma' set — default changed to 'all' in Prettier v3",
                            "best-practices"))

    if 'printWidth' in config and isinstance(config['printWidth'], int):
        if config['printWidth'] < 40:
            issues.append(Issue(filepath, 'printWidth', "print-width-very-short", Severity.WARNING,
                                f"printWidth {config['printWidth']} is very short and may cause awkward line breaks",
                                "best-practices"))

    if config.get('useTabs') is True and 'tabWidth' not in config:
        issues.append(Issue(filepath, 'useTabs', "tabs-no-width", Severity.INFO,
                            "useTabs is true but tabWidth not specified (defaults to 2)",
                            "best-practices"))

    plugins = config.get('plugins', [])
    if isinstance(plugins, list):
        for i, p in enumerate(plugins):
            if not isinstance(p, str):
                issues.append(Issue(filepath, f"plugins[{i}]", "plugin-not-string", Severity.ERROR,
                                    "Plugin entries must be strings", "best-practices"))
            elif not p.strip():
                issues.append(Issue(filepath, f"plugins[{i}]", "plugin-empty", Severity.ERROR,
                                    "Plugin name is empty", "best-practices"))

    return issues


def format_text(issues):
    if not issues:
        return "✓ No issues found"
    lines = []
    by_sev = {Severity.ERROR: '✗', Severity.WARNING: '⚠', Severity.INFO: 'ℹ'}
    for i in issues:
        icon = by_sev.get(i.severity, '•')
        path_part = f" [{i.path}]" if i.path else ""
        lines.append(f"{icon} {i.severity.value.upper():8s} {i.rule:30s}{path_part} {i.message}")
    errors = sum(1 for i in issues if i.severity == Severity.ERROR)
    warnings = sum(1 for i in issues if i.severity == Severity.WARNING)
    infos = sum(1 for i in issues if i.severity == Severity.INFO)
    lines.append(f"\n{errors} error(s), {warnings} warning(s), {infos} info(s)")
    return '\n'.join(lines)


def format_json(issues):
    return json.dumps([{
        'file': i.file, 'path': i.path, 'rule': i.rule,
        'severity': i.severity.value, 'message': i.message,
        'category': i.category
    } for i in issues], indent=2)


def format_summary(issues):
    errors = sum(1 for i in issues if i.severity == Severity.ERROR)
    warnings = sum(1 for i in issues if i.severity == Severity.WARNING)
    infos = sum(1 for i in issues if i.severity == Severity.INFO)
    return f"Errors: {errors} | Warnings: {warnings} | Info: {infos} | Total: {len(issues)}"


def main():
    if len(sys.argv) < 3:
        print("Usage: prettierrc_validator.py <command> <config-file> [--format json|text|summary]")
        print("Commands: lint, options, deprecated, overrides, validate")
        sys.exit(2)

    command = sys.argv[1]
    filepath = sys.argv[2]
    fmt = 'text'
    for i, arg in enumerate(sys.argv):
        if arg == '--format' and i + 1 < len(sys.argv):
            fmt = sys.argv[i + 1]

    config, cfg_format, error = load_config(filepath)
    if error:
        print(f"Error: {error}")
        sys.exit(2)

    if config is None:
        print("Error: Could not parse config")
        sys.exit(2)

    issues = []
    if command == 'lint':
        issues.extend(lint_structure(filepath, config))
        issues.extend(lint_options(filepath, config))
        issues.extend(lint_deprecated(filepath, config))
        issues.extend(lint_overrides(filepath, config))
        issues.extend(lint_best_practices(filepath, config))
    elif command == 'options':
        issues.extend(lint_options(filepath, config))
    elif command == 'deprecated':
        issues.extend(lint_deprecated(filepath, config))
    elif command == 'overrides':
        issues.extend(lint_overrides(filepath, config))
    elif command == 'validate':
        issues.extend(lint_structure(filepath, config))
    else:
        print(f"Unknown command: {command}")
        sys.exit(2)

    if fmt == 'json':
        print(format_json(issues))
    elif fmt == 'summary':
        print(format_summary(issues))
    else:
        print(format_text(issues))

    has_errors = any(i.severity == Severity.ERROR for i in issues)
    sys.exit(1 if has_errors else 0)


if __name__ == '__main__':
    main()
