# PR / Issue Scope Expansion

When new findings emerge during in-progress work, decide whether to **expand** the existing PR/issue or **split** into a separate one — and update title/body accordingly.

## When to Use

- Mid-implementation, you discover an additional change required to make the original work coherent (e.g., a config refactor, a structural fix, a related bug)
- The new finding shares the same blast radius as the in-progress work (same files, same review context, same deploy unit)
- The user says "expand the PR/issue", "widen the scope", "include that too", or rejects splitting

**Anti-pattern (the "nickel-and-dime" pattern)**: Defaulting to "small PR is good" and pushing every related fix into a follow-up PR or "post-merge cleanup". Small ≠ correct. Coherence matters more than line count.

## Decision Matrix — Expand vs Split

Use this table to decide:

| Signal | Expand current PR/issue | Split into new PR/issue |
|---|---|---|
| Same file or directly coupled file | ✅ | |
| Required for the original work to verify end-to-end | ✅ | |
| Same deploy unit / same release window | ✅ | |
| Reverting one without the other leaves broken state | ✅ | |
| User said "include it" or "expand" | ✅ | |
| Different reviewer / domain expertise needed | | ✅ |
| Different release cadence | | ✅ |
| Independent of original work (could ship alone) | | ✅ |
| Adds significant unrelated diff (>100 LOC + different concern) | | ✅ |

**Default bias**: when in doubt, **expand**. The cost of splitting too eagerly (post-merge cleanup, forgotten follow-ups, broken coherence) is higher than a slightly larger PR.

## Mandatory Procedure (Expansion)

When you decide to expand, **all four steps are required** — partial expansion (commit added but title/body stale) is a violation:

### 1. Commit the new change in the same branch

Add the new finding's commits to the existing PR's branch. Do not create a separate branch.

### 2. Update the PR/issue title

The title must reflect the **expanded scope**, not the original narrow scope.

```bash
gh pr edit <N> -R <repo> --title "<expanded title>"
gh issue edit <N> -R <repo> --title "<expanded title>"
```

Title pattern: `<type>(<scope>): <primary work> + <expansion>` or restructure entirely if the scope shifted.

### 3. Update the PR/issue body

The body must:
- Add the new finding to the **Summary / Changes** section
- Update the **Test Plan** with new verification items (and check off completed ones)
- Add to **Files to modify** or equivalent
- Update **Relates to** with any new linked issues

```bash
gh pr edit <N> -R <repo> --body-file <updated-body>
gh issue edit <N> -R <repo> --body-file <updated-body>
```

### 4. Cross-link in linked issues / epic

If the PR is linked to an epic or other issues, update those bodies too — the expanded scope changes what they track.

## Examples

### Example 1: PR scope expansion (infra repo, integration apply)

**Original PR scope**: integration terraform apply (namespace rename for an internal project)

**Discovered mid-work**:
- `secrets.production.auto.tfvars` leaks into all env plans (structural defect)
- A shared module needs additional variables to preserve imported values for two downstream projects
- The main repo's `secrets.*.auto.tfvars` should be renamed to `secrets.*.tfvars`

**Wrong approach** (the "nickel-and-dime" pattern):
- PR = code changes only (Makefile, .gitignore, module.tf, variables.tf)
- "The secrets rename happens after this PR merges"
- Title stays narrow: "fix(PAM): integration apply"

**Correct approach** (expansion):
- PR = all 4 changes bundled (code + secrets rename + import preservation + secrets defect fix)
- Title updated: `fix(PAM): integration apply + module import preservation + secrets auto-load defect fix`
- Body updated: Summary + Test Plan + Files to modify all reflect 4 areas
- Reason: all four changes share the same blast radius (the IaC directory) and the original work's verification (`make plan ENV=integration` clean) requires all four

### Example 2: Issue scope expansion

**Original issue**: "fix(PAM): apply OAuth Source rename to dev-A environment (follow-up to #306)"

**Discovered**: dev-A also needs VPN URL config + automation-template arg update + `dt-source-auto-redirect` flow rename impact.

- Update issue title: `fix(PAM): apply OAuth Source rename in dev-A + adjacent environment hardening (follow-up to #306)`
- Update issue body: add discovered scope to Verification table
- Cross-link epic: epic body's Phase 4 row updated to reflect expanded scope

## Forbidden — Cleanup-Deferral Pattern

These phrases are red flags that you are splitting when you should be expanding:

- "Do X after the PR merges"
- "X as a follow-up PR"
- "Stage A in this PR, Stage B as a separate issue"
- "Code now, cleanup later"

If the deferred work is required for the original work to be **complete and verifiable**, it belongs in this PR. Use this skill's decision matrix to challenge the deferral instinct.

## Title/Body Update Checklist (HARD STOP)

Before marking expansion complete, verify all of these:

- [ ] Commits added to existing branch (not a separate branch)
- [ ] PR/issue title updated with `gh pr edit` / `gh issue edit`
- [ ] PR/issue body Summary section reflects expanded scope
- [ ] Test Plan items added/updated for new findings
- [ ] Files to modify list updated
- [ ] Linked epic/parent issue body updated if scope changed
- [ ] Cross-references (`Relates to #N`) added for newly linked issues

Skipping any of these = "expanded the work but left metadata stale" — the same coherence loss the expansion was meant to prevent.

## Cross-references

- `code-workflow` Step 4 (Implement) — call this skill the moment a new finding emerges, not after PR is created
- `pr` topic (`pr.md`) — initial PR creation. Use `expand` when adding to an existing PR mid-work
- `plan-to-issue` topic — initial issue body. Use `expand` when issue scope grows during implementation
- `commit-tidy` — handles commit-level split/squash. `expand` handles PR/issue-level scope decisions
