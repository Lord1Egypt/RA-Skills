## Description:

Use when the user wants a periodic keyword position report, including quick wins, striking distance, and movement since the last period, as a document from Search Console data or TrustGrowth keyword lifecycle data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[trustgrowth](https://clawhub.ai/user/trustgrowth)

### License/Terms of Use:

MIT-0

## Use Case:

SEO teams, site owners, and developers use this skill to turn keyword position evidence into a periodic report that highlights movement, quick wins, striking-distance queries, and the next actions justified by the data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports that the skill directs agents to run an unbundled validator from a dynamically located skills root without integrity checks.

Mitigation: Use the skill only where the Groundcrew validator path is trusted and controlled, or require the validator to be bundled or pinned before allowing that command to run.

## Reference(s):

- [Connectors and categories](references/connectors.md)
- [Reporting contract](references/reporting.md)
- [ClawHub skill page](https://clawhub.ai/trustgrowth/skills/keyword-report)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, files, guidance]

**Output Format:** [Markdown report with evidence labels; CSV detail file when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports use SHIP, FIX, BLOCK, or UNDECIDED verdicts and label measured, user-provided, and estimated values.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
