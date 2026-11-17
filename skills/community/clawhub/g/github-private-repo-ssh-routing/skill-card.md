## Description:

Diagnoses SSH keys, host aliases, and Git remotes for GitHub private repositories in multi-repo or automation environments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[darinrowe](https://clawhub.ai/user/darinrowe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to diagnose GitHub private repository SSH routing problems, choose an appropriate identity model, and update repo remotes or automation configuration with the least necessary access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Read-only SSH audits can expose SSH host aliases, usernames, identity file paths, proxy or jump-host details, and unrelated account metadata.

Mitigation: Run the audit script only in a private terminal and redact SSH aliases, usernames, key paths, and proxy or jump-host details before sharing output.

Risk: Broad SSH configuration inspection can reveal unrelated hosts or keys on the machine.

Mitigation: Prefer alias-scoped checks such as `ssh -G <alias>` and inspect only the selected key path when possible.

## Reference(s):

- [Decision Guide](references/decision-guide.md)
- [Identity Model Boundaries](references/identity-model-boundaries.md)
- [Key Storage by System](references/key-storage-by-system.md)
- [OpenClaw Automation Notes](references/openclaw-automation.md)
- [Patterns](references/patterns.md)
- [Symptoms](references/symptoms.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and SSH configuration blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include read-only audit command guidance and redaction guidance for sensitive SSH metadata.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
