## Description: <br>
A Chinese-first PRD collaboration workflow that helps an agent guide product discovery and produce complete PRD documentation for product, design, engineering, testing, operations, and project management teams. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shixiangyu2](https://clawhub.ai/user/shixiangyu2) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Product managers, designers, engineers, QA teams, operations teams, and project managers use this skill to turn a product idea into a structured PRD through a 10-step dialog workflow. The workflow produces requirements, market analysis, user flows, prototypes, UI guidance, functional specifications, data models, technical plans, testing plans, analytics events, operations plans, and project milestones. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow scaffolds local files and can run npm, Playwright, build, update, and rollback commands. <br>
Mitigation: Run those commands only inside a dedicated PRD project directory and review generated changes before reusing them. <br>
Risk: Generated analytics, authentication, and security defaults are templates rather than production-ready security guidance. <br>
Mitigation: Treat these sections as review-required drafts and validate them against project security, privacy, and compliance requirements. <br>
Risk: The PDF workflow depends on Playwright browser tooling. <br>
Mitigation: Update or lock Playwright before use and install browser dependencies in a controlled environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shixiangyu2/prd-skill-workflow2) <br>
- [README](README.md) <br>
- [PRD design system reference](references/design-system.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, HTML/PDF-oriented content templates, Mermaid diagrams, JSON configuration, and shell or npm commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can scaffold local PRD project files and generate HTML/PDF outputs when its Node.js and Playwright tooling is run in a project directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence, SKILL.md frontmatter, and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
