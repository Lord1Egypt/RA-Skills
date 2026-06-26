## Description: <br>
Metaso lets an agent search Metaso, read webpages, and create Metaso chat completions through an OOMOL-connected account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to operate Metaso from an agent session through OOMOL's oo CLI, including search, webpage reading, and Metaso-grounded chat completions. It is most useful when the user has already connected a Metaso account in OOMOL and wants the agent to inspect live action schemas before running connector commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an OOMOL-connected Metaso account and requires sensitive credentials managed outside the agent session. <br>
Mitigation: Install it only when the user trusts OOMOL and intends the agent to use the connected Metaso account. <br>
Risk: Write actions can create Metaso chat completions or otherwise affect account-backed service usage. <br>
Mitigation: Inspect the live connector schema first and confirm the exact payload and expected effect with the user before running any action tagged [write]. <br>
Risk: Setup commands for installing or signing into the oo CLI can change the local environment or open account access flows. <br>
Mitigation: Run install, login, or connection setup only after a matching command failure or an explicit user request. <br>


## Reference(s): <br>
- [Metaso homepage](https://metaso.cn) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL connection settings for Metaso](https://console.oomol.com/app-connections?provider=metaso) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return Metaso connector responses as JSON, including data and meta.executionId fields.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
