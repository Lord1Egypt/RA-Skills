## Description: <br>
Loomio lets an agent search and read Loomio poll data through an OOMOL-connected account using the oo CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to retrieve Loomio poll details and list polls in a group through an OOMOL-connected account without handling raw Loomio API tokens. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive Loomio credentials through OOMOL and depends on OOMOL as an intermediary for Loomio access. <br>
Mitigation: Install only if that intermediary model is acceptable, connect Loomio through OOMOL intentionally, and avoid exposing raw API tokens in prompts or command payloads. <br>
Risk: First-time setup commands can install the oo CLI or start account connection flows. <br>
Mitigation: Use setup steps only after an auth, connection, or missing-CLI failure, as directed by the skill. <br>


## Reference(s): <br>
- [ClawHub Loomio skill page](https://clawhub.ai/oomol/oo-loomio) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [Loomio homepage](https://www.loomio.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON CLI responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses oo connector schema before oo connector run; Loomio connector responses are JSON with data and meta.executionId.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
