## Description: <br>
Use this skill to search and read Checkly data through an OOMOL-connected account instead of calling the Checkly API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and external users use this skill to inspect Checkly checks, check results, current statuses, and account details through an OOMOL-managed connector. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill routes Checkly access through an OOMOL-managed connector and requires the user to connect a Checkly account. <br>
Mitigation: Install only after confirming trust in OOMOL as the connector provider and confirming the intended Checkly account connection. <br>
Risk: A future connector schema or skill version could expose write or destructive Checkly actions. <br>
Mitigation: Require explicit user approval before running any action that writes, removes, overwrites, or changes Checkly data. <br>
Risk: First-time setup may require installing the oo CLI before the connector can run. <br>
Mitigation: Use organization-approved installation practices and fall back to setup steps only after a command fails because the CLI, authentication, or connection is missing. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/oomol/skills/oo-checkly) <br>
- [Checkly Homepage](https://www.checklyhq.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector actions return JSON data with execution metadata when run.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
