## Description:

Enriches a company or person lead from public-web signals before outreach, producing an ICP-fit verdict, key facts, red flags, and optional structured output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jernejcicorbin-hub](https://clawhub.ai/user/jernejcicorbin-hub)

### License/Terms of Use:

MIT-0

## Use Case:

Sales, growth, and lead-qualification users use this skill to verify a known company, domain, or person lead before outreach. It resolves identity, checks ICP fit and activity, surfaces disqualifiers, and keeps weak evidence marked as ambiguous.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Lead enrichment queries are sent to Prismfy.

Mitigation: Use the skill only for leads whose query details are appropriate to send to Prismfy.

Risk: PRISMFY_API_KEY can be exposed if stored persistently in shell startup files.

Mitigation: Set the key only for the session or manage it through a dedicated secret manager.

Risk: Custom Prismfy endpoint environment variables can redirect requests.

Mitigation: Use custom endpoints only when the exact HTTPS host is trusted.

Risk: Exported JSON reports may contain lead research details.

Mitigation: Keep reports out of shared folders and source control.

## Reference(s):

- [Prismfy](https://prismfy.io)
- [ClawHub skill page](https://clawhub.ai/jernejcicorbin-hub/skills/lead-enrichment-skill)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Concise chat text or Markdown-style bullets, with optional structured JSON report files when export mode is requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PRISMFY_API_KEY, curl, and jq; uses Prismfy public-web search and can write an output file through --out.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
