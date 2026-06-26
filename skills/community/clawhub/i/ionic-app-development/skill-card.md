## Description: <br>
Guides the agent through general Ionic Framework development, including core concepts, component references, CLI usage, layout, theming, animations, gestures, development workflow, and troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[robingenz](https://clawhub.ai/user/robingenz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to answer Ionic Framework development questions, select component references, propose Ionic UI code, run common Ionic CLI workflows, and troubleshoot existing Ionic apps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional device-testing commands can expose an Ionic development server to other devices on the local network. <br>
Mitigation: Use external or live-reload serving only temporarily on trusted networks and stop the development server when testing is complete. <br>
Risk: Setup guidance may ask the agent to install or use the Ionic CLI from npm. <br>
Mitigation: Confirm the user trusts the @ionic/cli package and review proposed install commands before execution. <br>


## Reference(s): <br>
- [Action and Button Components](references/components-action.md) <br>
- [Data Display Components](references/components-data-display.md) <br>
- [Form Components](references/components-form.md) <br>
- [Layout Components](references/components-layout.md) <br>
- [Media Components](references/components-media.md) <br>
- [Navigation Components](references/components-navigation.md) <br>
- [Overlay Components](references/components-overlay.md) <br>
- [Progress Components](references/components-progress.md) <br>
- [Scroll and Virtual Components](references/components-scroll.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline code examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; no direct tool calls or credential access are required.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
