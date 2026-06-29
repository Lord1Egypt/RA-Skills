## Description: <br>
KIE.AI helps an agent check account credits and convert generated file URLs through an OOMOL-connected KIE.AI account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when they want an agent to operate KIE.AI through an OOMOL-connected account for read-oriented account and generated-file URL tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Account credit details and generated file download URLs can be sensitive. <br>
Mitigation: Treat account balances and temporary download URLs as private user data and disclose them only when needed for the user's task. <br>
Risk: First-time setup or login commands can initiate OOMOL account access setup. <br>
Mitigation: Run install, login, or connection steps only when the user expects setup or when an action fails with the matching authentication or connection error. <br>
Risk: Connector action payloads can drift if the service contract changes. <br>
Mitigation: Inspect the live connector schema before running an action and build payloads from that schema. <br>


## Reference(s): <br>
- [KIE.AI homepage](https://kie.ai) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [KIE.AI skill on ClawHub](https://clawhub.ai/oomol/skills/oo-kie-ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Actions return JSON from the oo CLI; inspect the live connector schema before constructing payloads.] <br>

## Skill Version(s): <br>
1.0.0 (source: skill frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
