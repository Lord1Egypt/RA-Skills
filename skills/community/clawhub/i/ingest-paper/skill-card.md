## Description:

Ingest Paper helps an agent analyze user-provided research materials and store structured summaries, concepts, and resource pages in a personal knowledge base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[myd2002](https://clawhub.ai/user/myd2002)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and research teams use this skill to ingest papers, technical documents, project pages, meeting notes, and similar materials into a Gitea-backed research knowledge base with Chinese summaries and cross-linked concept or resource pages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence reports plaintext HTTP Gitea configuration and an over-privileged Gitea admin token.

Mitigation: Deploy only after changing GITEA_URL to HTTPS and replacing the site-admin token with the narrowest service credential that supports the required repository operations.

Risk: The release evidence reports broad file-read and persistence behavior for uploaded source files and generated knowledge-base content.

Mitigation: Run in a controlled environment, review what user materials may be persisted, and confirm that remote logs and uploaded source files are acceptable for the intended data.

Risk: Dependency installation and document parsing run locally against user-provided files.

Mitigation: Install dependencies in a pinned virtual environment and scan the skill before deployment, following the release evidence security guidance.

## Reference(s):

- [Ingest Paper ClawHub skill page](https://clawhub.ai/myd2002/skills/ingest-paper)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON-producing helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Chinese structured summaries, catalog updates, optional PDF archival links, concept/resource pages, and optional Feishu table records.]

## Skill Version(s):

2.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
