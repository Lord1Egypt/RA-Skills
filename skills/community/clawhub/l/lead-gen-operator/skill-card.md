## Description:

Automated lead generation assistant - finds companies, scores them, writes personalized outreach emails, and tracks pipeline.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawdquip](https://clawhub.ai/user/clawdquip)

### License/Terms of Use:


## Use Case:

Sales teams and business development operators use this skill to find prospects, enrich and score leads, draft outreach, send Gmail-backed messages when connected, and track pipeline follow-ups in OpenClaw.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores prospect data and outreach drafts in local workspace memory and can export that data to CSV.

Mitigation: Avoid sensitive or regulated contact data, protect exported files, and document deletion and retention controls before operational use.

Risk: The skill can send outreach through a connected Gmail tool and mutates lead status automatically.

Mitigation: Review generated recipients, message content, and status updates before sending or bulk-updating leads.

Risk: Security guidance identifies unsafe local file and command patterns, unvalidated memory filenames, CSV serialization concerns, and unpinned dependencies.

Mitigation: Prefer a patched version that validates memory filenames, avoids shell command construction from web-derived fields, safely serializes CSV, and pins dependencies.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/clawdquip/skills/lead-gen-operator)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON, CSV]

**Output Format:** [Markdown and plain text guidance with JSON memory records, CSV exports, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OpenClaw, Node.js, web search/fetch skills, and optional Gmail/gog integration; stores lead data in local workspace memory.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter metadata and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
