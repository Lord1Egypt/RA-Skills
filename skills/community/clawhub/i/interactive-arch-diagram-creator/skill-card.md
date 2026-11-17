## Description:

Generates an interactive static HTML architecture diagram from a local code repository by scanning source files, summarizing modules, creating a PlantUML mindmap, and rendering Mermaid sub-flowcharts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[panrusheng](https://clawhub.ai/user/panrusheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to understand a local repository's architecture, module responsibilities, and cross-layer relationships as a browsable static HTML report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repository scans may read files outside the intended target when symlinks are present.

Mitigation: Install and run the skill only on trusted repositories, and avoid repositories that contain symlinks or untrusted file layouts.

Risk: Generated HTML reports can behave as active web pages and may run injected scripts.

Mitigation: Treat generated reports as active HTML, review reports before sharing, and open them only in a controlled browser context when scanning untrusted code.

Risk: Source contents are sent into the agent workflow for summarization and diagram generation.

Mitigation: Avoid running the workflow on repositories that may contain secrets, sensitive source, or untrusted code comments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/panrusheng/skills/interactive-arch-diagram-creator)
- [Prompt templates](references/prompts.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Static HTML file with embedded JSON data, plus intermediate JSON, PlantUML, and Mermaid text during generation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs in a repository root, may reuse a JSON cache, and writes the generated HTML report to the selected output directory.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
