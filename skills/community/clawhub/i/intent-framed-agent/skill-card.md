## Description: <br>
Frames coding-agent implementation sessions with explicit intent capture, drift checks, and resolution records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Xiao1804](https://clawhub.ai/user/Xiao1804) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and coding agents use this skill when moving from planning into non-trivial code changes to establish an execution contract, monitor scope drift, and record the outcome. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact includes npx installation commands from an external source. <br>
Mitigation: Verify the package or repository source before running installation commands. <br>
Risk: Intent records may include sensitive project details and can be captured in session transcripts when Entire CLI is configured. <br>
Mitigation: Avoid placing secrets or confidential data in intent frames, and review transcript retention before enabling capture. <br>
Risk: The skill may check local Entire CLI status when tool access is available. <br>
Mitigation: Allow only the documented status check and continue without CLI integration if the tool is unavailable or unexpected. <br>


## Reference(s): <br>
- [Intent Framed Agent on ClawHub](https://clawhub.ai/Xiao1804/intent-framed-agent) <br>
- [Entire CLI](https://github.com/entireio/cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with structured intent, drift-check, and resolution blocks plus optional shell command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Preserves fixed block headers and fields for parseability.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
