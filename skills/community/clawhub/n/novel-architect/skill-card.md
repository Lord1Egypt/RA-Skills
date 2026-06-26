## Description: <br>
A Chinese-language novel-writing workflow that guides premise refinement, outline planning, chapter drafting, quality checks, and final delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[z625662197](https://clawhub.ai/user/z625662197) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Writers and agent operators use this skill to manage Chinese web-novel projects from initial direction through outline, chapter drafting, revision gates, and final manuscript delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release includes local automation, host-inspection, publishing, cleanup, and self-evolution tools that exceed the core novel-writing workflow. <br>
Mitigation: Review the scripts before use, run the skill in an isolated project, and disable or remove those paths unless they are intentionally needed. <br>
Risk: Helper commands may act on local project files if run without a clear target. <br>
Mitigation: Pass an explicit bookRoot for workflow commands and avoid running npm scripts blindly. <br>
Risk: The package is tagged as requiring OAuth tokens or other sensitive credentials. <br>
Mitigation: Provide only the minimum credentials required for the intended workflow and keep them out of generated manuscript or state files. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/z625662197/novel-architect) <br>
- [Skill definition](SKILL.md) <br>
- [Script index](scripts/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown prose with optional shell commands, manuscript files, and JSON status outputs from helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses an explicit bookRoot and may create FBS state, memory, output, and deliverable files.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata; artifact frontmatter reports 1.0.0 and package.json reports 2.1.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
