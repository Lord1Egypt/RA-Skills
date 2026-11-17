## Description:

Memory hygiene and adjudication layer for OpenClaw agent workflows that deduplicates entities, resolves naming conflicts, separates facts from goals from speculation, archives stale records, enforces consistent schemas, detects contradictions, and preserves provenance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[honouralexwill](https://clawhub.ai/user/honouralexwill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to clean accumulated OpenClaw memory records before downstream use. It adjudicates duplicate, conflicting, stale, and schema-drifted records into a human-readable report and structured output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repository instructions may prompt an agent to run unaudited external Saturnday commands or install hooks.

Mitigation: Require explicit human approval before running Saturnday commands or installing hooks from the artifact.

Risk: Generated Markdown and JSON reports can contain memory contents and provenance details.

Mitigation: Treat reports as sensitive data and restrict storage, sharing, and downstream logging according to the workspace data policy.

Risk: Test and development tooling may be inappropriate for untrusted users.

Mitigation: Run the package in a controlled agent or developer workspace and avoid exposing development commands as an unauthenticated service.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/honouralexwill/skills/memory-referee)
- [Saturnday](https://www.saturnday.dev)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Markdown adjudication report and structured JSON report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes counts, classifications, conflicts, archived stale records, schema violations, and provenance chain entries.]

## Skill Version(s):

0.1.0 (source: server release metadata and package.json; SKILL.md frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
