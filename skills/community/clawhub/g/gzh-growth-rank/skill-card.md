## Description: <br>
Fetches RedFoxHub WeChat public-account reading growth rankings for a requested recent date and presents the results as a Markdown table with optional trend analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[if530770](https://clawhub.ai/user/if530770) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External WeChat account operators, content editors, and analysts use this skill to discover fast-growing public accounts, inspect linked representative articles, and summarize topic or content-type patterns from retrieved ranking data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a RedFoxHub API key and can read REDFOX_API_KEY from the environment or shell profile files. <br>
Mitigation: Set REDFOX_API_KEY as an environment variable, avoid exposing it in code, prompts, logs, or output files, and rotate or revoke the key when it is no longer needed. <br>
Risk: Ranking data is retrieved from an external service and may be unavailable, empty, or outside the supported date window. <br>
Mitigation: Use only the script's returned data, preserve the output without fabricating rankings, and clearly report API failures or unsupported dates. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/if530770/gzh-growth-rank) <br>
- [Core workflow](references/core_workflow.md) <br>
- [API specification](references/api-spec.md) <br>
- [RedFoxHub API keys](https://redfox.hk/settings/api-keys?source=clawhub) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown tables and concise narrative guidance, with shell command snippets when setup or direct script execution is needed.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires REDFOX_API_KEY; ranking queries are limited to recent dates supported by the RedFoxHub API.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
