## Description:

LinkedIn job-sprint automation - verify or refresh login in a dedicated Playwright profile, then run Easy Apply automation for a user-approved application sprint.

This skill is ready for commercial/non-commercial use.

## Publisher:

[umerkha2007](https://clawhub.ai/user/umerkha2007)

### License/Terms of Use:

MIT-0

## Use Case:

External users and job seekers use this skill to verify LinkedIn login state, configure search criteria, and run controlled LinkedIn Easy Apply sprints through a separately installed runtime.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on a separately installed runtime that is not included in the reviewed package.

Mitigation: Install the runtime only from the maintainer's canonical release source and verify the archive hash and pinned cli.py hash before use.

Risk: The runtime can submit real LinkedIn applications and optionally send real hiring-team connection requests through the user's logged-in session.

Mitigation: Require explicit confirmation for each run, including the number of applications to submit, and disable automatic connection requests when that behavior is not desired.

Risk: The Chrome profile, .env file, Anthropic API key, resume text, and application log can contain sensitive personal or account data.

Mitigation: Keep those files private, use a user-controlled non-shared runtime directory, and restrict outbound network access to LinkedIn and Anthropic where allowlisting is available.

## Reference(s):

- [LinkedIn Automation README](references/README.md)
- [ClawHub Skill Page](https://clawhub.ai/umerkha2007/skills/linkedin-easy-apply)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and human-readable runtime output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runtime commands print progress lines to stdout; application outcomes may also be persisted to a JSON log by the runtime.]

## Skill Version(s):

1.0.11 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
