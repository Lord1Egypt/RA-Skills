## Description: <br>
Ground truth layer for AI agents — provide verified facts in every prompt and expose read/search tools for edict management, with write tools opt-in. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mssteuer](https://clawhub.ai/user/mssteuer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this OpenClaw plugin to inject curated, verified facts into agent context and optionally expose tools for listing, searching, adding, updating, or removing those facts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent facts can shape future agent prompts if runtime writes are enabled. <br>
Mitigation: Keep edicts curated and trusted; disable write tools or restrict tool names to read-only operations unless persistent mutation is intentional. <br>
Risk: Incorrect or stale edicts can cause agents to follow outdated facts or constraints. <br>
Mitigation: Review edicts regularly and use stale or expiry metadata to clean up facts that should no longer influence prompts. <br>
Risk: A package/version mismatch can install behavior different from the reviewed release. <br>
Mitigation: Verify the package name and version before installation. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/mssteuer/openclaw-plugin-edicts) <br>
- [Edicts documentation](https://edicts.ai) <br>
- [OpenClaw plugin package](https://www.npmjs.com/package/openclaw-plugin-edicts) <br>
- [Core library package](https://www.npmjs.com/package/edicts) <br>
- [API reference](https://edicts.ai/docs/reference/api/) <br>
- [OpenClaw integration guide](https://edicts.ai/docs/integrations/openclaw/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON/YAML configuration examples, shell commands, and prompt-context text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May inject locally stored facts into agent prompts; runtime write tools are opt-in and configurable.] <br>

## Skill Version(s): <br>
1.0.6 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
