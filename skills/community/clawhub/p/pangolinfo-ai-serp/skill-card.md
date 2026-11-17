## Description:

Helps an agent query Google SERP and AI Overview results, run conversational AI Mode searches, collect cited sources, and compare Google Trends keyword interest.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pangolinfo](https://clawhub.ai/user/pangolinfo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to ground answers with Google search results, AI Overview citations, conversational follow-up searches, and relative keyword trend signals. It is suited for SERP monitoring, off-site demand research, reputation research, preliminary text trademark screening, and trend comparison.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pangolinfo API keys can be exposed if placed in URLs, command lines, logs, traces, or screenshots.

Mitigation: Use a narrowly scoped key, prefer Authorization headers or a protected MCP secret store, avoid URL or command-line key placement, and rotate any key that may have been exposed.

Risk: AI Overview content may be unavailable for some queries, and Google Trends values are relative rather than absolute volume.

Mitigation: Fall back to organic results when AI Overview is absent, preserve cited sources when available, and label trend values as relative 0-100 interest rather than search volume.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pangolinfo/skills/pangolinfo-ai-serp)
- [Pangolinfo website](https://www.pangolinfo.com)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration, guidance]

**Output Format:** [Markdown summaries with cited links, SERP tables, trend summaries, and MCP tool-call arguments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Google AI Overview citations, organic result fields, related searches, screenshots when requested, and relative 0-100 keyword trend values.]

## Skill Version(s):

4.0.0 (source: server release metadata; artifact frontmatter says 3.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
