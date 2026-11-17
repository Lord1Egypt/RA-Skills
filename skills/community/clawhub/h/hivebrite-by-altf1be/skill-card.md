## Description:

Hivebrite Admin API CLI for users, companies, events, groups, donations, memberships, emailings, mentoring, news, projects, media center, forums, and more, with OAuth2 or bearer-token authentication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abdelkrim](https://clawhub.ai/user/abdelkrim)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and authorized Hivebrite administrators use this skill to run CLI-driven Hivebrite Admin API workflows across member, event, group, donation, content, mentoring, media, and network-management domains.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles powerful Hivebrite admin credentials and may cache OAuth tokens on disk.

Mitigation: Use least-privilege or short-lived credentials where possible, protect or avoid .env files, and clear the OAuth cache when credentials change.

Risk: Create, update, delete, send, and approval commands can perform live production actions in a Hivebrite tenant.

Mitigation: Install and run the skill only for tenants you are authorized to administer, review commands before execution, and verify destructive actions before using confirmation flags.

Risk: A mistaken tenant URL can send secrets or administrative requests to the wrong destination.

Mitigation: Verify HIVEBRITE_BASE_URL carefully before use and prefer HTTPS tenant URLs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/abdelkrim/skills/hivebrite-by-altf1be)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance]

**Output Format:** [Markdown setup guidance and shell commands with text or JSON CLI responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Hivebrite tenant URL and admin credentials or access token.]

## Skill Version(s):

1.0.0 (source: server release evidence, package.json, _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
