## Description: <br>
OpenDART CLI helps agents use Korea FSS DART OpenAPI data from the terminal to retrieve disclosures, company profiles, financial statements, shareholder holdings, executive holdings, and disclosure document ZIP files as JSON. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chloepark85](https://clawhub.ai/user/chloepark85) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, financial analysts, and agent builders use this skill to query Korean corporate disclosure data and pipe structured JSON results into research, monitoring, and finance workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a sensitive OpenDART API credential. <br>
Mitigation: Provide the credential only through OPENDART_API_KEY and avoid placing it in command arguments, logs, or shared files. <br>
Risk: The skill can write local cache files and disclosure document ZIP files. <br>
Mitigation: Review the cache location and document output path before running download commands. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/chloepark85/opendart-cli) <br>
- [OpenDART official site](https://opendart.fss.or.kr) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON-oriented CLI examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OPENDART_API_KEY for API access; can create a local corp-code cache and save disclosure document ZIP files to user-selected paths.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence, target metadata, SKILL.md frontmatter, pyproject.toml, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
