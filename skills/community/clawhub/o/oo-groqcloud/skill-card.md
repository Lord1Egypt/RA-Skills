## Description:

Connects an agent to GroqCloud through OOMOL to list models, retrieve model details, create chat completions, and transcribe or translate audio.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers using GroqCloud through an OOMOL-connected account can inspect connector schemas, retrieve model information, create chat completions, and transcribe or translate audio.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup instructions run remote installer code that was not verified by the security review.

Mitigation: Install the oo CLI separately from a verified source, review the installer, and require approval for installation changes.

Risk: The documented automatic agent-skill synchronization may change local skills.

Mitigation: Check the synchronization setting and disable it if it is not needed.

Risk: Chat requests send selected content through OOMOL to GroqCloud and may incur usage charges.

Mitigation: Review the content before sending and consider the account's usage and billing.

## Reference(s):

- [GroqCloud API documentation](https://console.groq.com/docs/overview)
- [GroqCloud](https://groq.com)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Text, JSON, Shell commands]

**Output Format:** [JSON connector requests and responses, with shell commands for CLI invocation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chat prompts and supplied audio may be sent through OOMOL to GroqCloud; usage may incur charges.]

## Skill Version(s):

1.0.7 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
