## Description:

Control Android Chrome via ADB and raw WebSocket CDP. No Playwright needed for navigate, JS injection, cookies, DOM, scroll, click.

This skill is ready for commercial/non-commercial use.

## Publisher:

[laolaoshiren](https://clawhub.ai/user/laolaoshiren)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and test engineers use this skill to operate Android Chrome through ADB and Chrome DevTools Protocol for navigation, JavaScript execution, DOM inspection, cookie handling, scrolling, clicking, and ADB screenshots.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CDP access can control Chrome and expose authenticated browser sessions.

Mitigation: Install and run the skill only when that browser-control capability is intended and understood.

Risk: Exposing the DevTools port beyond localhost can allow remote browser control.

Mitigation: Keep the DevTools port bound to localhost, and avoid LAN sharing unless it is inside an authenticated and encrypted trusted tunnel.

Risk: Cookie and screenshot inspection can reveal sensitive user data.

Mitigation: Inspect cookies or screenshots only after explicit user approval and handle the results as sensitive data.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/laolaoshiren/skills/phone-chrome-cdp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local Android Debug Bridge connection and Chrome DevTools port forwarding.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
