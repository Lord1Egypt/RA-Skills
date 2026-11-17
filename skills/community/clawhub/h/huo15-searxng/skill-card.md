## Description:

Deploys a self-hosted SearXNG search engine with Docker Compose and configures OpenClaw to use the local search endpoint.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaobod1](https://clawhub.ai/user/zhaobod1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to install, check, and remove a local SearXNG instance for self-hosted web search. It is intended for environments where Docker is available and a local HTTP port can be exposed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates and manages a persistent Docker SearXNG container and exposes a local port.

Mitigation: Review the generated Docker Compose settings before installation, bind the service to localhost where possible, and install only in environments approved for local containers.

Risk: The install and environment scripts can modify shell configuration by adding SEARXNG_BASE_URL to ~/.zshrc.

Mitigation: Inspect shell configuration changes before sourcing the file and use the uninstall script or manual edits to remove stale environment variables.

Risk: The SearXNG image is referenced with the latest tag, so installations may change as upstream images change.

Mitigation: Pin the SearXNG image to a reviewed version or digest before deploying in controlled environments.

Risk: The README includes a curl-to-shell Docker installation command for Linux troubleshooting.

Mitigation: Prefer operating-system package repositories or reviewed Docker installation steps instead of piping remote install scripts directly to the shell.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zhaobod1/skills/huo15-searxng)
- [SearXNG Documentation](https://docs.searxng.org/)
- [OpenClaw SearXNG Configuration](https://docs.openclaw.ai/tools/searxng-search)
- [SearXNG GitHub Repository](https://github.com/searxng/searxng)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Text]

**Output Format:** [Markdown with inline shell commands and status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create Docker Compose configuration, SearXNG settings, a persistent Docker container, local data directories, and a SEARXNG_BASE_URL shell environment entry.]

## Skill Version(s):

1.2.2 (source: server release metadata; artifact frontmatter and _meta.json report 1.2.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
