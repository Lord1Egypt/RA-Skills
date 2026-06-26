## Description: <br>
Execute RunningHub ComfyUI workflows via API to submit tasks, query status, and retrieve results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[uiueux](https://clawhub.ai/user/uiueux) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation users use this skill to submit, monitor, and retrieve results from RunningHub-hosted ComfyUI workflows, including workflows that accept uploaded images as inputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected images, workflow inputs, and generated outputs are sent to RunningHub for processing. <br>
Mitigation: Use the skill only with images and workflow data that may be shared with RunningHub, and review the service's data handling expectations before use. <br>
Risk: The skill can save a RunningHub API key in a local config file. <br>
Mitigation: Prefer environment variables or protect the local config file, avoid committing it, and rotate the API key if exposure is suspected. <br>
Risk: The included Chrome DevTools automation script can control a browser session when remote debugging is enabled. <br>
Mitigation: Prefer the documented API client path; run Chrome automation only with an intentionally started disposable browser profile. <br>


## Reference(s): <br>
- [ClawHub Photo Retouching release](https://clawhub.ai/uiueux/photo-retouching) <br>
- [RunningHub platform](https://www.runninghub.ai/) <br>
- [RunningHub workflow URL pattern](https://www.runninghub.ai/#/workflow/WORKFLOW_ID) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command examples, Python API snippets, JSON configuration, and task/result status text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces RunningHub task identifiers, status responses, and output URLs when workflows complete.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
