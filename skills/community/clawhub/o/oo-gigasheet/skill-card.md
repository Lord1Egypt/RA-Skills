## Description: <br>
Gigasheet (gigasheet.com). Use this skill for Gigasheet requests involving searching and reading data through the OOMOL connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to inspect Gigasheet datasets, library metadata, exports, account usage, and storage details through an OOMOL-connected Gigasheet account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a connected Gigasheet account and OOMOL credential handling. <br>
Mitigation: Install only for environments where the agent is allowed to access that connected account, and treat credentials and account sessions as sensitive. <br>
Risk: Connector actions depend on live schemas and account state, so stale assumptions can produce incorrect payloads or failed commands. <br>
Mitigation: Fetch the action schema with `oo connector schema` before constructing payloads and retry setup only when authentication or connection errors occur. <br>


## Reference(s): <br>
- [Gigasheet Skill on ClawHub](https://clawhub.ai/oomol/oo-gigasheet) <br>
- [Gigasheet Homepage](https://www.gigasheet.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI Install Guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before constructing action payloads; command results may include JSON data and execution metadata.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
