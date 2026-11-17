## Description:

Configure Anthropic OAuth tokens (sk-ant-oat01-*) to work with OpenClaw as API keys via environment variable injection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiafar](https://clawhub.ai/user/jiafar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure OpenClaw to pass Anthropic OAuth tokens through environment variable injection for global or per-agent model provider setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill teaches users to repurpose Anthropic OAuth or subscription tokens as OpenClaw API credentials.

Mitigation: Use only provider-supported API keys or officially documented authentication flows unless explicit authorization and account-policy risk acceptance are in place.

Risk: OAuth or subscription tokens may be persisted in configuration, shell history, logs, backups, or repositories.

Mitigation: Avoid storing real tokens in persistent config or version control, review generated commands before execution, and rotate any exposed tokens.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jiafar/skills/oauth-disguise)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes configuration snippets, verification steps, troubleshooting guidance, and token-handling security notes.]

## Skill Version(s):

1.1.1 (source: server release evidence; artifact frontmatter says 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
