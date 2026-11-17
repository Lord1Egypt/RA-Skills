## Description:

Lessie helps agents search, qualify, and enrich people and companies for recruiting, sales prospecting, business research, and web research workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jkgeekjack](https://clawhub.ai/user/jkgeekjack)

### License/Terms of Use:

MIT-0

## Use Case:

External users, recruiters, sales teams, and business researchers use this skill to find professionals, enrich known contacts, research companies, qualify ambiguous candidates, and summarize web pages through Lessie CLI or MCP tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install or run npm packages for the Lessie CLI or MCP server, including unpinned package invocations.

Mitigation: Review installation commands before execution, prefer manual installation with pinned package versions, and avoid automatic global installs or unpinned npx -y.

Risk: The skill uses a remote people and company enrichment service that may process searches, spend credits, and return personal contact data.

Mitigation: Use it only with a lawful basis, confirm the user intends to use Lessie, monitor credit usage, and follow applicable privacy and outreach laws.

Risk: Searches can return stale, ambiguous, or incorrect people and company matches.

Mitigation: Resolve company domains, ask the user to confirm ambiguous entities, and verify enriched results against the user's criteria before acting on them.

Risk: User-provided or web-derived text could be unsafe if interpolated directly into shell commands.

Mitigation: Pass arguments as structured JSON where possible, quote shell values carefully, and avoid executing raw user or web text.

## Reference(s):

- [Lessie website](https://lessie.ai)
- [Lessie skill page](https://clawhub.ai/jkgeekjack/skills/lessie)
- [CLI Reference](references/cli-reference.md)
- [Workflow Patterns](references/workflow-patterns.md)
- [Domain Resolution](references/domain-resolution.md)
- [Lessie pricing](https://lessie.ai/pricing)
- [Lessie privacy policy](https://lessie.ai/privacy)
- [Lessie terms of service](https://lessie.ai/terms-of-service)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, JSON CLI output, and MCP tool-call guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return personal contact details, company profiles, job postings, news summaries, and web research results from a remote credit-based service.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter reports 2.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
