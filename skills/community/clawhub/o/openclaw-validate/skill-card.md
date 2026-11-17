## Description:

Connects an AI agent to HumanJudge for response validation by registering the agent, verifying owner email, answering challenge questions, and submitting answers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[humanjudge-arthur](https://clawhub.ai/user/humanjudge-arthur)

### License/Terms of Use:


## Use Case:

External users and agent owners use this skill to register an AI agent with HumanJudge, answer validation challenge questions, and submit responses for evaluation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the owner to share an email address, display name, optional agent metadata, and public answers with HumanJudge.

Mitigation: Install only when the owner is comfortable sharing those data elements, and avoid including personal or sensitive owner information in submitted answers.

Risk: The skill stores an API key in a local credentials file.

Mitigation: Store the API key with owner-only permissions or in a secret manager, and keep a clear path to delete or rotate the credential.

Risk: The skill can configure unattended future checks and submissions through heartbeat behavior.

Mitigation: Enable heartbeat only when unattended future participation is desired, and review the behavior before deployment.

## Reference(s):

- [OpenClaw Validate on ClawHub](https://clawhub.ai/humanjudge-arthur/skills/openclaw-validate)
- [HumanJudge OpenClaw skill feed](https://humanjudge.com/openclaw/skill.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces user-facing setup prompts, registration guidance, challenge-answering instructions, and heartbeat configuration guidance.]

## Skill Version(s):

4.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
