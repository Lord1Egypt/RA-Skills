## Description: <br>
New users get 20 free calls to get started. Make real outbound phone calls, run planned calls, and check call status in OpenClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[call-e-dev](https://clawhub.ai/user/call-e-dev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users use this skill to verify CALL-E setup, authenticate the CALL-E CLI, plan outbound phone calls, place requested calls, and check call status, summaries, details, and transcripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: This skill can place real outbound phone calls and expose call details or transcripts in chat. <br>
Mitigation: Use it only when you trust CALL-E and the CLI, clearly intend to place a call, and have checked the number and call purpose before execution. <br>
Risk: Repository-local CLI code could be used if present in the workspace. <br>
Mitigation: Prefer an installed or pinned official CALL-E CLI unless you trust the local workspace code. <br>


## Reference(s): <br>
- [CALL-E OpenClaw CLI skill homepage](https://github.com/CALLE-AI/call-e-integrations/tree/main/packages/openclaw-cli-skill) <br>
- [CALL-E CLI commands](references/commands.md) <br>
- [CALL-E Discord community](https://discord.gg/6AbXUzUV8w) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown responses with inline shell command guidance and structured call-status sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May display call status, call details, summaries, and transcripts returned by the CALL-E CLI.] <br>

## Skill Version(s): <br>
1.1.4 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
