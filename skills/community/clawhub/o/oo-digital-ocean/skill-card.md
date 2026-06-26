## Description: <br>
Use this skill for DigitalOcean requests involving account and resource lookup, listing, and approved Droplet lifecycle operations through an OOMOL-connected account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and cloud administrators use this skill to inspect DigitalOcean account, Droplet, App Platform, database, DNS, firewall, load balancer, and VPC resources through an OOMOL-connected account. It can also initiate basic Droplet lifecycle actions when the user explicitly approves the target action. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan reports that the skill can trigger DigitalOcean Droplet lifecycle changes while describing untagged actions as safe to run directly. <br>
Mitigation: Treat manage_droplet_lifecycle as a write action and require explicit user approval of the target Droplet and lifecycle operation before execution. <br>
Risk: The skill may require running remote installer commands for the oo CLI during first-time setup. <br>
Mitigation: Run remote installer commands only when the CLI is missing and after confirming that the user trusts OOMOL and needs the CLI for this workflow. <br>
Risk: The skill requires sensitive DigitalOcean credentials through an OOMOL-connected account. <br>
Mitigation: Use least-privilege DigitalOcean credentials, review connection scopes, and avoid connecting production resources unless the user has approved the operational risk. <br>


## Reference(s): <br>
- [DigitalOcean homepage](https://www.digitalocean.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON command responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses OOMOL server-side credential injection and returns connector responses containing data and execution metadata.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
