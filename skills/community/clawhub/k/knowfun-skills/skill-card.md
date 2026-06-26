## Description: <br>
Generates educational content with the Knowfun.io API, including courses, posters, games, and films. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[duguyixiaono1](https://clawhub.ai/user/duguyixiaono1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, educators, trainers, and content creators use this skill to create and manage Knowfun.io content-generation tasks from text or URLs. It helps agents check task status, retrieve results, inspect schemas, list tasks, and report credit usage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Knowfun.io API key and sends prompts, URLs, and task data to the external Knowfun.io service. <br>
Mitigation: Use a temporary environment variable or protected secret manager, review data before submission, and install only when this external data sharing is acceptable. <br>
Risk: Creating tasks through remote chat or natural-language prompts may consume Knowfun.io credits. <br>
Mitigation: Use approval gates before task creation and check credit balance with the skill before running high-volume or ambiguous requests. <br>
Risk: Setup guidance may encourage storing API keys in shell startup files or using manual installs that are harder to audit. <br>
Mitigation: Prefer scoped session secrets or a managed secret store, and review the downloaded files before sudo, symlink, or manual installation steps. <br>


## Reference(s): <br>
- [Knowfun ClawHub Skill Page](https://clawhub.ai/duguyixiaono1/knowfun-skills) <br>
- [Knowfun API Platform](https://www.knowfun.io/api-platform) <br>
- [API Reference](api-reference.md) <br>
- [Usage Examples](examples.md) <br>
- [Skill Instructions](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown summaries with inline shell commands and JSON API response fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include task IDs, status values, credit balance details, schema fields, and generated-content URLs returned by Knowfun.io.] <br>

## Skill Version(s): <br>
1.0.15 (source: server release metadata, package.json, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
