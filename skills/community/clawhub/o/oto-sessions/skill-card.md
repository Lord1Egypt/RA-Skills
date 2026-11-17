## Description:

Oto Sessions helps agents save, list, delete, and reuse authenticated browser sessions across websites and accounts through the Oto framework.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mbahar](https://clawhub.ai/user/mbahar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to manage reusable logged-in browser sessions for automation workflows that need authenticated access. It supports saving sessions after manual login, checking and listing sessions, deleting sessions, launching browsers with saved state, and switching between multiple accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved browser sessions can function like sensitive credentials if exposed or reused without consent.

Mitigation: Keep session files in a trusted local directory, avoid shared or synced folders, and require explicit user approval before creating or reusing sessions for high-value accounts.

Risk: The setup flow installs and runs external Oto code that handles authenticated sessions.

Mitigation: Pin and review the Oto commit and npm dependency tree before installation or use.

Risk: A user-controlled OTO_PATH can redirect wrappers to a different local Oto installation.

Mitigation: Restrict OTO_PATH to a trusted directory and review it before running session commands.

## Reference(s):

- [Setup Guide](references/SETUP.md)
- [Integration Guide](references/INTEGRATION.md)
- [Oto GitHub](https://github.com/mbahar/oto)
- [Playwright Docs](https://playwright.dev)
- [ClawHub Skill Page](https://clawhub.ai/mbahar/skills/oto-sessions)
- [Publisher Profile](https://clawhub.ai/user/mbahar)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JavaScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose commands that create, reuse, inspect, or delete local browser session files.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
