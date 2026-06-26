## Description: <br>
NewsData.io (newsdata.io). Use this skill for NewsData.io news retrieval, source listing, cryptocurrency news, and historical archive search through an OOMOL-connected account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to query NewsData.io through the OOMOL oo CLI for latest news, breaking news, cryptocurrency news, source-domain discovery, and historical archive search. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an OOMOL-connected NewsData.io account and uses sensitive credentials brokered by OOMOL. <br>
Mitigation: Install only when OOMOL and the oo CLI are acceptable for the user's NewsData.io account, and review first-time setup commands before running them. <br>
Risk: A listed action is tagged write even though the connector is primarily news-retrieval oriented. <br>
Mitigation: Confirm any write-tagged action's exact payload and intended effect with the user before execution. <br>
Risk: Connector schemas may change over time. <br>
Mitigation: Fetch the live action schema with `oo connector schema` before constructing a payload. <br>


## Reference(s): <br>
- [NewsData.io homepage](https://newsdata.io) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands call the OOMOL oo CLI and return connector JSON responses when executed.] <br>

## Skill Version(s): <br>
1.0.2 (source: server evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
