# Support File Map

Full index of every reference and script bundled with `ocas-skilllab`, with a
conditional **When to read** column so the agent loads only what each operation needs.

| File | When to read |
|------|-------------|
| `references/skilllab-frontmatter-standards.md` | During D1 audit — full frontmatter requirements, optional fields, anti-patterns |
| `references/skilllab-pitfalls.md` | During any skilllab operation — 60+ pitfalls covering batch replace, YAML errors, caching |
| `references/audit-2026-05-30.md` | May 2026 audit — fixes, grep false-positive lesson, remaining issues |
| `ocas-forge/references/auto-generated-skill-cleanup.md` | Before deleting auto-generated skill thin wrappers |
| `references/merge-session-2026-05-29.md` | May 2026 merge/cleanup session historical reference |
| `references/skill-publish-spec-compliance-checklist.md` | When auditing skills against agentskills.io spec |
| `references/skill-publish-github-push-recipe.md` | When publishing a new skill repo to GitHub |
| `references/skill-publish-github-sync-existing-skills.md` | When bulk-syncing local skills to existing GitHub repos |
| `references/skill-publish-agentskill-evaluation-criteria.md` | When evaluating skill quality/security scores |
| `references/skill-sanitize-checklist.md` | Post-sanitize verification checklist + scanner false-positives |
| `scripts/secret-scan.sh` | Secret-scan gate — scans working tree + .git/config + full history; exits 1 if secrets found |
| `references/mempalace-gotchas.md` | MemPalace MCP tool constraints — kg_add character rejections, drawer vs. KG guidance |
| `references/audit-2026-06-05.md` | June 2026 audit — git merge conflict repair, cross-profile write guard, remaining author gaps |
| `references/audit-2026-06-18.md` | June 2026 audit — full library scan, 94 skills, 26 missing authors, YAML errors, orphaned refs |
| `references/critique-rubric.md` | During Phase 2 scoring — full 10-dimension rubric |
| `references/critique-issue-categorization.md` | During Phase 3 — Critical/Major/Minor rules |
| `references/critique-assessment-mode.md` | Before assessment — decision table for assess vs. fix |
| `references/critique-audit-checklist.md` | During Phase 6 — quick-pass compliance checklist |
| `references/critique-improvement-plan-template.md` | During Phase 4 — plan format and examples |
| `references/critique-usage-examples.md` | Before executing critique commands — score table format, code ratio |
| `references/critique-quick-reference.md` | Before executing — full command table |
| `references/critique-standard-headings.md` | During Phase 1 — required heading names and common non-standard variants |
| `references/critique-inline-to-refs-pattern.md` | Before Phase 5 — moving inline content to references |
| `references/critique-agentic-script-pattern.md` | During D9 assessment — checklist for script quality |
| `references/nous-skill-requirements.md` | During D1 audit — official Hermes skill system requirements from Nous Research docs |
| `references/critique-agentskill-scanner-guide.md` | After manual review — scanner false positives |
| `references/design-library.md` | When building any UI — design reference library (glitch aesthetic, DESIGN.md spec, 72 brand systems, 67 styles, 200 iOS apps, taste-skill anti-slop enforcement), usage guide, refresh commands |
| `$HERMES_HOME/../indigo/skills/responsive-design/references/` | Responsive CSS — container queries, fluid typography, Grid/Flexbox, breakpoints, responsive nav/images/tables (wshobson) |
| `references/critique-10khr-learnings.md` | During 10khr — accumulated grinding patterns |
| `references/critique-10khr-may-2026-batch.md` | During batch critique — scoring insights, fix frequency table |
| `references/critique-10khr-may-2026-learnings.md` | After May 2026 batch — reusable fix patterns |
| `references/critique-10khr-may-2026.md` | May 2026 session — setup and configuration |
| `references/critique-10khr-2026-05-29.md` | May 29 session log — historical reference |
| `references/critique-10khr-2026-05-29-learnings.md` | After May 29 session — bulk rewrite strategy, YAML traps |
| `references/critique-10khr-2026-05-30.md` | May 30 session log — historical reference |
| `references/critique-10khr-2026-05-30-r2.md` | May 30 session round 2 — historical reference |
| `references/critique-10khr-2026-05-30-learnings.md` | After May 30 session — distilled patterns |
| `references/critique-2026-06-15-session-learnings.md` | June 15 session — critique workflow validation, failed-attempt encoding anti-pattern, profile↔monorepo sync |
| `references/recursive-skill-discovery.md` | Before writing any skill discovery code — recursive glob pattern, symlink dedup |
| `references/skill-architecture-sprawl-audit-2026-06-17.md` | Skill sprawl audit — merge candidates, anti-patterns, class-level umbrella principle |
| `references/soul-repo-skill-install-gap.md` | Skills in `<fs-root>/soul/skills/` not visible until installed in active profile — detection + fix |
| `references/monorepo-skill-detection.md` | Before creating git repos for skills — detect monorepo source: fields and sync to the correct repo |
| `references/10khr-scope-clarification.md` | Before running 10khr or autofix — clarifies skill library vs code repo targeting |
| `references/tool-integration-pattern.md` | Before integrating an external tool — evaluation flow + concrete example |
| `references/critique-10khr-d9-help-injection.md` | When adding --help to scripts quickly — lightweight pattern without full argparse refactoring |
| `references/critique-10khr-runner-heuristic-checks.md` | During 10khr — exact string checks the runner uses to score each dimension |
| `references/critique-10khr-2026-06-30-session.md` | June 30 grinding — support file map extraction pattern, D6 "why" fix, duplicate-section removal |
| `references/critique-10khr-d3-template-extraction.md` | During D3 fix — scan order for extracting inline templates to get under 450 lines |
| `references/critique-10khr-fix-patterns-2026-06-25.md` | During 10khr grinding — systematic fix patterns per dimension, execution order, path bug fix |
| `references/critique-10khr-2026-06-27-session.md` | June 27 grinding session — ocas-imagine 44→50/50, D1/D3/D5/D7 fixes documented |
| `references/critique-10khr-2026-06-27-look-session.md` | June 27 grinding session — ocas-look 40→50/50, D6/D9 heuristic-blind-spot pattern |
| `references/critique-10khr-2026-06-29-session-2.md` | June 29 second grinding session — --help injection pattern, D2 trigger keywords, skip rule |
| `references/critique-10khr-2026-06-29-session.md` | June 29 grinding session — 61/61 at 50/50, 450-line threshold pattern, map dedup, D7/D9 fixes |
| `references/critique-10khr-2026-06-29-koda-session.md` | June 29 KODA grinding session — 7/26 at 50/50, imported community skill rewrite pattern, gh+curl dedup, cross-profile pitfall |
| `scripts/critique_code_ratio.py` | During Phase 2 — code ratio measurement |
| `scripts/critique_10khr_runner.py` | During 10khr — heuristic scoring and targeting (over-scores by 6-10pt) |

## Added 2026-08-24 (ocas-skilllab grind)

| `references/critique-10khr-grind-pitfalls.md` | Full dated narratives behind the distilled 10khr-mode rules | When a grind misbehaves: wrong target, score disagreement, state-file drift, or a D3/D5/D8/D9 heuristic anomaly |
| `references/cron-grind-resilience.md` | Cron-environment grind properties (degraded reads, execute_code block, write_file chroot) | During any autonomous/cron grind before relying on agentic read/write tools |
| `references/merge-parallel-copy-dedupe.md` | 7-step symlink-consolidation procedure for skill families duplicated across trees/profiles | Before any cross-tree dedupe; never delete until Step-3 superset check is 0 |
| `references/skill-publish-github-mechanics.md` | Dated GitHub playbooks: new monorepo creation, existing-remote reconciliation, bulk rename, eng-skills namespace | When doing those four repo operations |
| `references/secret-history-rewrite.md` | Secret remediation playbook incl. git filter-branch history rewrite + rotation | When secret-scan.sh exits 1 and a real secret needs scrubbing |
| `references/rename-cache-updates.md` | Exact cache-key rewrite snippets for renames | During a skill rename |
