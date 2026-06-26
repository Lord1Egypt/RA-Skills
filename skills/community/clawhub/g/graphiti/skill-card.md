## Description: <br>
Knowledge graph operations via Graphiti API. Search facts, add episodes, and extract entities/relationships. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[emasoudy](https://clawhub.ai/user/emasoudy) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to search a Graphiti knowledge graph and add new episodes or memories through the Graphiti REST API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can add persistent entries to a Graphiti knowledge graph. <br>
Mitigation: Avoid storing secrets or untrusted content as memories, and review additions before using the knowledge graph as shared context. <br>
Risk: The agent sends search and memory-write requests to the configured Graphiti endpoint. <br>
Mitigation: Verify the Graphiti endpoint before use and prefer Clawdbot configuration for selecting the service URL. <br>


## Reference(s): <br>
- [Graphiti project](https://github.com/getzep/graphiti) <br>
- [Graphiti skill page](https://clawhub.ai/emasoudy/graphiti) <br>
- [Environment discovery helper](references/env-check.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a reachable Graphiti service backed by Neo4j and Qdrant.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
