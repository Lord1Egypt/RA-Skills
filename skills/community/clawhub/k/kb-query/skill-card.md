## Description:

Answer Research KB questions from the team Gitea-backed knowledge base with OpenClaw reasoning, optional reference attachments, stable citations, OpenClaw-led evidence selection, and optional high-value Q&A persistence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[myd2002](https://clawhub.ai/user/myd2002)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and research-team KB users use this skill to answer questions against a team Gitea-backed knowledge base, optionally using temporary attachments for context and persisting reusable high-value Q&A entries when policy allows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a bot token to read and write a Gitea-backed knowledge base.

Mitigation: Run it only with trusted backend payloads and a tightly scoped bot account limited to the intended KB repository.

Risk: Payload or environment configuration can select the Gitea host used by the helper scripts.

Mitigation: Require an allowlisted HTTPS Gitea host before production use.

Risk: The skill reads attachment paths and writes result paths supplied through backend payloads.

Mitigation: Constrain attachment and result paths to trusted directories and reject symlinks or path traversal.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/myd2002/skills/kb-query)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown answer text with JSON result files and cited KB sources]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update high-value Q&A pages, catalog entries, and index entries when policy and evidence gates allow.]

## Skill Version(s):

1.0.8 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
