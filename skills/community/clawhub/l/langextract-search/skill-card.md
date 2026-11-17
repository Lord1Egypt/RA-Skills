## Description:

Integrates Zhipu AI search, DuckDuckGo search, and multi-model structured extraction into a complete search-to-report workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luw2007](https://clawhub.ai/user/luw2007)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and agents use this skill to run configurable web searches across Zhipu AI Search and DuckDuckGo, then extract structured summaries, key points, facts, and source references from the combined results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and retrieved content may be sent to configured search and model providers.

Mitigation: Avoid confidential queries and review provider configuration before running the workflow.

Risk: Generated reports may contain incomplete, stale, or provider-biased search and extraction results.

Mitigation: Review generated Markdown and JSON outputs before relying on them for decisions.

Risk: API keys can be exposed if literal credentials are stored in configuration.

Mitigation: Keep API keys in environment variables instead of committing literal values to conf.json.

Risk: Unpinned Python dependencies can introduce supply-chain or compatibility risk.

Mitigation: Use pinned dependencies or a reviewed requirements file before deployment.

## Reference(s):

- [Search parameter configuration](references/search-params.md)
- [Workflow details](references/workflow-details.md)
- [Google LangExtract](https://github.com/google/langextract)
- [Langextract Search on ClawHub](https://clawhub.ai/luw2007/skills/langextract-search)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration]

**Output Format:** [Markdown reports and optional JSON result files generated from search and extraction results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include Zhipu search results, DuckDuckGo search results, extracted structured information, workflow summaries, and full JSON results when requested.]

## Skill Version(s):

0.1.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
