## Description: <br>
Unified Kaggle skill for account setup, competition reports, dataset and model downloads, notebook execution, competition submissions, badge collection, and general Kaggle questions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shepsci](https://clawhub.ai/user/shepsci) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to automate Kaggle account setup, competition exploration, dataset and model workflows, notebook execution, competition submissions, and badge collection through guided commands and reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use live Kaggle credentials to create, upload, submit, edit, or delete account resources. <br>
Mitigation: Use dry-run or status modes first and require explicit confirmation before uploads, notebook pushes, competition submissions, profile edits, deletes, or scheduled streak actions. <br>
Risk: Kaggle API tokens or keys could be exposed if pasted into chat, echoed, logged, or committed. <br>
Mitigation: Place credentials locally, keep file permissions strict, avoid logging secret values, and rotate credentials if exposure occurs. <br>
Risk: Badge automation and streak workflows can affect account state or run against the wrong account. <br>
Mitigation: Avoid important accounts for badge phases, verify the active Kaggle identity before execution, and keep scheduling manual unless the user explicitly opts in. <br>


## Reference(s): <br>
- [Kaggle Skill Page](https://clawhub.ai/shepsci/kaggle) <br>
- [Registration Setup Guide](modules/registration/references/kaggle-setup.md) <br>
- [Competition Categories](modules/comp-report/references/competition-categories.md) <br>
- [Kaggle Platform Knowledge](modules/kllm/references/kaggle-knowledge.md) <br>
- [KaggleHub API Reference](modules/kllm/references/kagglehub-reference.md) <br>
- [Kaggle CLI Reference](modules/kllm/references/cli-reference.md) <br>
- [Kaggle MCP Reference](modules/kllm/references/mcp-reference.md) <br>
- [Badge Catalog](modules/badge-collector/references/badge-catalog.md) <br>
- [Kaggle MCP](https://www.kaggle.com/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, JSON snippets, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate local Kaggle workflow files and reports when the user explicitly runs supported scripts.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
