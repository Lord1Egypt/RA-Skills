## Description: <br>
Generates single-file HTML slide reports with dark and light presentation styling for strategy, architecture, cost, and roadmap briefings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dengjiawei1226](https://clawhub.ai/user/dengjiawei1226) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and business users use this skill to turn report content into browser-ready HTML presentation decks with reusable slide components, SVG architecture diagrams, navigation, and print/PDF support. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the agent to append future lessons into the installed skill file without clear user control. <br>
Mitigation: Require explicit user approval before modifying installed skill files, and review any accumulated lessons before reuse or redistribution. <br>
Risk: Confidential report content could be exposed if generated outputs are uploaded or shared outside the local workspace. <br>
Mitigation: Keep generated reports local unless upload is explicitly approved, and review content for sensitive data before sharing. <br>
Risk: Remote fonts and example external links may contact third-party services when reports are opened. <br>
Mitigation: Replace remote fonts and external links with local or system alternatives when working with confidential material. <br>


## Reference(s): <br>
- [Design System](artifact/references/design-system.md) <br>
- [SVG Architecture Rules](artifact/references/svg-architecture-rules.md) <br>
- [Component Index](artifact/components/README.md) <br>
- [Examples](artifact/examples/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Files, Markdown, Guidance] <br>
**Output Format:** [Single-file HTML with optional Markdown planning notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are intended for local browser preview, screenshot capture, or print/PDF export.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
