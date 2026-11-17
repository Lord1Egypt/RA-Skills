## Description:

Nightfall AI (nightfall.ai). Use this skill for ANY Nightfall AI request — reading, creating, and updating data. Whenever a task involves Nightfall AI, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to scan text for sensitive data through a connected Nightfall AI account, with optional redaction and configured alerts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic CLI setup can execute unverified code and make broader changes to the agent environment.

Mitigation: Review and install a verified CLI release separately before use, and consider disabling automatic skill synchronization using the documented upstream control.

Risk: Scanning can send text, policies, and alert effects through OOMOL to Nightfall AI.

Mitigation: Approve the exact text, policies, and alert effects before running the scan.

## Reference(s):

- [Nightfall AI developer API documentation](https://help.nightfall.ai/developer-api/nightfall_apis/dlp)
- [Nightfall AI homepage](https://www.nightfall.ai/)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Shell commands, JSON payloads, Guidance]

**Output Format:** [Shell commands with JSON input and structured action results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action input fields are obtained from the live connector schema; scan_text accepts up to 50,000 strings totaling 500 KB.]

## Skill Version(s):

1.0.2 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
