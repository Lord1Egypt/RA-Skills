## Description: <br>
Connect to TigerGraph distributed graph database to query, load, and manage large-scale knowledge graph data using GSQL and REST++ APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fisa712](https://clawhub.ai/user/fisa712) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and graph engineers use this skill to generate TigerGraph connection, query, loading, and graph analytics guidance for knowledge graph workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The connector may report successful TigerGraph connections, queries, inserts, or CSV loads without performing real TigerGraph client operations. <br>
Mitigation: Treat generated connector behavior as sample material until real TigerGraph client calls are implemented and tested against a non-production graph. <br>
Risk: Prompts or source files may expose TigerGraph credentials if users include live API tokens, usernames, or passwords. <br>
Mitigation: Use scoped tokens, keep secrets out of prompts and source files, and require explicit approval before live data or schema changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fisa712/knowledge-graph-tigergraph-connector) <br>
- [TigerGraph official documentation](https://docs.tigergraph.com/) <br>
- [GSQL reference](https://docs.tigergraph.com/gsql-ref/current/) <br>
- [REST++ API guide](https://docs.tigergraph.com/api/rest-api/) <br>
- [pyTigerGraph documentation](https://pytigergraph.github.io/intro/) <br>
- [TigerGraph patterns](references/tigergraph-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline code blocks and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Python snippets, GSQL examples, REST++ endpoint guidance, and operational recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
