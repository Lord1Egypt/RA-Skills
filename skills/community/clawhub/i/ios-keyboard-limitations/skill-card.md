## Description: <br>
iOS keyboard extension technical limitations and workarounds. Use when planning or building iOS custom keyboards with voice/audio features, dictation, or system integration needs. Covers memory limits, sandbox restrictions, microphone access, app launching, and viable alternative architectures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[usimic](https://clawhub.ai/user/usimic) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and iOS app teams use this skill to evaluate whether a custom keyboard is viable for voice, dictation, or system-integration workflows. It helps compare keyboard extensions with share extensions, standalone app flows, and Siri Shortcuts before implementation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated app code or architecture plans based on this skill may affect microphone access, clipboard use, networking, App Groups, or user-consent flows. <br>
Mitigation: Review generated iOS code and configuration separately for those behaviors before implementation or release. <br>
Risk: Keyboard-extension workarounds can create unreliable or high-friction user flows involving manual app switching and clipboard handoff. <br>
Mitigation: Prototype the full user flow and prefer Apple-supported share extension, standalone app, or Siri Shortcuts architectures when voice or audio capture is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/usimic/ios-keyboard-limitations) <br>
- [Apple custom keyboard documentation](https://developer.apple.com/documentation/uikit/keyboards_and_input/creating_a_custom_keyboard) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown guidance with decision tables, architecture recommendations, and Swift snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; generated iOS app code should be reviewed separately for microphone, clipboard, networking, App Groups, and user-consent behavior.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
