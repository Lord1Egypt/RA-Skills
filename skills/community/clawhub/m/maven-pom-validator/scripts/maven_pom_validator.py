#!/usr/bin/env python3
"""
Maven POM Validator — lint, validate, and audit Maven pom.xml files.
Pure Python stdlib only.
"""

import argparse
import json
import re
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

MAVEN_NS = "http://maven.apache.org/POM/4.0.0"

VALID_PACKAGING = {"jar", "war", "pom", "ear", "rar", "maven-plugin", "ejb", "par"}
VALID_SCOPES = {"compile", "test", "provided", "runtime", "system", "import"}
DEPRECATED_PLUGINS = {
    "maven-eclipse-plugin": "Use IDE-native Maven support instead",
    "maven-idea-plugin": "Use IDE-native Maven support instead",
    "build-helper-maven-plugin": "Consider standard Maven lifecycle instead",
    "exec-maven-plugin": "Prefer build-time alternatives for portability",
}
WILDCARD_VERSION_PATTERNS = re.compile(
    r"^(LATEST|RELEASE|\[.*\]|\(.*\)|.*,.*)", re.IGNORECASE
)

LEVEL_ERROR = "ERROR"
LEVEL_WARN = "WARN"
LEVEL_INFO = "INFO"


# ---------------------------------------------------------------------------
# Finding dataclass (plain dict for stdlib compat)
# ---------------------------------------------------------------------------

def finding(level: str, rule: str, message: str, location: str = "") -> dict:
    return {"level": level, "rule": rule, "message": message, "location": location}


# ---------------------------------------------------------------------------
# XML helpers
# ---------------------------------------------------------------------------

def _tag(local: str) -> str:
    """Return qualified tag name, trying namespaced first."""
    return local  # we strip ns in parse


def parse_pom(path: str):
    """Parse pom.xml, stripping namespace for easy access. Returns (root, findings)."""
    findings = []
    try:
        tree = ET.parse(path)
        root = tree.getroot()
    except ET.ParseError as e:
        findings.append(finding(LEVEL_ERROR, "valid-xml", f"XML parse error: {e}"))
        return None, findings
    except FileNotFoundError:
        findings.append(finding(LEVEL_ERROR, "file-not-found", f"File not found: {path}"))
        return None, findings

    # Strip namespace prefixes so we can use simple tag names
    for elem in root.iter():
        if "}" in elem.tag:
            elem.tag = elem.tag.split("}", 1)[1]

    return root, findings


def find_text(root, *path) -> str:
    """Navigate path and return stripped text or ''."""
    node = root
    for step in path:
        if node is None:
            return ""
        node = node.find(step)
    if node is None or node.text is None:
        return ""
    return node.text.strip()


def find_all(root, *path):
    """Navigate all but last step, then findall last step."""
    node = root
    for step in path[:-1]:
        if node is None:
            return []
        node = node.find(step)
    if node is None:
        return []
    return node.findall(path[-1])


# ---------------------------------------------------------------------------
# Rule checkers
# ---------------------------------------------------------------------------

def check_structure(root) -> list:
    findings = []

    # Rule 2: required elements
    for elem in ("groupId", "artifactId", "version", "modelVersion"):
        val = find_text(root, elem)
        if not val:
            findings.append(finding(
                LEVEL_ERROR, "required-elements",
                f"Missing required element <{elem}>",
                f"<{elem}>"
            ))

    # Rule 3: modelVersion = 4.0.0
    mv = find_text(root, "modelVersion")
    if mv and mv != "4.0.0":
        findings.append(finding(
            LEVEL_ERROR, "model-version",
            f"<modelVersion> should be '4.0.0', got '{mv}'",
            "<modelVersion>"
        ))

    # Rule 4: groupId format (reverse domain, at least one dot or simple lowercase)
    group_id = find_text(root, "groupId")
    if group_id:
        if not re.match(r"^[a-z][a-z0-9_\-]*(\.[a-z][a-z0-9_\-]*)+$", group_id):
            findings.append(finding(
                LEVEL_WARN, "groupid-format",
                f"groupId '{group_id}' does not follow reverse-domain convention (e.g. com.example)",
                "<groupId>"
            ))

    # Rule 5: packaging
    packaging = find_text(root, "packaging")
    if packaging and packaging not in VALID_PACKAGING:
        findings.append(finding(
            LEVEL_WARN, "packaging-value",
            f"packaging '{packaging}' is not a standard value ({', '.join(sorted(VALID_PACKAGING))})",
            "<packaging>"
        ))

    return findings


def _iter_dependencies(root):
    """Yield (dep_element, in_management) for all dependencies."""
    # Direct dependencies
    for dep in find_all(root, "dependencies", "dependency"):
        yield dep, False
    # dependencyManagement
    for dep in find_all(root, "dependencyManagement", "dependencies", "dependency"):
        yield dep, True


def check_dependencies(root) -> list:
    findings = []
    version_text = find_text(root, "version")
    is_snapshot_project = version_text.endswith("-SNAPSHOT") if version_text else False

    seen = {}
    for dep, in_mgmt in _iter_dependencies(root):
        g = find_text(dep, "groupId")
        a = find_text(dep, "artifactId")
        v = find_text(dep, "version")
        scope = find_text(dep, "scope") or "compile"
        system_path = find_text(dep, "systemPath")
        loc = f"{g}:{a}"

        # Rule 6: no duplicates
        key = (g, a, in_mgmt)
        if key in seen:
            findings.append(finding(
                LEVEL_ERROR, "duplicate-dependency",
                f"Duplicate dependency: {loc}",
                loc
            ))
        else:
            seen[key] = True

        # Rule 7: no SNAPSHOT in release
        if v and v.endswith("-SNAPSHOT") and not is_snapshot_project:
            findings.append(finding(
                LEVEL_WARN, "snapshot-in-release",
                f"SNAPSHOT dependency '{v}' in non-SNAPSHOT project: {loc}",
                loc
            ))

        # Rule 8: version defined (skip if in dependencyManagement — allowed to inherit)
        if not in_mgmt and not v:
            findings.append(finding(
                LEVEL_WARN, "missing-version",
                f"No version specified for dependency: {loc} (should be managed or explicit)",
                loc
            ))

        # Rule 9: no wildcard versions
        if v and WILDCARD_VERSION_PATTERNS.match(v):
            findings.append(finding(
                LEVEL_ERROR, "wildcard-version",
                f"Wildcard/dynamic version '{v}' in dependency: {loc}",
                loc
            ))

        # Rule 10: valid scope
        if scope and scope not in VALID_SCOPES:
            findings.append(finding(
                LEVEL_ERROR, "invalid-scope",
                f"Invalid scope '{scope}' for dependency: {loc}",
                loc
            ))

        # Rule 11: system scope needs systemPath
        if scope == "system" and not system_path:
            findings.append(finding(
                LEVEL_ERROR, "system-scope-path",
                f"system-scoped dependency {loc} must have <systemPath>",
                loc
            ))

    return findings


def _iter_plugins(root):
    """Yield plugin elements from both build/plugins and build/pluginManagement."""
    for plugin in find_all(root, "build", "plugins", "plugin"):
        yield plugin, False
    for plugin in find_all(root, "build", "pluginManagement", "plugins", "plugin"):
        yield plugin, True
    # reporting plugins
    for plugin in find_all(root, "reporting", "plugins", "plugin"):
        yield plugin, False


def check_plugins(root) -> list:
    findings = []
    seen = {}

    for plugin, in_mgmt in _iter_plugins(root):
        g = find_text(plugin, "groupId") or "org.apache.maven.plugins"
        a = find_text(plugin, "artifactId")
        v = find_text(plugin, "version")
        loc = f"{g}:{a}"

        # Rule 12: version pinned
        if not in_mgmt and not v:
            findings.append(finding(
                LEVEL_WARN, "plugin-version-unpinned",
                f"Plugin version not pinned: {loc}",
                loc
            ))

        # Rule 13: no duplicate plugins
        key = (g, a, in_mgmt)
        if key in seen:
            findings.append(finding(
                LEVEL_ERROR, "duplicate-plugin",
                f"Duplicate plugin: {loc}",
                loc
            ))
        else:
            seen[key] = True

        # Rule 14: groupId specified
        if not find_text(plugin, "groupId"):
            findings.append(finding(
                LEVEL_INFO, "plugin-groupid-missing",
                f"Plugin {a} has no explicit <groupId> (defaulting to org.apache.maven.plugins)",
                loc
            ))

        # Rule 15: deprecated plugins
        if a in DEPRECATED_PLUGINS:
            findings.append(finding(
                LEVEL_WARN, "deprecated-plugin",
                f"Deprecated plugin {a}: {DEPRECATED_PLUGINS[a]}",
                loc
            ))

        # Rule 16: configuration — check for suspicious patterns
        config = plugin.find("configuration")
        if config is not None:
            config_text = ET.tostring(config, encoding="unicode")
            if re.search(r"[A-Za-z]:\\\\|/home/|/root/|/Users/", config_text):
                findings.append(finding(
                    LEVEL_WARN, "hardcoded-path-in-plugin",
                    f"Possible hardcoded absolute path in plugin configuration: {loc}",
                    loc
                ))

    return findings


def check_best_practices(root) -> list:
    findings = []
    _props_elem = root.find("properties")
    properties = _props_elem if _props_elem is not None else ET.Element("properties")
    props = {child.tag: (child.text or "").strip() for child in properties}

    # Rule 17: properties for version management
    # Count how many dependency versions are hardcoded vs. using ${...}
    hardcoded_versions = []
    for dep, _ in _iter_dependencies(root):
        v = find_text(dep, "version")
        g = find_text(dep, "groupId")
        a = find_text(dep, "artifactId")
        if v and not v.startswith("${") and not v.endswith("-SNAPSHOT") and len(v) > 0:
            hardcoded_versions.append(f"{g}:{a}:{v}")
    if len(hardcoded_versions) >= 3:
        findings.append(finding(
            LEVEL_INFO, "use-properties-for-versions",
            f"{len(hardcoded_versions)} dependencies use hardcoded versions; "
            f"consider extracting to <properties> (e.g. <spring.version>)",
            "<dependencies>"
        ))

    # Rule 18: dependencyManagement in parent POMs
    packaging = find_text(root, "packaging")
    if packaging == "pom":
        dm = root.find("dependencyManagement")
        if dm is None:
            findings.append(finding(
                LEVEL_WARN, "dependency-management-missing",
                "Parent POM (packaging=pom) should declare <dependencyManagement>",
                "<dependencyManagement>"
            ))

    # Rule 19: UTF-8 encoding
    encoding_prop = props.get("project.build.sourceEncoding", "")
    if not encoding_prop:
        findings.append(finding(
            LEVEL_WARN, "encoding-not-set",
            "project.build.sourceEncoding not set in <properties>; add <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>",
            "<properties>"
        ))

    # Rule 20: Java source/target
    has_source = any(k in props for k in (
        "maven.compiler.source", "maven.compiler.release", "java.version"
    ))
    if not has_source:
        # also check compiler plugin config
        for plugin, _ in _iter_plugins(root):
            a = find_text(plugin, "artifactId")
            if a == "maven-compiler-plugin":
                config = plugin.find("configuration")
                if config is not None:
                    if config.find("source") is not None or config.find("release") is not None:
                        has_source = True
                        break
    if not has_source:
        findings.append(finding(
            LEVEL_WARN, "java-version-not-set",
            "Java source/target version not set; add <maven.compiler.source> or <maven.compiler.release> to <properties>",
            "<properties>"
        ))

    # Rule 21: no hardcoded paths in build config
    build = root.find("build")
    if build is not None:
        build_text = ET.tostring(build, encoding="unicode")
        # Check for OS-specific or user-specific paths but skip ${...} expressions
        path_matches = re.findall(r"(?<!\$\{)[A-Za-z]:\\\\[^<]+|(?<!\$\{)/(?:home|root|Users|opt|usr)/[^<]+", build_text)
        for match in path_matches:
            findings.append(finding(
                LEVEL_WARN, "hardcoded-path",
                f"Hardcoded absolute path in <build>: {match.strip()}",
                "<build>"
            ))

    # Rule 22: SCM section
    scm = root.find("scm")
    if scm is None:
        findings.append(finding(
            LEVEL_INFO, "scm-missing",
            "No <scm> section found; recommended for release management and CI traceability",
            "<scm>"
        ))

    return findings


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_validate(pom_path: str, strict: bool) -> tuple:
    """Quick structural validation."""
    root, parse_findings = parse_pom(pom_path)
    if root is None:
        return parse_findings, bool(parse_findings)

    findings = parse_findings + check_structure(root)
    has_errors = any(f["level"] == LEVEL_ERROR for f in findings)
    has_warnings = any(f["level"] == LEVEL_WARN for f in findings)
    failed = has_errors or (strict and has_warnings)
    return findings, failed


def cmd_dependencies(pom_path: str, strict: bool) -> tuple:
    root, parse_findings = parse_pom(pom_path)
    if root is None:
        return parse_findings, True

    findings = parse_findings + check_dependencies(root)
    has_errors = any(f["level"] == LEVEL_ERROR for f in findings)
    has_warnings = any(f["level"] == LEVEL_WARN for f in findings)
    failed = has_errors or (strict and has_warnings)
    return findings, failed


def cmd_plugins(pom_path: str, strict: bool) -> tuple:
    root, parse_findings = parse_pom(pom_path)
    if root is None:
        return parse_findings, True

    findings = parse_findings + check_plugins(root)
    has_errors = any(f["level"] == LEVEL_ERROR for f in findings)
    has_warnings = any(f["level"] == LEVEL_WARN for f in findings)
    failed = has_errors or (strict and has_warnings)
    return findings, failed


def cmd_lint(pom_path: str, strict: bool) -> tuple:
    """Full lint: all rule groups."""
    root, parse_findings = parse_pom(pom_path)
    if root is None:
        return parse_findings, True

    findings = (
        parse_findings
        + check_structure(root)
        + check_dependencies(root)
        + check_plugins(root)
        + check_best_practices(root)
    )
    has_errors = any(f["level"] == LEVEL_ERROR for f in findings)
    has_warnings = any(f["level"] == LEVEL_WARN for f in findings)
    failed = has_errors or (strict and has_warnings)
    return findings, failed


# ---------------------------------------------------------------------------
# Output formatters
# ---------------------------------------------------------------------------

LEVEL_ICON = {LEVEL_ERROR: "[ERROR]", LEVEL_WARN: "[WARN] ", LEVEL_INFO: "[INFO] "}


def format_text(findings: list, pom_path: str, failed: bool) -> str:
    lines = [f"Maven POM Validator — {pom_path}", ""]
    if not findings:
        lines.append("No issues found.")
    else:
        errors = [f for f in findings if f["level"] == LEVEL_ERROR]
        warnings = [f for f in findings if f["level"] == LEVEL_WARN]
        infos = [f for f in findings if f["level"] == LEVEL_INFO]
        for group in (errors, warnings, infos):
            for f in group:
                icon = LEVEL_ICON.get(f["level"], "       ")
                loc = f"  ({f['location']})" if f["location"] else ""
                lines.append(f"  {icon} [{f['rule']}] {f['message']}{loc}")
        lines.append("")
        lines.append(
            f"Summary: {len(errors)} error(s), {len(warnings)} warning(s), {len(infos)} info(s)"
        )
    lines.append("")
    lines.append("Result: FAIL" if failed else "Result: PASS")
    return "\n".join(lines)


def format_json(findings: list, pom_path: str, failed: bool) -> str:
    output = {
        "file": pom_path,
        "result": "FAIL" if failed else "PASS",
        "summary": {
            "errors": sum(1 for f in findings if f["level"] == LEVEL_ERROR),
            "warnings": sum(1 for f in findings if f["level"] == LEVEL_WARN),
            "infos": sum(1 for f in findings if f["level"] == LEVEL_INFO),
        },
        "findings": findings,
    }
    return json.dumps(output, indent=2)


def format_markdown(findings: list, pom_path: str, failed: bool) -> str:
    lines = [f"# Maven POM Validator Report", "", f"**File:** `{pom_path}`", ""]
    result_badge = "FAIL" if failed else "PASS"
    lines.append(f"**Result:** {result_badge}  ")

    errors = [f for f in findings if f["level"] == LEVEL_ERROR]
    warnings = [f for f in findings if f["level"] == LEVEL_WARN]
    infos = [f for f in findings if f["level"] == LEVEL_INFO]
    lines.append(
        f"**Summary:** {len(errors)} error(s) | {len(warnings)} warning(s) | {len(infos)} info(s)"
    )
    lines.append("")

    if not findings:
        lines.append("No issues found.")
        return "\n".join(lines)

    for level, group, heading in (
        (LEVEL_ERROR, errors, "Errors"),
        (LEVEL_WARN, warnings, "Warnings"),
        (LEVEL_INFO, infos, "Info"),
    ):
        if group:
            lines.append(f"## {heading}")
            lines.append("")
            for f in group:
                loc = f" — `{f['location']}`" if f["location"] else ""
                lines.append(f"- **[{f['rule']}]** {f['message']}{loc}")
            lines.append("")

    return "\n".join(lines)


FORMATTERS = {
    "text": format_text,
    "json": format_json,
    "markdown": format_markdown,
}


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Maven POM Validator — lint and validate pom.xml files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Commands:
  lint          Full lint pass (all 20+ rules)
  validate      Structural validation only
  dependencies  Dependency audit only
  plugins       Plugin audit only

Examples:
  python3 maven_pom_validator.py lint pom.xml
  python3 maven_pom_validator.py lint pom.xml --strict --format json
  python3 maven_pom_validator.py dependencies pom.xml --format markdown
  python3 maven_pom_validator.py validate pom.xml --strict
""",
    )
    parser.add_argument("command", choices=["lint", "validate", "dependencies", "plugins"])
    parser.add_argument("pom", help="Path to pom.xml file")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit 1 on warnings (CI mode)",
    )
    parser.add_argument(
        "--format",
        choices=["text", "json", "markdown"],
        default="text",
        help="Output format (default: text)",
    )

    args = parser.parse_args()

    commands = {
        "lint": cmd_lint,
        "validate": cmd_validate,
        "dependencies": cmd_dependencies,
        "plugins": cmd_plugins,
    }

    findings, failed = commands[args.command](args.pom, args.strict)
    formatter = FORMATTERS[args.format]
    print(formatter(findings, args.pom, failed))

    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
