## Description: <br>
Operates Codacy through an OOMOL-connected account for reading user, organization, repository, language, tool, and pattern data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to query Codacy data through the OOMOL connector without handling raw API tokens directly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive Codacy credentials through an OOMOL-connected account. <br>
Mitigation: Confirm the ClawHub skill name, publisher, and files before installation, and connect Codacy only through the documented OOMOL account flow. <br>
Risk: Connector inputs can change over time, causing incorrect or failed Codacy calls if stale payloads are reused. <br>
Mitigation: Fetch each action's live schema with `oo connector schema` before building a payload. <br>
Risk: Future write or destructive Codacy actions could change or remove data if executed without review. <br>
Mitigation: Confirm the exact target, payload, and expected effect with the user before running any action tagged `[write]` or `[destructive]`. <br>


## Reference(s): <br>
- [Codacy homepage](https://www.codacy.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-codacy) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill instructs the agent to fetch live connector schemas before running Codacy actions.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
