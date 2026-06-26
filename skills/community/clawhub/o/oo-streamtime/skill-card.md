## Description: <br>
Streamtime (streamtime.net). Use this skill for Streamtime requests that read, create, or update data through the OOMOL-connected Streamtime connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external collaborators, and agents with an authorized OOMOL-connected Streamtime account use this skill to inspect Streamtime organisation records and to create or update companies, contacts, and jobs after user confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access Streamtime data through an OOMOL-connected account and requires sensitive credentials managed by that connection. <br>
Mitigation: Install only when the agent should use that Streamtime account, and sign in to the oo CLI only from trusted OOMOL sources. <br>
Risk: Create and update actions can change Streamtime companies, contacts, and jobs. <br>
Mitigation: Review the exact action payload and expected effect with the user before running write actions. <br>
Risk: Incorrect payloads can target the wrong Streamtime record or fail against the connector contract. <br>
Mitigation: Fetch the live connector schema for the selected action before constructing payloads. <br>


## Reference(s): <br>
- [ClawHub Streamtime listing](https://clawhub.ai/oomol/oo-streamtime) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [Streamtime homepage](https://www.streamtime.net) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before actions; write actions require user confirmation.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
