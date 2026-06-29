## Description: <br>
Control this macOS desktop via screenshots, AppleScript, mouse/keyboard automation, OCR/template matching, and verify loops. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[igallta](https://clawhub.ai/user/igallta) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill when an agent must work with real macOS desktop surfaces, native dialogs, canvas apps, Electron apps, or visual workflows. It helps the agent capture the screen, choose a low-fragility control method, act once, and verify the result. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose visible desktop content through screenshots and clipboard-assisted text entry. <br>
Mitigation: Close or hide sensitive windows before use and review screenshot output paths. <br>
Risk: Mouse and keyboard automation can trigger externally visible or irreversible actions. <br>
Mitigation: Require explicit confirmation before submitting forms, sending messages, deleting data, making payments, posting publicly, or changing accounts. <br>
Risk: Screen Recording and Accessibility permissions broaden what the runtime process can observe or control. <br>
Mitigation: Grant these permissions only when needed and avoid granting them broadly. <br>


## Reference(s): <br>
- [Source Notes](references/source-notes.md) <br>
- [ClawHub skill page](https://clawhub.ai/igallta/mac-gui-control) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON helper output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled helper emits JSON for screen capture, app activation, keyboard, mouse, and template-matching operations.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
