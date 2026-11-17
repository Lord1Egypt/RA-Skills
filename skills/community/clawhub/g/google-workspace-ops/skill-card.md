## Description:

Operate across Google Drive, Docs, Sheets, and Slides as a unified workflow to find, summarize, edit, migrate, or clean shared documents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[djc00p](https://clawhub.ai/user/djc00p)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and workspace operators use this skill to find canonical Google Drive assets, inspect Docs, Sheets, and Slides, and make or recommend precise cleanup, restructuring, summarization, and migration changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make live changes to shared Google Workspace files.

Mitigation: Review the selected file, ranges, and planned edits before applying changes; use copies or version history for important documents.

Risk: Google credentials may grant broader Drive, Docs, Sheets, or Slides access than the task requires.

Mitigation: Install and run the skill only with credentials scoped to the minimum needed access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/djc00p/skills/google-workspace-ops)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Structured plain text or Markdown with ASSET, CURRENT STATE, ACTION, and FOLLOW-UPS sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include file identity, document structure, edits made or recommended, and cleanup follow-ups]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
