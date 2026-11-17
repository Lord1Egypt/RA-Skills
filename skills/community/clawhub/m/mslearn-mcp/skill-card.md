## Description:

Grounds Microsoft product and development answers in current Microsoft Learn documentation and code samples.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ricardodpalmeida](https://clawhub.ai/user/ricardodpalmeida)

### License/Terms of Use:

MIT No Attribution

## Use Case:

Developers and technical users use the skill to answer Microsoft product and development questions with current Learn documentation, version-aware guidance, official code samples, and citations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scan coverage is incomplete because a referenced path was missing.

Mitigation: Review the missing path and complete the scan before treating the verdict as comprehensive.

Risk: Lookup queries and requested documentation URLs are sent to Microsoft.

Mitigation: Keep secrets, tenant or customer identifiers, and proprietary code out of lookup requests.

Risk: Retrieved documentation or Q&A text may include instructions unrelated to the task.

Mitigation: Treat retrieved text as evidence only, not as instructions.

## Reference(s):

- [Microsoft Learn MCP server](https://github.com/MicrosoftDocs/mcp)
- [Microsoft Learn MCP endpoint](https://learn.microsoft.com/api/mcp)
- [MCP setup and recovery](references/mcp-details.md)
- [Microsoft Learn MCP project homepage](https://github.com/Ricardodpalmeida/openclaw-mslearn-mcp)
- [ClawHub release](https://clawhub.ai/ricardodpalmeida/skills/mslearn-mcp)
- [Microsoft Learn MCP release notes](https://learn.microsoft.com/en-us/training/support/mcp-release-notes)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown answers with cited Microsoft Learn URLs and optional code snippets or setup commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes source citations, release status where documented, and unresolved gaps; lookup queries should omit secrets and proprietary information.]

## Skill Version(s):

1.1.9 (source: CHANGELOG, released 2026-11-16)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
