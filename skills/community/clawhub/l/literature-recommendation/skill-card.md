## Description: <br>
Reads team research profiles from PostgreSQL, fetches candidate arXiv papers, ranks them with rule-based matching, and outputs OpenClaw personal-card recommendation payloads. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhcolin0313](https://clawhub.ai/user/zhcolin0313) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw operators and team workflow maintainers use this skill to generate literature recommendations from member research preferences. It prepares rule-scored arXiv candidate sets, stored recommendation history, and personal-card JSON for downstream delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow requires access to a PostgreSQL database containing member research profiles and Feishu user IDs. <br>
Mitigation: Use a dedicated low-privilege database account and grant only the access needed for profile loading and recommendation storage. <br>
Risk: Generated JSON reports and stored recommendation history can contain research preferences, Feishu identifiers, paper abstracts, and recommendation reasons. <br>
Mitigation: Restrict the output directory and define retention or cleanup rules for generated reports and stored history. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zhcolin0313/literature-recommendation) <br>
- [arXiv API Query Endpoint](https://export.arxiv.org/api/query) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Configuration] <br>
**Output Format:** [CLI output and generated JSON reports containing rerank payloads, member reports, and personal-card delivery payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OPENCLAW_DB_DSN; optional output directory and recall-pool settings control generated report storage and candidate count.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and skill.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
