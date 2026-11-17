## Description:

Build, preview, and deploy markdown-first sites with local preview, Cloudflare bundles, and agent-readable raw markdown routes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jolestar](https://clawhub.ai/user/jolestar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to work with markdown-first mdorigin sites, including local preview, index and search generation, Cloudflare bundle output, and agent-readable markdown routes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install guidance includes an unpinned npm package install.

Mitigation: Prefer a project-local, pinned mdorigin version for important projects.

Risk: Cloudflare deployment and sync commands can publish or move site assets and may use sensitive deployment credentials.

Mitigation: Run Cloudflare deployment commands only when you intend to publish or sync those assets, and review the mdorigin package and docs when sensitive credentials are present.

## Reference(s):

- [Mdorigin HTML docs](https://mdorigin.jolestar.workers.dev)
- [Mdorigin raw markdown home](https://mdorigin.jolestar.workers.dev/README.md)
- [Routing docs](https://mdorigin.jolestar.workers.dev/concepts/routing.md)
- [Configuration docs](https://mdorigin.jolestar.workers.dev/reference/configuration.md)
- [Extensions docs](https://mdorigin.jolestar.workers.dev/guides/extensions.md)
- [Cloudflare docs](https://mdorigin.jolestar.workers.dev/guides/cloudflare.md)
- [OpenAPI schema](https://mdorigin.jolestar.workers.dev/api/openapi.json)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include mdorigin CLI commands and Cloudflare deployment guidance.]

## Skill Version(s):

0.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
