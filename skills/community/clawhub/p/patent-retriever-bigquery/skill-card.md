## Description:

Zeelin Patent Retriever converts natural-language patent research intent into auditable Google Patents BigQuery retrieval plans and validated JSON evidence outputs for downstream analysis and drafting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangyuwen-bri](https://clawhub.ai/user/yangyuwen-bri)

### License/Terms of Use:


## Use Case:

Developers, patent researchers, and product teams use this skill to retrieve, deduplicate, and structure Google Patents BigQuery evidence for prior-art and technology-intelligence workflows. It supports filter-aware searches by keyword, geography, date, assignee/inventor, and IPC/CPC without providing legal conclusions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A mutable query plan can redirect BigQuery access beyond the stated Google Patents dataset.

Mitigation: Before execution, verify query_plan.json keeps the table set to patents-public-data.patents.publications.

Risk: BigQuery searches have no default billing cap.

Mitigation: Set a nonzero --max-bytes-billed limit and prefer narrower date windows, country scopes, and keyword filters before broad scans.

Risk: Google Cloud credentials may grant broader access than this skill requires.

Mitigation: Run the skill in an isolated environment with a narrowly scoped Google Cloud identity.

Risk: Unpinned Python dependencies can affect reproducibility.

Mitigation: Pin or lock dependencies before production use when reproducible installs are required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yangyuwen-bri/skills/patent-retriever-bigquery)
- [Project homepage](https://github.com/yangyuwen-bri/patent-retriever-bigquery)
- [Methodology](references/methodology.md)
- [Quickstart](examples/quickstart.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON files]

**Output Format:** [Markdown guidance with bash and Python snippets plus validated JSON artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces concept_scan.json, query_plan.json, retriever_raw.json, and retriever_result.json; retriever results require publication_number and title entries.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
