## Description:

Answer Research KB dialogue questions with team-overview-guided web search, external citations, optional reference attachments, and no QA persistence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[myd2002](https://clawhub.ai/user/myd2002)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Research KB users use this skill to answer dialogue questions by first reading team overview context, then performing focused web search and returning cited, team-relevant answers without persisting QA entries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Gitea credentials and repository access for Research KB content.

Mitigation: Install only with trusted backend payloads and use a least-privilege, preferably read-only Gitea bot token.

Risk: Payload-controlled host, repository, attachment, or result paths could broaden access if deployment boundaries are loose.

Mitigation: Fix or allowlist Gitea host and repository values, constrain attachments to an upload directory, and confine result paths to the task workspace.

Risk: Generated answers depend on external web sources and may contain uncited or time-sensitive claims if search evidence is incomplete.

Mitigation: Require recorded webSources for important external claims and review answers before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/myd2002/skills/kb-web-query)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown answer with cited sources plus JSON result files written by helper commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [External web sources must be recorded; QA persistence is disabled.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
