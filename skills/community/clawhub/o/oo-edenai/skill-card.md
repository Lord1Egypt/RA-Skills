## Description:

Eden AI (edenai.co). Use this skill for ANY Eden AI request — searching and reading data. Whenever a task involves Eden AI, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External developers use the skill to access Eden AI through an OOMOL-connected account, list models, and create chat completions. It guides agents to check each action's schema before sending a request.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup directly executes remote code whose behavior has not been verified.

Mitigation: Review and verify the CLI installation before allowing automatic setup.

Risk: Chat generation may incur charges even though the skill treats it as a read-only action.

Mitigation: Authorize chat generation deliberately and set suitable spending limits.

Risk: Skill synchronization settings can affect other agent installations.

Mitigation: Check synchronization settings before proceeding with setup.

Risk: Content submitted through the integration is processed by OOMOL and Eden AI.

Mitigation: Submit only content intended for those services to process.

## Reference(s):

- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [Eden AI homepage](https://www.edenai.co)
- [Eden AI chat completions documentation](https://www.edenai.co/docs/v3/llms/chat-completions)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text, Shell commands, Guidance]

**Output Format:** [JSON responses and shell commands with setup and usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chat completion content and available models depend on the connected Eden AI account and selected model.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
