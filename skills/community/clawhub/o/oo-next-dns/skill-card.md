## Description: <br>
NextDNS helps an agent read profiles, logs, and analytics through an OOMOL-connected NextDNS account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent inspect NextDNS profiles, query DNS logs, and summarize analytics for an authenticated account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: DNS logs and analytics can reveal browsing and device activity from the connected account. <br>
Mitigation: Treat generated outputs as sensitive and avoid sharing log details beyond the intended audience. <br>
Risk: The skill requires an OOMOL-connected NextDNS account and may prompt setup if the CLI or connection is missing. <br>
Mitigation: Install or sign in to the OOMOL CLI only when needed, and connect NextDNS through the documented OOMOL connection flow. <br>


## Reference(s): <br>
- [ClawHub NextDNS Skill Page](https://clawhub.ai/oomol/oo-next-dns) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [NextDNS Homepage](https://nextdns.io/) <br>
- [OOMOL NextDNS Connection](https://console.oomol.com/app-connections?provider=next_dns) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only connector actions; requires an authenticated OOMOL-connected NextDNS account.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
