## Description: <br>
Automatically fixes broken OpenCLI adapters when commands fail by guiding an agent through diagnostics, targeted adapter patching, retries, and an optional upstream GitHub issue after a verified fix. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liberalchang](https://clawhub.ai/user/liberalchang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill when an OpenCLI site adapter fails because a website DOM, API, or response schema changed. It helps collect diagnostic context, make a bounded adapter-source patch, retry the command, and prepare an upstream issue after a verified local fix. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can edit the specific OpenCLI adapter file reported by diagnostics. <br>
Mitigation: Review the file diff before keeping the repair, and keep changes limited to the adapter source path named in the diagnostic context. <br>
Risk: Diagnostic output can contain private page, browser, or network data. <br>
Mitigation: Review diagnostic content before sharing it or using it in an upstream issue. <br>
Risk: The skill can prepare and optionally publish a GitHub issue after a verified fix. <br>
Mitigation: Confirm the issue draft with the user before running any issue creation command. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liberalchang/opencli-autofix) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown with inline shell and code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include bounded file edits to the OpenCLI adapter source path and an issue draft for user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
