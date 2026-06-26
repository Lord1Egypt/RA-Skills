## Description: <br>
Generate, audit, and maintain a PROJECT-NARRATIVE.md file that captures a project's architecture, decisions, infrastructure, and state. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tcd004](https://clawhub.ai/user/tcd004) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to create, audit, update, and report on a living project narrative that helps future maintainers understand or reconstruct a repository. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated narratives and archives can expose sensitive repository context such as architecture, git remotes, commit history, and credential-location references. <br>
Mitigation: Review PROJECT-NARRATIVE.md and narrative-archive files before committing or sharing them, and keep real secrets out of the narrative. <br>
Risk: Optional URL checking contacts every URL in the document. <br>
Mitigation: Use --check-urls only when contacting those URLs is acceptable for the project and environment. <br>
Risk: A stale or incorrect narrative can mislead maintainers about the current project state. <br>
Mitigation: Run audits after significant changes, review drift findings by severity, and update or regenerate the narrative when needed. <br>


## Reference(s): <br>
- [Project Narrator ClawHub page](https://clawhub.ai/tcd004/project-narrator) <br>
- [Narrative Template](references/narrative-template.md) <br>
- [Narrative Examples](references/examples.md) <br>
- [AgentWyre](https://agentwyre.ai) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown files, audit reports, and command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated narratives may include project structure, git remotes, commit history, credential-location references, and optional URL-check results.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
