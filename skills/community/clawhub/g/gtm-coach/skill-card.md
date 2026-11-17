## Description:

Coaches founders through go-to-market planning, weekly priorities, channel choices, and evidence-based marketing drafts and scorecards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shujip](https://clawhub.ai/user/shujip)

### License/Terms of Use:

MIT-0

## Use Case:

Founders and external teams use this skill to assess a project's go-to-market stage, select one weekly priority, and create supporting marketing drafts and a local dashboard. The founder decides whether to publish or send anything.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs persistently and can replace its installed copy from a remote source at new sessions without confirmation.

Mitigation: Review the skill before installation and re-review updates; do not install it if automatic replacement is unacceptable.

Risk: A project access token and go-to-market plans are stored in local project files.

Mitigation: Keep .gtm/ gitignored, limit access to those files, and never share or commit the token.

Risk: Dashboard sharing can disclose sensitive business plans and metrics.

Mitigation: Review dashboard content before using share buttons and omit sensitive business details from public drafts.

## Reference(s):

- [GTM Coach ClawHub release](https://clawhub.ai/shujip/skills/gtm-coach)
- [GTM Coach homepage](https://www.nichestarter.ai/gtm-coach)
- [GTM Coach playbook](artifact/playbook.md)
- [GTM dashboard and scorecard guide](artifact/dashboard.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Files]

**Output Format:** [Text and Markdown guidance; local JSON, Markdown, and HTML files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One weekly GTM artifact at a time; dashboard and scorecard are separate local outputs.]

## Skill Version(s):

1.5.2 (source: server release, skill frontmatter, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
