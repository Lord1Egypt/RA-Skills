## Description:

Use this skill for BrowserStack tasks involving reading, creating, and updating data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and QA teams use this skill to read BrowserStack Automate build and session data and update session status through a connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup directs the agent to execute a downloaded CLI installer; the installer contents and full local effects are unverified.

Mitigation: Require approval before installation, use a pinned and independently verified CLI installer, and check which additional agent skills it installs.

## Reference(s):

- [BrowserStack Automate API documentation](https://www.browserstack.com/docs/automate/api-reference/selenium/introduction)
- [BrowserStack](https://www.browserstack.com)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-browserstack)

## Skill Output:

**Output Type(s):** [API data, JSON, Shell commands, Guidance]

**Output Format:** [JSON payloads and CLI responses, with Markdown instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes BrowserStack build and session data; session-status updates change BrowserStack state.]

## Skill Version(s):

1.0.4 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
