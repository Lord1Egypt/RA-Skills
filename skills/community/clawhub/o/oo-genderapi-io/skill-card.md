## Description: <br>
GenderAPI.io helps an agent use OOMOL's GenderAPI.io connector to infer likely gender from a first name, email address, username, or nickname. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to run read-only GenderAPI.io lookups through an OOMOL-connected account. It is intended for tasks that need likely gender inference from names, email addresses, usernames, or nicknames. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a connected GenderAPI.io API key through OOMOL. <br>
Mitigation: Confirm the user trusts OOMOL as the connector provider before installing or using the skill. <br>
Risk: Connector actions may change over time even though the current skill lists only read actions. <br>
Mitigation: Inspect the live connector schema before building payloads and get separate approval for any future write or destructive action. <br>
Risk: Gender inference can produce sensitive or inaccurate classifications. <br>
Mitigation: Use results as probabilistic signals, avoid treating them as identity facts, and apply appropriate review for privacy-sensitive workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-genderapi-io) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>
- [GenderAPI.io homepage](https://www.genderapi.io) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, JSON, configuration guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON connector responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill directs the agent to inspect live connector schemas before execution and to use OOMOL-managed credentials rather than handling raw GenderAPI.io tokens.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
