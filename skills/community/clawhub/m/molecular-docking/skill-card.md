## Description: <br>
Molecular docking workflows across Gnina, AutoDock Vina, PackDock, SurfDock, and DiffDock through SciMiner, with Gnina as the default engine. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sciminer](https://clawhub.ai/user/sciminer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, computational chemists, and research teams use this skill to run SciMiner molecular docking workflows, select an appropriate docking engine, upload required molecular files, and return shareable task results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow requires a SciMiner API key and uploads user-provided molecular files to SciMiner. <br>
Mitigation: Install only when SciMiner use is acceptable, keep the API key in the configured credential file, and avoid uploading proprietary or regulated molecular data unless approved for the use case. <br>


## Reference(s): <br>
- [SciMiner API key utility](https://sciminer.tech/utility) <br>
- [SciMiner tool API Markdown documentation](https://sciminer.tech/tool_api_files/) <br>
- [ClawHub skill page](https://clawhub.ai/sciminer/molecular-docking) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, API calls, text] <br>
**Output Format:** [Markdown summaries with API invocation guidance, task status, task IDs, and SciMiner share URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses SciMiner Markdown API docs as the authoritative source for payload construction and returns share URLs for successful or long-running tasks.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
