## Description:

Use market access value for academic writing workflows that need structured execution, explicit assumptions, and clear output boundaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, market access writers, and health economics teams use this skill to draft payer-facing pharmacoeconomic value propositions, including ICER narratives, budget impact text, value dossier sections, and payer objection handlers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The packaged script can overwrite arbitrary writable files through its --output path.

Mitigation: Run it only in a disposable workspace, choose a new output path, and avoid pointing --output at existing files until path confinement and overwrite protection are added.

Risk: The skill's academic-writing framing is broader than its payer-value behavior.

Mitigation: Use it only for explicit market-access or pharmacoeconomic drafting and stop when the request becomes general academic writing or unsupported expert advice.

## Reference(s):

- [Audit Reference](references/audit-reference.md)
- [ClawHub skill page](https://clawhub.ai/aipoch-ai/skills/market-access-value)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and generated payer-facing text files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write a local text file through scripts/main.py; no external dependencies are documented.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
