# YAML Schemas Reference

Complete field definitions for all five persistence files.
Load this file when you need to validate or extend the YAML structures.

---

## migration-state.yaml

| Field | Type | Description |
|-------|------|-------------|
| `meta.source_lang` | string | Source programming language (lowercase) |
| `meta.target_lang` | string | Target programming language (lowercase) |
| `meta.source_dir` | string | Relative path from workspace root to source project |
| `meta.target_dir` | string | Relative path from workspace root to translated output |
| `meta.lang_pair_module` | string | Key used to load `references/lang-pairs/<key>.md` |
| `meta.source_version` | string | Git commit/tag of source; ensures reproducible baseline |
| `phases.*` | enum | `TODO \| IN_PROGRESS \| DONE` |
| `current_task.status` | enum | `TODO \| IN_PROGRESS \| DONE \| BLOCKED` |
| `current_task.block_reason` | string | Machine-readable summary of why task is blocked |
| `current_task.human_input_required` | string | Human-readable question to resolve block |
| `decisions_log` | list | Audit trail; append every human decision here |
| `phase_gates.*` | object | PGR tracking block; one entry per gate (PGR_0 through PGR_5) |

---

## `phase_gates` Block

The `phase_gates` block in `migration-state.yaml` tracks the Phase Gate Review (PGR) state for each
phase transition. It is updated automatically by the PGR loop. See `references/phase-gate-review.md`
for the full protocol.

| Field | Type | Description |
|-------|------|-------------|
| `phase_gates.PGR_N.status` | enum | `TODO \| IN_PROGRESS \| PASSED` — current state of this PGR gate |
| `phase_gates.PGR_N.iteration_count` | integer | Number of audit loops completed (0 = not yet started; >1 = findings were found and fixed) |
| `phase_gates.PGR_N.findings_resolved` | integer | Cumulative count of findings fixed across all iterations |
| `phase_gates.PGR_N.passed_at` | string | ISO 8601 timestamp when the gate achieved zero findings; empty until PASSED |
| `phase_gates.PGR_N.last_report` | string | One-line summary of the final audit result, e.g. `"PGR-1 PASSED: 47 items checked, 3 findings resolved over 2 iterations"` |

### Invariants

- `status: PASSED` requires `passed_at` to be non-empty. A gate with `status: PASSED` and
  empty `passed_at` is an integrity violation — the session start protocol must detect and re-run it.
- The corresponding `phases.PN_xxx: DONE` must only be set by the PGR loop as the final action
  of a `PASSED` gate. Never set `DONE` directly in phase handling code.
- `iteration_count` is incremented once per full fix-and-re-audit cycle, not once per finding.
  An `iteration_count` of 1 with a large phase output should be treated with suspicion
  (see Rule PGR-AC-5 in `references/phase-gate-review.md`).
- `findings_resolved` is cumulative across all iterations. If iteration 1 fixes 3 findings and
  iteration 2 fixes 1 more, `findings_resolved` ends at 4.

### Example (after PGR-1 passes on second iteration)

```yaml
phase_gates:
  PGR_1:
    status: PASSED
    iteration_count: 2
    findings_resolved: 4
    passed_at: "2024-11-15T14:32:07Z"
    last_report: "PGR-1 PASSED: 52 items checked, 4 findings resolved over 2 iterations"
```

---

## asset-inventory.yaml

### `type` values

| Value | Meaning |
|-------|---------|
| `source_code` | Compilable/interpretable source file |
| `test_code` | Test file (unit, integration, e2e) |
| `test_fixture` | Data file consumed by tests |
| `build_config` | Makefile, CMakeLists, build.gradle, pyproject.toml, etc. |
| `ci_config` | GitHub Actions, GitLab CI, Jenkinsfile, etc. |
| `documentation` | README, docs/, wiki, algorithm notes |
| `asset_binary` | Binary files (images, compiled artifacts, .npy, etc.) |
| `asset_text` | Non-code text assets (templates, SQL schemas, proto files) |
| `dependency_manifest` | requirements.txt, Cargo.toml, go.mod, package.json |
| `environment_config` | .env, .env.example, docker-compose.yml, Dockerfile |
| `script` | Shell scripts, utility scripts |
| `other` | Anything not covered above — always explain in `notes` |

### `migration_strategy` values

| Value | Action |
|-------|--------|
| `translate` | Rewrite in target language; creates new file at `target_path` |
| `adapt` | Keep general structure, rewrite language-specific parts (CI, build) |
| `direct_use` | Copy byte-for-byte; target code reads it as-is |
| `preserve` | Include in target project unchanged; role may be clarified later |
| `reference_only` | Not migrated; must be read during P3 (docs, algorithm notes) |
| `generated` | Target toolchain generates this automatically (lock files, etc.) |

---

## ecosystem-map.yaml

### `category` values

| Value | Examples |
|-------|---------|
| `type` | int, float64, numpy.float32, uint8 |
| `stdlib` | os.path, collections.OrderedDict, io.BytesIO |
| `third_party` | numpy.ndarray, requests.Session, sqlalchemy.Column |
| `idiom` | list comprehension, generator expression, decorator pattern |
| `runtime_behavior` | GIL, GC timing, dict iteration order, integer overflow |

### `precision_delta` values

- `none` — identical precision
- `narrower` — target type has less precision (document max acceptable error)
- `wider` — target type has more precision (generally safe, document anyway)
- `different_representation` — same bit width but different semantics (e.g., IEEE vs fixed-point)

---

## ipo-registry.yaml

### `magic_numbers.origin` values

| Value | Meaning |
|-------|---------|
| `documented` | Explained in comments, docstring, or referenced document |
| `inferred_from_context` | AI derived meaning from usage pattern; not stated explicitly |
| `unknown` | Cannot determine purpose; flag for human review |

### `side_effects` format

List strings describing each side effect:
```yaml
side_effects:
  - "writes to file: {path_param}/output.csv"
  - "mutates: self.cache (dict)"
  - "reads env var: DATABASE_URL"
  - "network: GET https://api.example.com/data"
```

### `inferred_invariants` format

Assumptions the code makes but does not assert:
```yaml
inferred_invariants:
  - "caller guarantees sum(data) ≈ 1.0 (not checked)"
  - "input list is non-empty (would divide by zero otherwise)"
  - "file at path is UTF-8 encoded (no encoding specified)"
```

### `known_source_behaviors` format

Behaviors in the target code that are sometimes mistaken for bugs during P5 verification,
but actually faithfully reproduce the source code's design. Populated during P5 triage
when T2 verdict is `source_matches_target: true`.

```yaml
known_source_behaviors:
  - desc: "Returns nil on cache miss instead of raising an error — callers must guard"
    source_file: "cache.py"
    source_lines: "47-52"
    intentional: true       # true = deliberate design choice in source
                            # false = source has a bug; target faithfully reproduces it
    annotation_added: true  # SOURCE-FAITHFUL comment added in target code
    annotation_location: "internal/cache/cache.go:89"
    human_decision_required: false   # only true when intentional: false (source bug)
```

**`intentional: false` triggers a BLOCK**: if the source has a genuine bug and the target
faithfully reproduces it, a human must decide whether to fix source + re-run P3, or accept
the known deviation. The block must not be silently resolved by the AI.
