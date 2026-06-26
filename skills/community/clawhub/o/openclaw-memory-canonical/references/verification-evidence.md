# Verification Evidence — openclaw-memory-canonical v4.6.14

Date: 2026-04-14
Host: /home/irtual/.openclaw/workspace

This evidence reflects the final accepted state after a fresh full 10-round rerun from the v4.6.13 baseline.

## Host-level practical evidence
- `bash skills/openclaw-memory-canonical/scripts/health-check.sh` on the real workspace during final publish preparation returned FAIL only because the live `memory/working-buffer.md` in this active session was 135 lines (`>80`), while the header itself remained valid.
- That observed FAIL was treated as current host/session state, not as a new packaged-skill defect in `openclaw-memory-canonical`, because the accepted 10-round review found no new runtime, recovery, or contract seam inside the skill artifact itself.
- Conclusion: this line is an honest release-surface refresh after a fresh 10-round convergence pass, not a functional runtime change release.

## Orchestrator evidence used in this revision
- Qwen Orchestrator dry-run succeeded before the rerun.
- AI Orchestrator dry-run succeeded before the rerun.
- This rerun executed as a fresh full 10-round alternating review.
- Round 1 (AI Orchestrator / DeepSeek): identified release-honesty drift as the strongest seam; no runtime/script patch justified.
- Round 2 (Qwen): agreed the main seam was release-honesty refresh for a new rerun/publish line and proposed an additional `Tag Vocabulary (Frozen)` wording change.
- Round 3 (AI Orchestrator / DeepSeek): rejected the `Frozen vocabulary` rename as non-material wording churn and kept only the deferred release-surface refresh.
- Round 4 (Qwen): repeated the already-rejected wording seam instead of engaging the accepted synthesis; treated as session pollution rather than a new artifact seam.
- Round 5 (AI Orchestrator / DeepSeek): confirmed no stronger seam existed beyond deferred release-honesty refresh.
- Round 6 (Qwen recovery session): converged on the accepted synthesis and confirmed no stronger seam existed.
- Rounds 7-10 (DeepSeek / Qwen / DeepSeek / Qwen): all confirmatory only; no new material runtime, recovery, package-hygiene, or weak-model-execution seam was found.

## Accepted changes in this rerun
1. No runtime or contract patch was justified.
2. No package-hygiene or script-behavior patch was justified.
3. The only accepted change in this release is honest refresh of version/changelog/evidence/test-log surfaces to record the completed 10-round rerun from the v4.6.13 baseline.

## Release-scope validation target
This release focuses on:
1. recording the completed fresh 10-round no-new-fix convergence result
2. preserving an honest distinction between live host-session state and packaged-skill defects
3. publishing a newer line only as explicit release-surface refresh evidence, not as fake functional churn
4. keeping package metadata and publish evidence synchronized with the actual reviewed state

## Deterministic package validation
- Generated `references/package-tree.sha256` after the latest accepted metadata/evidence update set with:
  - `cd skills/openclaw-memory-canonical && find . -type f -not -path './.clawhub/*' -not -path './.logs/*' -not -path './.sessions/*' -not -path './.profile/*' -not -path './node_modules/*' -not -path './dist/*' -not -path './references/package-tree.sha256' -not -name '*.tmp' -not -name '*.pending' -not -name '*.lock' | sort | xargs sha256sum > references/package-tree.sha256`
- Important detail: the hash list excludes `references/package-tree.sha256` itself to avoid self-referential drift.
- Purpose: deterministic package-tree snapshot aligned with publish-scope exclusion rules before ClawHub publication.
