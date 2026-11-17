## Description:

KIE.AI (kie.ai). Use this skill for ANY KIE.AI request — searching and reading data. Whenever a task involves KIE.AI, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to check KIE.AI account credits and obtain temporary download URLs for generated files through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute unverified downloaded code and make broader changes to the agent's skills.

Mitigation: Review and approve CLI setup separately; consider disabling automatic skill synchronization with OO_SKILLS_SYNC_DISABLED=1.

## Reference(s):

- [KIE.AI](https://kie.ai)
- [KIE.AI API documentation](https://docs.kie.ai/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API calls, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON payload examples; connector results are JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the oo CLI and an authenticated OOMOL account connected to KIE.AI.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
