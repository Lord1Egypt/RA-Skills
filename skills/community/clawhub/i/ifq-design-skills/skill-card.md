## Description: <br>
Use this skill when the user asks for an HTML-first visual design deliverable: interactive prototype, slide deck, motion demo, infographic, dashboard, landing page, whitepaper, changelog, business card, social cover, brand system, design critique, multi-variant exploration, or export planning for MP4, GIF, PPTX, PDF, or SVG. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[peixl](https://clawhub.ai/user/peixl) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users, designers, product teams, and agent operators use this skill to turn natural-language visual design requests into local HTML-first artifacts such as prototypes, decks, dashboards, infographics, social cards, brand systems, critiques, and export-ready source structures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated previews may make optional outbound HTTPS requests for fonts, icons, factual checks, or image assets. <br>
Mitigation: Review generated HTML before sharing, prefer system or self-hosted assets for sensitive work, and run without browser/network access when external fetching is not acceptable. <br>
Risk: Optional personal memory or asset indexes can expose sensitive personal data, private local paths, credentials, or customer material through prompts or outputs. <br>
Mitigation: Keep sensitive material out of optional memory indexes and generated artifacts unless the operator has explicitly approved that use. <br>
Risk: The skill creates and edits local HTML design artifacts in the active workspace. <br>
Mitigation: Install only for workflows where workspace file creation is intended, inspect changed files before use, and keep agent filesystem permissions scoped to the active workspace. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/peixl/ifq-design-skills) <br>
- [ClawDIS homepage](https://github.com/peixl/ifq-design-skills) <br>
- [Agent compatibility](references/agent-compatibility.md) <br>
- [Modes](references/modes.md) <br>
- [Workflow](references/workflow.md) <br>
- [Verification](references/verification.md) <br>
- [Asset protocol](references/asset-protocol.md) <br>
- [Anti-slop preflight](references/anti-ai-slop.md) <br>
- [Template index](assets/templates/INDEX.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with local HTML, SVG, CSS/JS source files, verification notes, and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are workspace-scoped and may include assumptions, caveats, template routes, and export plans; MP4, GIF, PDF, and PPTX automation is not bundled in the ClawHub-safe package.] <br>

## Skill Version(s): <br>
2.4.3 (source: SKILL.md frontmatter, CHANGELOG, clawhub.json, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
