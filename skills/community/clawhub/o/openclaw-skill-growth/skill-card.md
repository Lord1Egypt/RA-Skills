## Description: <br>
Make OpenClaw Skills observable, diagnosable, and safely improvable over time. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Shuai-DaiDai](https://clawhub.ai/user/Shuai-DaiDai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw skill maintainers use this wrapper to discover, install, and operate a plugin that observes skill behavior, diagnoses recurring issues, proposes reviewable changes, previews patches, and supports guarded apply flows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The underlying project can analyze run history and generate patches for skill files, so generated proposals or patches may contain incorrect or unsuitable guidance. <br>
Mitigation: Start with report or dry-run commands, inspect generated patches before applying them to real skills, and compare outcomes after changes. <br>
Risk: Run logs and reports may contain sensitive task history or operational details. <br>
Mitigation: Keep run logs and generated outputs private when they include sensitive task history. <br>
Risk: Installing the linked project runs npm dependency installation from the GitHub repository. <br>
Mitigation: Review the linked GitHub repository and dependency lockfile before running npm install. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Shuai-DaiDai/openclaw-skill-growth) <br>
- [Project homepage](https://github.com/Shuai-DaiDai/openclaw-skill-growth) <br>
- [GitHub release v0.1.0](https://github.com/Shuai-DaiDai/openclaw-skill-growth/releases/tag/v0.1.0) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and file-oriented workflow guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May point users to reports, diagnoses, proposals, patches, evaluations, and generated JSON files from the underlying project.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
