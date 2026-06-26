## Description: <br>
Add a knowledge graph layer to an AI agent for relationship reasoning and multi-hop recall. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vnesin-sarai](https://clawhub.ai/user/vnesin-sarai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to add entity extraction, graph storage, relationship traversal, and graph-assisted retrieval to AI agent memory systems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill guides agents to build persistent relationship memory from indexed content, which may expose sensitive relationships if broad or confidential data sources are included. <br>
Mitigation: Scope indexed sources deliberately, avoid sensitive documents unless intended, and apply retention and access controls to any SQLite or Neo4j graph. <br>
Risk: Graph results can become noisy or misleading when entity extraction creates too many low-value edges. <br>
Mitigation: Create edges only between named entities, prune orphan or weak nodes periodically, and evaluate relationship queries against expected results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vnesin-sarai/knowledge-graph-agents) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Configuration] <br>
**Output Format:** [Markdown with SQL, Cypher, and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; no installer or required runtime commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
