## Description: <br>
Helps agents search and read Productboard workspace data through OOMOL's Productboard connector and oo CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and product teams use this skill to let an agent retrieve Productboard entities, notes, teams, members, and workspace configurations through their connected OOMOL account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill allows an agent to read Productboard workspace data through OOMOL's connector. <br>
Mitigation: Install it only when the user trusts OOMOL's connector and intends to grant Productboard read/search access. <br>
Risk: Broad Productboard routing could make the skill eligible for ambiguous Productboard requests. <br>
Mitigation: Clarify ambiguous requests and inspect the live action schema before running commands with uncertain scope. <br>
Risk: Future actions tagged write or destructive could change or remove Productboard data. <br>
Mitigation: Require explicit user confirmation of the target, payload, and expected effect before any write or destructive action. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/oomol/skills/oo-productboard) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI Install Guide](https://cli.oomol.com/install-guide.md) <br>
- [Productboard Homepage](https://www.productboard.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documents read-oriented Productboard get/list actions and directs agents to inspect live action schemas before constructing payloads.] <br>

## Skill Version(s): <br>
1.0.1 (source: artifact frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
