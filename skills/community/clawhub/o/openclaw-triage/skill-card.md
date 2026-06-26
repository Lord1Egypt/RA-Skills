## Description: <br>
OpenClaw Triage investigates agent workspaces, builds event timelines, assesses incident scope, and collects forensic evidence from local OpenClaw security data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AtlasPA](https://clawhub.ai/user/AtlasPA) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, security engineers, and agent workspace operators use this skill to investigate suspicious workspace changes, correlate local security-tool findings, preserve evidence, and guide incident response. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Response commands can modify or remove workspace items during containment, remediation, or protection workflows. <br>
Mitigation: Run investigation, timeline, scope, and evidence commands first, and back up the workspace before using contain, remediate, or protect. <br>
Risk: Remediation can invoke helper tools found inside the workspace being investigated. <br>
Mitigation: Verify workspace-local helper tools before allowing remediation to run them. <br>


## Reference(s): <br>
- [OpenClaw Triage on ClawHub](https://clawhub.ai/AtlasPA/openclaw-triage) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text reports, JSON exports, Markdown documentation, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally with Python 3 and writes investigation state and evidence artifacts into the target workspace when evidence or response commands are used.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
