# Governance

How this project makes decisions. Short on purpose — the project is small, and a
governance document nobody reads is worse than none.

## Roles

| Role | Who | Does |
|---|---|---|
| Maintainer | `@JohnSmithfan` | Merges, cuts releases, owns the licence surface |
| Contributor | anyone | Opens issues and PRs |

There is no formal election. A contributor who has landed a sustained run of
merged work and reviews gets write access by maintainer invitation.

## What the maintainer owns exclusively

- `LICENSE` and `LICENSES/` — the dual-licence model (GPL-3.0 infrastructure /
  CC BY-NC-SA 4.0 generated content) is a legal surface, not a preference
- `SECURITY.md` contact channel
- `GOVERNANCE.md` itself
- Cutting a release tag

Everything else is open to PR.

## Decision process

1. **Proposal** — issue (feature request, errata, or docs) with the problem stated
   before the solution.
2. **Discussion** — open for at least 7 days for anything that changes a module
   contract or a script's CLI.
3. **Decision** — maintainer decides. Silence is not consent; an undecided proposal
   stays open.
4. **Record** — the outcome goes in `CHANGELOG.md`. A decision that is not recorded
   will be re-litigated next month.

### Tie-breakers, in order

1. Does it break an existing subproject? If yes, it does not ship without a
   migration note.
2. Does it match what field use actually settled on? `references/subproject-playbook.md`
   wins over `SKILL.md` when they disagree.
3. Does it keep every file reviewable in a diff?

## Changing the Skill contract

`SKILL.md` and the `modules/*/SKILL.md` files define agent behaviour. A change there
affects every subproject at once. Required before merge:

- [ ] The change is described in terms of the problem, not just the new wording
- [ ] `SUBPROJECTS.md` impact noted — which registered subprojects are affected
- [ ] Version bumped (see below)

## Versioning

Semantic Versioning:

| Change | Bump |
|---|---|
| Breaking change to a module contract or script CLI | MAJOR |
| New module, script, or capability | MINOR |
| Docs, errata, hygiene | PATCH |

Every SKILL.md file carries the same `version` field. They are bumped together —
a version skew between `SKILL.md` and `modules/` is a defect.

## Adding a script

Scripts are shared infrastructure consumed by every subproject:

1. Lives in `scripts/`, `_` prefix if it is an internal helper
2. Takes the project root from the current working directory, `--root` to override
3. Writes text with `newline='\n'`
4. No absolute paths to any subproject
5. Listed in `scripts/README.md`, and in `SUBPROJECTS.md` for the subprojects that use it
6. Ships with tests in `tests/` — a script without a test is a script nobody can change safely

## Branch protection

`main` is protected. A push straight to it is rejected; every change arrives as
a pull request. Required before merge:

- The `CI` workflow is green (hygiene, references, tests, metadata)
- One approving review, requested automatically by `CODEOWNERS`
- Force push and branch deletion disabled

These are settings, not files, so they cannot live in this repository. They are
recorded here because a CODEOWNERS file without them requests reviewers who can
be ignored.

## Issue responsiveness

Labels are the taxonomy (`.github/labels.yml`, synced by the `label-sync`
workflow). Targets, not guarantees:

| Label | First response |
|---|---|
| `bug` | 7 days |
| `security` | 48 hours, privately |
| `enhancement`, `docs` | 30 days |

The `stale` workflow closes an issue that has had no activity for 60 days and
no label that pins it open.

## Code of conduct

[CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) applies to every space this project uses.
Reports go to the maintainer privately.
