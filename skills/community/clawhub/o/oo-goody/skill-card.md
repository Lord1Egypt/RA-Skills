## Description: <br>
This skill operates Goody through OOMOL's oo CLI, guiding agents to inspect action schemas and run Goody connector actions with validated JSON payloads. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill when they want an agent to operate a Goody account through an OOMOL-connected account, including reading account context, orders, products, payment methods, workspaces, and active catalog products. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a user-connected OOMOL and Goody account, so connector actions can access account data available to that integration. <br>
Mitigation: Install it only when Goody operation through OOMOL is intended, and connect only accounts whose accessible data is appropriate for the agent to use. <br>
Risk: Write or destructive connector actions could change Goody account state if run with an incorrect payload. <br>
Mitigation: Review the live action schema, confirm the exact payload and expected effect with the user, and require explicit approval before state-changing or destructive actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-goody) <br>
- [Publisher profile](https://clawhub.ai/user/oomol) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [Goody homepage](https://www.ongoody.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before building action payloads.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
