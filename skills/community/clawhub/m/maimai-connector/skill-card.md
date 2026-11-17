## Description:

Use the Maimai Enterprise browser adapter to check account access, list talent profiles and jobs, and guide QR-code reauthentication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cw20051219-commits](https://clawhub.ai/user/cw20051219-commits)

### License/Terms of Use:

MIT

## Use Case:

Recruiters and developers use the adapters to check Maimai Enterprise account and search access, retrieve talent profiles and job listings, and restore a login with a QR code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags browser commands run without sandbox isolation and a persistent background heartbeat while using an authenticated browser session.

Mitigation: Review the sandbox instructions and heartbeat workflow before installation; use the reduced-isolation browser session only if you are comfortable with it, and monitor the heartbeat while it is active.

## Reference(s):

- [GitHub source repository](https://github.com/cw20051219-commits/maimai-connector)
- [ClawHub release](https://clawhub.ai/cw20051219-commits/skills/maimai-connector)

## Skill Output:

**Output Type(s):** [JSON, Code, Shell commands, Configuration instructions, Guidance, Files]

**Output Format:** [JSON responses and Markdown guidance with JavaScript and Python code and shell commands; QR-code PNG files during reauthentication]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Adapter calls accept optional pagination, page-size, and project parameters; QR-code generation requires a login ID.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
