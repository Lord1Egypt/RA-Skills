## Description: <br>
Bumps versions, updates changelogs, and coordinates version changes across files for releases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and release maintainers use this skill when preparing a release, bumping semantic versions, updating changelogs, and checking related version references across project files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can propose edits to version and changelog files, and incorrect version updates could create misleading release metadata. <br>
Mitigation: Review the proposed diffs, verify the intended version number, and run the relevant project tests or builds before accepting changes. <br>
Risk: Broad trigger words such as version, release, changelog, semver, and bump may activate the workflow during general discussion. <br>
Mitigation: Confirm that the user intends to prepare a release or update project versions before applying file changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-sanctum-version-updates) <br>
- [Sanctum plugin homepage](https://github.com/athola/claude-night-market/tree/master/plugins/sanctum) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and file-change summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose edits to versioned configuration, changelog, README, and documentation files for user review.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
