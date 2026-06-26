## Description: <br>
Intelligent multi-topic deep research tool that coordinates independent research agents for parallel retrieval and systematic Markdown research document generation. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[NeverChenX](https://clawhub.ai/user/NeverChenX) <br>

### License/Terms of Use: <br>
CC-BY-NC-SA-4.0 <br>


## Use Case: <br>
Developers, analysts, and researchers use this skill to split related research questions across independent agents, gather source-backed findings, and produce a structured overview plus detailed topic reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive or private input may be passed to research subagents and stored in generated Markdown reports. <br>
Mitigation: Use a deliberate output location and avoid providing sensitive material unless local storage and subagent processing are acceptable. <br>
Risk: Web-retrieved research can contain outdated, incomplete, or misleading information. <br>
Mitigation: Review generated reports and their source links before relying on conclusions or recommendations. <br>
Risk: Generated files may be saved into a project directory that is later shared or committed. <br>
Mitigation: Check the generated 03 - Deep Research directory before sharing, publishing, or committing outputs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/NeverChenX/multi-search) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Guidance] <br>
**Output Format:** [Markdown research overview and per-topic Markdown reports saved in a local research directory] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May launch multiple independent research agents and save reports under a project-specific 03 - Deep Research directory.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter, CHANGELOG, release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
