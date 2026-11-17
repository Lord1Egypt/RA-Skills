## Description:

Injects a lightweight, dependency-free inline text editor into static HTML pages so users can edit wording in the browser and export only changed text blocks for source backfill.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ytisvibecoding](https://clawhub.ai/user/ytisvibecoding)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to turn static HTML reports, dashboards, and generated pages into editable text-only copies for non-technical review. It supports a round trip where the user's exported JSON changes are applied back to the source HTML by content match.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Edited text blocks are represented as raw HTML and may introduce executable markup into the page.

Mitigation: Review exported JSON diffs and the resulting HTML for markup or scripts before deployment.

Risk: Applying an untrusted or incorrect JSON diff can modify source HTML unexpectedly.

Mitigation: Use dry runs and backups, and apply only JSON diffs from trusted, reviewed editing sessions.

Risk: Report or dashboard content may be exposed if sent to an external AI during the edit round trip.

Mitigation: Avoid sending confidential report content to external services unless that handling is approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ytisvibecoding/skills/html-text-editor-lite)
- [Publisher profile](https://clawhub.ai/user/ytisvibecoding)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and generated HTML or JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces an editable HTML copy by default, can export changed text blocks as JSON, and can apply reviewed JSON changes back to the source HTML.]

## Skill Version(s):

1.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
