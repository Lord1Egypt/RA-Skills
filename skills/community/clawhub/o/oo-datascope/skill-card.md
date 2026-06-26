## Description: <br>
DataScope helps agents read, create, and update DataScope records through an OOMOL-connected account using the oo CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent inspect DataScope connector schemas, list locations, answers, and metadata list elements, and prepare confirmed create or update actions for DataScope records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill operates a connected DataScope account and requires sensitive credentials. <br>
Mitigation: Install it only if you trust OOMOL and intend to let the agent operate DataScope through the connected account. <br>
Risk: Create and update actions can change DataScope records. <br>
Mitigation: Review the exact payload and expected effect before approving any write action. <br>


## Reference(s): <br>
- [ClawHub DataScope skill page](https://clawhub.ai/oomol/oo-datascope) <br>
- [DataScope homepage](https://www.mydatascope.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May run oo CLI connector actions that return JSON data and execution metadata.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
