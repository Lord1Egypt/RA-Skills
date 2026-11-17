## Description:

Deploy and manage Netlify sites with npx netlify, including auth, linking, preview deploys, production releases, and config checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to deploy, link, configure, and validate Netlify-hosted web projects from the terminal while keeping preview deployments as the default path before production release.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses an unpinned Netlify CLI in login and deployment workflows.

Mitigation: Prefer a pinned, trusted Netlify CLI version or a lockfile-managed local dependency before executing deployment commands.

Risk: Production deploys can publish unreviewed changes if approval gates are skipped.

Mitigation: Keep production deploys behind explicit user confirmation and use preview deployments for validation first.

Risk: Environment variable import commands can expose secrets to Netlify unintentionally.

Mitigation: Review variables before importing .env files and only publish secrets intended for Netlify.

## Reference(s):

- [Netlify Documentation](https://docs.netlify.com)
- [Netlify Deploy on ClawHub](https://clawhub.ai/ivangdavila/skills/netlify-deploy)
- [Netlify API](https://api.netlify.com)
- [Netlify App](https://app.netlify.com)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash and TOML code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include deploy URLs, environment status, and a concrete next step after deployment.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
