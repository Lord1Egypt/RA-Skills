## Description: <br>
Scholarly literature and bibliographic databases: OpenAlex, Crossref, Europe PMC, PubMed, DOAJ, DBLP, and Semantic Scholar. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
AGPL-3.0 <br>


## Use Case: <br>
Researchers, developers, and agents use this skill to search public scholarly metadata, inspect bibliographic records, and query academic service agents through Pilot Protocol. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries are sent through Pilot Protocol service agents and may be visible to the pilotctl binary, daemon, or service-agent network. <br>
Mitigation: Use the skill for public scholarly metadata searches only, and avoid confidential, unpublished, or sensitive research queries. <br>
Risk: The skill depends on a running Pilot Protocol daemon, network 9 membership, and reachable service agents. <br>
Mitigation: Confirm pilotctl is installed, the daemon is running, the daemon has joined network 9, and the target agent contract has been checked with /help before use. <br>


## Reference(s): <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>
- [ClawHub Skill Page](https://clawhub.ai/teoslayer/pilot-service-agents-academic) <br>
- [Pilot Skills Catalog](https://teoslayer.github.io/pilot-skills/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses pilotctl to request agent help, structured data, summaries, and inbox responses from public academic metadata agents.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
