## Description:

Generate complete OpenClaw skill projects with SkillPay.me billing pre-wired. Describe what you want, get deployable code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wms2537](https://clawhub.ai/user/wms2537)

### License/Terms of Use:


## Use Case:

Developers use this skill to scaffold deployable OpenClaw skill projects with SKILL.md, Cloudflare Worker files, SkillPay billing integration, and deployment commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated project files and shell commands may include user-provided skill names, descriptions, or environment variable identifiers.

Mitigation: Review generated files and commands before running, deploying, or publishing, and use simple allowlisted names and environment variable identifiers.

Risk: The generated project may send user ID, skill details, and billing data to external services.

Mitigation: Confirm data-sharing expectations and required secrets before deployment.

Risk: Generated deployment commands depend on Wrangler behavior and project configuration.

Mitigation: Pin Wrangler before use and test locally before publishing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wms2537/skills/openclaw-skill-scaffolder)
- [OpenClaw Skill Scaffolder endpoint](https://openclaw-skill-scaffolder.swmengappdev.workers.dev/scaffold)
- [SkillPay billing API](https://skillpay.me/api/billing/charge)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration]

**Output Format:** [JSON object containing file templates and deployment commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes SKILL.md, wrangler.toml, TypeScript Worker code, billing type definitions, deploy commands, and a test command.]

## Skill Version(s):

2.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
