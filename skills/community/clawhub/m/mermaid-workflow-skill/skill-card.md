## Description: <br>
Creates Mermaid diagram definition files, converts them to PNG images with Mermaid CLI, and inserts the image links into Markdown documents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[runmanfm-bit](https://clawhub.ai/user/runmanfm-bit) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and technical writers use this skill to generate project roadmap, architecture, flowchart, sequence, class, state, Gantt, and ER diagrams, render them as PNG images, and place them into Markdown reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Mermaid rendering may run Chromium with sandboxing disabled. <br>
Mitigation: Use the skill only with trusted Mermaid inputs or render inside a container or virtual machine, and keep Chromium sandboxing enabled where the environment supports it. <br>
Risk: Markdown insertion can edit files in place. <br>
Mitigation: Use version control or backups before insertion and review the changed Markdown before relying on the output. <br>
Risk: The conversion flow may fall back to automatic npx execution for Mermaid CLI. <br>
Mitigation: Avoid automatic npx execution in sensitive environments and install or pin trusted Mermaid CLI tooling before running conversions. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/runmanfm-bit/mermaid-workflow-skill) <br>
- [README](README.md) <br>
- [Skill definition](SKILL.md) <br>
- [Example workflow](examples/example_workflow.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, Mermaid .mmd text, shell command sequences, PNG file paths, and Markdown image references.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May modify Markdown files in place when inserting generated image links.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
