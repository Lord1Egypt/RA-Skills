## Description:

Provides iOS keyboard extension technical limitations and workarounds for planning or building custom keyboards with voice/audio features, dictation, or system integration needs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[usimic](https://clawhub.ai/user/usimic)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to assess whether an iOS custom keyboard is viable for voice, dictation, networking, storage, or app-integration features and to compare supported alternatives such as share extensions, full app flows, and Siri Shortcuts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Keyboard Full Access is sensitive for users and may create privacy concerns when networking or shared data access is required.

Mitigation: Explain why Full Access is needed in the companion app and avoid requiring it unless the keyboard feature cannot work without network access.

Risk: Voice and audio features inside a keyboard extension can lead to non-working flows because the extension cannot access the microphone and has strict sandbox limits.

Mitigation: Use the skill's recommended supported alternatives, such as a share extension, full app mode, or Siri Shortcuts, before committing to a keyboard-based voice workflow.

Risk: Manual app-switching and clipboard-based workarounds can interrupt the user flow or expose text to clipboard overwrite behavior.

Mitigation: Reserve these patterns for fallback flows and document the expected user steps and clipboard behavior clearly.

## Reference(s):

- [Apple: Creating a Custom Keyboard](https://developer.apple.com/documentation/uikit/keyboards_and_input/creating_a_custom_keyboard)

## Skill Output:

**Output Type(s):** [guidance, analysis, markdown, code, configuration]

**Output Format:** [Markdown guidance with inline Swift examples, architectural options, and a decision matrix]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only; no bundled code execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
