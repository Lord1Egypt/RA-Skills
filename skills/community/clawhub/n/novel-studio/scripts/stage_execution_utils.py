#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

from chapter_progress_utils import resolve_dispatch_chapter_labels
from check_stage_ready import file_gate_errors, state_gate_errors
from load_project_state import reconstruct
from revision_utils import normalize_state
from stage_persistence_utils import PROOFREADING_REPORT

STAGES = {'drafting', 'polishing', 'proofreading'}
PROTOCOL_RETURN_FIELDS = [
    'status',
    'changedFiles',
    'createdFiles',
    'blockedReasons',
    'summary',
    'notesForNextStage',
    'risks',
]
PROOFREADING_REQUIRED_STAGE_FIELDS = [
    'judgment',
    'continuity',
    'logic',
    'characterOOC',
    'blockers',
    'fixDirection',
]
PROTOCOL_STATUSES = {'completed', 'blocked', 'needs_clarification'}
PROOFREADING_JUDGMENTS = {'acceptable', 'conditionally acceptable', 'needs revision'}
PLATFORM_PROFILES = {'起点模式', '番茄模式', '通用模式'}
LEDGER_FILES = [
    '05B_世界规则账本.md',
    '05C_伏笔回收台账.md',
    '05D_关系状态表.md',
    '05E_能力与资源变化表.md',
]
SHA256_HEX_RE = re.compile(r'^[0-9a-f]{64}$')


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


def exists_nonempty(path: Path) -> bool:
    return path.exists() and path.is_file() and path.read_text(encoding='utf-8').strip() != ''


def read_text(path: Path) -> str:
    return path.read_text(encoding='utf-8')


def read_optional(path: Path) -> str | None:
    if exists_nonempty(path):
        return read_text(path)
    return None


def parse_bool(raw: str) -> bool:
    lowered = raw.strip().lower()
    if lowered == 'true':
        return True
    if lowered == 'false':
        return False
    raise ValueError('value must be true or false')


def canonical_acceptance_hints(stage: str) -> list[str]:
    return {
        'drafting': ['只写批准的 manuscript 文件', '不要修改规划和状态文件'],
        'polishing': ['保留已批准意图和人物口吻', '不要把上游问题静默改成新设定'],
        'proofreading': ['只读校对', '给出明确 judgment 和 blocker'],
    }[stage]


def canonical_proofreading_report_path() -> list[str]:
    return [PROOFREADING_REPORT]


def ensure_project(project: Path) -> Path:
    project = project.expanduser().resolve()
    if not project.exists() or not project.is_dir():
        raise ValueError(f'project not found: {project}')
    return project


def ensure_outside_project(project: Path, path: Path, label: str) -> Path:
    resolved = path.expanduser().resolve()
    try:
        resolved.relative_to(project)
    except ValueError:
        return resolved
    raise ValueError(f'{label} must stay outside project root: {resolved}')


def dispatch_layout(dispatch_dir: Path) -> dict[str, Path]:
    dispatch_dir = dispatch_dir.expanduser().resolve()
    return {
        'bundleFile': dispatch_dir / 'bundle.json',
        'promptFile': dispatch_dir / 'prompt.txt',
        'manifestFile': dispatch_dir / 'manifest.json',
        'rawFile': dispatch_dir / 'child-response.txt',
        'resultFile': dispatch_dir / 'result.json',
        'validatedFile': dispatch_dir / 'validated.json',
    }


def load_or_reconstruct_state(project: Path) -> dict:
    state_file = project / '.novel-state.json'
    if state_file.exists():
        return normalize_state(json.loads(state_file.read_text(encoding='utf-8')), project)
    return normalize_state(reconstruct(project), project)


def normalize_stage(stage: str) -> str:
    lowered = stage.strip().lower()
    if lowered not in STAGES:
        raise ValueError(f'unknown stage: {stage}')
    return lowered


def normalize_relpath(raw: str) -> str:
    if not raw or not raw.strip():
        raise ValueError('path cannot be empty')
    if any(token in raw for token in ['*', '?', '[', ']']):
        raise ValueError(f'globs are not allowed: {raw}')
    candidate = Path(os.path.normpath(raw.strip()))
    if candidate.is_absolute():
        raise ValueError(f'absolute paths are not allowed: {raw}')
    parts = candidate.parts
    if not parts or any(part == '..' for part in parts):
        raise ValueError(f'path escapes project root: {raw}')
    if candidate.name in {'.', ''}:
        raise ValueError(f'invalid path: {raw}')
    return candidate.as_posix()


def canonical_json(payload: object) -> str:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def payload_digest(payload: object) -> str:
    digest = hashlib.sha256()
    digest.update(canonical_json(payload).encode('utf-8'))
    return digest.hexdigest()


def validate_digest_string(value: object, label: str) -> str:
    if not isinstance(value, str) or not SHA256_HEX_RE.fullmatch(value):
        raise ValueError(f'{label} must be a 64-character lowercase hex string')
    return value


def ensure_unique_strings(values: list[str], label: str) -> None:
    seen = set()
    duplicates = []
    for value in values:
        if value in seen and value not in duplicates:
            duplicates.append(value)
        seen.add(value)
    if duplicates:
        raise ValueError(f'{label} contains duplicate entries: ' + ', '.join(duplicates))


def normalize_relpaths(values: list[str], label: str = 'paths') -> list[str]:
    normalized = [normalize_relpath(value) for value in values]
    ensure_unique_strings(normalized, label)
    return normalized


def project_files(project: Path) -> list[str]:
    files = []
    for path in project.rglob('*'):
        if path.is_file():
            files.append(path.relative_to(project).as_posix())
    return sorted(files)


def hash_file(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def hash_bytes(raw: bytes) -> str:
    digest = hashlib.sha256()
    digest.update(raw)
    return digest.hexdigest()


def hash_text(text: str) -> str:
    digest = hashlib.sha256()
    digest.update(text.encode('utf-8'))
    return digest.hexdigest()


def utf8_size(text: str) -> int:
    return len(text.encode('utf-8'))


def snapshot_project(project: Path) -> dict[str, dict[str, object]]:
    snapshot = {}
    for relpath in project_files(project):
        full_path = project / relpath
        snapshot[relpath] = {
            'sha256': hash_file(full_path),
            'size': full_path.stat().st_size,
        }
    return snapshot


def compute_diff(project: Path, baseline: dict[str, dict[str, object]]) -> dict[str, list[str]]:
    current = snapshot_project(project)
    changed = []
    created = []
    deleted = []

    for relpath, info in current.items():
        if relpath not in baseline:
            created.append(relpath)
            continue
        if baseline[relpath]['sha256'] != info['sha256']:
            changed.append(relpath)

    for relpath in baseline:
        if relpath not in current:
            deleted.append(relpath)

    return {
        'changedFiles': sorted(changed),
        'createdFiles': sorted(created),
        'deletedFiles': sorted(deleted),
    }


def ensure_stage_ready(project: Path, state: dict, stage: str) -> None:
    errors = []
    errors.extend(file_gate_errors(project, stage))
    errors.extend(state_gate_errors(state, stage))
    current_stage = state.get('workflow', {}).get('currentStage')
    if current_stage and current_stage != stage:
        errors.append(f'current stage mismatch: state={current_stage}, requested={stage}')
    if errors:
        raise ValueError('; '.join(errors))


def load_character_package(project: Path) -> dict[str, str]:
    package = {}
    characters = project / 'characters'
    if characters.is_dir():
        for path in sorted(characters.glob('*.md')):
            package[path.relative_to(project).as_posix()] = read_text(path)
    summary = project / '03_人物小传.md'
    if exists_nonempty(summary):
        package[summary.relative_to(project).as_posix()] = read_text(summary)
    return package


def load_manuscript_inputs(project: Path, relpaths: list[str] | None = None) -> dict[str, str]:
    if relpaths is None:
        relpaths = [
            path.relative_to(project).as_posix()
            for path in sorted((project / 'manuscript').glob('*.md'))
        ]
    inputs = {}
    for relpath in relpaths:
        path = project / relpath
        if exists_nonempty(path):
            inputs[relpath] = read_text(path)
    return inputs


def base_output_contract(stage: str, target_files: list[str]) -> dict[str, object]:
    contract = {
        'requiredReturnFields': list(PROTOCOL_RETURN_FIELDS),
        'mustWriteFiles': list(target_files),
    }
    if stage == 'proofreading':
        contract['requiredStageFields'] = [
            'judgment',
            'continuity',
            'logic',
            'characterOOC',
            'blockers',
            'fixDirection',
        ]
    return contract


def build_child_prompt(execution_package: dict[str, object]) -> str:
    stage = str(execution_package.get('stage') or execution_package.get('taskType') or 'unknown')
    package_json = json.dumps(execution_package, ensure_ascii=False, indent=2)
    return f"""
You are the {stage} child agent for this novel-studio dispatch.

Follow only the executionPackage. Do not assume hidden thread context.
If the package is insufficient, return `needs_clarification` with zero file writes.
Return exactly one JSON object and nothing else.
Do not echo the full executionPackage back.

executionPackage:
{package_json}
""".strip()


def extract_single_json_object(raw_text: str) -> dict:
    text = raw_text.strip()
    if not text:
        raise ValueError('child returned empty output')
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError('child must return exactly one JSON object') from exc
    if not isinstance(parsed, dict):
        raise ValueError('child output must be a JSON object')
    return parsed


def base_result_summary_fields() -> dict[str, object]:
    return {
        'lastDelegatedStage': None,
        'lastDelegatedScope': None,
        'lastDelegationStatus': None,
        'lastDelegationSummary': None,
        'lastDelegationBlockers': [],
        'lastDelegationRisks': [],
        'lastDelegatedAt': None,
    }


def read_json_file(path: Path) -> dict:
    return json.loads(path.read_text(encoding='utf-8'))


def normalize_result_paths(values: object, label: str) -> list[str]:
    if not isinstance(values, list):
        raise ValueError(f'{label} must be a list')
    normalized = []
    for value in values:
        if not isinstance(value, str):
            raise ValueError(f'{label} items must be strings')
        normalized.append(normalize_relpath(value))
    ensure_unique_strings(normalized, label)
    return sorted(normalized)


def normalize_string_list(values: object, label: str) -> list[str]:
    if not isinstance(values, list):
        raise ValueError(f'{label} must be a list')
    normalized = []
    for value in values:
        if not isinstance(value, str):
            raise ValueError(f'{label} items must be strings')
        normalized.append(value)
    ensure_unique_strings(normalized, label)
    return normalized


def require_text(value: object, label: str, *, allow_empty: bool = False) -> str:
    if not isinstance(value, str):
        raise ValueError(f'{label} must be a string')
    if not allow_empty and not value.strip():
        raise ValueError(f'{label} must be a non-empty string')
    return value


def validate_relpath_text_map(values: object, label: str, *, allow_empty: bool = False) -> dict[str, str]:
    if not isinstance(values, dict):
        raise ValueError(f'{label} must be an object')
    normalized = {}
    for key, value in values.items():
        if not isinstance(key, str):
            raise ValueError(f'{label} keys must be strings')
        relpath = normalize_relpath(key)
        normalized[relpath] = require_text(value, f'{label}.{relpath}')
    if not allow_empty and not normalized:
        raise ValueError(f'{label} must not be empty')
    return normalized


def validate_baseline_snapshot(baseline: object) -> dict[str, dict[str, object]]:
    if not isinstance(baseline, dict):
        raise ValueError('validationContext.baselineFiles must be a dict')

    normalized = {}
    for relpath, info in baseline.items():
        if not isinstance(relpath, str):
            raise ValueError('validationContext.baselineFiles keys must be strings')
        normalized_relpath = normalize_relpath(relpath)
        if not isinstance(info, dict):
            raise ValueError(f'validationContext.baselineFiles.{normalized_relpath} must be an object')
        sha256 = info.get('sha256')
        size = info.get('size')
        if not isinstance(sha256, str) or not SHA256_HEX_RE.fullmatch(sha256):
            raise ValueError(
                f'validationContext.baselineFiles.{normalized_relpath}.sha256 must be a 64-character lowercase hex string'
            )
        if type(size) is not int or size < 0:
            raise ValueError(
                f'validationContext.baselineFiles.{normalized_relpath}.size must be a non-negative integer'
            )
        normalized[normalized_relpath] = {
            'sha256': sha256,
            'size': size,
        }
    return normalized


def ensure_text_matches_baseline_snapshot(
    baseline: dict[str, dict[str, object]],
    relpath: str,
    text: str,
    label: str,
) -> None:
    info = baseline.get(relpath)
    if info is None:
        raise ValueError(f'{label} must reference an existing baseline file: {relpath}')
    if info['sha256'] != hash_text(text) or info['size'] != utf8_size(text):
        raise ValueError(f'{label} must match baseline snapshot for {relpath}')


def top_level_manuscript_files_from_snapshot(baseline: dict[str, dict[str, object]]) -> list[str]:
    return sorted(
        relpath
        for relpath in baseline
        if relpath.startswith('manuscript/')
        and len(Path(relpath).parts) == 2
        and Path(relpath).suffix == '.md'
    )


def bundle_fingerprint_payload(validation: dict) -> dict[str, object]:
    return {
        'projectRoot': validation.get('projectRoot'),
        'stage': validation.get('stage'),
        'batchRange': validation.get('batchRange'),
        'executionPackageDigest': validation.get('executionPackageDigest'),
        'baselineFilesDigest': validation.get('baselineFilesDigest'),
    }


def validate_bundle_fingerprints(
    package: dict,
    validation: dict,
    baseline: dict[str, dict[str, object]],
) -> dict[str, str]:
    execution_package_digest = validate_digest_string(
        validation.get('executionPackageDigest'),
        'validationContext.executionPackageDigest',
    )
    baseline_files_digest = validate_digest_string(
        validation.get('baselineFilesDigest'),
        'validationContext.baselineFilesDigest',
    )
    bundle_fingerprint = validate_digest_string(
        validation.get('bundleFingerprint'),
        'validationContext.bundleFingerprint',
    )

    if execution_package_digest != payload_digest(package):
        raise ValueError('validationContext.executionPackageDigest mismatch')
    if baseline_files_digest != payload_digest(baseline):
        raise ValueError('validationContext.baselineFilesDigest mismatch')
    if bundle_fingerprint != payload_digest(bundle_fingerprint_payload(validation)):
        raise ValueError('validationContext.bundleFingerprint mismatch')

    return {
        'executionPackageDigest': execution_package_digest,
        'baselineFilesDigest': baseline_files_digest,
        'bundleFingerprint': bundle_fingerprint,
    }


def build_bundle_manifest(
    bundle_file: Path,
    bundle: dict,
    *,
    prompt_file: Path | None = None,
    prompt_text: str | None = None,
) -> dict[str, object]:
    validation = bundle['validationContext']
    bundle_file = bundle_file.expanduser().resolve()
    if prompt_file is not None:
        prompt_file = prompt_file.expanduser().resolve()
    return {
        'bundleFile': str(bundle_file),
        'bundleSha256': hash_bytes(bundle_file.read_bytes()),
        'executionPackageDigest': validation['executionPackageDigest'],
        'baselineFilesDigest': validation['baselineFilesDigest'],
        'bundleFingerprint': validation['bundleFingerprint'],
        'promptFile': str(prompt_file) if prompt_file is not None else None,
        'promptSha256': hash_text(prompt_text) if prompt_text is not None else None,
    }


def validate_bundle_manifest(manifest: object, bundle_file: Path, bundle: dict) -> dict[str, object]:
    if not isinstance(manifest, dict):
        raise ValueError('bundle manifest must be a JSON object')

    bundle_file = bundle_file.expanduser().resolve()
    actual_bundle_sha256 = hash_bytes(bundle_file.read_bytes())
    expected_bundle_file = manifest.get('bundleFile')
    expected_bundle_sha256 = validate_digest_string(manifest.get('bundleSha256'), 'bundle manifest.bundleSha256')
    expected_execution_package_digest = validate_digest_string(
        manifest.get('executionPackageDigest'),
        'bundle manifest.executionPackageDigest',
    )
    expected_baseline_files_digest = validate_digest_string(
        manifest.get('baselineFilesDigest'),
        'bundle manifest.baselineFilesDigest',
    )
    expected_bundle_fingerprint = validate_digest_string(
        manifest.get('bundleFingerprint'),
        'bundle manifest.bundleFingerprint',
    )

    if expected_bundle_file != str(bundle_file):
        raise ValueError('bundle manifest mismatch: bundleFile')
    if expected_bundle_sha256 != actual_bundle_sha256:
        raise ValueError('bundle manifest mismatch: bundleSha256')

    validation = bundle.get('validationContext', {})
    if expected_execution_package_digest != validation.get('executionPackageDigest'):
        raise ValueError('bundle manifest mismatch: executionPackageDigest')
    if expected_baseline_files_digest != validation.get('baselineFilesDigest'):
        raise ValueError('bundle manifest mismatch: baselineFilesDigest')
    if expected_bundle_fingerprint != validation.get('bundleFingerprint'):
        raise ValueError('bundle manifest mismatch: bundleFingerprint')

    prompt_file = manifest.get('promptFile')
    prompt_sha256 = manifest.get('promptSha256')
    resolved_prompt_file = None
    if prompt_file is not None and not isinstance(prompt_file, str):
        raise ValueError('bundle manifest.promptFile must be a string or null')
    if prompt_sha256 is not None:
        validate_digest_string(prompt_sha256, 'bundle manifest.promptSha256')

    if prompt_file is not None:
        resolved_prompt_file = Path(prompt_file).expanduser().resolve()
        if prompt_sha256 is None:
            raise ValueError('bundle manifest mismatch: promptSha256')
        if not resolved_prompt_file.exists() or not resolved_prompt_file.is_file():
            raise ValueError('bundle manifest mismatch: promptFile')
        if hash_bytes(resolved_prompt_file.read_bytes()) != prompt_sha256:
            raise ValueError('bundle manifest mismatch: promptSha256')

    return {
        'bundleFile': expected_bundle_file,
        'bundleSha256': expected_bundle_sha256,
        'executionPackageDigest': expected_execution_package_digest,
        'baselineFilesDigest': expected_baseline_files_digest,
        'bundleFingerprint': expected_bundle_fingerprint,
        'promptFile': str(resolved_prompt_file) if resolved_prompt_file is not None else None,
        'promptSha256': prompt_sha256,
    }


def validate_required_inputs(
    required_inputs: object,
    stage: str,
    batch_range: object,
    target_files: list[str],
    baseline: dict[str, dict[str, object]],
) -> dict[str, object]:
    if not isinstance(required_inputs, dict):
        raise ValueError('requiredInputs must be an object')

    require_text(required_inputs.get('batchRange'), 'requiredInputs.batchRange')
    if required_inputs.get('batchRange') != batch_range:
        raise ValueError('requiredInputs.batchRange must match executionPackage.batchRange')

    outline = require_text(required_inputs.get('outline'), 'requiredInputs.outline')
    ensure_text_matches_baseline_snapshot(baseline, '02_大纲.md', outline, 'requiredInputs.outline')

    batch_plan = require_text(required_inputs.get('batchPlan'), 'requiredInputs.batchPlan')
    ensure_text_matches_baseline_snapshot(
        baseline,
        '05_本轮章节规划.md',
        batch_plan,
        'requiredInputs.batchPlan',
    )
    chapter_labels = normalize_string_list(
        required_inputs.get('chapterLabels'),
        'requiredInputs.chapterLabels',
    )
    expected_chapter_labels = resolve_dispatch_chapter_labels(stage, batch_plan, target_files)
    if chapter_labels != expected_chapter_labels:
        raise ValueError('requiredInputs.chapterLabels must match the approved plan labels for this dispatch')

    character_files = validate_relpath_text_map(
        required_inputs.get('characterFiles'),
        'requiredInputs.characterFiles',
    )
    for relpath, text in character_files.items():
        ensure_text_matches_baseline_snapshot(
            baseline,
            relpath,
            text,
            f'requiredInputs.characterFiles.{relpath}',
        )

    validated = {
        'batchRange': required_inputs['batchRange'],
        'outline': outline,
        'batchPlan': batch_plan,
        'chapterLabels': chapter_labels,
        'characterFiles': character_files,
    }

    style_bible = require_text(required_inputs.get('styleBible'), 'requiredInputs.styleBible')
    ensure_text_matches_baseline_snapshot(
        baseline,
        '01A_风格圣经.md',
        style_bible,
        'requiredInputs.styleBible',
    )
    mainline_spec = require_text(required_inputs.get('mainlineSpec'), 'requiredInputs.mainlineSpec')
    ensure_text_matches_baseline_snapshot(
        baseline,
        '01B_总主线与卷级推进.md',
        mainline_spec,
        'requiredInputs.mainlineSpec',
    )
    opening_design = require_text(required_inputs.get('openingDesign'), 'requiredInputs.openingDesign')
    ensure_text_matches_baseline_snapshot(
        baseline,
        '04A_开篇设计.md',
        opening_design,
        'requiredInputs.openingDesign',
    )
    platform_profile = require_text(required_inputs.get('platformProfile'), 'requiredInputs.platformProfile')
    if platform_profile not in PLATFORM_PROFILES:
        raise ValueError('requiredInputs.platformProfile must be one of: 起点模式, 番茄模式, 通用模式')
    track_guide = require_text(required_inputs.get('trackGuide'), 'requiredInputs.trackGuide')
    ensure_text_matches_baseline_snapshot(
        baseline,
        '00C_底盘与切口决策.md',
        track_guide,
        'requiredInputs.trackGuide',
    )
    ledger_snapshot = validate_relpath_text_map(
        required_inputs.get('ledgerSnapshot'),
        'requiredInputs.ledgerSnapshot',
    )
    if sorted(ledger_snapshot) != LEDGER_FILES:
        raise ValueError('requiredInputs.ledgerSnapshot must exactly contain the four canonical ledger files')
    for relpath, text in ledger_snapshot.items():
        ensure_text_matches_baseline_snapshot(
            baseline,
            relpath,
            text,
            f'requiredInputs.ledgerSnapshot.{relpath}',
        )
    validated['styleBible'] = style_bible
    validated['mainlineSpec'] = mainline_spec
    validated['openingDesign'] = opening_design
    validated['platformProfile'] = platform_profile
    validated['trackGuide'] = track_guide
    validated['ledgerSnapshot'] = ledger_snapshot

    recap = required_inputs.get('recap')
    if recap is not None and not isinstance(recap, str):
        raise ValueError('requiredInputs.recap must be a string or null')
    if recap is not None:
        ensure_text_matches_baseline_snapshot(
            baseline,
            '05_前情回顾.md',
            recap,
            'requiredInputs.recap',
        )
    validated['recap'] = recap

    if stage == 'polishing':
        validated['polishingFocus'] = require_text(
            required_inputs.get('polishingFocus'),
            'requiredInputs.polishingFocus',
        )

    if stage in {'polishing', 'proofreading'}:
        manuscript_files = validate_relpath_text_map(
            required_inputs.get('manuscriptFiles'),
            'requiredInputs.manuscriptFiles',
        )
        if any(not relpath.startswith('manuscript/') for relpath in manuscript_files):
            raise ValueError('requiredInputs.manuscriptFiles must stay under manuscript/')
        for relpath, text in manuscript_files.items():
            ensure_text_matches_baseline_snapshot(
                baseline,
                relpath,
                text,
                f'requiredInputs.manuscriptFiles.{relpath}',
            )
        if stage == 'polishing' and list(manuscript_files) != target_files:
            raise ValueError('requiredInputs.manuscriptFiles must exactly match targetFiles for polishing')
        if stage == 'proofreading':
            expected_manuscript_files = top_level_manuscript_files_from_snapshot(baseline)
            if sorted(manuscript_files) != expected_manuscript_files:
                raise ValueError(
                    'requiredInputs.manuscriptFiles must match baseline manuscript snapshot for proofreading'
                )
        validated['manuscriptFiles'] = manuscript_files

    return validated


def validate_output_contract(contract: object, stage: str, target_files: list[str]) -> dict[str, object]:
    if not isinstance(contract, dict):
        raise ValueError('outputContract must be an object')

    required_return_fields = normalize_string_list(
        contract.get('requiredReturnFields'),
        'outputContract.requiredReturnFields',
    )
    if required_return_fields != PROTOCOL_RETURN_FIELDS:
        raise ValueError('outputContract.requiredReturnFields must match the protocol contract')

    must_write_files = normalize_result_paths(
        contract.get('mustWriteFiles'),
        'outputContract.mustWriteFiles',
    )
    if must_write_files != target_files:
        raise ValueError('outputContract.mustWriteFiles must exactly match targetFiles')

    validated = {
        'requiredReturnFields': required_return_fields,
        'mustWriteFiles': must_write_files,
    }

    if stage == 'proofreading':
        required_stage_fields = normalize_string_list(
            contract.get('requiredStageFields'),
            'outputContract.requiredStageFields',
        )
        if required_stage_fields != PROOFREADING_REQUIRED_STAGE_FIELDS:
            raise ValueError('outputContract.requiredStageFields must match the proofreading protocol')
        validated['requiredStageFields'] = required_stage_fields

    return validated


def validate_execution_package_contract(
    package: dict,
    validation: dict,
) -> dict[str, object]:
    stage = normalize_stage(package.get('stage', ''))
    target_files = normalize_result_paths(package.get('targetFiles', []), 'targetFiles')
    overwrite_flag = package.get('overwriteFlag')
    if not isinstance(overwrite_flag, bool):
        raise ValueError('overwriteFlag must be a boolean')

    baseline = validate_baseline_snapshot(validation.get('baselineFiles'))
    must_not_modify = normalize_result_paths(package.get('mustNotModify', []), 'mustNotModify')
    acceptance_hints = normalize_string_list(package.get('acceptanceHints'), 'acceptanceHints')
    if acceptance_hints != canonical_acceptance_hints(stage):
        raise ValueError('acceptanceHints must match canonical stage hints')

    if stage == 'drafting':
        if not target_files:
            raise ValueError('drafting targetFiles must not be empty')
        if any(not relpath.startswith('manuscript/') for relpath in target_files):
            raise ValueError('drafting targetFiles must stay under manuscript/')
        if not overwrite_flag:
            existing_targets = [relpath for relpath in target_files if relpath in baseline]
            if existing_targets:
                raise ValueError(
                    'drafting overwrite flag is false but target files already exist: '
                    + ', '.join(existing_targets)
                )
    elif stage == 'polishing':
        if not target_files:
            raise ValueError('polishing targetFiles must not be empty')
        if any(not relpath.startswith('manuscript/') for relpath in target_files):
            raise ValueError('polishing targetFiles must stay under manuscript/')
        missing_targets = [relpath for relpath in target_files if relpath not in baseline]
        if missing_targets:
            raise ValueError(
                'polishing targetFiles must refer to existing baseline files: '
                + ', '.join(missing_targets)
            )
    elif stage == 'proofreading':
        if target_files != canonical_proofreading_report_path():
            raise ValueError('proofreading targetFiles must be exactly [05A_本轮校对报告.md]')
        if not overwrite_flag:
            raise ValueError('proofreading overwriteFlag must be true')
    else:
        raise ValueError(f'unsupported stage for execution package validation: {stage}')

    if stage in {'drafting', 'polishing', 'proofreading'}:
        expected_must_not_modify = sorted(relpath for relpath in baseline if relpath not in target_files)
        if must_not_modify != expected_must_not_modify:
            raise ValueError('mustNotModify must exactly match baselineFiles minus targetFiles')

    required_inputs = validate_required_inputs(
        package.get('requiredInputs'),
        stage,
        package.get('batchRange'),
        target_files,
        baseline,
    )
    output_contract = validate_output_contract(package.get('outputContract'), stage, target_files)

    return {
        'stage': stage,
        'targetFiles': target_files,
        'overwriteFlag': overwrite_flag,
        'mustNotModify': must_not_modify,
        'acceptanceHints': acceptance_hints,
        'requiredInputs': required_inputs,
        'outputContract': output_contract,
        'baselineFiles': baseline,
    }


def validate_result_payload(result: dict, stage: str) -> dict[str, object]:
    for field in PROTOCOL_RETURN_FIELDS:
        if field not in result:
            raise ValueError(f'missing required result field: {field}')

    status = result['status']
    if status not in PROTOCOL_STATUSES:
        raise ValueError(f'invalid status: {status}')

    changed_files = normalize_result_paths(result['changedFiles'], 'changedFiles')
    created_files = normalize_result_paths(result['createdFiles'], 'createdFiles')
    blocked_reasons = normalize_string_list(result['blockedReasons'], 'blockedReasons')
    risks = normalize_string_list(result['risks'], 'risks')
    summary = require_text(result['summary'], 'summary')
    notes_for_next_stage = require_text(result['notesForNextStage'], 'notesForNextStage', allow_empty=True)

    validated = dict(result)
    validated['changedFiles'] = changed_files
    validated['createdFiles'] = created_files
    validated['blockedReasons'] = blocked_reasons
    validated['summary'] = summary
    validated['notesForNextStage'] = notes_for_next_stage
    validated['risks'] = risks

    if status == 'blocked' and not blocked_reasons:
        raise ValueError('blocked status requires non-empty blockedReasons')
    if status == 'needs_clarification' and not blocked_reasons:
        raise ValueError('needs_clarification status requires non-empty blockedReasons')
    if status == 'completed' and blocked_reasons:
        raise ValueError('completed status must not include blockedReasons')

    if stage == 'proofreading' and status == 'completed':
        for field in PROOFREADING_REQUIRED_STAGE_FIELDS:
            if field not in result:
                raise ValueError(f'missing required proofreading field: {field}')
        if result['judgment'] not in PROOFREADING_JUDGMENTS:
            raise ValueError(f'invalid proofreading judgment: {result["judgment"]}')
        validated['judgment'] = result['judgment']
        validated['continuity'] = require_text(result['continuity'], 'proofreading continuity')
        validated['logic'] = require_text(result['logic'], 'proofreading logic')
        validated['characterOOC'] = require_text(result['characterOOC'], 'proofreading characterOOC')
        validated['fixDirection'] = require_text(result['fixDirection'], 'proofreading fixDirection')
        validated['blockers'] = normalize_string_list(result['blockers'], 'proofreading blockers')
        if validated['judgment'] == 'acceptable' and validated['blockers']:
            raise ValueError('proofreading blockers must be empty when judgment is acceptable')
        if validated['judgment'] == 'conditionally acceptable' and validated['blockers']:
            raise ValueError('proofreading blockers must be empty when judgment is conditionally acceptable')
        if validated['judgment'] == 'conditionally acceptable' and not validated['risks']:
            raise ValueError('proofreading risks must be non-empty when judgment is conditionally acceptable')
        if validated['judgment'] == 'needs revision' and not validated['blockers']:
            raise ValueError('proofreading blockers must be non-empty when judgment is needs revision')
    return validated


def validate_bundle_and_result(project: Path, bundle: dict, result: dict) -> dict[str, object]:
    package = bundle.get('executionPackage')
    validation = bundle.get('validationContext')
    if not isinstance(package, dict) or not isinstance(validation, dict):
        raise ValueError('bundle must contain executionPackage and validationContext')

    stage = normalize_stage(package.get('stage', ''))
    task_type = normalize_stage(package.get('taskType', ''))
    validation_stage = normalize_stage(validation.get('stage', ''))
    if task_type != stage or validation_stage != stage or validation.get('batchRange') != package.get('batchRange'):
        raise ValueError('bundle stage metadata mismatch')
    if str(project) != package.get('projectRoot'):
        raise ValueError('project root mismatch between project and bundle')
    if str(project) != validation.get('projectRoot'):
        raise ValueError('project root mismatch between validation context and project')

    baseline = validate_baseline_snapshot(validation.get('baselineFiles'))
    bundle_fingerprints = validate_bundle_fingerprints(package, validation, baseline)
    validated_package = validate_execution_package_contract(package, validation)
    validated = validate_result_payload(result, stage)
    actual = compute_diff(project, baseline)

    if actual['deletedFiles']:
        raise ValueError('deleted files are not allowed: ' + ', '.join(actual['deletedFiles']))

    if validated['status'] in {'blocked', 'needs_clarification'}:
        if actual['changedFiles'] or actual['createdFiles'] or actual['deletedFiles']:
            raise ValueError('non-completed status returned with filesystem writes')

    if actual['changedFiles'] != validated['changedFiles'] or actual['createdFiles'] != validated['createdFiles']:
        raise ValueError(
            'diff mismatch between actual filesystem changes and child-reported changedFiles/createdFiles'
        )

    target_files = validated_package['targetFiles']
    overwrite_flag = validated_package['overwriteFlag']
    must_not_modify = validated_package['mustNotModify']
    actual_touched = sorted(set(actual['changedFiles'] + actual['createdFiles']))
    if target_files and not overwrite_flag and actual['changedFiles']:
        raise ValueError(
            'overwrite flag is false but existing target files were modified: '
            + ', '.join(actual['changedFiles'])
        )
    forbidden_touches = [path for path in actual_touched if path in must_not_modify]
    if forbidden_touches:
        raise ValueError('forbidden files were modified: ' + ', '.join(forbidden_touches))

    if any(path not in target_files for path in actual_touched):
        raise ValueError('out-of-scope writes detected: ' + ', '.join(actual_touched))

    if stage == 'proofreading':
        forbidden_touches = [path for path in actual_touched if path != PROOFREADING_REPORT]
        if forbidden_touches:
            raise ValueError('proofreading may only write the canonical report file')

    if validated['status'] == 'completed':
        untouched_required_outputs = [
            relpath
            for relpath in validated_package['outputContract']['mustWriteFiles']
            if relpath not in actual_touched
        ]
        if untouched_required_outputs:
            raise ValueError(
                'completed result did not touch required output files: '
                + ', '.join(untouched_required_outputs)
            )
        for relpath in validated_package['outputContract']['mustWriteFiles']:
            path = project / relpath
            if not exists_nonempty(path):
                raise ValueError(f'expected output is missing or empty: {relpath}')

    return {
        'stage': stage,
        'package': package,
        'result': validated,
        'actualDiff': actual,
        'bundleFingerprints': bundle_fingerprints,
    }
