## Description:

Compile backend-uploaded source files into Research KB Markdown wiki pages, write them to Gitea, archive sources, and return structured JSON results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[myd2002](https://clawhub.ai/user/myd2002)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and knowledge-base operators use this skill to turn backend-uploaded research, document, and code-source snapshots into traceable Chinese Markdown wiki pages in a configured Gitea-backed Research KB.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task-supplied local file paths and repository targets may allow unintended source access or writes.

Mitigation: Enforce a server-side upload root, repository allowlist, symlink rejection, path-traversal checks, and file-hash verification before ingestion.

Risk: Using an administrative Gitea token increases the impact of misconfiguration or malicious task input.

Mitigation: Use a repository-scoped service token with the minimum permissions needed for the target knowledge base.

Risk: Uploaded source material may contain secrets or sensitive content that could be archived or published into the knowledge base.

Mitigation: Scan and redact secrets before archiving or publishing uploaded material.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/myd2002/skills/kb-ingest)

## Skill Output:

**Output Type(s):** [markdown, json, files]

**Output Format:** [Markdown wiki pages and research_kb_agent_result JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes pages, catalogs, indexes, optional import reports, and archived sources to a configured Gitea-backed knowledge base.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
