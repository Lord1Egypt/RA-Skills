## Description:

Use the Netlify CLI to create or link Netlify sites and set up CI/CD from GitHub, especially for monorepos with multiple sites in one repository.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ajmwagar](https://clawhub.ai/user/ajmwagar)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to create Netlify sites, link local project folders, configure GitHub-backed continuous deployment, manage per-site environment variables, and apply monorepo deployment patterns for Hugo sites.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper scripts can write Netlify configuration from user-supplied values, which could affect CI builds if reviewed poorly.

Mitigation: Review helper scripts before use, pass only normal Hugo version strings, and inspect generated netlify.toml files before committing or deploying.

Risk: Netlify authentication tokens and environment variables may expose deployment or application secrets.

Mitigation: Treat NETLIFY_AUTH_TOKEN and Netlify environment variables as secrets, scope them with least privilege, and rotate them if exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ajmwagar/skills/netlify)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown with inline bash and TOML examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Netlify CLI commands and netlify.toml configuration for Hugo monorepo sites.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
