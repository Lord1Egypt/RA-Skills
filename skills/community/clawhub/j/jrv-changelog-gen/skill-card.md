## Description: <br>
Generate changelogs from git commit history with conventional commit parsing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Johnnywang2001](https://clawhub.ai/user/Johnnywang2001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to generate release notes and changelogs from local git commit history, including conventional commit groupings, breaking change summaries, and markdown or JSON output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated changelogs may expose private commit history or contributor information if shared outside the repository team. <br>
Mitigation: Review generated output before sharing it beyond the intended audience. <br>
Risk: Using the output-file option can overwrite an existing file at the selected path. <br>
Mitigation: Use -o or --output only with an intended destination path and review the target before running. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Johnnywang2001/jrv-changelog-gen) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown or JSON changelog content, with optional file output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can group commits by conventional commit type, report breaking changes, and write to an intended output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
