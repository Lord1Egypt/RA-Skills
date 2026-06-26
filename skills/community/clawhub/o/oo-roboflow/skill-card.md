## Description: <br>
Roboflow (roboflow.com). Use this skill for Roboflow project discovery, version inspection, hosted object detection, workflow validation, workflow execution, and inference server diagnostics through an OOMOL-connected account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect Roboflow projects and versions, run object detection, validate or run Roboflow workflows, and check inference server diagnostics from an agent session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Workflow runs, saved workflow runs, and object detection can process sensitive inputs or consume Roboflow and OOMOL-connected account resources. <br>
Mitigation: Require explicit user intent before running execution actions and confirm payloads that include sensitive image data, workflow inputs, workspace identifiers, or project versions. <br>
Risk: The source skill describes untagged actions as reads even though inference and workflow execution perform processing through a connected account. <br>
Mitigation: Treat detect_objects, run_workflow, and run_saved_workflow as execution actions rather than passive reads. <br>
Risk: The skill requires sensitive credentials through an OOMOL-connected Roboflow account. <br>
Mitigation: Use the server-managed credential flow, avoid exposing raw tokens, and only perform setup or reconnection when an authentication or connection error requires it. <br>


## Reference(s): <br>
- [Roboflow homepage](https://roboflow.com/) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [ClawHub Roboflow skill page](https://clawhub.ai/oomol/oo-roboflow) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payloads or responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return Roboflow connector data, action schemas, execution IDs, detection results, workflow outputs, metrics, or setup guidance depending on the requested action.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
