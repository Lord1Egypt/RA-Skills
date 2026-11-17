## Description:

Finds Amazon ABA search terms from natural-language time and ranking criteria, translates results into Chinese, and exports keyword data as JSON and six-column CSV files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External e-commerce operators and agents use this skill to discover seasonal, trending, ranking-jump, and long-tail Amazon ABA keywords across supported marketplaces. It helps users review translated keyword, search-frequency-rank, marker, and notes columns in CSV/JSON outputs for manual screening and follow-up analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Keyword queries, prompts, account metadata, uploaded files, and feedback may be sent to external LinkFox services.

Mitigation: Install only when LinkFox is trusted for those data types, avoid sensitive prompts, and review feedback or uploads before sending.

Risk: Credential-bearing network configuration can direct authenticated requests to the configured tool gateway.

Mitigation: Keep LINKFOX_TOOL_GATEWAY and related API URL variables unset unless they point to trusted LinkFox HTTPS hosts, and use a scoped API key.

Risk: Runtime dependencies and helper skills affect network behavior and generated outputs.

Mitigation: Install runtime dependencies from a trusted pinned environment and review generated CSV/JSON results before acting on them.

## Reference(s):

- [ABA New Keyword Mining Expert API](skills/linkfox-aba-new-keyword-miner/references/api.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files]

**Output Format:** [Markdown guidance with JSON API parameters, stdout summaries, saved JSON responses, and UTF-8 BOM CSV exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CSV exports contain sequence number, search term, Chinese translation, search frequency rank, marker, and notes columns; full JSON responses are saved alongside CSV files.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
