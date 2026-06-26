## Description: <br>
Diagnose index1 environment - check Python, Ollama, models, index health. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gladego](https://clawhub.ai/user/gladego) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect a local index1 setup, check index health, review Ollama model availability, and get fix recommendations before or after troubleshooting search behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Diagnostic output may include local index, database, model, or environment details that should not be shared broadly. <br>
Mitigation: Review diagnostic output before sharing it outside the local troubleshooting context. <br>
Risk: Installer, model-pull, and indexing commands can change the local environment or add selected local directories to an index. <br>
Mitigation: Treat remediation commands as manual actions and run them only after confirming the source, target directories, and expected local changes. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration guidance] <br>
**Output Format:** [Markdown with inline shell commands and diagnostic guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local environment health summaries, installed model listings, index status details, and recommended manual remediation commands.] <br>

## Skill Version(s): <br>
2.0.3 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
