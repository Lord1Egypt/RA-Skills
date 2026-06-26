## Description: <br>
Guides agents through safe edits to OpenClaw configuration by backing up openclaw.json, verifying keys against source, validating before restart, and recovering from gateway failures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codeinonenight](https://clawhub.ai/user/codeinonenight) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill when changing OpenClaw gateway settings, validating configuration keys, or recovering from a failed restart caused by invalid openclaw.json values. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unreviewed changes to OpenClaw session visibility, agent-to-agent messaging, or tool allow/deny settings can alter gateway behavior. <br>
Mitigation: Review proposed configuration changes before writing them and confirm the key names against installed OpenClaw source. <br>
Risk: Invalid or unknown openclaw.json keys can prevent the OpenClaw gateway from starting. <br>
Mitigation: Create a timestamped backup, validate with OpenClaw status checks before restart, and restore the latest known-good backup if validation reports errors. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operational checklists and command examples; it does not directly execute configuration changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
