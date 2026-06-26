## Description: <br>
Research paper knowledge base for storing and querying academic papers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[myd2002](https://clawhub.ai/user/myd2002) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers and agents use this skill to save arXiv links or uploaded PDFs into a personal paper knowledge base, generate concise paper metadata and summaries, and query previously stored papers. It coordinates Gitea-backed paper storage with Feishu table records for retrieval and review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill ships and uses high-impact Gitea admin access. <br>
Mitigation: Do not use the bundled token; rotate it if it was ever valid, require HTTPS, and replace admin-wide repository creation with least-privilege access. <br>
Risk: The skill stores user identity mappings, paper metadata, generated notes, and PDFs in remote Gitea and Feishu systems. <br>
Mitigation: Tell users explicitly what will be stored and where, and apply appropriate access controls before deployment. <br>
Risk: PDF upload paths could reference files outside the paper ingestion request. <br>
Mitigation: Restrict PDF paths to files produced or uploaded for the current request. <br>


## Reference(s): <br>
- [Paper Kb on ClawHub](https://clawhub.ai/myd2002/paper-kb) <br>
- [Publisher profile: myd2002](https://clawhub.ai/user/myd2002) <br>
- [arXiv API endpoint used by the skill](http://export.arxiv.org/api/query?id_list={arxiv_id}) <br>
- [arXiv PDF endpoint used by the skill](https://arxiv.org/pdf/{arxiv_id}.pdf) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, configuration, guidance] <br>
**Output Format:** [Markdown and structured tool-call payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update Gitea repositories, Markdown paper records, PDF copies, index data, and Feishu table rows.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
