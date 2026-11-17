## Description:

Queries a configured JisuAI account for balance and remaining call count, then returns the requested account status to the user.

This skill is ready for commercial/non-commercial use.

## Publisher:

[outrice](https://clawhub.ai/user/outrice)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users with a configured JisuAI API key use this skill to ask an agent for their account balance, remaining call count, or both. The skill reads the local OpenClaw configuration and queries the JisuAI balance service on the user's behalf.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence says the skill reads a local OpenClaw API key and sends it to the JisuAI balance service over plaintext HTTP in the URL, which can expose the credential.

Mitigation: Install only if that credential exposure is acceptable; rotate any key previously used with this implementation and prefer a version that uses HTTPS and avoids query-string credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/outrice/skills/jisuai-balance)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration]

**Output Format:** [Plain text response produced by a Python script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns balance, remaining call count, or an error message depending on the query and service response.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
