## Description:

Helps agents draft and manage freelance workflow artifacts such as job examples, proposals, status summaries, and invoices for platforms named by the skill.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neckr0ik](https://clawhub.ai/user/neckr0ik)

### License/Terms of Use:

MIT

## Use Case:

Freelancers or agents supporting freelancers use this skill to draft proposals, inspect locally stored job and proposal status, and produce invoice text or JSON. Users should manually verify opportunities and review any client-facing output before use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat job search results as live freelance-platform data even though the security evidence says the inspected code mostly creates synthetic local job records.

Mitigation: Label generated jobs as examples and verify opportunities directly on the relevant platform before sending proposals or committing to work.

Risk: Generated proposals, invoices, and client messages may be inaccurate, misleading, or unsuitable for client-facing use.

Mitigation: Manually review and edit all client-facing output before sending, and keep any platform or client action under direct user control.

Risk: The skill stores business records locally and proposal generation may include client or project details in prompts sent to a local Ollama model.

Mitigation: Avoid sensitive client data unless the local model and filesystem handling are acceptable, and protect or delete records under ~/.freelance-automator as needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/neckr0ik/skills/neckr0ik-freelance-automator)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and plain text with CLI command examples; invoices may be text or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores local job, proposal, client, and invoice records under ~/.freelance-automator.]

## Skill Version(s):

1.0.0 (source: frontmatter, claw.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
