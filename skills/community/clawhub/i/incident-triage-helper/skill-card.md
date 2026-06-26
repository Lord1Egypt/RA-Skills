## Description: <br>
Helps agents review, validate, and package a local skill for handoff or publication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[li-chi](https://clawhub.ai/user/li-chi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and maintainers use this skill to review metadata, check required package files, and prepare a local skill archive before handoff or publication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release name suggests incident triage, while the artifact content behaves as a local skill validation and packaging helper. <br>
Mitigation: Confirm the intended package before installation and revise the release metadata or artifact contents if incident triage behavior is required. <br>
Risk: The artifact includes local shell scripts that validate package files and create an archive. <br>
Mitigation: Review scripts/validate.sh and scripts/package.sh before execution, and run them only in a local workspace containing the expected package files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/li-chi/incident-triage-helper) <br>
- [README](artifact/README.md) <br>
- [Review Checklist](artifact/docs/review-checklist.md) <br>
- [Assessment Notes](artifact/docs/assessment-notes.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, files] <br>
**Output Format:** [Markdown with inline shell commands and local file references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create a local tar.gz package archive when the packaging script is run.] <br>

## Skill Version(s): <br>
0.4.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
