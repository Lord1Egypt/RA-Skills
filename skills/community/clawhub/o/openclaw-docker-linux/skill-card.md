## Description: <br>
Guides Linux users through running OpenClaw in Docker with Tailscale remote access, including setup, configuration, credentials, and common troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[djc00p](https://clawhub.ai/user/djc00p) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to set up and manage OpenClaw in Docker on Linux, including docker-compose configuration, environment variables, permissions, Tailscale access, and troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup requires sensitive API tokens and an OpenClaw gateway token. <br>
Mitigation: Store secrets in a local .env file with restrictive permissions, avoid committing it, and mask tokens in terminal output. <br>
Risk: Exposing port 18789 can make the OpenClaw instance reachable outside the intended host or tailnet. <br>
Mitigation: Keep port 18789 bound to 127.0.0.1 unless intentionally exposing it through Tailscale or a tightly scoped firewall rule. <br>
Risk: Optional host credential mounts can expose GitHub, package registry, or other local credentials to the container. <br>
Mitigation: Leave optional host credential mounts disabled unless needed and only enable mounts for container images the user trusts. <br>
Risk: Docker setup and repair commands can change local configuration or require elevated trust. <br>
Mitigation: Review docker-setup.sh and any --fix command before running it, especially when using sudo or modifying OpenClaw configuration. <br>


## Reference(s): <br>
- [OpenClaw Docker Setup on ClawHub](https://clawhub.ai/djc00p/openclaw-docker-linux) <br>
- [ClawHub package homepage](https://clawhub.com/djc00p/openclaw-docker-linux) <br>
- [Docker Configuration](references/docker-config.md) <br>
- [OpenClaw Docker Quickstart](references/quickstart.md) <br>
- [OpenClaw Docker Management Script](references/docker-setup.sh) <br>
- [Critical Gotchas](references/gotchas.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash, YAML, and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Linux-focused Docker setup guidance that references Docker, docker-compose, Tailscale, ANTHROPIC_API_KEY, and OPENCLAW_GATEWAY_TOKEN.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release metadata and skill frontmatter metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
