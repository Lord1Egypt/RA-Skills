## Description:

Free Brave API alternative for OpenClaw. Completely FREE web search. No API key required. Secure localhost-only deployment. Supports hidden --dev flag for local development.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pipepi](https://clawhub.ai/user/pipepi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to deploy and query a local SearXNG-backed web search service as a no-key alternative to Brave API search.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer starts a persistent Docker container named searxng-local and replaces any existing container with that name.

Mitigation: Review before installing, avoid name collisions, and remove the service with docker rm -f searxng-local when it is no longer needed.

Risk: The installer pulls an unpinned SearXNG container image.

Mitigation: Use a reviewed image tag or digest before production deployment.

Risk: Installer shell quoting can be unsafe when the skill is installed under an unusual path.

Mitigation: Install from a simple trusted local path or patch the installer to pass Docker arguments without shell interpolation.

Risk: Setting SEARXNG_BASE_URL can redirect health checks and searches away from the default localhost service.

Mitigation: Keep SEARXNG_BASE_URL unset unless the alternate endpoint is intentionally trusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pipepi/skills/local-search-pro)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Plain text and Markdown-style guidance with shell commands and search-result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires docker, python3, and the Python requests package; defaults to a localhost SearXNG endpoint.]

## Skill Version(s):

1.0.10 (source: server release, SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
