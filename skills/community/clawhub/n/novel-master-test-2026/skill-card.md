## Description:

Supports publication-grade Chinese novel creation from project setup through worldbuilding, character design, outlining, chapter drafting, foreshadowing tracking, and quality control.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bbroot](https://clawhub.ai/user/bbroot)

### License/Terms of Use:

MIT

## Use Case:

External creators and writing-focused agents use this skill to plan and draft Chinese novels, maintain story and character state, track foreshadowing, and perform chapter-level quality checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Helper scripts can create or update files outside the intended project folder.

Mitigation: Run the skill only in a dedicated Chinese novel workspace, review generated paths before execution, and avoid untrusted book or character names.

Risk: Documentation points users to an unverified external GitHub install path while server-resolved provenance is unavailable.

Mitigation: Use the ClawHub release as the review baseline and verify a pinned external release or commit before following any external install path.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bbroot/skills/novel-master-test-2026)
- [Plot Structure](references/plot-structure.md)
- [Character Design](references/character-design.md)
- [Foreshadowing](references/foreshadowing.md)
- [Style Guide](references/style-guide.md)
- [Process Per Character](references/process-per-character.md)
- [Node Compressed Graph](references/node-compressed-graph.md)
- [Quantum Auditor](references/quantum-auditor.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown prose, structured templates, JSON tracker entries, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local novel project files and tracker state when helper scripts are used.]

## Skill Version(s):

1.0.0 (source: server release metadata; source skill frontmatter declares 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
