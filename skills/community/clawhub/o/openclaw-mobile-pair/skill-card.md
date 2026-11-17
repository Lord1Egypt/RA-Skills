## Description:

Generates a mobile pairing code for OpenClaw control app users.

This skill is ready for commercial/non-commercial use.

## Publisher:

[szx19970521](https://clawhub.ai/user/szx19970521)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users and operators use this skill to generate a mobile control center pairing code, receive the generated file path, and get the next step for connecting a mobile app.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The referenced PowerShell script is missing from the artifact and would be resolved at runtime.

Mitigation: Use only a release that bundles or pins the script and resolves it from the installed skill directory.

Risk: Pairing-code generation reads a local gateway token and sends data to a user-provided BFF URL.

Mitigation: Confirm the BFF URL is trusted and review token handling before installing or running the skill.

Risk: The command template bypasses PowerShell execution policy.

Mitigation: Prefer a version that avoids execution-policy bypass or review the script before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/szx19970521/skills/openclaw-mobile-pair)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown text with PowerShell command guidance and pairing results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns a pairing code, an output file path, and a short next step for the mobile user.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
