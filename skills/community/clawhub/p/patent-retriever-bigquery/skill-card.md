## Description: <br>
Team ZeeLin's production-grade patent evidence retrieval skill for Google Patents BigQuery converts natural-language research intent into auditable multi-round retrieval plans with explicit filters and validated JSON artifacts for downstream analysis and drafting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yangyuwen-bri](https://clawhub.ai/user/yangyuwen-bri) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, patent researchers, and technical teams use this skill to turn natural-language patent research goals into filtered Google Patents BigQuery searches and structured retrieval artifacts for downstream review, analysis, and drafting. It retrieves and structures patent evidence only and does not provide legal conclusions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses Google Cloud credentials and may run BigQuery jobs that incur charges or create cloud-side logs. <br>
Mitigation: Use a dedicated least-privilege service account, set billing controls where available, and run only in a Google Cloud project approved for this retrieval work. <br>
Risk: The generated query plan may not strictly preserve the intended Google Patents BigQuery table scope or user-specified filters. <br>
Mitigation: Review query_plan.json before execution and confirm the table remains patents-public-data.patents.publications, with filters and limits matching the request. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/yangyuwen-bri/patent-retriever-bigquery) <br>
- [Homepage](https://github.com/yangyuwen-bri/patent-retriever-bigquery) <br>
- [Methodology](references/methodology.md) <br>
- [Quickstart](examples/quickstart.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and generated JSON files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces concept_scan.json, query_plan.json, retriever_raw.json, and retriever_result.json; outputs should be schema-validated before downstream use.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
