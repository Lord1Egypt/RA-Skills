## Description: <br>
Optimizes the OpenClaw 4.2 /compact prompt to produce structured summaries when users report poor compression quality, incomplete summaries, lost context, weak /compact formatting, or ask to improve the compact prompt. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nicshliu](https://clawhub.ai/user/nicshliu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to improve /compact behavior with a structured nine-section summary format that preserves intent, files, errors, pending tasks, and current work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The compact prompt asks for broad conversation summaries that may preserve full user messages, file paths, code, private URLs, personal data, credentials, or proprietary details. <br>
Mitigation: Add explicit redaction rules before use and omit or mask secrets, tokens, credentials, personal data, private URLs, and proprietary code unless they are necessary. <br>
Risk: Installing the prompt as a global systemPrompt or hook can affect all future OpenClaw compact behavior. <br>
Mitigation: Prefer the manual per-/compact prompt first, then review and test any global configuration change before keeping it enabled. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nicshliu/openclaw-compact-improver) <br>
- [/Compact optimization prompt template](references/compact-prompt.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with compact-summary templates, inline shell commands, and configuration instructions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prompt-only skill; may suggest manual /compact instructions or updates to OpenClaw system prompt or hook configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
