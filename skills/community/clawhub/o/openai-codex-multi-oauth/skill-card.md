## Description: <br>
Helps agents and operators manage, inspect, and debug multiple OpenAI Codex OAuth profiles in OpenClaw, including profile switching, session overrides, usage mismatches, auth order, active-slot routing, and broken-token recovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[WTHH031230](https://clawhub.ai/user/WTHH031230) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and support engineers use this skill to diagnose and repair OpenClaw deployments that maintain more than one OpenAI Codex OAuth profile. It helps compare stored preference, auth order, session override, effective runtime profile, usage source, and display metadata before applying narrow fixes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose local account, session, workspace, usage, and profile details while diagnosing OpenClaw Codex OAuth state. <br>
Mitigation: Run it only when local profile diagnostics are intended, prefer scoped --profile or test --state-dir runs, and redact emails, account IDs, workspace IDs, session targets, and usage output before sharing logs or screenshots. <br>
Risk: The usage-report script can use stored OAuth tokens to query live Codex usage data, and --raw can include sensitive API response fields. <br>
Mitigation: Avoid --raw unless necessary, limit requests to the specific profiles being debugged, and review output for sensitive identifiers before retaining or transmitting it. <br>
Risk: Troubleshooting may lead to local auth-store or session-state edits that affect active profile selection. <br>
Mitigation: Back up relevant OpenClaw auth/session files first, change only the inconsistent layer, and re-test profile selection, /status, and usage behavior after each change. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/WTHH031230/openai-codex-multi-oauth) <br>
- [Runtime files and inspection points](references/runtime-files.md) <br>
- [Profile-specific usage debugging](references/usage-debugging.md) <br>
- [Workflows](references/workflows.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, code references, and optional JSON output from bundled diagnostic scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Bundled scripts inspect local OpenClaw state and can optionally fetch live usage with stored OAuth credentials.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
