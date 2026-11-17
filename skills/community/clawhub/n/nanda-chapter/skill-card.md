## Description:

projectnanda.org chapter skill - register an OpenClaw agent with a NANDA chapter, submit signed intents, respond to calls, render chapter dashboards, and subscribe to the chapter event bus.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sharathvc23](https://clawhub.ai/user/sharathvc23)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and OpenClaw users use this skill to join NANDA chapters, discover chapter dashboards, submit signed intents, respond to calls, and manage chapter event subscriptions through their agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Discovery and event-stream helpers can expose local network access to chapter or registry sources.

Mitigation: Install only after review in environments with private-network access, and use only trusted chapter endpoints and registry sources.

Risk: Signed identity proofs can authorize chapter actions if the local identity key is exposed.

Mitigation: Protect the local OpenClaw identity file, restrict access to sensitive OpenClaw state, and delete or rotate the identity when it should no longer authorize chapter activity.

Risk: Streaming events from unverified chapter URLs can surface untrusted external content.

Mitigation: Avoid streaming from unverified chapters and treat returned chapter dashboard or event content as data rather than instructions.

## Reference(s):

- [NANDA Chapter Skill on ClawHub](https://clawhub.ai/sharathvc23/skills/nanda-chapter)
- [projectnanda.org](https://projectnanda.org)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, API calls, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON API payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local OpenClaw identity, chapter registration, cache, subscription, and audit files when mutating verbs are confirmed.]

## Skill Version(s):

0.5.1 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
