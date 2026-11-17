## Description:

Static concurrency and race-condition auditor for Go, Java, Python, Node.js/TypeScript that reports shared-state mutations without synchronization and TOCTOU patterns mapped to CWE-362 and CWE-367.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phy041](https://clawhub.ai/user/phy041)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this skill to audit Go, Java, Python, and Node.js/TypeScript codebases for race-condition and time-of-check-time-of-use patterns before relying on runtime tests alone.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release security verdict is suspicious because the embedded scanner fails at startup, which can create false confidence in audit coverage.

Mitigation: Review and fix the embedded Python before installing or relying on this skill as a security control.

Risk: The skill reports static findings that may be incomplete or noisy compared with runtime concurrency behavior.

Mitigation: Use findings as review prompts and pair them with runtime tools such as race detectors or thread sanitizers where available.

## Reference(s):

- [Canlah AI homepage](https://canlah.ai)
- [ClawHub skill page](https://clawhub.ai/phy041/skills/phy-concurrency-audit)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, json]

**Output Format:** [Markdown guidance with shell command examples and optional JSON scanner output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The described scanner is local and dependency-free, but release security evidence says the embedded Python fails at startup and should be reviewed before use.]

## Skill Version(s):

1.0.3 (source: server release evidence, artifact metadata, target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
