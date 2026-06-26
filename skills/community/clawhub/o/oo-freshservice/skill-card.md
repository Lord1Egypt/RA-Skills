## Description: <br>
Freshservice enables an agent to read and create Freshservice tickets, service requests, locations, and service catalog data through the OOMOL Freshservice connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, support teams, and developers use this skill to list and retrieve Freshservice tickets, create tickets or service requests, and resolve Freshservice locations or service catalog items through an OOMOL-connected Freshservice account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access Freshservice records through an OOMOL-connected account. <br>
Mitigation: Install only when agent access to Freshservice is intended, and use an account with the least Freshservice permissions needed. <br>
Risk: Ticket and service request creation can change Freshservice state. <br>
Mitigation: Review the write payload and expected effect with the user before approving creation actions. <br>


## Reference(s): <br>
- [ClawHub Freshservice skill](https://clawhub.ai/oomol/oo-freshservice) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [Freshservice homepage](https://www.freshworks.com/freshservice/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON connector payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Write actions require user confirmation of the exact payload and expected effect before execution.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
