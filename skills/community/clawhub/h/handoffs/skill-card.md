## Description:

Record and track structured task handoff logs across sessions with status, summary, artifacts, next-step notes, and confidence in JSONL format.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sumo0221](https://clawhub.ai/user/sumo0221)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to write and inspect persistent handoff logs so work can be transferred between agents or sessions with task status, summaries, artifacts, and next steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent plaintext handoff logs may expose task summaries, file paths, artifact names, and next-step notes.

Mitigation: Avoid putting secrets in handoff fields and restrict permissions on ~/.sumo/handoffs.

Risk: The reader's date argument can escape the intended handoff log directory when influenced by untrusted input.

Mitigation: Validate --date strictly as YYYY-MM-DD before use and avoid passing untrusted arguments until that validation is fixed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sumo0221/skills/handoffs)
- [Publisher profile](https://clawhub.ai/user/sumo0221)

## Skill Output:

**Output Type(s):** [Files, Text, Shell commands, Configuration]

**Output Format:** [JSONL records with console text and Markdown usage examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores records under ~/.sumo/handoffs/YYYY-MM-DD.jsonl and maintains a chain registry.]

## Skill Version(s):

1.0.0 (source: server release metadata, target metadata, and SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
