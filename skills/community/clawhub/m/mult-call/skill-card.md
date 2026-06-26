## Description: <br>
Mult Call analyzes intent-recognition output, retrieves related QA and SQL examples from a vector knowledge base, and retrieves table DDL from a graph database. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LoveNerverMore](https://clawhub.ai/user/LoveNerverMore) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data-agent builders use this skill as a retrieval step after intent recognition to gather table schema, metric context, and similar QA/SQL examples before SQL generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill loads shared environment variables into a Python subprocess, which can expose unrelated credentials if the shared skills .env contains broad secrets. <br>
Mitigation: Install it only with least-privilege credentials for this workflow, and keep unrelated API keys, account tokens, and production secrets out of the shared .env. <br>
Risk: Business questions and retrieval context may be sent to configured Neo4j, Milvus, and embedding endpoints. <br>
Mitigation: Review those endpoint configurations before using the skill with sensitive business questions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/LoveNerverMore/mult-call) <br>
- [Publisher profile](https://clawhub.ai/user/LoveNerverMore) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, configuration] <br>
**Output Format:** [JSON containing table DDL, indicator metrics, and QA/SQL pairs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Neo4j failures degrade to empty or default DDL, and Milvus failures degrade to empty QA pairs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
