## Description: <br>
AI-driven full-project language migration workflow for porting, translating, or rewriting codebases across programming languages with structural equivalence, asset coverage, persistent YAML state, and verification evidence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[suifei](https://clawhub.ai/user/suifei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to guide an AI coding agent through a multi-phase codebase migration: asset inventory, ecosystem mapping, function-level IPO analysis, translation, verification, and gap reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can authorize broad scanning, writing, fixing, and command execution across a project. <br>
Mitigation: Set explicit source and target directories, keep the source tree read-only, review diffs frequently, and approve build or test commands before execution. <br>
Risk: A migration can introduce behavioral divergence if evidence, phase gates, or no-mock verification steps are skipped. <br>
Mitigation: Require the documented phase gates, READ_EVIDENCE, BEHAVIOR_PROOF, real-data tests, and full-suite reruns before accepting translated code. <br>
Risk: Generated migration reports and YAML state files may become stale or inconsistent across long-running sessions. <br>
Mitigation: Resume from migration_workspace/migration-state.yaml, audit phase-gate status before advancing, and run the gap report when status is unclear. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/suifei/lang-migration) <br>
- [README](README.md) <br>
- [Phase 0: Bootstrap](references/phase-0-bootstrap.md) <br>
- [Phase 1: Asset Scan](references/phase-1-asset-scan.md) <br>
- [Phase 2: Ecosystem Mapping](references/phase-2-ecosystem-map.md) <br>
- [Phase 3: IPO Analysis](references/phase-3-ipo-analysis.md) <br>
- [Phase 4: Translation](references/phase-4-translation.md) <br>
- [Phase 5: Verification](references/phase-5-verification.md) <br>
- [Phase 6: Gap Report](references/phase-6-gap-report.md) <br>
- [Phase Gate Review Protocol](references/phase-gate-review.md) <br>
- [TDD Retrospective Protocol](references/tdd-retrospective.md) <br>
- [YAML Schemas Reference](references/schemas.md) <br>
- [Language Pair Template](references/lang-pairs/TEMPLATE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with YAML state files, code changes, shell commands, and generated migration reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update migration_workspace YAML files, translated source files, verification reports, and gap reports during an agent-led migration.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
