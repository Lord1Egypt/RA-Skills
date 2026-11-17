## Description:

Opens Brave browser to Claude AI (Anthropic). Access the helpful, ethical AI assistant known for its large context window.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ruchir17-cmd](https://clawhub.ai/user/ruchir17-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to open Claude.ai in Brave for chatting with Claude, comparing AI responses, and working with long documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Invoking the skill may open Brave and connect to Claude.ai unexpectedly.

Mitigation: Narrow trigger phrases and add an explicit tool or permission declaration before deployment.

Risk: The Windows launch path uses shell=True.

Mitigation: Replace it with a safer browser-opening method before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ruchir17-cmd/skills/open-claude)
- [Claude.ai](https://claude.ai)
- [Brave Browser](https://brave.com)

## Skill Output:

**Output Type(s):** [shell commands, text, guidance]

**Output Format:** [Text status message with an operating-system-specific browser launch command]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Opens Brave and connects to Claude.ai; requires Brave, internet access, and a Claude account.]

## Skill Version(s):

1.0.0 (source: release metadata and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
