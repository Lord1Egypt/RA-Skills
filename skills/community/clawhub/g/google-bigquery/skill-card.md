## Description: <br>
Google BigQuery API integration with managed OAuth for running SQL queries, managing datasets and tables, and analyzing data at scale. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data analysts use this skill to access BigQuery through Maton-managed OAuth, run SQL queries, inspect projects, datasets, and tables, manage resources, and retrieve analytics results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on a Maton API key and OAuth-brokered access to a connected Google BigQuery account. <br>
Mitigation: Install only if Maton is trusted to broker access, store the API key securely, and use least-privilege Google permissions. <br>
Risk: BigQuery requests can read sensitive data, modify datasets or tables, write query results, or incur usage costs. <br>
Mitigation: Verify the intended project, dataset, table, connection ID, and operation before requests; require explicit review for create, update, delete, write, or high-cost queries. <br>


## Reference(s): <br>
- [ClawHub Google BigQuery Skill](https://clawhub.ai/byungkyu/google-bigquery) <br>
- [Maton](https://maton.ai) <br>
- [BigQuery API Overview](https://cloud.google.com/bigquery/docs/reference/rest) <br>
- [BigQuery Datasets API](https://cloud.google.com/bigquery/docs/reference/rest/v2/datasets) <br>
- [BigQuery Tables API](https://cloud.google.com/bigquery/docs/reference/rest/v2/tables) <br>
- [BigQuery Jobs API](https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs) <br>
- [BigQuery Standard SQL Reference](https://cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with API paths and inline code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MATON_API_KEY and a BigQuery OAuth connection; write operations require explicit user approval.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
