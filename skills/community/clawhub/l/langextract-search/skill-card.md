## Description: <br>
Integrates Zhipu Search, DuckDuckGo Search, and multi-model structured extraction into a complete search-to-summary workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luw2007](https://clawhub.ai/user/luw2007) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
Developers and researchers use this skill to run web searches across configured providers, combine the retrieved snippets, and extract concise structured findings with a configured OpenAI-compatible model. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and retrieved page snippets are sent to the configured search and model providers. <br>
Mitigation: Install only when this data sharing is acceptable, keep API keys in environment variables where possible, and use trusted model base URLs and proxies. <br>
Risk: Local output files may contain sensitive search queries, snippets, or extracted findings. <br>
Mitigation: Delete generated output files after sensitive searches and avoid running sensitive queries in shared workspaces. <br>
Risk: Unpinned dependencies or untrusted network configuration can change the behavior of provider calls. <br>
Mitigation: Use a virtual environment with pinned dependencies and review configured provider endpoints and proxy settings before use. <br>


## Reference(s): <br>
- [Langextract Search ClawHub Listing](https://clawhub.ai/luw2007/langextract-search) <br>
- [Search Parameter Configuration](references/search-params.md) <br>
- [Workflow Details](references/workflow-details.md) <br>
- [Google LangExtract](https://github.com/google/langextract) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown result files, optional JSON result files, and terminal status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes timestamped search results, extracted information, and workflow summaries under the configured output directory.] <br>

## Skill Version(s): <br>
0.1.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
