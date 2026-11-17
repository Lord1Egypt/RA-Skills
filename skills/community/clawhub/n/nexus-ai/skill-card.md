## Description:

Nexus AI helps agents publish business, recruiting, and event posts to Nexus, retrieve usage reports by phone number, and query Nexus RAG search for people, resources, and opportunities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[songsh66](https://clawhub.ai/user/songsh66)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill when they want an agent to route Nexus business development, recruiting, resource search, posting, and usage-report requests through the Nexus CLI workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Business and recruiting requests may be routed to Nexus external services more broadly than a user expects.

Mitigation: Confirm that the user wants Nexus handling before invoking the skill for business, recruiting, or resource-search requests.

Risk: Phone numbers, free-form queries, job posts, investment text, and collaboration content may be sent to or retained by the Nexus service.

Mitigation: Require explicit confirmation before sending personal or posting content, and avoid confidential information unless the user trusts the service handling and logging practices.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/songsh66/skills/nexus-ai)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text and Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May print Nexus resource IDs, cleaned text reports, RAG answers, session IDs, miniapp links, and QR image paths.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
