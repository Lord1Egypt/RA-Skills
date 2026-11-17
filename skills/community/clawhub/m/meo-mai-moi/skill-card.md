## Description:

Use for Meo Mai Moi pet-owner tasks when an agent needs to help a user manage pets through the documented API, including listing pets, updating profiles, managing health records, understanding helper profiles, and navigating placement workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[troioi-vn](https://clawhub.ai/user/troioi-vn)

### License/Terms of Use:

MIT-0

## Use Case:

External pet owners and developers use this skill to connect an agent to a Meo Mai Moi account, perform documented pet-management API tasks, and handle sensitive updates with read-first workflows and confirmation for consequential actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A bearer token can expose a user's Meo Mai Moi account and pet data if pasted into public chats, logs, commits, or shared prompts.

Mitigation: Store the token as a local secret or environment variable and avoid displaying, logging, or committing it.

Risk: Deletes, status changes, health-history edits, placement handovers, and ownership transfers can have lasting real-world effects.

Mitigation: Read current state first, confirm identifiers and user intent, make the smallest documented change, then re-read to verify the result.

Risk: Using undocumented routes, unsupported methods, or guessed payload fields can corrupt workflow state or fail silently.

Mitigation: Use documented API routes and fields, avoid unsupported PATCH assumptions, and stop when the public contract is incomplete.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/troioi-vn/skills/meo-mai-moi)
- [Meo Mai Moi Docs](https://meo-mai-moi.com/docs)
- [Meo Mai Moi API Integration Guide](https://meo-mai-moi.com/docs/api-integration.html)
- [Meo Mai Moi Project Page](https://project.meo-mai-moi.com)
- [Meo Mai Moi API Reference](references/api.md)
- [Meo Mai Moi Domain Model](references/domain-model.md)
- [Meo Mai Moi Workflows](references/workflows.md)
- [Install and Example Prompts](references/examples.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline JSON and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe API endpoints, request headers, response handling, setup steps, and safety constraints for pet-management actions.]

## Skill Version(s):

0.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
