## Description:

Send explicitly authorized LINE Official Account Chat messages through a persistent Chromium session; user-operated LINE login or reauthentication may use a temporary remote noVNC handoff that grants interactive browser control.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mosluce](https://clawhub.ai/user/mosluce)

### License/Terms of Use:

MIT

## Use Case:

External users and operators use this skill to send an explicitly authorized message to a named LINE Official Account Chat recipient from an already authenticated Chromium session. It also guides user-operated login or reauthentication through a temporary noVNC handoff when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send LINE business messages and security evidence reports a real recipient-matching flaw.

Mitigation: Use only non-sensitive test messages until exact recipient matching is fixed, require explicit recipient and message authorization, and stop rather than retry when post-send verification fails.

Risk: Security evidence reports unpinned dependency execution through the Playwright runtime path.

Mitigation: Provision a pinned and reviewed Playwright runtime before production use.

Risk: The optional login handoff grants interactive browser control to anyone with the handoff URL.

Mitigation: Run the browser under an unprivileged dedicated account, share handoff URLs only with the intended user in a private channel, treat each URL as a short-lived bearer secret, and revoke it promptly after login.

## Reference(s):

- [Handoff operations](references/handoff-operations.md)
- [LINE OA Chat UI selector notes](references/line-oa-ui-selectors.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Text]

**Output Format:** [Markdown with inline shell commands and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces no-send dry-run guidance by default and requires explicit send authorization for external message delivery.]

## Skill Version(s):

0.1.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
