## Description: <br>
Hetzner Cloud CLI for managing servers, volumes, firewalls, networks, DNS, and snapshots. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pasogott](https://clawhub.ai/user/pasogott) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and infrastructure operators use this skill to get cautious Hetzner Cloud CLI setup guidance and command examples for managing servers, volumes, firewalls, networks, DNS, snapshots, and related resources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can propose commands that create or modify cloud infrastructure, including firewall, network, server, volume, and snapshot operations. <br>
Mitigation: Require explicit user confirmation after showing the exact command, and review each proposed command before execution. <br>
Risk: Hetzner API tokens or other credentials could be exposed if handled carelessly. <br>
Mitigation: Use project-specific least-privilege tokens, never paste tokens into chat, and never log credentials. <br>
Risk: Infrastructure changes can cause service disruption or data loss. <br>
Mitigation: Suggest a snapshot before modifications and do not execute delete commands. <br>


## Reference(s): <br>
- [Hetzner Cloud CLI repository](https://github.com/hetznercloud/cli) <br>
- [Hetzner Cloud Console](https://console.hetzner.cloud/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands are presented for user review and confirmation; the skill forbids delete commands and credential disclosure.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
