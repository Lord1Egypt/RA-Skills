## Description: <br>
Provides step-by-step diagnostics and command-line fixes for common OpenClaw issues including memory plugin faults, Feishu disconnects, LLM timeouts, and Telegram errors. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Wayne19820905](https://clawhub.ai/user/Wayne19820905) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to diagnose and repair OpenClaw runtime, plugin, gateway, and channel configuration issues. It is especially useful when recovering memory behavior, Feishu connectivity, Telegram configuration, or LLM timeout handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Repair commands may modify OpenClaw configuration, plugin allow lists, or local gateway service state. <br>
Mitigation: Review each command before execution, back up openclaw.json before configuration changes, and run openclaw doctor after changes. <br>
Risk: Troubleshooting guidance includes high-impact local workflows such as restarting services and changing channel settings. <br>
Mitigation: Use the commands only in the intended ClawHub or Convex development context and confirm the target OpenClaw environment before applying fixes. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes local diagnostic and repair commands that should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
