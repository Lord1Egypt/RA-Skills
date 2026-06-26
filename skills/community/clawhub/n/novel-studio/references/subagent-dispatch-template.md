# Subagent Dispatch Template

Use this template when the parent agent is about to dispatch `drafting`, `polishing`, or `proofreading`.

## 1. Parent-side invariants
- build the bundle immediately before child dispatch
- send only `executionPackage` to the child
- keep `validationContext` parent-side only
- delegate with `fork_context = false`
- do not modify project files after bundle build and before validation finishes
- if parent-side files changed or the session was interrupted, discard the old bundle and rebuild a fresh one
- do not add hidden requirements outside `requiredInputs`; if context is missing, fix the bundle builder or rebuild the package
- keep `targetFiles`, `requiredInputs`, `mustNotModify`, and `outputContract` internally consistent
- for `proofreading`, keep `targetFiles=[]`, `overwriteFlag=false`, and a full-project `mustNotModify` snapshot
- reject duplicated paths inside `targetFiles`, `mustNotModify`, `changedFiles`, or `createdFiles`
- keep `executionPackageDigest`, `baselineFilesDigest`, and `bundleFingerprint` in sync with the built bundle; if anything changes, rebuild instead of hand-editing
- if a prompt file is emitted, keep `promptFile` and `promptSha256` aligned with the actual child prompt text

Helper scripts:
- `scripts/prepare_stage_subagent_dispatch.py` prepares a reusable bundle file plus the child prompt
- `scripts/prepare_stage_subagent_dispatch.py` can also emit a sidecar manifest for bundle integrity checks
- `scripts/prepare_stage_subagent_dispatch.py` can return a standard dispatch workspace layout via `dispatchDir` plus raw/result/validated artifact paths
- the standard `dispatchDir` layout is `bundle.json`, `prompt.txt`, `manifest.json`, `child-response.txt`, `result.json`, and `validated.json`
- if explicit `bundleFile`, `promptFile`, and `manifestFile` share one parent directory, infer that parent as `dispatchDir` for the remaining artifacts
- `scripts/extract_stage_subagent_result.py` turns the child raw response into exactly one JSON result object
- `scripts/extract_stage_subagent_result.py` can read `rawFile` and write `resultFile` directly from `dispatchDir`
- `scripts/finalize_stage_subagent_dispatch.py` validates the child result and applies accepted state updates
- `scripts/finalize_stage_subagent_dispatch.py` can read `bundleFile` / `manifestFile` / `resultFile` and write `validatedFile` directly from `dispatchDir`
- `scripts/subagent_dispatch_runtime.py` exposes `prepare_dispatch`, `record_child_output`, and `finalize_dispatch` for Python parents
- all dispatch artifacts must stay outside project root

## 2. Build the execution bundle

Drafting example:

```bash
python3 skills/novel-studio/scripts/build_stage_execution_package.py \
  "$PROJECT_ROOT" \
  drafting \
  --batch-range "第1章-第3章" \
  --target-file "manuscript/第1章_开端.md" \
  --target-file "manuscript/第2章_转折.md" \
  --target-file "manuscript/第3章_反转.md" \
  > "$TMP_DIR/bundle.json"
```

Polishing example:

```bash
python3 skills/novel-studio/scripts/build_stage_execution_package.py \
  "$PROJECT_ROOT" \
  polishing \
  --batch-range "第1章-第3章" \
  --target-file "manuscript/第1章_开端.md" \
  --target-file "manuscript/第2章_转折.md" \
  --target-file "manuscript/第3章_反转.md" \
  --polishing-focus "压缩开篇废话，增强结尾钩子和人物口吻区分" \
  > "$TMP_DIR/bundle.json"
```

Proofreading example:

```bash
python3 skills/novel-studio/scripts/build_stage_execution_package.py \
  "$PROJECT_ROOT" \
  proofreading \
  --batch-range "第1章-第3章" \
  > "$TMP_DIR/bundle.json"
```

When you want one predictable artifact layout, prefer:

```bash
python3 skills/novel-studio/scripts/prepare_stage_subagent_dispatch.py \
  "$PROJECT_ROOT" \
  drafting \
  --batch-range "第1章-第3章" \
  --target-file "manuscript/第1章_开端.md" \
  --dispatch-dir "$TMP_DIR"
```

If you already pass explicit `--bundle-file`, `--prompt-file`, and `--manifest-file` paths under one shared parent directory, `prepare_stage_subagent_dispatch.py` will infer that parent as `dispatchDir` and keep `rawFile`, `resultFile`, and `validatedFile` alongside them.

## 3. Parent dispatch skeleton

```python
import json

bundle = json.loads(build_bundle_stdout)
execution_package = bundle["executionPackage"]

child_prompt = f"""
You are the {execution_package["stage"]} child agent for this novel-studio dispatch.

Follow only the executionPackage. Do not assume hidden thread context.
If the package is insufficient, return `needs_clarification` with zero file writes.
Return exactly one JSON object and nothing else.
Do not echo the full executionPackage back.

executionPackage:
{json.dumps(execution_package, ensure_ascii=False, indent=2)}
"""

child = spawn_agent(
    agent_type="worker",
    fork_context=False,
    message=child_prompt,
)
```

The parent should treat the build output as runtime-only:
- `executionPackage` goes to the child
- `validationContext` stays with the parent

## 4. Child prompt template

Use this structure when dispatching the child:

```text
You are the {stage} child agent for this dispatch.

Scope:
- batchRange: {batchRange}
- targetFiles: {targetFiles}
- overwriteFlag: {overwriteFlag}

Hard rules:
- modify only files allowed by targetFiles
- never modify files listed in mustNotModify
- do not assume hidden context outside requiredInputs
- if the package is insufficient, return needs_clarification with zero file writes
- return exactly one JSON object with the required protocol fields
- treat `outputContract` as binding, not advisory

Stage-specific reminder:
- drafting: write only approved manuscript files
- polishing: preserve approved intent and honor polishingFocus
- proofreading: read-only only; do not modify any project file; include judgment, continuity, logic, characterOOC, blockers, and fixDirection

executionPackage:
{...inline JSON...}
```

## 5. Parent result handling skeleton

After the child returns raw text:

```bash
python3 skills/novel-studio/scripts/extract_stage_subagent_result.py \
  --dispatch-dir "$TMP_DIR" \
  --project-root "$PROJECT_ROOT"

python3 skills/novel-studio/scripts/finalize_stage_subagent_dispatch.py \
  "$PROJECT_ROOT" \
  --dispatch-dir "$TMP_DIR"
```

If you need to deviate from the standard layout, pass explicit file arguments and let them override the `dispatchDir` defaults.

Parent handling rules:
- if validation fails, stop and surface the failure
- if the child returns prose, multiple JSON blocks, or malformed JSON, treat it as protocol failure
- if the child returns `blocked` or `needs_clarification`, require non-empty `blockedReasons`
- if the child returns `completed`, require empty `blockedReasons`
- if the child returns `completed`, require every `outputContract.mustWriteFiles` path to be touched by the dispatch
- if `proofreading` returns `completed`, require non-empty judgment fields; if judgment is `needs revision`, require non-empty blockers
- if `proofreading` returns `completed` with judgment `acceptable`, require empty blockers
- if `proofreading` returns `completed` with judgment `conditionally acceptable`, require empty blockers and non-empty risks
- do not hand-edit the child result just to make validation pass
- apply only validated results
- summarize the accepted result for the user only after validation and apply succeed

## 6. End-to-End Parent Example

Use this as a concrete parent-side reference when you want one reusable flow for all three stages without making prompt-vs-file responsibilities ambiguous.

```python
import tempfile
from pathlib import Path

from subagent_dispatch_runtime import finalize_dispatch, prepare_dispatch, record_child_output


def dispatch_stage(
    project_root: str,
    stage: str,
    batch_range: str,
    target_files: list[str] | None = None,
    polishing_focus: str | None = None,
) -> dict:
    target_files = target_files or []
    tmp_dir = Path(tempfile.mkdtemp(prefix="novel-stage-"))

    payload = prepare_dispatch(
        project_root,
        stage,
        batch_range=batch_range,
        target_files=target_files,
        polishing_focus=polishing_focus,
        dispatch_dir=tmp_dir,
    )
    dispatch_dir = Path(payload["dispatchDir"])

    child = spawn_agent(
        agent_type="worker",
        fork_context=False,
        message=payload["childPrompt"],
    )
    child_done = wait_agent(ids=[child.id], timeout_ms=180000)
    record_child_output(project_root, child_done["final_message"], dispatch_dir=dispatch_dir)
    applied = finalize_dispatch(
        project_root,
        dispatch_dir=dispatch_dir,
    )
    return applied
```

Read this example with the shared protocol:
- the parent still sends only `payload["childPrompt"]` to the child, not local artifact paths
- `prepare_dispatch` creates both the child prompt and the parent-side dispatch artifacts
- `record_child_output` only records the raw child response into the parent-side dispatch workspace
- `finalize_dispatch` runs extract + validation + apply in one parent-side step
- the parent validates before apply every time
- if `wait_agent` times out or returns no usable final message, treat it as infrastructure failure and retry at most once
