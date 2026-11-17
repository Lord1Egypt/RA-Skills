## Description:

LinkedIn automation skill for searching people and companies, fetching profiles, sending messages and InMails, managing connections, creating posts, reacting, commenting, and using Sales Navigator.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vprudnikoff](https://clawhub.ai/user/vprudnikoff)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to direct an agent through Linked API's LinkedIn CLI for profile research, company research, outreach, content posting, engagement, connection management, analytics, and Sales Navigator workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can cause a third-party Linked API cloud browser to act on a user's LinkedIn account.

Mitigation: Require explicit confirmation before messages, posts, comments, reactions, connection changes, company-page actions, or custom workflows.

Risk: The skill requires Linked API and identification tokens that grant account access through the linked service.

Mitigation: Treat both tokens as secrets, avoid entering them in chat or shell history, and revoke and rotate them if exposed.

Risk: The global third-party CLI performs live LinkedIn actions without enough safety scoping in the evidence.

Mitigation: Pin and audit the CLI before use and install only when comfortable with the third-party service operating the account.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/vprudnikoff/skills/linkedapi-linkedin)
- [Linked API Workflow Documentation](https://linkedapi.io/docs/building-workflows/)
- [Linked API Application Dashboard](https://app.linkedapi.io)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with CLI command examples and JSON response expectations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CLI actions may take 30 seconds to several minutes and should use machine-readable JSON output.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
