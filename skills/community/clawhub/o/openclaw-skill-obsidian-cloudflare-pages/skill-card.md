## Description:

Publish selected Obsidian markdown from a vault to a static site and deploy to Cloudflare Pages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davidyoh](https://clawhub.ai/user/davidyoh)

### License/Terms of Use:


## Use Case:

Developers and knowledge workers use this skill to publish selected Obsidian vault or Markdown folders as a Quartz static site on Cloudflare Pages with optional Basic Auth and branding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The implementation can run unpinned third-party code and deploy generated output to Cloudflare Pages.

Mitigation: Audit and harden the script before installation, use a dedicated empty workspace, a scoped Cloudflare token, and a test project or subdomain before production use.

Risk: Credential handling can expose Cloudflare or Basic Auth secrets through local configuration or generated middleware.

Mitigation: Keep secrets in uncommitted environment files or shell environment variables, prefer env-backed Basic Auth credentials, and avoid storing Basic Auth passwords in config.

Risk: Setup and sync behavior can delete or mutate files in the configured publishing workspace.

Mitigation: Use --dry-run first, configure a dedicated workspace, and set ALLOW_DESTRUCTIVE=1 only when intentionally allowing fallback cleanup of a non-empty workspace.

## Reference(s):

- [Cloudflare Pages](https://pages.cloudflare.com/)
- [Obsidian Web Clipper](https://obsidian.md/clipper)

## Skill Output:

**Output Type(s):** [markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate or mutate local publishing workspace files and Cloudflare Pages middleware when commands are executed.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
