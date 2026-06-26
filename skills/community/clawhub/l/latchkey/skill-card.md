## Description: <br>
Interact with arbitrary third-party or self-hosted services (AWS, Slack, Google Drive, Dropbox, GitHub, GitLab, Linear, Coolify...) using their HTTP APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hynek-urban](https://clawhub.ai/user/hynek-urban) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use Latchkey to make authenticated HTTP API requests through a credential-injecting curl wrapper for configured third-party or self-hosted services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A broad credential-injecting API wrapper can let an agent act across many configured services. <br>
Mitigation: Install only if the latchkey npm package is trusted and configure one narrowly scoped service at a time. <br>
Risk: Authenticated API calls may write, delete, change permissions, post publicly, affect billing, or touch production resources. <br>
Mitigation: Prefer read-only or least-privilege tokens, avoid production, admin, or payment credentials unless necessary, and require confirmation before sensitive actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hynek-urban/latchkey) <br>
- [Slack conversations.create API endpoint](https://slack.com/api/conversations.create) <br>
- [Discord current user API endpoint](https://discord.com/api/v10/users/@me) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include authenticated API request examples and credential setup guidance.] <br>

## Skill Version(s): <br>
2.3.0+5 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
