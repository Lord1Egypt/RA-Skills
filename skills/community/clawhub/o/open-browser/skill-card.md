## Description:

OpenBrowser automates complex multi-step browser tasks by visually interacting with pages using screenshots for clicks, typing, scrolling, and verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[softpudding](https://clawhub.ai/user/softpudding)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation-focused users use this skill to control a Chrome session for multi-step browsing workflows such as form filling, scraping, UI testing, navigation, and page verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill grants an external browser automation agent broad control over a live Chrome session.

Mitigation: Use only on sessions and sites where automated interaction is acceptable, and avoid financial, healthcare, internal, credential, and account-management pages without explicit safeguards.

Risk: Browser UUIDs act as capability tokens for controlling a registered browser.

Mitigation: Keep the browser UUID private, rotate or recopy it when exposure is suspected, and validate the UUID before submitting tasks.

Risk: Task text, screenshots, page contents, and typed data may be sent through the configured OpenBrowser and LLM stack.

Mitigation: Do not enter sensitive data unless the configured stack is approved for that data, and review the selected LLM endpoint and API-key configuration before use.

Risk: Mutable remote setup commands can install changing upstream code.

Mitigation: Pin and review the upstream repository before running setup commands in a trusted browser environment.

Risk: Background execution can continue browser automation with reduced operator visibility.

Mitigation: Prefer foreground runs for sensitive tasks, monitor logs when background mode is necessary, and stop unexpected or stuck conversations promptly.

Risk: The artifact includes a GitHub star test that changes account state.

Mitigation: Avoid account-changing tests and use neutral verification tasks instead.

## Reference(s):

- [API Reference](references/api_reference.md)
- [Setup Guide](references/setup.md)
- [Troubleshooting](references/troubleshooting.md)
- [ClawHub Skill Page](https://clawhub.ai/softpudding/skills/open-browser)
- [uv Documentation](https://docs.astral.sh/uv/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May stream browser-agent progress, status, errors, usage metrics, and completion messages through SSE-backed command output.]

## Skill Version(s):

0.1.0 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
