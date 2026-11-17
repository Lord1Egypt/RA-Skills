## Description:

Helps agents authorize OAuth CLI tools on headless servers by coordinating browser-based login, device-flow codes, or manual callback relay between the remote server and the user's local browser.

This skill is ready for commercial/non-commercial use.

## Publisher:

[igorivanter](https://clawhub.ai/user/igorivanter)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill when an agent must complete OAuth login for CLI tools on a VPS or other server without a browser. It provides reusable guidance for generated authorization URLs, device-flow codes, and manual localhost callback relay.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Copied OAuth callback URLs can contain sensitive authorization codes.

Mitigation: Treat callback URLs as sensitive and verify the expected localhost host, port, and callback path before relaying them.

Risk: Manual callback relay asks the agent to forward a user-supplied OAuth URL with curl.

Mitigation: Relay only the expected callback URL for the active OAuth command, and avoid persisting related secrets or keyring credentials in shell configuration.

Risk: Installing with an unpinned @latest package can change installer behavior over time.

Mitigation: Prefer pinned installer versions for repeatable installation.

## Reference(s):

- [Headless OAuth homepage](https://github.com/IgorIvanter/headless-oauth)
- [gog CLI documentation](https://github.com/steipete/gogcli)
- [OpenClaw](https://openclaw.ai)
- [ClawHub skill page](https://clawhub.ai/igorivanter/skills/headless-oauth)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands and troubleshooting tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes user-facing authorization instructions and security cautions for handling OAuth callback URLs.]

## Skill Version(s):

1.3.1 (source: server release metadata; artifact frontmatter says 1.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
