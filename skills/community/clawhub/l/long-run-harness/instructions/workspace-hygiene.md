# Workspace Hygiene and Artifact Management

Long-running harnesses generate a lot of byproducts. Treat artifact routing as a first-class
feature, not an afterthought.

## Directory Contract

Use this structure by default:

```text
project_dir/
  harness-state/
    spec.md
    sprints.md
    contracts/
    handoffs/
    evals/
    evidence/
      sprint-N/
        commands/
        screenshots/
        browser/
        axe/
        lighthouse/
        source/
        api/
        git/
        artifacts/
    tmp/
  harness-logs/
    run-YYYYMMDD-HHMMSS.log
    devserver.log
```

Allowed generated locations:

- `harness-state/**`
- `harness-logs/**`
- app/source files explicitly required by the sprint
- test files explicitly required by the sprint

Disallowed for generated evidence/log/test output:

- `src/**` unless it is product source/test code
- `public/**` unless the sprint explicitly requires a public asset
- `docs/**` unless the output is a user-requested document
- repo root loose files such as `lh-report.json`, `console.log`, `output.txt`

## Path Helpers

Put all path construction in one place:

```python
def ensure_workspace(project_dir: Path, sprint: int | None = None) -> dict[str, Path]:
    state = project_dir / "harness-state"
    logs = project_dir / "harness-logs"
    paths = {
        "state": state,
        "logs": logs,
        "contracts": state / "contracts",
        "handoffs": state / "handoffs",
        "evals": state / "evals",
        "tmp": state / "tmp",
        "evidence": state / "evidence",
    }
    if sprint is not None:
        root = state / "evidence" / f"sprint-{sprint}"
        paths.update({
            "sprint_evidence": root,
            "commands": root / "commands",
            "screenshots": root / "screenshots",
            "browser": root / "browser",
            "axe": root / "axe",
            "lighthouse": root / "lighthouse",
            "source": root / "source",
            "api": root / "api",
            "git": root / "git",
            "artifacts": root / "artifacts",
        })
    for path in paths.values():
        path.mkdir(parents=True, exist_ok=True)
    return paths
```

All code that writes files must receive paths from this helper. Do not concatenate ad hoc
artifact paths in agents.

## Command Output Capture

Never let build/test output spill into random files. Use a helper:

```python
def run_recorded(cmd: list[str], cwd: Path, out_dir: Path, name: str, timeout: int = 900) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    started = time.time()
    result = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True, timeout=timeout)
    record = {
        "cmd": cmd,
        "cwd": str(cwd),
        "returncode": result.returncode,
        "seconds": round(time.time() - started, 2),
        "stdout_path": str(out_dir / f"{name}.stdout.txt"),
        "stderr_path": str(out_dir / f"{name}.stderr.txt"),
    }
    Path(record["stdout_path"]).write_text(result.stdout)
    Path(record["stderr_path"]).write_text(result.stderr)
    (out_dir / f"{name}.json").write_text(json.dumps(record, indent=2))
    return record
```

## Retention Policy

Add a cleanup step at startup:

- Keep all current sprint artifacts.
- Keep the last N run logs (`workspace.keep_last_runs`, default 10).
- Keep the last N evidence folders per sprint (`workspace.keep_last_evidence_per_sprint`, default 3).
- Delete `harness-state/tmp/**` at the start of each run unless `--keep-tmp` is set.

## Public Evidence Surfaces

Avoid public evidence routes/files. If a sprint truly needs one:

1. Declare it in the sprint contract under `evidence.public_routes`.
2. Include why browser-only evidence is insufficient.
3. Add a cleanup criterion or follow-up sprint.
4. Prefix route/file names consistently, e.g. `/__harness/sprint-N/...`.

Do not create one-off `public/__sprint-*` or `src/app/api/sprint-*` artifacts unless the
contract explicitly permits them.

## Verification Before Completion

Before saying the harness is ready, verify:

```bash
find . -maxdepth 2 -type f \
  \( -name '*lighthouse*' -o -name '*axe*' -o -name '*screenshot*' -o -name '*eval*' \) \
  -not -path './harness-state/*' \
  -not -path './harness-logs/*'
```

Any result is a workspace hygiene bug unless it is declared product output.
