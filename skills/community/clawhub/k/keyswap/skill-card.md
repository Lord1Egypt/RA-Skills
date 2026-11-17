## Description:

Rotate Claude Max API token for OpenClaw Anthropic profiles when the user requests a key swap, key rotation, new key, keyswap, or provides a new `sk-ant-` token.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jawaddxb](https://clawhub.ai/user/jawaddxb)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw operators use this skill to rotate Claude Max API tokens for the configured Anthropic profiles and restart the OpenClaw gateway after the update.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles a powerful Claude Max API token and can be triggered by broad key-rotation phrases.

Mitigation: Use the skill only after an explicit user request, avoid pasting tokens into ambiguous conversations, and install it only when this exact OpenClaw profile rotation is needed.

Risk: The security guidance flags unsafe shell-style invocation and token handling that needs review before installation.

Mitigation: Prefer a reviewed version that reads the token from protected input, validates the full token format, avoids printing token fragments, and passes arguments without shell interpolation.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with an inline shell command and status summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May request a Claude Max API token from the user and reports success or script error output.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
