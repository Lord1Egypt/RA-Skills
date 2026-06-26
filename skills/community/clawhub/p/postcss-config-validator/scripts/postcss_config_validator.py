#!/usr/bin/env python3
"""PostCSS Config Validator — validate .postcssrc, .postcssrc.json, package.json#postcss, and detect JS/TS configs."""

import json
import os
import sys
from pathlib import Path

# --- Constants ---

VALID_TOP_KEYS = {"plugins", "parser", "syntax", "stringifier", "map", "from", "to"}

JS_TS_EXTENSIONS = {".js", ".cjs", ".mjs", ".ts"}

JS_TS_CONFIG_NAMES = {
    "postcss.config.js", "postcss.config.cjs", "postcss.config.mjs", "postcss.config.ts",
}

JSON_CONFIG_NAMES = {".postcssrc", ".postcssrc.json"}

ALL_CONFIG_NAMES = JS_TS_CONFIG_NAMES | JSON_CONFIG_NAMES

DEPRECATED_PLUGINS = {
    "autoprefixer-core": "Renamed to 'autoprefixer' since v6",
    "postcss-cssnext": "Replaced by 'postcss-preset-env'",
    "lost": "Unmaintained — consider 'postcss-grid' or CSS Grid",
    "postcss-sprites": "Deprecated — use CSS image-set() or a bundler sprite plugin",
    "cssnext": "Renamed to 'postcss-cssnext', then replaced by 'postcss-preset-env'",
}

KNOWN_PARSERS = {
    "postcss-scss", "postcss-less", "postcss-html", "sugarss", "postcss-styl",
}

# Top ~50 well-known PostCSS plugins for P6 info check
TOP_PLUGINS = {
    "autoprefixer", "postcss-preset-env", "postcss-import", "postcss-nested",
    "postcss-nesting", "postcss-custom-properties", "postcss-custom-media",
    "postcss-mixins", "postcss-simple-vars", "postcss-extend", "postcss-extend-rule",
    "postcss-url", "postcss-assets", "postcss-modules", "postcss-color-function",
    "postcss-color-mod-function", "postcss-calc", "postcss-flexbugs-fixes",
    "postcss-normalize", "postcss-reporter", "postcss-browser-reporter",
    "postcss-sorting", "postcss-utilities", "postcss-font-magician",
    "postcss-pxtorem", "postcss-px-to-viewport", "postcss-rem",
    "postcss-responsive-type", "postcss-write-svg", "postcss-svgo",
    "postcss-inline-svg", "postcss-logical", "postcss-dir-pseudo-class",
    "postcss-gap-properties", "postcss-overflow-shorthand", "postcss-place",
    "cssnano", "postcss-clean", "postcss-discard-comments", "postcss-discard-duplicates",
    "postcss-merge-rules", "postcss-minify-selectors", "postcss-normalize-url",
    "tailwindcss", "@tailwindcss/nesting", "postcss-scss", "postcss-less",
    "postcss-html", "sugarss", "postcss-styl", "postcss-focus-visible",
    "postcss-focus-within",
}

# Features included in postcss-preset-env that people sometimes add separately
PRESET_ENV_INCLUDED_PLUGINS = {
    "postcss-custom-properties", "postcss-custom-media", "postcss-nesting",
    "postcss-color-function", "postcss-color-mod-function", "postcss-logical",
    "postcss-dir-pseudo-class", "postcss-gap-properties", "postcss-overflow-shorthand",
    "postcss-place", "postcss-focus-visible", "postcss-focus-within",
    "postcss-custom-selectors", "postcss-media-minmax", "postcss-lab-function",
    "postcss-color-functional-notation",
}


class Finding:
    def __init__(self, rule_id, severity, message, detail=None):
        self.rule_id = rule_id
        self.severity = severity
        self.message = message
        self.detail = detail

    def to_dict(self):
        d = {"rule": self.rule_id, "severity": self.severity, "message": self.message}
        if self.detail:
            d["detail"] = self.detail
        return d

    def to_text(self):
        if self.severity == "error":
            icon = "❌"
        elif self.severity == "warning":
            icon = "⚠️"
        else:
            icon = "ℹ️"
        s = f"{icon} [{self.rule_id}] {self.message}"
        if self.detail:
            s += f"\n   → {self.detail}"
        return s


# --- Config loading ---

def detect_config_type(filepath):
    """Return 'js_ts', 'json', or 'package_json'."""
    p = Path(filepath)
    if p.name in JS_TS_CONFIG_NAMES:
        return "js_ts"
    if p.name == "package.json":
        return "package_json"
    # .postcssrc, .postcssrc.json, or anything else — treat as JSON
    return "json"


def load_config(filepath):
    """Load and parse a PostCSS config. Returns (config_dict, error_string, config_type)."""
    p = Path(filepath)
    config_type = detect_config_type(filepath)

    if not p.exists():
        return None, f"File not found: {filepath}", config_type

    # JS/TS detection before reading content — these can't be statically validated regardless
    if config_type == "js_ts":
        return None, "JS_TS_DETECTED", config_type

    try:
        text = p.read_text(encoding="utf-8").strip()
    except Exception as e:
        return None, f"Cannot read file: {e}", config_type

    if not text:
        return None, "File is empty", config_type

    if config_type == "package_json":
        try:
            pkg = json.loads(text)
        except json.JSONDecodeError as e:
            return None, f"Invalid JSON syntax: {e}", config_type
        if "postcss" not in pkg:
            return None, "No 'postcss' key in package.json", config_type
        postcss = pkg["postcss"]
        if not isinstance(postcss, dict):
            return None, "package.json#postcss must be an object", config_type
        return postcss, None, config_type

    # JSON config (.postcssrc, .postcssrc.json)
    try:
        config = json.loads(text)
    except json.JSONDecodeError as e:
        return None, f"Invalid JSON syntax: {e}", config_type

    if not isinstance(config, dict):
        return None, "PostCSS config must be a JSON object", config_type

    return config, None, config_type


def find_sibling_configs(filepath):
    """Find other PostCSS config files in the same directory."""
    directory = Path(filepath).parent
    siblings = []
    all_names = list(ALL_CONFIG_NAMES)
    for name in all_names:
        p = directory / name
        if p.exists() and str(p.resolve()) != str(Path(filepath).resolve()):
            siblings.append(name)
    # Check package.json#postcss
    pkg = directory / "package.json"
    if pkg.exists() and Path(filepath).name != "package.json":
        try:
            d = json.loads(pkg.read_text(encoding="utf-8"))
            if "postcss" in d:
                siblings.append("package.json#postcss")
        except Exception:
            pass
    return siblings


def get_plugin_name(entry):
    """Extract plugin name from various plugin formats: string, [name, opts], key in dict."""
    if isinstance(entry, str):
        return entry
    if isinstance(entry, list) and len(entry) > 0:
        return str(entry[0])
    return ""


def get_plugins_list(config):
    """Extract a normalized list of plugin names from config.plugins (object or array)."""
    plugins = config.get("plugins")
    if plugins is None:
        return []
    if isinstance(plugins, dict):
        return list(plugins.keys())
    if isinstance(plugins, list):
        return [get_plugin_name(p) for p in plugins]
    return []


def get_plugins_ordered(config):
    """Get ordered list of (index, name) for ordering checks."""
    plugins = config.get("plugins")
    if plugins is None:
        return []
    if isinstance(plugins, dict):
        return list(enumerate(plugins.keys()))
    if isinstance(plugins, list):
        return [(i, get_plugin_name(p)) for i, p in enumerate(plugins)]
    return []


# --- Rule checks ---

def check_structure(config, filepath, config_type):
    """Rules S4: unknown top-level keys."""
    findings = []
    unknown = set(config.keys()) - VALID_TOP_KEYS
    if unknown:
        findings.append(Finding("S4", "warning",
            f"Unknown top-level keys: {', '.join(sorted(unknown))}",
            f"Valid keys: {', '.join(sorted(VALID_TOP_KEYS))}"))
    return findings


def check_plugins(config):
    """Rules P1-P6: plugin issues."""
    findings = []
    plugins_raw = config.get("plugins")
    plugin_names = get_plugins_list(config)

    # P1: empty plugins
    if plugins_raw is not None:
        is_empty = False
        if isinstance(plugins_raw, dict) and len(plugins_raw) == 0:
            is_empty = True
        elif isinstance(plugins_raw, list) and len(plugins_raw) == 0:
            is_empty = True
        if is_empty:
            findings.append(Finding("P1", "warning",
                "Empty plugins object/array",
                "Plugins section exists but contains no plugins"))

    # P2: deprecated plugins
    for pn in plugin_names:
        if pn in DEPRECATED_PLUGINS:
            findings.append(Finding("P2", "warning",
                f"Deprecated plugin: {pn}",
                DEPRECATED_PLUGINS[pn]))

    # P3: duplicate plugins
    seen = {}
    for pn in plugin_names:
        if pn:
            if pn in seen:
                findings.append(Finding("P3", "warning",
                    f"Duplicate plugin: {pn}"))
            seen[pn] = True

    # Ordering checks (P4, P5) — need indexed list
    ordered = get_plugins_ordered(config)
    name_index = {name: idx for idx, name in ordered}

    # P4: autoprefixer should be after postcss-preset-env
    if "autoprefixer" in name_index and "postcss-preset-env" in name_index:
        if name_index["autoprefixer"] < name_index["postcss-preset-env"]:
            findings.append(Finding("P4", "info",
                "autoprefixer is before postcss-preset-env",
                "autoprefixer should run after postcss-preset-env for best results"))

    # P4 also: cssnano should be last
    if "cssnano" in name_index:
        cssnano_idx = name_index["cssnano"]
        max_idx = max(idx for idx, _ in ordered) if ordered else 0
        if cssnano_idx < max_idx:
            findings.append(Finding("P4", "info",
                "cssnano is not the last plugin",
                "cssnano (minifier) should be the last plugin in the chain"))

    # P5: postcss-import should be first
    if "postcss-import" in name_index:
        if name_index["postcss-import"] != 0:
            findings.append(Finding("P5", "info",
                "postcss-import is not the first plugin",
                "postcss-import must be first so that @import statements are resolved before other transforms"))

    # P6: unknown/uncommon plugin names
    for pn in plugin_names:
        if pn and pn not in TOP_PLUGINS and pn not in DEPRECATED_PLUGINS:
            # Only flag if it looks like a real package name (not a local path)
            if not pn.startswith("./") and not pn.startswith("../") and not pn.startswith("/"):
                findings.append(Finding("P6", "info",
                    f"Uncommon plugin: {pn}",
                    "Not in top 50 PostCSS plugins list — verify the name is correct"))

    return findings


def check_tailwind(config):
    """Rules T1-T3: Tailwind integration."""
    findings = []
    plugin_names = set(get_plugins_list(config))

    if "tailwindcss" not in plugin_names:
        return findings

    # T1: tailwindcss without nesting plugin
    has_nesting = ("@tailwindcss/nesting" in plugin_names or
                   "postcss-nesting" in plugin_names or
                   "postcss-nested" in plugin_names)
    if not has_nesting:
        findings.append(Finding("T1", "info",
            "tailwindcss without a nesting plugin",
            "If you use CSS nesting, add @tailwindcss/nesting or postcss-nesting before tailwindcss"))

    # T2: tailwindcss after autoprefixer (wrong order)
    ordered = get_plugins_ordered(config)
    name_index = {name: idx for idx, name in ordered}
    if "autoprefixer" in name_index and "tailwindcss" in name_index:
        if name_index["tailwindcss"] > name_index["autoprefixer"]:
            findings.append(Finding("T2", "warning",
                "tailwindcss is after autoprefixer",
                "tailwindcss should come before autoprefixer in the plugin chain"))

    # T3: postcss-preset-env with tailwindcss
    if "postcss-preset-env" in plugin_names:
        findings.append(Finding("T3", "info",
            "postcss-preset-env used alongside tailwindcss",
            "Tailwind handles most modern CSS features; postcss-preset-env may conflict or be redundant"))

    return findings


def check_syntax_parser(config):
    """Rules X1-X3: parser/syntax issues."""
    findings = []
    parser = config.get("parser")
    syntax = config.get("syntax")

    # X1: both parser and syntax
    if parser and syntax:
        findings.append(Finding("X1", "warning",
            "Both 'parser' and 'syntax' are set",
            "Only one should be specified — 'syntax' sets both parser and stringifier, 'parser' sets only the parser"))

    # X2: unknown parser
    if parser and isinstance(parser, str) and parser not in KNOWN_PARSERS:
        findings.append(Finding("X2", "info",
            f"Unknown parser: {parser}",
            f"Known parsers: {', '.join(sorted(KNOWN_PARSERS))}"))

    # X3: parser set but no matching preprocessor plugin
    if parser and isinstance(parser, str):
        plugin_names = set(get_plugins_list(config))
        preprocessor_indicators = {
            "postcss-scss": {"postcss-scss", "@csstools/postcss-sass"},
            "postcss-less": {"postcss-less", "less"},
            "postcss-html": {"postcss-html"},
            "sugarss": {"sugarss"},
            "postcss-styl": {"postcss-styl"},
        }
        expected = preprocessor_indicators.get(parser, set())
        # If parser is known and there are expected companion plugins, check
        if expected and not (expected & plugin_names):
            findings.append(Finding("X3", "info",
                f"Parser '{parser}' set but no related preprocessor plugin found",
                "This may be intentional, but verify the parser matches your file types"))

    return findings


def check_source_maps(config):
    """Rules M1-M2: source map settings."""
    findings = []
    map_val = config.get("map")

    if map_val is False:
        findings.append(Finding("M1", "info",
            "Source maps disabled (map: false)",
            "Consider enabling source maps in development for easier debugging"))

    if isinstance(map_val, dict):
        if map_val.get("inline") is True:
            findings.append(Finding("M2", "info",
                "Inline source maps enabled (map.inline: true)",
                "Inline source maps increase file size — consider external maps for production"))

    return findings


def check_best_practices(config):
    """Rules B1-B3: best practices."""
    findings = []
    plugins_raw = config.get("plugins")
    plugin_names = get_plugins_list(config)

    # B1: no plugins configured at all
    if plugins_raw is None:
        findings.append(Finding("B1", "warning",
            "No 'plugins' key in config",
            "A PostCSS config without plugins does nothing — add at least autoprefixer"))

    # B2: postcss-preset-env AND individual feature plugins it includes
    if "postcss-preset-env" in plugin_names:
        redundant = [pn for pn in plugin_names if pn in PRESET_ENV_INCLUDED_PLUGINS]
        if redundant:
            findings.append(Finding("B2", "info",
                f"Plugins redundant with postcss-preset-env: {', '.join(redundant)}",
                "postcss-preset-env already includes these features"))

    # B3: very large number of plugins
    if len(plugin_names) > 15:
        findings.append(Finding("B3", "info",
            f"Large number of plugins ({len(plugin_names)})",
            "More than 15 plugins may impact build performance — consider consolidating"))

    return findings


# --- Orchestrators ---

def validate_all(config, filepath, config_type):
    """Run all checks and return combined findings."""
    findings = []
    findings.extend(check_structure(config, filepath, config_type))
    findings.extend(check_plugins(config))
    findings.extend(check_tailwind(config))
    findings.extend(check_syntax_parser(config))
    findings.extend(check_source_maps(config))
    findings.extend(check_best_practices(config))
    return findings


def check_structure_only(config, filepath, config_type):
    """Run structure checks only (for 'check' command)."""
    return check_structure(config, filepath, config_type)


# --- Output formatting ---

def format_text(findings, filepath):
    if not findings:
        return f"✅ {filepath}: No issues found"
    lines = [f"\U0001f4cb {filepath}: {len(findings)} issue(s) found\n"]
    for f in findings:
        lines.append(f.to_text())
    errors = sum(1 for f in findings if f.severity == "error")
    warnings = sum(1 for f in findings if f.severity == "warning")
    infos = sum(1 for f in findings if f.severity == "info")
    if errors:
        icon = "❌"
    elif warnings:
        icon = "⚠️"
    else:
        icon = "ℹ️"
    lines.append(f"\n{icon} {errors} error(s), {warnings} warning(s), {infos} info(s)")
    return "\n".join(lines)


def format_json(findings, filepath):
    return json.dumps({
        "file": filepath,
        "findings": [f.to_dict() for f in findings],
        "summary": {
            "errors": sum(1 for f in findings if f.severity == "error"),
            "warnings": sum(1 for f in findings if f.severity == "warning"),
            "infos": sum(1 for f in findings if f.severity == "info"),
            "total": len(findings),
        }
    }, indent=2)


def format_summary(findings, filepath):
    errors = sum(1 for f in findings if f.severity == "error")
    warnings = sum(1 for f in findings if f.severity == "warning")
    infos = sum(1 for f in findings if f.severity == "info")
    status = "FAIL" if errors else ("WARN" if warnings else "PASS")
    return f"{status} | {filepath} | {errors} errors, {warnings} warnings, {infos} infos"


def format_output(findings, filepath, fmt):
    if fmt == "json":
        return format_json(findings, filepath)
    elif fmt == "summary":
        return format_summary(findings, filepath)
    else:
        return format_text(findings, filepath)


# --- explain / suggest commands ---

def explain_config(config, filepath, config_type):
    lines = [f"\U0001f4d6 PostCSS Config Explanation: {filepath}\n"]

    if config_type == "package_json":
        lines.append("Source: package.json#postcss\n")

    parser = config.get("parser")
    if parser:
        lines.append(f"Parser: {parser}")
        if parser in KNOWN_PARSERS:
            parser_desc = {
                "postcss-scss": "SCSS syntax (allows SCSS-style comments, variables, etc.)",
                "postcss-less": "Less syntax support",
                "postcss-html": "Parse CSS inside HTML/Vue/Svelte files",
                "sugarss": "Indent-based CSS syntax (like Sass without braces)",
                "postcss-styl": "Stylus syntax support",
            }
            lines.append(f"  {parser_desc.get(parser, '')}")

    syntax = config.get("syntax")
    if syntax:
        lines.append(f"Syntax: {syntax} (sets both parser and stringifier)")

    stringifier = config.get("stringifier")
    if stringifier:
        lines.append(f"Stringifier: {stringifier}")

    map_val = config.get("map")
    if map_val is not None:
        if map_val is False:
            lines.append("\nSource maps: Disabled")
        elif map_val is True:
            lines.append("\nSource maps: Enabled (default external)")
        elif isinstance(map_val, dict):
            inline = "inline" if map_val.get("inline") else "external"
            lines.append(f"\nSource maps: Enabled ({inline})")

    plugin_names = get_plugins_list(config)
    if plugin_names:
        lines.append(f"\nPlugins ({len(plugin_names)}, applied in order):")
        for pn in plugin_names:
            desc = ""
            if pn == "autoprefixer":
                desc = " - adds vendor prefixes"
            elif pn == "postcss-preset-env":
                desc = " - modern CSS features with polyfills"
            elif pn == "postcss-import":
                desc = " - resolves @import statements"
            elif pn == "postcss-nested" or pn == "postcss-nesting":
                desc = " - CSS nesting support"
            elif pn == "cssnano":
                desc = " - CSS minification"
            elif pn == "tailwindcss":
                desc = " - Tailwind CSS utility framework"
            elif pn == "@tailwindcss/nesting":
                desc = " - Tailwind-compatible nesting"
            elif pn == "postcss-mixins":
                desc = " - Sass-like mixins"
            elif pn == "postcss-simple-vars":
                desc = " - Sass-like variables"
            lines.append(f"  {pn}{desc}")
    else:
        lines.append("\nNo plugins configured.")

    from_val = config.get("from")
    to_val = config.get("to")
    if from_val:
        lines.append(f"\nInput: {from_val}")
    if to_val:
        lines.append(f"Output: {to_val}")

    return "\n".join(lines)


def suggest_improvements(config, filepath):
    lines = [f"\U0001f4a1 Suggestions for {filepath}\n"]
    suggestions = []
    plugin_names = set(get_plugins_list(config))

    # No plugins at all
    if not plugin_names:
        suggestions.append("Add plugins to your PostCSS config — without them it does nothing. Start with 'autoprefixer'.")

    # Missing autoprefixer
    if plugin_names and "autoprefixer" not in plugin_names:
        suggestions.append("Add 'autoprefixer' — it's the most common PostCSS plugin and handles vendor prefixes automatically")

    # Using deprecated plugins
    for pn in plugin_names:
        if pn in DEPRECATED_PLUGINS:
            suggestions.append(f"Replace '{pn}': {DEPRECATED_PLUGINS[pn]}")

    # postcss-cssnext -> postcss-preset-env
    if "postcss-cssnext" in plugin_names and "postcss-preset-env" not in plugin_names:
        suggestions.append("Replace 'postcss-cssnext' with 'postcss-preset-env' (actively maintained successor)")

    # Consider postcss-preset-env
    individual_features = plugin_names & PRESET_ENV_INCLUDED_PLUGINS
    if individual_features and "postcss-preset-env" not in plugin_names:
        suggestions.append(
            f"Consider using 'postcss-preset-env' instead of individual plugins: {', '.join(sorted(individual_features))}")

    # Tailwind without nesting
    if "tailwindcss" in plugin_names:
        has_nesting = ("@tailwindcss/nesting" in plugin_names or
                       "postcss-nesting" in plugin_names)
        if not has_nesting:
            suggestions.append("Add '@tailwindcss/nesting' before 'tailwindcss' if you use CSS nesting")

    # postcss-import missing when using other plugins
    if plugin_names and "postcss-import" not in plugin_names and len(plugin_names) > 2:
        suggestions.append("Consider adding 'postcss-import' to resolve @import statements before other transforms")

    # Source maps not configured
    if "map" not in config:
        suggestions.append("Consider setting 'map' for source map generation (helps debugging)")

    if not suggestions:
        lines.append("No suggestions — config looks good!")
    else:
        for s in suggestions:
            lines.append(f"  • {s}")

    return "\n".join(lines)


# --- CLI ---

def main():
    if len(sys.argv) < 3:
        print("Usage: postcss_config_validator.py <command> <file> [--format text|json|summary] [--strict]")
        print("Commands: validate, check, explain, suggest")
        sys.exit(2)

    command = sys.argv[1]
    filepath = sys.argv[2]
    fmt = "text"
    strict = False
    i = 3
    while i < len(sys.argv):
        if sys.argv[i] == "--format" and i + 1 < len(sys.argv):
            fmt = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--strict":
            strict = True
            i += 1
        else:
            i += 1

    if command not in ("validate", "check", "explain", "suggest"):
        print(f"❌ Unknown command: {command}")
        print("Valid commands: validate, check, explain, suggest")
        sys.exit(2)

    config, error, config_type = load_config(filepath)

    # Handle load errors
    if error:
        # S5: JS/TS config detected
        if error == "JS_TS_DETECTED":
            finding = Finding("S5", "info",
                f"JS/TS config detected: {Path(filepath).name}",
                "JavaScript/TypeScript configs cannot be statically validated — export your config as .postcssrc.json for validation")
            if command in ("validate", "check"):
                print(format_output([finding], filepath, fmt))
                sys.exit(0)
            else:
                print(finding.to_text())
                sys.exit(0)

        # S1: file not found / unreadable
        if "not found" in error or "Cannot read" in error:
            finding = Finding("S1", "error", error)
            if command in ("validate", "check"):
                print(format_output([finding], filepath, fmt))
            else:
                print(finding.to_text())
            sys.exit(2)

        # S2: empty config
        if "empty" in error.lower():
            finding = Finding("S2", "error", error)
            if command in ("validate", "check"):
                print(format_output([finding], filepath, fmt))
            else:
                print(finding.to_text())
            sys.exit(1)

        # S3: invalid JSON
        if "Invalid JSON" in error:
            finding = Finding("S3", "error", error)
            if command in ("validate", "check"):
                print(format_output([finding], filepath, fmt))
            else:
                print(finding.to_text())
            sys.exit(1)

        # Any other load error
        finding = Finding("S1", "error", error)
        if command in ("validate", "check"):
            print(format_output([finding], filepath, fmt))
        else:
            print(finding.to_text())
        sys.exit(1)

    # Config loaded successfully
    if command == "explain":
        print(explain_config(config, filepath, config_type))
        sys.exit(0)

    if command == "suggest":
        print(suggest_improvements(config, filepath))
        sys.exit(0)

    # validate or check
    if command == "check":
        findings = check_structure_only(config, filepath, config_type)
    else:
        findings = validate_all(config, filepath, config_type)

    # --strict: promote warnings and infos to errors
    if strict:
        for f in findings:
            if f.severity in ("warning", "info"):
                f.severity = "error"

    print(format_output(findings, filepath, fmt))

    errors = sum(1 for f in findings if f.severity == "error")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
