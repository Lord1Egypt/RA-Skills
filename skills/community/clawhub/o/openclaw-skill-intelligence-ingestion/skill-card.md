## Description:

Auto-analyzes URLs and external information for OpenClaw strategic value, classifies the content, creates Obsidian notes, updates memory, and returns a concise ingestion summary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[2233admin](https://clawhub.ai/user/2233admin)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to turn shared URLs, articles, tweets, and pasted external information into structured OpenClaw intelligence notes, memory updates, strategic value scores, and next-step recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically ingest shared links and pasted content and archive the results into Obsidian and OpenClaw memory.

Mitigation: Use it only when that archival behavior is intended, narrow the trigger scope, and require confirmation before file or memory writes.

Risk: Fetched external content may be untrusted, misleading, inaccessible, or attacker-controlled.

Mitigation: Treat fetched content as untrusted input, review generated notes before relying on them, and preserve source links for later verification.

Risk: The skill references fixed Obsidian and memory paths that may not match every deployment environment.

Mitigation: Review and adjust target paths before use, and pin installation to a reviewed release or commit.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/2233admin/skills/openclaw-skill-intelligence-ingestion)
- [Repository homepage](https://github.com/sarahmirrand001-oss/openclaw-skill-intelligence-ingestion)
- [Repository skill specification](https://github.com/sarahmirrand001-oss/openclaw-skill-intelligence-ingestion/blob/main/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown notes, memory-log entries, and concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create Obsidian notes and update OpenClaw memory files when the host agent has the required filesystem access.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
