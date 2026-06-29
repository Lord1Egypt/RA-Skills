## Description: <br>
Bumps versions, updates changelogs, and coordinates version changes across files for releases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and release maintainers use this skill when preparing releases, bumping project versions, updating changelogs, and checking related documentation and configuration files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger words such as version, release, changelog, semver, and bump may activate the skill for adjacent maintenance requests. <br>
Mitigation: Phrase requests explicitly and confirm that release or version maintenance is intended before applying suggested changes. <br>
Risk: Version bumps and changelog updates can affect multiple files and may introduce incorrect release metadata. <br>
Mitigation: Review the planned file changes and diff before allowing edits, then run the relevant tests or build checks for the changed project. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-sanctum-version-updates) <br>
- [Source homepage from ClawHub metadata](https://github.com/athola/claude-night-market/tree/master/plugins/sanctum) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with command snippets and change summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose file edits, version updates, changelog entries, verification commands, and release follow-up steps.] <br>

## Skill Version(s): <br>
1.9.13 (source: ClawHub server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
