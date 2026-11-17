## Description:

Build a concise incident dossier from operational logs, audits, JSON/JSONL files, and state snapshots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neo1307](https://clawhub.ai/user/neo1307)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to turn logs, JSON/JSONL audit trails, state snapshots, screenshots, and reports into a structured incident report with timeline, blast radius, likely root cause, recovery status, and next actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated dossiers may summarize misleading or adversarial evidence.

Mitigation: Review raw source lines before relying on conclusions, and render generated Markdown with raw HTML and remote resource loading disabled when evidence may be untrusted.

Risk: Timelines and root-cause hypotheses can be wrong when timestamps are missing, conflicting, or only partially parsed.

Mitigation: Verify the generated timeline against representative raw lines and state uncertainty explicitly before asserting root cause or incident scope.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/neo1307/skills/incident-dossier)
- [Publisher profile](https://clawhub.ai/user/neo1307)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown incident dossier with concise narrative sections and timeline bullets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate a Markdown file when the bundled local parser is run with explicit JSON or JSONL evidence inputs.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
