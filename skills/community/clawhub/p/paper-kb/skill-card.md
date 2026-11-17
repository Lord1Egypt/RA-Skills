## Description:

Research paper knowledge base for storing and querying academic papers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[myd2002](https://clawhub.ai/user/myd2002)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers and developers use this skill to save arXiv links or uploaded PDFs into a personal paper knowledge base, organize paper summaries and metadata in Gitea and Feishu, and query previously stored papers in natural language.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Overly powerful or exposed Gitea credentials could expose or modify private paper repositories.

Mitigation: Revoke the exposed token, remove hardcoded secrets from the release, and require deployment-provided credentials with least-privilege access.

Risk: Plain HTTP access to the configured Gitea service can expose credentials and paper data in transit.

Mitigation: Require HTTPS for Gitea endpoints before installation or runtime use.

Risk: Weak server-side user authorization could allow cross-user access to paper metadata or stored files.

Mitigation: Enforce server-side authorization checks before reading or writing user, repository, Feishu, or paper records.

Risk: PDF ingestion from local paths can expose unintended local files.

Mitigation: Restrict PDF processing to approved user-provided upload paths and reject arbitrary local file paths.

Risk: Users may not understand what identity and paper data is stored in Gitea and Feishu.

Mitigation: Document the stored identity fields, paper metadata, generated summaries, PDFs, Gitea locations, and Feishu table records before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/myd2002/skills/paper-kb)
- [Publisher profile](https://clawhub.ai/user/myd2002)
- [arXiv API query endpoint](http://export.arxiv.org/api/query?id_list={arxiv_id})
- [arXiv PDF endpoint](https://arxiv.org/pdf/{arxiv_id}.pdf)

## Skill Output:

**Output Type(s):** [text, markdown, files, configuration, guidance]

**Output Format:** [Chinese user-facing text, Markdown paper notes, JSON tool responses, and configured Gitea/Feishu records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can store generated Markdown, optional PDFs, index metadata, and Feishu table rows for each registered user.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
