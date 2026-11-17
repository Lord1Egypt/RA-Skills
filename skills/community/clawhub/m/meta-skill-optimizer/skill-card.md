## Description:

Self-improving AI skill optimizer that learns from feedback, auto-tunes prompts, optimizes tool usage patterns, and evolves based on success/failure analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jason-aka-chen](https://clawhub.ai/user/jason-aka-chen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to record execution outcomes, learn from successes and failures, tune prompts, recommend tools, and export learned optimization patterns for future agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optimizer can persist prompts, task context, errors, tool parameters, and results as local plaintext learning records.

Mitigation: Avoid storing secrets, credentials, private file contents, customer data, or sensitive prompts; add redaction, retention limits, restricted file permissions, and a clear or disable path before use with sensitive workflows.

Risk: The installation instructions include an unpinned pip command.

Mitigation: Review dependencies and pin approved package versions before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jason-aka-chen/skills/meta-skill-optimizer)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python and shell examples plus JSON-like result objects]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist learned task, prompt, tool, error, and outcome records to local JSON storage when the optimizer is used.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
