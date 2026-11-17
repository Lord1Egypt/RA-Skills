# Offline packages

Two profiles share one envelope, one set of commands, and one set of refusal
categories:

| Profile | `schema_version` | Carries |
| --- | --- | --- |
| Source-only | `glr.source-package.v1` | one flat, source-only file list (ADR-0027) |
| Group-scoped | `glr.training-package.v1` | `source` plus optional `model`, `dataset`, `knowledge` and `report` groups (ADR-0041) |

A package is a file list plus digests. It never carries a virtual environment,
an interpreter, a cache, a run store, or a dependency, and GLR never resolves,
downloads, installs, or executes anything. `source` is the only group allowed by
default; every other group is deny-by-default and needs a declared group, a
group-scoped role, an extension allowlist, and a group-specific proof.

For a trained-stage installer, follow the project's `USER_RELEASE.md` or the
sibling adapter-builder `references/user-releases.md`. That uses a separately
prepared runtime and model bundle; this contract is unchanged by it.

## Commands

```powershell
glr --project PROJECT --json package plan --manifest selection.json
glr --project PROJECT --json package export --manifest selection.json --output source.zip
glr --json package inspect source.zip
glr --json package import source.zip --destination NEW_DIRECTORY --expected-environment ENVIRONMENT_ID --expected-contract SHA256
glr --project NEW_DIRECTORY --json package conformance source.zip
```

1. Select individual files and review their contents and redistribution rights.
   Exclude secrets, host paths, private endpoints and recipient-local overrides.
   Extension checks are not a secret scanner. Include exactly one project
   manifest, the dependency locks, and the source needed to explain and
   reproduce the project. **Discovery never recurses a workspace**: there is no
   "package this directory" mode.
2. Write a selection file in one of the two strict shapes below. The project owns
   the contract SHA-256 over observation/action/reward/knowledge and
   ruleset/content identity; do not invent a fingerprint from the package name.
3. `plan` is a dry run: review the exact inventory, sizes, digests, groups and
   audit entries before export. It hashes bytes and compresses nothing, so a
   plan and the export it previews carry the same `content_sha256`.
4. `export` writes the archive. An existing output is refused. A new archive is
   deterministic for identical inputs.
5. The recipient runs `inspect` offline. Inspection verifies the envelope, every
   declared size and digest, and every group admission predicate. It deserializes
   nothing — a weight, checkpoint or trajectory payload is bound by size and
   digest only.
6. The recipient runs `import` into a directory that does not exist yet, whose
   parent does. `--expected-environment` and `--expected-contract` must come from
   the reviewed handoff, never from the untrusted package itself. Import stages
   beside the destination and promotes with one atomic no-replace rename, so a
   refused or interrupted import leaves an existing project untouched.
7. Recreate dependencies from the lock through VX as a separate, authorized step.
8. The recipient runs `conformance` offline. Add `--expected-environment` and
   `--expected-contract` to re-assert the reviewed handoff at this gate. A nested
   working directory resolves upward to the project manifest. Exit `0` means the
   synthetic conformance check passed; `4` means reproduction is blocked and
   `blockers` explains why.

## Entry groups, roots, and limits

Group ownership is a package-root directory. A path under a group root whose
group is not declared is a **refusal**, which is what makes deny-by-default
mechanical. Every group-scoped package declares `source`.

| Group | Root | Compression | Max files | Max per file | Max group bytes | Roles |
| --- | --- | --- | --- | --- | --- | --- |
| `source` | everything else | `stored` | 1,024 | 16 MiB | 128 MiB | `project-manifest`, `dependency-lock`, `source-file` |
| `model` | `models/` | `deflated` | 64 | 1 GiB | 4 GiB | `model-manifest`, `model-input`, `model-artifact` |
| `dataset` | `data/` | `deflated` | 512 | 1 GiB | 4 GiB | `dataset-manifest`, `dataset-payload` |
| `knowledge` | `knowledge/` | `deflated` | 256 | 64 MiB | 256 MiB | `knowledge-snapshot` |
| `report` | `reports/` | `deflated` | 64 | 16 MiB | 64 MiB | `aggregate-report` |

Two ceilings sit above the per-group caps and are what a recipient actually
pays for: **1,024 files** and **4 GiB** expanded per package. The file ceiling
equals the archive member gate, so a package can never contain more files than
an archive may carry.

A role is an assertion the exporter makes, not a label GLR infers: a declared
role that disagrees with its path or its group is a refusal. Roles grant no
behavior and are never an execution hint.

## Per-group admission proofs

| Group | Proof required in addition to the extension allowlist |
| --- | --- |
| `model` | exactly one `model-manifest` named `manifest.json` at the bundle root, verifying as `glr.model-bundle.v1` for the *same* `environment_id` and `protocol_version`, with non-empty seeds, inputs and artifacts; every other model file must be declared by that bundle, under `inputs/` or `artifacts/` as its role states |
| `dataset` | a reviewed `glr.dataset-allowlist.v1` naming each exact path (`reviewed_by`, `review_date`, `entries`), **and** a recorded `glr.redistribution-authorization.v1` (`approver`, `scope`, `license`, `date`), **and** a `glr.demonstration-artifact.v1` manifest binding every payload by size and digest with an allowed origin and outcome |
| `knowledge` | a `glr.knowledge-snapshot.v1` file, validated against the wall clock and a declared `max_age_days` that the knowledge group must carry; a snapshot stamped in the future is refused, and a group with no declared budget is refused. `max_age_days` must be a **positive** integer — the CLI refuses `0` and enforces **no upper bound**, so treat an implausibly large budget as a review finding rather than expecting a refusal |
| `report` | aggregate outputs only (`json`, `md`, `csv`); a path component named `trajectory`, `trajectories`, `episodes`, `episode`, `recordings`, `logs`, `runs` or `raw` is refused by name as well as by type |

Refused for every group: the deserializer-only formats `pkl`, `pickle`,
`joblib`, `npy`, `npz`, `dill`; a path component that is empty, dot-prefixed, or
one of `target`, `node_modules`, `recordings`, `screenshots`, `logs`,
`datasets`, `secrets`, `credentials`, `cache`, `.glr`; and any recipient-local
override form.

Nothing is deserialized. Only a declared manifest or snapshot is ever read into
memory, and only under an 8 MiB inspection cap.

## Selection shapes

Source-only (`glr.source-package.v1`) — one flat file list:

```json
{
  "schema_version": "glr.source-package.v1",
  "package_version": "1.0.0",
  "required_glr": ">=0.18.0, <1.0.0",
  "environment_id": "synthetic.example",
  "protocol_version": "1.0",
  "contract_sha256": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
  "source_revision": "reviewed-source-revision",
  "redistribution_license": "MIT",
  "files": ["glr-project.toml", "pyproject.toml", "uv.lock", "train.py"]
}
```

Group-scoped (`glr.training-package.v1`) — declared groups, each with its own
files, roles, and admission records:

```json
{
  "schema_version": "glr.training-package.v1",
  "package_version": "1.0.0",
  "required_glr": ">=0.18.0, <1.0.0",
  "environment_id": "synthetic.example",
  "protocol_version": "1.0",
  "contract_sha256": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
  "source_revision": "reviewed-source-revision",
  "redistribution_license": "MIT",
  "entry_groups": ["source", "report"],
  "groups": {
    "source": {
      "files": [
        {"path": "glr-project.toml", "role": "project-manifest"},
        {"path": "uv.lock", "role": "dependency-lock"},
        {"path": "train.py", "role": "source-file"}
      ]
    },
    "report": {
      "files": [
        {"path": "reports/round-summary.json", "role": "aggregate-report"}
      ]
    }
  }
}
```

A `dataset` export adds `dataset_allowlist` and `redistribution_authorization`
at the selection root; a `knowledge` group adds `max_age_days` beside its
`files`. Every struct denies unknown fields, so an unknown group, role, field,
or schema version fails closed at parse time.

The `a` fingerprint above is a synthetic placeholder, not a usable compatibility
receipt. Read CLI help from the installed version: source changes do not update
an installed CLI.

## Recipient conformance

`glr package conformance` checks a package that is already materialized on disk.
It reads and hashes bytes; it never runs a role, hook, installer or trainer, and
it never installs, resolves, or fetches anything. The report keeps its axes
independent, so a passing check is a statement about the package and the
destination tree — never about training:

| Field | Meaning |
| --- | --- |
| `status`, `offline`, `executed` | `synthetic-conformance`, `true`, `false`. |
| `package.valid` | The archive verified offline: identity, inventory, sizes and digests. |
| `package.groups` | Per-group rollup: declared, file count, bytes, admission, and the checks that ran. |
| `audit` | `glr.package-audit.v1`: one record per admitted file (`path`, `group`, `role`, `size_bytes`, `sha256`, `admitted_by`), plus the authorization and allowlist when a `dataset` export carried them. |
| `materialization` | `complete` / `incomplete`, with `missing`, `mismatched` and `unexpected` path lists. |
| `local_overrides` | Recipient-local files matching `*.local.*` or `*.local` in any path component, reported and never merged. |
| `artifacts.run_store`, `artifacts.forbidden` | A denied cache, output or run-store path is present in the destination. |
| `dependency_setup` | `declared` or `missing`; `performed` is always `false`, and the `lock_files` are named. |
| `prerequisites` | Declared role and task programs that must already exist; each carries `available`, `blocker` and a `remediation` string. Never fetched. |
| `blockers` | One record per blocked axis, each with `kind`, `detail` and `remediation`. |
| `axes` | `package_validity`, `materialization`, `dependency_setup`, `synthetic_reproduction`, then `training`, `live_acceptance` and `policy_quality` as `not-evaluated`. |
| `claims.training_succeeded`, `training_performed`, `training_ready` | Always `false`. |

Exit code `0` means `axes.synthetic_reproduction == "pass"`; `4` means
reproduction is blocked. Read `blockers` before reporting either one.

**Local overrides.** The patterns `*.local.*` and `*.local` match **per path
component**, not on the whole path string, and the export gate and the
conformance scan share one predicate. `glr-project.local.json` and a directory
component ending in `.local` — for example `a.local/b.json` or
`a.local/sub/b.json` — are refused by the export allowlist, so a package never
carries them. In the materialized destination the conformance scan reports them
under `local_overrides.present_in_destination` and ignores them; it never merges
them into the project (ADR-0021). Supplying them is a separate, explicit
recipient action.

**Missing prerequisites.** An unavailable role or task program is a blocker with
a `remediation` string, not permission to download a game, install a provider SDK
or launch training. A blocked reproduction is still reported as a valid,
completely materialized package.

## Refusals and error categories

Every refusal is a contract violation with a stable category and a nonzero exit,
never a warning that lets an export or import continue. The message is prefixed
`source package:` for the shared envelope and `training package:` for a group
admission predicate; both surface as `contract violation: …`, with
`error_type` `ContractViolation` in `--json` output. A refusal never leaves a
partial archive, a partial destination, or an unbounded receipt.

Categories you will actually see:

- `non-portable path component` / `path exceeds portable limits` — traversal,
  absolute, drive/UNC or device form, a dot-prefixed or Windows-reserved
  component, more than 16 components, more than 240 bytes, or non-ASCII.
- `source-only allowlist excludes this path` — the extension or a denied
  component is not admitted for `source`.
- `carries a denied path component`, `{group} allowlist excludes …`,
  `needs a deserializer that import must never run`, `has no extension and
  cannot be admitted` — a group admission predicate refused one file. A global
  denied component is reported before the group-specific one, so
  `reports/logs/x.json` is refused as a denied component rather than as a raw
  log, while `reports/trajectory/x.json` reaches the report-specific message.
- `{path} belongs to the {group} group, which this package does not declare` —
  content under an undeclared group root.
- `unsupported schema or file count` — an unknown `schema_version`.
- `incompatible GLR version` — `required_glr` does not match this CLI.
- `environment or contract fingerprint mismatch` — `--expected-environment` or
  `--expected-contract` disagrees with the package.
- `destination already exists` — import never replaces a project.
- `archive size limit exceeded`, `{path} expands {ratio}x, past the 200:1
  ratio cap`, and the expanded-size refusals — an archive bomb or an over-cap
  group, refused before any expanded byte is written. The ratio is computed as
  `size_bytes / compressed`, so the `200` is `MAX_EXPANSION_RATIO`; a zero
  compressed size skips the check.
- `a model group needs exactly one model-manifest`, `is not declared by the
  model bundle`, `was trained for … and cannot join a package for …` — model
  verification failed.
- `is not on the reviewed dataset allowlist`, `is a dataset payload that no
  demonstration manifest binds` — dataset authorization or provenance failed.
- `a knowledge group must declare max_age_days so freshness is reviewable`,
  `knowledge max_age_days must be positive`, `is stamped in the future` —
  freshness or snapshot validation failed. A `max_age_days` on any group other
  than `knowledge` is refused with `max_age_days only applies to the knowledge
  group, not {group}`.
- `is a raw log, recording or trajectory, not an aggregate` — a `report` path
  component or type is not an aggregate.

## Trust boundaries to report separately

Package validity, dependency setup, synthetic reproduction, live acceptance and
policy quality are independent results, and a skill or report that collapses them
is wrong:

- **A valid package is not a successful training run.** `claims.training_succeeded`
  is always `false`, and `training_ready` is `false` on import.
- **A checksum proves integrity, not trust.** It attests that the bytes you
  received are the bytes that were exported. It says nothing about the publisher
  or about model quality.
- **A verified `glr.model-bundle.v1` proves artifact identity and config parity,
  not policy quality, hardware determinism, or live gameplay.**
- **A passing `conformance` proves the environment and protocol match and the
  declared files materialized.** It does not prove that a role ran, that a
  prerequisite exists, or that reproduction succeeded; missing prerequisites are
  blockers on their own axis.
- **Import does not authorize setup, execution, or deployment.** Setup is a
  separate, authorized recipient action, taken after the trust and compatibility
  checks.
- **Portability.** Public receipts, manifests and archives use portable selected
  paths only. Never echo a source-machine root, and never put a credential,
  private endpoint, account, or process/window identifier into a package or a
  receipt.

## Wire schemas

- `docs/schemas/source-package.schema.json` and
  `source-package-selection.schema.json` — `glr.source-package.v1`, unchanged.
- `docs/schemas/training-package.schema.json` and
  `training-package-selection.schema.json` — `glr.training-package.v1`.
- `docs/schemas/package-audit.schema.json` — `glr.package-audit.v1`.

Decisions: ADR-0027 (offline source-only project packages) and ADR-0041
(portable training packages as group-scoped, non-executing envelopes) in the
repository's `docs/decisions/`. The staged delivery plan is
`docs/planning/training-package-phases.md`. A Skill bundle ships standalone, so
these are repository references to read in a checkout — resolve them there, not
relative to this file.
