## Description:

AI-driven workflow for full-project programming language migration with structural equivalence checks, persistent YAML state, real-test verification, and human-gated blocking when migration decisions cannot be made safely.

This skill is ready for commercial/non-commercial use.

## Publisher:

[suifei](https://clawhub.ai/user/suifei)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineering teams use this skill to port, translate, or rewrite complete codebases from one programming language to another while preserving structure, assets, behavioral evidence, and verification records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read or copy sensitive project configuration while scanning and migrating a source tree.

Mitigation: Use it only on repositories where broad source-tree review is acceptable, and remove or sanitize live secrets such as .env files, credential JSON/YAML, private keys, and production configuration before use.

Risk: Autonomous migration and phase-gate loops can apply broad project changes.

Mitigation: Require human approval before copying configuration into the target project or allowing automated review loops to apply fixes.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/suifei/skills/lang-migration)
- [Skill README](README.md)
- [Phase 0 Bootstrap](references/phase-0-bootstrap.md)
- [Phase 1 Asset Scan](references/phase-1-asset-scan.md)
- [Phase 2 Ecosystem Map](references/phase-2-ecosystem-map.md)
- [Phase 3 IPO Analysis](references/phase-3-ipo-analysis.md)
- [Phase 4 Translation](references/phase-4-translation.md)
- [Phase 5 Verification](references/phase-5-verification.md)
- [Phase 6 Gap Report](references/phase-6-gap-report.md)
- [Phase Gate Review](references/phase-gate-review.md)
- [YAML Schemas](references/schemas.md)
- [TDD Retrospective Protocol](references/tdd-retrospective.md)
- [Language Pair Modules](references/lang-pairs/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with YAML state files, code changes, shell commands, and verification summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update migration workspace YAML files and translated project files during agent execution.]

## Skill Version(s):

1.3.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
