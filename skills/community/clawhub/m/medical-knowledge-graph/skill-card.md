## Description: <br>
Medical Knowledge Graph helps agents query a medical graph covering diseases, drugs, symptoms, diagnoses, complications, diet, and their relationships. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[alinklab](https://clawhub.ai/user/alinklab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to inspect the medical graph schema and run read-only Cypher queries against a third-party knowledge graph API. It is best suited for preliminary research workflows where results are reviewed before practical use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Graph queries are sent to xiaobenyang's external API. <br>
Mitigation: Avoid submitting sensitive patient information unless the service's privacy terms and deployment context meet the user's requirements. <br>
Risk: The API key is stored in a local .env file. <br>
Mitigation: Protect the local environment file, rotate exposed keys, and avoid committing credentials. <br>
Risk: The artifact contains mismatched school-search template references. <br>
Mitigation: Treat those references as quality issues and rely on the documented medical graph tools for actual use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alinklab/medical-knowledge-graph) <br>
- [Xiaobenyang API provider](https://xiaobenyang.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, API calls] <br>
**Output Format:** [Markdown summaries of JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an XBY_APIKEY before API-backed graph queries can run.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
