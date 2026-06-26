## Description: <br>
Knack (knack.com). Use this skill for ANY Knack request - reading, creating, updating, and deleting data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and operators use this skill to work with Knack records through an OOMOL-connected account. It supports listing, retrieving, creating, updating, and deleting records after inspecting the live connector schema. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a connected OOMOL account and Knack credentials. <br>
Mitigation: Install it only when the user trusts OOMOL and intends to let the agent operate the connected Knack account. <br>
Risk: Create and update actions can change Knack records. <br>
Mitigation: Confirm the exact payload and expected effect with the user before running write actions. <br>
Risk: Delete actions can remove Knack records. <br>
Mitigation: Require explicit approval of the object key, record ID, and expected effect before running destructive actions. <br>
Risk: Connector schemas can change over time, making stale payload assumptions risky. <br>
Mitigation: Inspect the live action schema before constructing payloads for connector actions. <br>


## Reference(s): <br>
- [ClawHub Knack skill page](https://clawhub.ai/oomol/oo-knack) <br>
- [Knack homepage](https://www.knack.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [OOMOL Knack connection](https://console.oomol.com/app-connections?provider=knack) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May run oo CLI connector actions that return JSON data and execution metadata.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
