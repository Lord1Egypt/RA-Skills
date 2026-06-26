## Description: <br>
PRD FullStack Skill guides an agent through a Chinese-language, full-stack PRD collaboration workflow that produces product, design, technical, testing, operations, and project planning documentation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ShiXiangYu2](https://clawhub.ai/user/ShiXiangYu2) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Product managers, designers, developers, testers, operations staff, and project managers use this skill to turn product ideas into a complete PRD through a 10-step conversational workflow. It supports structured sections for requirements, flows, UI guidance, architecture, testing, analytics, operations, and project planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated PRDs may include privacy-sensitive analytics, login logs, identifiers, retention, consent, or voice-input requirements without enough compliance review. <br>
Mitigation: Review generated PRDs before implementation and confirm privacy, consent, retention, and regulatory requirements with the responsible team. <br>
Risk: Broad activation wording can start the PRD workflow for general product-documentation requests. <br>
Mitigation: Confirm the user's intent, product scope, and desired output format before proceeding through the full workflow. <br>
Risk: Local build scripts generate files in the working project directory. <br>
Mitigation: Run initialization and build scripts only in directories where generated PRD files are expected. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ShiXiangYu2/prd-fullstack) <br>
- [Design System Reference](references/design-system.md) <br>
- [Collaboration Workflow Reference](COLLABORATION.md) <br>
- [Full-Stack PRD Structure](FULLSTACK_PRD.md) <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and structured PRD text with optional HTML/PDF generation through bundled templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes local templates, product-type JSON configs, checklists, and example PRD material.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version and artifact/package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
