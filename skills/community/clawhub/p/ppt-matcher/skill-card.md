## Description: <br>
PPT-Matcher analyzes existing PPTX files to extract color, font, layout, and decorative style patterns so agents can design or revise slides with a consistent presentation style. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tuobadaidai](https://clawhub.ai/user/tuobadaidai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, office users, and presentation-focused agents use this skill to inspect a reference PPTX, extract its design rules, and plan slide additions or rewrites that preserve the deck's visual style. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Slide rewrite workflows may delete and recreate target slides, which can remove content or formatting if the requested pages or redesign plan are wrong. <br>
Mitigation: Review the target slide numbers, extracted content, and proposed redesign before execution, and keep a backup copy of the PPTX before applying edits. <br>
Risk: Style analysis can miss or underrepresent gradient, transparent, or platform-specific visual details. <br>
Mitigation: Confirm accent colors, fonts, and gradient-heavy styling manually when the analysis reports unrecognized values or when the deck relies on non-solid visual effects. <br>


## Reference(s): <br>
- [Common PPT Page Design Patterns](references/design-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance, Configuration] <br>
**Output Format:** [Markdown-style guidance with console analysis summaries, inline shell commands, and structured slide content specifications] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce instructions for pptx-add-slides or file-agent; slide edits should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter, meta.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
