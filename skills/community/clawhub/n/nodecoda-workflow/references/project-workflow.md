# Project-Based Workflow

Detailed reference for the project mode. SKILL.md holds the protocol; this file holds the full state table, commands, and resume rules.

## When to use project mode vs lightweight mode

- **Project mode (default)**: the user wants a real, versioned, shareable Dify workflow. Create a project directory.
- **Lightweight mode (opt-in)**: quick validation of a `.ncoda` snippet, debugging a single node, or running an example. No project dir; state lives only in the conversation. State explicitly: "这是临时验证，正式工作流请走项目模式。"

## Project directory layout

```
<project-name>/
├── nodecoda.yaml            # manifest (agent-maintained YAML)
├── nodecoda.state.json      # state machine state (project.mjs-maintained JSON)
├── design.md                # requirements artifact (lean deep-interview)
├── <name>.ncoda             # source-of-truth (recompilable)
├── <name>.dify.yaml         # latest Dify artifact (overwritten every build)
└── <name>.build.json        # latest build record (status, build_id, sha256)

> 版本策略：一个目录管全部——源和产物放一起，不拆分 src/builds、不按 build_id
> 建目录、不保留旧版本：每次构建覆盖同名文件，版本化由你主动用 git 维护
> （改源码 → 重新 build → `git diff` → commit）。
> 需要按 build_id 的历史快照时用 `npx -y @nodecoda/skill save-build <build_id>`。
```

## Manifest (`nodecoda.yaml`)

```yaml
project: customer-support
mode: advanced-chat
target_profile: dify-1.16-graphon-0.6
language_identity: nodecoda/1
source: customer-support.ncoda
created_at: "2026-08-12T..."
```

## State (`nodecoda.state.json`)

```json
{ "phase": "DESIGNED", "rev": 0, "current_build_id": null, "source_sha256": null, "last_diagnostics": [], "history": [] }
```

## State machine - full transition table

| From | Allowed to |
|---|---|
| INIT | CLARIFYING, DESIGNED, CANCELLED |
| CLARIFYING | DESIGNED, CANCELLED |
| DESIGNED | SOURCE_READY, CANCELLED |
| SOURCE_READY | BUILDING, CANCELLED |
| BUILDING | SUCCEEDED, NEEDS_FIX, FAILED, CANCELLED |
| NEEDS_FIX | SOURCE_READY (rev+1), FAILED, CANCELLED |
| SUCCEEDED | SOURCE_READY (rev+1), CANCELLED |
| FAILED | (terminal) |
| CANCELLED | (terminal) |

`rev` auto-increments on `NEEDS_FIX->SOURCE_READY` and `SUCCEEDED->SOURCE_READY` unless `--rev` is given.

> **重建（同 Source 仅重编译）完整链（实证 2026-08-14）**：`SUCCEEDED -> SOURCE_READY (--rev +1) -> BUILDING (--build-id <新id>) -> SUCCEEDED (--sha256 <hash>)`。直接 `set-state SUCCEEDED` 会报 `illegal transition: SUCCEEDED -> SUCCEEDED`；每一步都不可跳过。同 Source 重建也要新 `idempotency_key`（如 `<project>-rev-<n>-<ts>`），否则网关返回旧 build。

## Commands

```bash
# detect or create (npx form works from anywhere; `node scripts/...` only if this repo is cloned)
npx -y @nodecoda/skill project resolve
npx -y @nodecoda/skill project init ./my-flow --project my-flow --mode workflow

# state
npx -y @nodecoda/skill project get-state ./my-flow
npx -y @nodecoda/skill project set-state ./my-flow DESIGNED
npx -y @nodecoda/skill project set-state ./my-flow BUILDING --build-id job_x
npx -y @nodecoda/skill project set-state ./my-flow SUCCEEDED --sha256 <hash>
npx -y @nodecoda/skill project set-state ./my-flow NEEDS_FIX --diagnostics '["err1"]'

# validate
node scripts/validate-project.mjs ./my-flow   # (repo-only) or npm run validate
```

## Resume protocol

On any session start inside a project dir, run `npx -y @nodecoda/skill project get-state .` and continue from `phase`:
- CLARIFYING/DESIGNED: continue or finalize design.md
- SOURCE_READY: submit build
- BUILDING: poll `get_workflow_build` with `current_build_id`
- NEEDS_FIX: read `last_diagnostics`, edit <name>.ncoda, set-state SOURCE_READY
- SUCCEEDED: deliver; or edit <name>.ncoda to rebuild
- FAILED/CANCELLED: report terminal state, do not auto-retry

## Lean deep-interview (project creation)

One question at a time, intent-first, max 5 rounds. If input/output/mode/boundaries are already answerable, skip to DESIGNED early.
1. 用途 (purpose)
2. 输入/输出 (input/output)
3. 模式与依赖 (mode + deps)
4. 边界与异常 (boundaries + error branches)

## Build loop (coding cycle)

```
SOURCE_READY -> build_dify_workflow(idempotency_key=<project>-rev-<n>)
  -> poll get_workflow_build (<=180s, admission <=3)
  -> SUCCEEDED: npx -y @nodecoda/skill save-build <build_id> --source <name>.ncoda
       + set-state SUCCEEDED --sha256 <hash>
  -> NEEDS_FIX: set-state NEEDS_FIX --diagnostics '<json>'; edit <name>.ncoda; set-state SOURCE_READY (rev+1); loop <=5
  -> FAILED/CANCELLED: terminal, keep diagnostics
```

## Rebuild protocol (重新编译已交付的流程)

`SUCCEEDED` 是**终态**,直接再 `set-state SUCCEEDED` 是 illegal transition。要重建,必须走完整链(每一跳都被状态机校验,**不能跳步**):

```bash
# SUCCEEDED -> SOURCE_READY(rev 自动 +1,除非 --rev)
npx -y @nodecoda/skill project set-state ./my-flow SOURCE_READY
# SOURCE_READY -> BUILDING(必须带新 build-id)
npx -y @nodecoda/skill project set-state ./my-flow BUILDING --build-id <new_build_id>
# BUILDING -> SUCCEEDED(带新 sha256)
npx -y @nodecoda/skill project set-state ./my-flow SUCCEEDED --sha256 <hash>
```

注意:新 rev 用**新幂等 key**(`<project>-rev-<n+1>`)。`set-state` 拒绝非法转移时会打印合法去向与本节链接。

## Hash fidelity

Saved `<name>.ncoda` bytes MUST equal the bytes passed to `build_dify_workflow`. The backend hashes exact submitted bytes (no trailing-newline normalization). If `source_sha256 != sha256(saved file)`, stop and reconcile.

## Credentials

`NODECODA_KEY` is read from env only. Never write it to manifest, state, design, or reports.
