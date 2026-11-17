## Description:

Enable and configure Moltbot/Clawdbot memory search for persistent context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackwang2999](https://clawhub.ai/user/jackwang2999)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to configure persistent memory search, create memory files, tune memorySearch settings, and troubleshoot provider or recall issues in Moltbot/Clawdbot.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The recommended memorySearch defaults may index private memory files and past chat transcripts through cloud embedding providers.

Mitigation: Review memory files and old session transcripts for secrets, credentials, personal data, and confidential project details before enabling indexing.

Risk: Cloud embedding providers may receive private or regulated data from indexed memory sources.

Mitigation: Prefer the local provider or limit sources to curated memory files when private or regulated data should not leave the machine.

## Reference(s):


## Skill Output:

**Output Type(s):** [markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON, Markdown, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may include configuration that indexes memory files and past session transcripts.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
