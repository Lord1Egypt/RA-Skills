## Description:

Builds and deploys polished website and app prototypes with optional analytics and waitlist capture.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jaswir](https://clawhub.ai/user/jaswir)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and makers use this skill to scaffold small static or Next.js websites, configure optional waitlist and analytics integrations, and deploy them to Vercel.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill needs a Vercel token and can deploy public sites.

Mitigation: Use a narrowly scoped, revocable Vercel token and revoke or rotate it when the skill no longer needs deployment access.

Risk: The local .skill-config file stores deployment and integration values.

Mitigation: Treat .skill-config as sensitive local data and keep it out of source control, logs, and shared workspaces.

Risk: Generated public pages may include analytics or privacy claims that need review.

Mitigation: Review each generated page before publishing and enable analytics only when the intended credentials and disclosures are in place.

Risk: Optional Google service-account credential paths increase credential-handling exposure.

Mitigation: Avoid providing Google service-account credentials unless analytics setup requires them, and store credential files outside generated site folders.

## Reference(s):

- [Website Builder Reference Workflow](references/workflow.md)
- [Idle Web Developer ClawHub page](https://clawhub.ai/jaswir/skills/idle-web-developer)
- [Jaswir ClawHub publisher profile](https://clawhub.ai/user/jaswir)
- [Vercel account tokens](https://vercel.com/account/tokens)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown status summaries with generated files, shell commands, and deployment URLs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write website files under an app directory and optionally deploy a public Vercel site.]

## Skill Version(s):

1.0.2 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
