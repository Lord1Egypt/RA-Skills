## Description: <br>
Eventzilla (eventzilla.net). Use this skill for Eventzilla requests involving searching and reading data through the OOMOL connector rather than calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to search and read Eventzilla events, attendees, tickets, transactions, organizers, and sub-organizers through an OOMOL-connected Eventzilla account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access to an OOMOL-connected Eventzilla account and can read event, attendee, ticket, transaction, and user data visible to that account. <br>
Mitigation: Install and connect it only for intended Eventzilla accounts, and review the requested action and query before execution. <br>
Risk: First-time setup may require CLI installation, OOMOL sign-in, or Eventzilla account connection steps. <br>
Mitigation: Approve setup steps only when an action fails because authentication or connection is missing, and only if granting that access is intended. <br>


## Reference(s): <br>
- [ClawHub Eventzilla skill listing](https://clawhub.ai/oomol/oo-eventzilla) <br>
- [Eventzilla homepage](https://www.eventzilla.net) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payloads or responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before constructing action payloads.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
