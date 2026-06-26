#!/usr/bin/env python3

from __future__ import annotations

import argparse
import importlib.util
import pathlib
import sys
try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib
from dataclasses import dataclass


SCRIPT_DIR = pathlib.Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

VALIDATOR_PATH = SCRIPT_DIR / "validate-memory-frontmatter.py"
DEFAULT_MANIFEST_NAME = "memory-governor-host.toml"
from memory_governor.contract.capabilities import CAPABILITY_FAMILIES
from memory_governor.contract.diagnosis_registry import DIAGNOSIS_TYPES
from memory_governor.audit import (
    AuthorizationPolicy,
    CapabilityDeclaration,
    DiagnosisConfig,
    parse_capability_declaration,
    reconcile_capability_contract,
    render_summary,
)

MANIFEST_TARGETS = {
    "long_term_memory",
    "daily_memory",
    "learning_candidates",
    "reusable_lessons",
    "proactive_state",
    "working_buffer",
    "project_facts",
    "system_rules",
    "tool_rules",
}
STRUCTURED_TARGETS = {
    "learning_candidates",
    "reusable_lessons",
    "proactive_state",
    "working_buffer",
}


@dataclass
class CheckResult:
    level: str
    message: str


@dataclass
class WriterContractInspection:
    path: pathlib.Path
    families: list[str] | None
    results: list[CheckResult]


def load_validator():
    spec = importlib.util.spec_from_file_location("memory_validator", VALIDATOR_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load validator from {VALIDATOR_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


VALIDATOR = load_validator()


def rel(path: pathlib.Path, root: pathlib.Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def validate_structured_file(path: pathlib.Path) -> list[str]:
    return VALIDATOR.validate_file(path)


def load_manifest(path: pathlib.Path) -> dict:
    return tomllib.loads(path.read_text(encoding="utf-8"))


def resolve_manifest_path(root: pathlib.Path, raw_path: str) -> pathlib.Path:
    expanded = pathlib.Path(raw_path).expanduser()
    if expanded.is_absolute():
        return expanded
    return (root / expanded).resolve()


def validate_manifest_paths_array(entry: dict, field_name: str) -> tuple[list[str] | None, str | None]:
    value = entry.get(field_name)
    if value is None:
        return None, None
    if not isinstance(value, list) or not value or not all(isinstance(p, str) for p in value):
        return None, f"{field_name} must be a non-empty string array if present"
    return value, None


def check_optional_path_list(
    root: pathlib.Path,
    entry: dict,
    field_name: str,
    label: str,
) -> list[CheckResult]:
    results: list[CheckResult] = []
    values, error = validate_manifest_paths_array(entry, field_name)
    if error is not None:
        return [CheckResult("ERROR", f"integration: {error}")]
    if values is None:
        return results

    for raw_path in values:
        resolved = resolve_manifest_path(root, raw_path)
        if resolved.exists():
            results.append(CheckResult("OK", f"{label}: {rel(resolved, root)}"))
        else:
            results.append(CheckResult("ERROR", f"{label}: missing {rel(resolved, root)}"))
    return results


def read_text_if_exists(path: pathlib.Path) -> str | None:
    if not path.exists() or not path.is_file():
        return None
    return path.read_text(encoding="utf-8")


def check_host_entry_contract(root: pathlib.Path, path: pathlib.Path) -> CheckResult:
    text = read_text_if_exists(path)
    if text is None:
        return CheckResult("ERROR", f"integration host entry: missing {rel(path, root)}")

    lowered = text.lower()
    if "memory-governor" not in lowered:
        return CheckResult("ERROR", f"integration host entry: {rel(path, root)} does not mention memory-governor")

    return CheckResult("OK", f"integration host entry: {rel(path, root)}")


def inspect_writer_contract(root: pathlib.Path, path: pathlib.Path) -> WriterContractInspection:
    results: list[CheckResult] = []
    text = read_text_if_exists(path)
    if text is None:
        results.append(CheckResult("ERROR", f"integration writer contract: missing {rel(path, root)}"))
        return WriterContractInspection(path=path, families=None, results=results)

    lowered = text.lower()
    if "## memory contract" not in lowered:
        results.append(CheckResult("ERROR", f"integration writer contract: {rel(path, root)} missing '## Memory Contract'"))
        return WriterContractInspection(path=path, families=None, results=results)
    if "memory-governor" not in lowered:
        results.append(CheckResult("ERROR", f"integration writer contract: {rel(path, root)} does not mention memory-governor"))
        return WriterContractInspection(path=path, families=None, results=results)

    results.append(CheckResult("OK", f"integration writer contract: {rel(path, root)}"))

    families, error = parse_capability_declaration(text)
    if error is not None:
        results.append(CheckResult("ERROR", f"integration writer contract: {rel(path, root)} {error}"))
        return WriterContractInspection(path=path, families=None, results=results)

    if families is None:
        results.append(CheckResult("WARN", f"integration writer contract: {rel(path, root)} missing machine-readable capability declaration"))
        return WriterContractInspection(path=path, families=None, results=results)

    results.append(CheckResult("OK", f"integration writer capabilities: {rel(path, root)} -> {', '.join(families)}"))
    return WriterContractInspection(path=path, families=families, results=results)


def check_integration_paths(root: pathlib.Path, integration: dict) -> tuple[list[CheckResult], list[WriterContractInspection]]:
    results: list[CheckResult] = []
    writer_inspections: list[WriterContractInspection] = []

    host_entry_paths, host_entry_error = validate_manifest_paths_array(integration, "host_entry_paths")
    if host_entry_error is not None:
        results.append(CheckResult("ERROR", f"integration: {host_entry_error}"))
    elif host_entry_paths is not None:
        for raw_path in host_entry_paths:
            results.append(check_host_entry_contract(root, resolve_manifest_path(root, raw_path)))

    writer_contract_paths, writer_contract_error = validate_manifest_paths_array(integration, "writer_contract_paths")
    if writer_contract_error is not None:
        results.append(CheckResult("ERROR", f"integration: {writer_contract_error}"))
    elif writer_contract_paths is not None:
        for raw_path in writer_contract_paths:
            writer_inspections.append(inspect_writer_contract(root, resolve_manifest_path(root, raw_path)))

    return results, writer_inspections


def find_manifest(root: pathlib.Path) -> pathlib.Path | None:
    candidate = root / DEFAULT_MANIFEST_NAME
    if candidate.exists():
        return candidate
    return None


def detect_profile(root: pathlib.Path) -> str:
    if find_manifest(root):
        return "manifest"
    if (root / "HOST.md").exists() and (root / "memory").exists():
        return "generic"
    if (root / "AGENTS.md").exists() and (root / "memory").exists():
        return "openclaw"
    return "unknown"


def check_file_exists(root: pathlib.Path, path: pathlib.Path, label: str, required: bool = True) -> CheckResult:
    if path.exists():
        return CheckResult("OK", f"{label}: {rel(path, root)}")
    level = "ERROR" if required else "WARN"
    return CheckResult(level, f"{label}: missing {rel(path, root)}")


def check_structured(root: pathlib.Path, path: pathlib.Path, label: str, required: bool = True) -> list[CheckResult]:
    results: list[CheckResult] = []
    if not path.exists():
        level = "ERROR" if required else "WARN"
        results.append(CheckResult(level, f"{label}: missing {rel(path, root)}"))
        return results

    errors = validate_structured_file(path)
    if errors:
        for error in errors:
            results.append(CheckResult("ERROR", error))
        return results

    results.append(CheckResult("OK", f"{label}: {rel(path, root)} (schema-valid)"))
    return results


def check_manifest(root: pathlib.Path, manifest_path: pathlib.Path) -> list[CheckResult]:
    results: list[CheckResult] = []
    try:
        manifest = load_manifest(manifest_path)
    except Exception as exc:  # noqa: BLE001
        return [CheckResult("ERROR", f"manifest: failed to parse {rel(manifest_path, root)} ({exc})")]

    results.append(CheckResult("OK", f"manifest: {rel(manifest_path, root)}"))

    version = manifest.get("version")
    if not isinstance(version, str):
        results.append(CheckResult("ERROR", "manifest: missing string field version"))
    else:
        results.append(CheckResult("OK", f"manifest version: {version}"))

    profile = manifest.get("profile")
    if profile is not None and not isinstance(profile, str):
        results.append(CheckResult("ERROR", "manifest: profile must be a string if present"))
    elif isinstance(profile, str):
        results.append(CheckResult("OK", f"declared profile: {profile}"))

    integration = manifest.get("integration")
    if integration is not None:
        if not isinstance(integration, dict):
            results.append(CheckResult("ERROR", "manifest: [integration] must be a table if present"))
            writer_inspections: list[WriterContractInspection] = []
        else:
            integration_results, writer_inspections = check_integration_paths(root, integration)
            results.extend(integration_results)
    else:
        writer_inspections = []

    capabilities = manifest.get("capabilities")
    declared_families: list[str] = []
    if capabilities is not None:
        if not isinstance(capabilities, dict):
            results.append(CheckResult("ERROR", "manifest: [capabilities] must be a table if present"))
        else:
            raw_declared_families = capabilities.get("families")
            if raw_declared_families is not None:
                if not isinstance(raw_declared_families, list) or not all(isinstance(item, str) for item in raw_declared_families):
                    results.append(CheckResult("ERROR", "manifest capabilities: families must be a string array if present"))
                else:
                    declared_families = raw_declared_families
                    unknown_families = sorted(set(declared_families) - set(CAPABILITY_FAMILIES))
                    for family in unknown_families:
                        results.append(CheckResult("ERROR", f"manifest capabilities: unknown family {family!r}"))
                    if not unknown_families:
                        results.append(CheckResult("OK", f"manifest capabilities: {', '.join(declared_families)}"))

    authorization = manifest.get("authorization")
    allowed_capabilities: list[str] = []
    if authorization is not None:
        if not isinstance(authorization, dict):
            results.append(CheckResult("ERROR", "manifest: [authorization] must be a table if present"))
        else:
            raw_allowed_capabilities = authorization.get("allowed_capabilities")
            if raw_allowed_capabilities is not None:
                if not isinstance(raw_allowed_capabilities, list) or not all(isinstance(item, str) for item in raw_allowed_capabilities):
                    results.append(CheckResult("ERROR", "manifest authorization: allowed_capabilities must be a string array if present"))
                else:
                    allowed_capabilities = raw_allowed_capabilities
                    unknown_allowed = sorted(set(allowed_capabilities) - set(CAPABILITY_FAMILIES))
                    for family in unknown_allowed:
                        results.append(CheckResult("ERROR", f"manifest authorization: unknown capability {family!r}"))
                    if not unknown_allowed:
                        results.append(CheckResult("OK", f"manifest authorization: {', '.join(allowed_capabilities)}"))

    diagnosis = manifest.get("diagnosis")
    enabled_types: list[str] = []
    if diagnosis is not None:
        if not isinstance(diagnosis, dict):
            results.append(CheckResult("ERROR", "manifest: [diagnosis] must be a table if present"))
        else:
            raw_enabled_types = diagnosis.get("enabled_types")
            if raw_enabled_types is not None:
                if not isinstance(raw_enabled_types, list) or not all(isinstance(item, str) for item in raw_enabled_types):
                    results.append(CheckResult("ERROR", "manifest diagnosis: enabled_types must be a string array if present"))
                else:
                    enabled_types = raw_enabled_types
                    unknown_types = sorted(set(enabled_types) - set(DIAGNOSIS_TYPES))
                    for diagnosis_type in unknown_types:
                        results.append(CheckResult("ERROR", f"manifest diagnosis: unknown type {diagnosis_type!r}"))
                    if not unknown_types:
                        results.append(CheckResult("OK", f"manifest diagnosis types: {', '.join(enabled_types)}"))

    effective_declarations: list[CapabilityDeclaration] = []
    for inspection in writer_inspections:
        results.extend(inspection.results)
        if inspection.families:
            effective_declarations.append(
                CapabilityDeclaration(
                    families=inspection.families,
                    source_artifact=rel(inspection.path, root) + " [capabilities]",
                )
            )

    if declared_families:
        effective_declarations.append(
            CapabilityDeclaration(
                families=declared_families,
                source_artifact=rel(manifest_path, root) + " [capabilities]",
            )
        )

    if not effective_declarations and allowed_capabilities:
        effective_declarations.append(
            CapabilityDeclaration(
                families=[],
                source_artifact="missing skill capability declaration",
            )
        )

    for declaration in effective_declarations:
        diagnostics = reconcile_capability_contract(
            declaration,
            AuthorizationPolicy(
                allowed_capabilities=allowed_capabilities,
                source_artifact=rel(manifest_path, root) + " [authorization]",
            ),
            DiagnosisConfig(enabled_types=enabled_types),
        )
        for diagnostic in diagnostics:
            for line_number, line in enumerate(render_summary(diagnostic)):
                level = diagnostic.severity if line_number == 0 else "OK"
                results.append(CheckResult(level, f"diagnostic: {line}"))

    targets = manifest.get("targets")
    if not isinstance(targets, dict):
        results.append(CheckResult("ERROR", "manifest: missing [targets] table"))
        return results

    unknown_targets = sorted(set(targets.keys()) - MANIFEST_TARGETS)
    for target in unknown_targets:
        results.append(CheckResult("WARN", f"manifest target {target!r}: not part of current standard target classes"))

    for target_name in sorted(targets.keys()):
        entry = targets[target_name]
        if not isinstance(entry, dict):
            results.append(CheckResult("ERROR", f"{target_name}: manifest entry must be a table"))
            continue

        mode = entry.get("mode")
        if mode not in {"single", "split", "directory", "pattern"}:
            results.append(CheckResult("ERROR", f"{target_name}: mode must be one of [directory, pattern, single, split]"))
            continue

        paths = entry.get("paths")
        if not isinstance(paths, list) or not paths or not all(isinstance(p, str) for p in paths):
            results.append(CheckResult("ERROR", f"{target_name}: paths must be a non-empty string array"))
            continue

        fallback_paths, fallback_error = validate_manifest_paths_array(entry, "fallback_paths")
        if fallback_error is not None:
            results.append(CheckResult("ERROR", f"{target_name}: {fallback_error}"))
            continue

        if mode == "single" and len(paths) != 1:
            results.append(CheckResult("ERROR", f"{target_name}: single mode must declare exactly one path"))
            continue

        if mode == "split" and len(paths) < 2:
            results.append(CheckResult("ERROR", f"{target_name}: split mode must declare at least two paths"))
            continue

        structured = entry.get("structured", target_name in STRUCTURED_TARGETS)
        if not isinstance(structured, bool):
            results.append(CheckResult("ERROR", f"{target_name}: structured must be a boolean if present"))
            continue

        resolved_paths = [resolve_manifest_path(root, raw_path) for raw_path in paths]
        resolved_fallback_paths = (
            [resolve_manifest_path(root, raw_path) for raw_path in fallback_paths]
            if fallback_paths is not None
            else []
        )

        if mode in {"single", "split"}:
            primary_missing = [resolved for resolved in resolved_paths if not resolved.exists()]
            primary_ok = not primary_missing
            fallback_ok = False

            if primary_ok:
                for resolved_path in resolved_paths:
                    results.append(CheckResult("OK", f"{target_name}: {rel(resolved_path, root)}"))
            elif resolved_fallback_paths:
                fallback_missing = [resolved for resolved in resolved_fallback_paths if not resolved.exists()]
                if not fallback_missing:
                    fallback_ok = True
                    for resolved_path in resolved_fallback_paths:
                        results.append(CheckResult("OK", f"{target_name}: fallback {rel(resolved_path, root)}"))
                else:
                    for missing_path in primary_missing:
                        results.append(CheckResult("WARN", f"{target_name}: primary missing {rel(missing_path, root)}"))
                    for missing_path in fallback_missing:
                        results.append(CheckResult("ERROR", f"{target_name}: fallback missing {rel(missing_path, root)}"))
                    continue
            else:
                for missing_path in primary_missing:
                    results.append(CheckResult("ERROR", f"{target_name}: missing {rel(missing_path, root)}"))
                continue

            active_paths = resolved_paths if primary_ok else resolved_fallback_paths
        else:
            active_paths = resolved_paths

        if mode == "directory":
            directory = active_paths[0]
            if directory.exists() and directory.is_dir():
                results.append(CheckResult("OK", f"{target_name}: {rel(directory, root)}"))
            else:
                results.append(CheckResult("ERROR", f"{target_name}: missing directory {rel(directory, root)}"))
            continue

        if mode == "pattern":
            pattern = paths[0]
            results.append(CheckResult("OK", f"{target_name}: pattern {pattern}"))
            continue

        if structured and mode == "single":
            results.extend(check_structured(root, active_paths[0], f"{target_name} manifest target"))
            continue

        if structured and mode == "split":
            structured_ok = False
            for resolved_path in active_paths:
                errors = validate_structured_file(resolved_path)
                if not errors:
                    structured_ok = True
                    results.append(CheckResult("OK", f"{target_name}: schema-valid slice {rel(resolved_path, root)}"))
                else:
                    results.append(CheckResult("WARN", f"{target_name}: non-canonical slice {rel(resolved_path, root)}"))
            if not structured_ok:
                results.append(CheckResult("ERROR", f"{target_name}: split adapter has no schema-valid canonical slice"))
            continue

    return results


def check_openclaw(root: pathlib.Path) -> list[CheckResult]:
    results: list[CheckResult] = []
    home = pathlib.Path.home()

    results.append(check_file_exists(root, root / "AGENTS.md", "system_rules entry"))
    results.append(check_file_exists(root, root / "MEMORY.md", "long_term_memory file", required=False))

    memory_dir = root / "memory"
    if memory_dir.exists():
        results.append(CheckResult("OK", f"daily_memory directory: {rel(memory_dir, root)}"))
    else:
        results.append(CheckResult("ERROR", "daily_memory directory: missing memory/"))

    self_improving = home / "self-improving"
    if self_improving.exists():
        results.append(CheckResult("OK", f"reusable_lessons adapter: external self-improving detected at {self_improving}"))
    else:
        results.extend(check_structured(root, root / "memory" / "reusable-lessons.md", "reusable_lessons fallback"))

    self_improving_candidates = home / "self-improving" / "candidates.md"
    if self_improving_candidates.exists():
        results.append(CheckResult("OK", f"learning_candidates adapter: external self-improving candidates detected at {self_improving_candidates}"))
    else:
        results.extend(check_structured(root, root / "memory" / "learning-candidates.md", "learning_candidates fallback"))

    proactivity_memory = home / "proactivity" / "memory.md"
    proactivity_session = home / "proactivity" / "session-state.md"
    if proactivity_memory.exists() and proactivity_session.exists():
        results.append(CheckResult("OK", f"proactive_state adapter: split proactivity adapter detected at {proactivity_memory.parent}"))
    else:
        results.extend(check_structured(root, root / "memory" / "proactive-state.md", "proactive_state fallback"))

    proactivity_buffer = home / "proactivity" / "memory" / "working-buffer.md"
    if proactivity_buffer.exists():
        results.append(CheckResult("OK", f"working_buffer adapter: external proactivity buffer detected at {proactivity_buffer}"))
    else:
        results.extend(check_structured(root, root / "memory" / "working-buffer.md", "working_buffer fallback"))

    results.append(check_file_exists(root, root / "TOOLS.md", "tool_rules file", required=False))
    return results


def check_generic(root: pathlib.Path) -> list[CheckResult]:
    results: list[CheckResult] = []
    results.append(check_file_exists(root, root / "HOST.md", "host governance note"))
    results.extend(check_structured(root, root / "memory" / "proactive-state.md", "proactive_state fallback"))
    results.extend(check_structured(root, root / "memory" / "reusable-lessons.md", "reusable_lessons fallback"))
    results.extend(check_structured(root, root / "memory" / "working-buffer.md", "working_buffer fallback"))
    results.append(check_file_exists(root, root / "skills", "skills directory", required=False))
    return results


def summarize(results: list[CheckResult]) -> str:
    if any(r.level == "ERROR" for r in results):
        return "FAIL"
    if any(r.level == "WARN" for r in results):
        return "WARN"
    return "PASS"


def main() -> int:
    parser = argparse.ArgumentParser(description="Check a host against memory-governor manifests or reference profiles.")
    parser.add_argument("host_root", help="Path to the host root to inspect")
    parser.add_argument(
        "--profile",
        choices=("auto", "manifest", "openclaw", "generic"),
        default="auto",
        help="Reference profile to check against",
    )
    args = parser.parse_args()

    root = pathlib.Path(args.host_root).resolve()
    if not root.exists():
        print(f"ERROR host root does not exist: {root}", file=sys.stderr)
        return 1

    profile = args.profile
    if profile == "auto":
        profile = detect_profile(root)

    if profile == "unknown":
        print("ERROR could not auto-detect profile. Use --profile manifest, --profile openclaw, or --profile generic.", file=sys.stderr)
        return 1

    if profile == "manifest":
        manifest_path = find_manifest(root)
        if manifest_path is None:
            print(f"ERROR manifest profile requested but {DEFAULT_MANIFEST_NAME} is missing.", file=sys.stderr)
            return 1
        results = check_manifest(root, manifest_path)
    elif profile == "openclaw":
        results = check_openclaw(root)
    else:
        results = check_generic(root)

    status = summarize(results)

    print(f"PROFILE: {profile}")
    print(f"STATUS: {status}")
    print("CHECKS:")
    for result in results:
        print(f"- {result.level} {result.message}")

    return 0 if status in {"PASS", "WARN"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
