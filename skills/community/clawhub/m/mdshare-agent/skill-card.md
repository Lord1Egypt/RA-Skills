## Description:

Create, read, unlock, update, and delete temporary Markdown shares through the MDShare service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cced3000](https://clawhub.ai/user/cced3000)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to publish Markdown as temporary MDShare links, retrieve shared Markdown, and manage protected or editable shares through explicit API workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Manage and edit links act like credentials and can allow anyone with the link to modify or delete a share.

Mitigation: Return only the public link by default, share manage or edit links only when needed, and treat token-bearing links as sensitive.

Risk: Burn-after-read shares may reveal or consume sensitive content if accessed without explicit user intent.

Mitigation: Require confirmation before consuming burn-after-read content and explain the effect before proceeding.

Risk: The security review marked the release suspicious because default link handling may expose powerful manage tokens.

Mitigation: Review before installing and use the skill only for content intentionally sent to MDShare.

## Reference(s):

- [MDShare API Reference](references/api.md)
- [MDShare Agent Workflows](references/workflows.md)
- [MDShare Agent Install Examples](references/install-examples.md)
- [MDshare Agent on ClawHub](https://clawhub.ai/cced3000/skills/mdshare-agent)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Guidance]

**Output Format:** [Markdown or text replies with MDShare links and JSON API payload guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include public, edit, and manage links; token-bearing links should be treated as sensitive.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
