## Description: <br>
Generates an interactive static HTML architecture diagram for the current code repository by scanning source files, summarizing them, creating a PlantUML mind map, and adding Mermaid sub-flowcharts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[panrusheng](https://clawhub.ai/user/panrusheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect a repository's high-level architecture and module relationships as an interactive browser-viewable HTML artifact. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Repository source files are read and used in model prompts, which can expose secrets, credentials, regulated data, or sensitive proprietary code. <br>
Mitigation: Run only on repositories that have been reviewed or sanitized, and exclude sensitive files before invoking the skill. <br>
Risk: Generated cache files, temporary files, and final HTML may contain architecture details or source-derived summaries. <br>
Mitigation: Review generated cache, /tmp artifacts, and HTML output before sharing or storing them in a sensitive environment. <br>
Risk: The generated HTML depends on a remote Mermaid CDN. <br>
Mitigation: Review or replace the CDN dependency before opening or distributing the output in restricted environments. <br>


## Reference(s): <br>
- [Prompt templates](references/prompts.md) <br>
- [ClawHub skill page](https://clawhub.ai/panrusheng/interactive-arch-diagram-creator) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Text, Shell commands, Guidance] <br>
**Output Format:** [Static HTML file with concise text instructions and intermediate JSON, PlantUML, and Mermaid data files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses repository source summaries and may create cache and temporary files during diagram generation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
