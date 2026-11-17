## Description:

Turns narrated job walkthrough recordings into editable numbered SOP documents using Plaud transcripts, Google Docs, and Google Sheets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

Operations, maintenance, facilities, field service, manufacturing, lab, franchise, and owner-led teams use this skill to turn approved narrated Plaud recordings into numbered SOPs, editable Google Docs, and run logs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable unpinned install commands can change between runs.

Mitigation: Prefer the listed OpenClaw install path or a pinned, verified installer before operational use.

Risk: Plaud transcripts may contain confidential operations, safety procedures, customer data, or regulated information that is copied into Google Docs and Sheets.

Mitigation: Use only recordings approved for export and review or redact transcripts before creating documents or logs.

Risk: Ambiguous narration can leave SOP steps incomplete or misleading.

Mitigation: Review the generated document's ambiguity section before using it as an operating procedure.

## Reference(s):

- [AgentPMT workflow page](https://www.agentpmt.com/agent-workflow-skills/narrated-walkthrough-to-a-numbered-sop-document)
- [ClawHub skill page](https://clawhub.ai/agentpmt/skills/narrated-walkthrough-to-a-numbered-sop-document)
- [AgentPMT account setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup)
- [Plaud tool skill](https://clawhub.ai/agentpmt/plaud)
- [Google Docs Connector tool skill](https://clawhub.ai/agentpmt/google-docs-connector)
- [Google Sheets tool skill](https://clawhub.ai/agentpmt/google-sheets)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Markdown-like SOP content written to Google Docs with structured run-log rows in Google Sheets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Flags ambiguous narration for human review and skips recordings that are not judged to be procedures.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
