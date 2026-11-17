## Description:

Browse websites, read web pages, interact with web apps, call website APIs, and automate web tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[4ier](https://clawhub.ai/user/4ier)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use Neo to inspect websites, read pages, discover and call web app APIs, and automate browser interactions through the Neo CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use real logged-in browser sessions and active website state.

Mitigation: Use a dedicated Chrome profile containing only accounts and data needed for the task.

Risk: The skill can export cookies, clear cookies, replay captured requests, and perform authenticated API actions.

Mitigation: Require manual review before cookie export/import, POST requests, replay, cookie clearing, or authenticated API actions.

Risk: The install metadata uses an unpinned third-party Neo CLI package.

Mitigation: Prefer a pinned and audited Neo CLI version before trusting it with active sessions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/4ier/skills/neo-browser)
- [Publisher profile](https://clawhub.ai/user/4ier)
- [@4ier/neo npm package](https://www.npmjs.com/package/@4ier/neo)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON or file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May operate through an authenticated Chrome profile; cookie handling and request replay require manual review.]

## Skill Version(s):

2.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
