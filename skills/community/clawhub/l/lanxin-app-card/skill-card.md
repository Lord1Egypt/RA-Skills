## Description:

Generates clean Lanxin appCard JSON messages for official Lanxin application cards with structured fields, links, and formatting options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iamdacai](https://clawhub.ai/user/iamdacai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate Lanxin appCard JSON for application-card messages such as approvals and notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Always-loaded behavior and broad triggers may activate the skill outside an explicit app-card sending request.

Mitigation: Install only when global Lanxin app-card formatting is needed, and narrow triggers or remove always-loaded behavior when packaging allows.

Risk: No-refusal and direct-output instructions may suppress normal refusals or clarifying questions.

Mitigation: Review generated cards before sending and allow clarifying questions or refusals for unsafe, ambiguous, or unsupported requests.

Risk: Card fields and links may expose secrets, internal URLs, local file paths, or unvalidated destinations.

Mitigation: Validate URLs and remove secrets, internal links, and local file paths before sharing a card.

## Reference(s):

- [Lanxin App Card ClawHub release](https://clawhub.ai/iamdacai/skills/lanxin-app-card)
- [iamdacai ClawHub publisher profile](https://clawhub.ai/user/iamdacai)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [Raw JSON object without Markdown fencing or surrounding prose]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces appCard objects and prohibits Markdown code blocks, extra explanatory text, lxfile tags, and lximg tags.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
