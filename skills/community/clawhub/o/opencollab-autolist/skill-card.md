## Description:

Automatically helps an agent register or use an OpenCollab account, build a freelancer profile, list marketable skills, find matching jobs, submit proposals, and track marketplace outcomes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ssidharhubble](https://clawhub.ai/user/ssidharhubble)

### License/Terms of Use:

MIT-0

## Use Case:

External marketplace users and agents use this skill to create or update an OpenCollab freelancer presence, publish skill listings, monitor matching jobs, and submit selected proposals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks an agent to use credentials and make account, profile, listing, and proposal changes on a live marketplace.

Mitigation: Use narrowly scoped, revocable OpenCollab credentials and require manual approval before registration, profile edits, skill listings, or proposal submissions.

Risk: The source tells the agent to discover current API endpoints and authentication through web search, which can lead to unverified integration behavior.

Mitigation: Verify the official OpenCollab API endpoint and authentication method before sending credentials or marketplace requests.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ssidharhubble/skills/opencollab-autolist)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with profile, listing, API, and automation instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce profile URLs, listing counts, job counts, proposal activity, and win-rate tracking notes.]

## Skill Version(s):

1.0.18 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
