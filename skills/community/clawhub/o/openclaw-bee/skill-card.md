## Description: <br>
BEE helps OpenClaw agents install and configure persistent, structured belief memory across sessions, including extraction, recall, namespace scoping, and troubleshooting guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vashkartik](https://clawhub.ai/user/vashkartik) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to install and configure BEE for persistent agent memory, scoped belief recall, and troubleshooting memory setup. It is intended for OpenClaw environments that need session-derived context to persist across restarts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: BEE stores session-derived beliefs persistently and may reuse them in later sessions. <br>
Mitigation: Avoid storing secrets or regulated data unless the package and database retention behavior have been reviewed; inspect, disable extraction, or delete the SQLite database when needed. <br>
Risk: Belief extraction may send session-derived content to the configured extraction model. <br>
Mitigation: Review the configured extraction model and data handling requirements before enabling extraction in sensitive environments. <br>
Risk: The skill installs a third-party npm or GitHub package. <br>
Mitigation: Install only after reviewing and trusting the @skysphere-labs/openclaw-bee package source and release. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vashkartik/openclaw-bee) <br>
- [BEE npm package](https://www.npmjs.com/package/@skysphere-labs/openclaw-bee) <br>
- [BEE project homepage declared by artifact](https://github.com/skysphere-labs/openclaw-bee) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes installation steps, OpenClaw configuration settings, and verification commands.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
