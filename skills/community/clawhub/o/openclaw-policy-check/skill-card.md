## Description:

Scan repositories for risky security patterns before execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spbavarva](https://clawhub.ai/user/spbavarva)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to run lightweight preflight scans of repositories or files for unsafe commands, possible secret leakage, and dangerous shell behavior before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner may read files outside the chosen scan root through symlinks.

Mitigation: Run it only on trusted repository trees or inspect and remove untrusted symlinks before scanning.

Risk: JSON output may print detected secrets verbatim.

Mitigation: Avoid JSON output on codebases that may contain real credentials, or handle the output as sensitive data.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown summary with optional JSON scanner output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes total findings, severity breakdown, top findings with file and line references, and brief remediation guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
