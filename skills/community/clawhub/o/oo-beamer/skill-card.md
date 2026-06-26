## Description: <br>
Beamer (getbeamer.com). Use this skill for Beamer requests that read, create, or update data through an OOMOL-connected account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect Beamer schemas, read Beamer posts and feed URLs, count unread posts, and create changelog posts through the oo CLI with an OOMOL-connected Beamer account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use an OOMOL-connected Beamer account and requires sensitive credentials managed outside the prompt. <br>
Mitigation: Install and use it only when the user intends to let an agent operate that connected Beamer account. <br>
Risk: The create_post action can publish or change visible Beamer changelog content. <br>
Mitigation: Review and confirm the exact create_post payload and expected effect before approving the action. <br>
Risk: Optional oo CLI installer commands fetch and execute remote installer scripts. <br>
Mitigation: Run those installers only when the CLI is needed and the user trusts OOMOL as the provider. <br>


## Reference(s): <br>
- [Beamer skill page](https://clawhub.ai/oomol/oo-beamer) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [Beamer homepage](https://www.getbeamer.com) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the live oo connector schema before running Beamer actions; command output may include JSON responses with execution metadata.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
