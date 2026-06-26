## Description: <br>
Automatically compresses OpenClaw tool outputs to reduce token usage by 60-99%. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jackkeller](https://clawhub.ai/user/jackkeller) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to automatically compress OpenClaw file-read and shell-output responses, lowering token usage while preserving enough context for agent work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can transparently process file contents and shell command output. <br>
Mitigation: Review the skill before installing, configure exclusions for sensitive paths and commands, and avoid use around secrets, credentials, private logs, or sensitive commands. <br>
Risk: Scope, retention, and install-time network behavior are not fully documented in the server security summary. <br>
Mitigation: Confirm opt-in controls, exclusions, caching behavior, retention behavior, and install-time dependency activity before deploying in sensitive environments. <br>


## Reference(s): <br>
- [Leanctx Integration on ClawHub](https://clawhub.ai/jackkeller/leanctx-integration) <br>
- [Publisher profile: jackkeller](https://clawhub.ai/user/jackkeller) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Compressed text or markdown-like tool output, with configuration and shell-command guidance in documentation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Compression is applied locally to eligible file reads and shell command outputs, with in-memory caching when enabled.] <br>

## Skill Version(s): <br>
0.1.4 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
