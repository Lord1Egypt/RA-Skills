## Description: <br>
Maps file structure and module organization of a codebase before architecture reviews, refactoring planning, or migration scope estimation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to map an unfamiliar repository's layout, dominant file patterns, and likely complexity hotspots before planning reviews, refactors, or migrations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger words such as files, structure, analysis, codebase, or exploration may activate the skill during general repository discussions. <br>
Mitigation: Use it in workspaces where local file inspection is acceptable, and review the generated observations before relying on them. <br>
Risk: File listings, counts, and hotspot summaries can reveal project structure or sensitive filenames. <br>
Mitigation: Avoid applying the skill to repositories whose structural metadata should not be shared in the active agent session. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-sanctum-file-analysis) <br>
- [Sanctum homepage](https://github.com/athola/claude-night-market/tree/master/plugins/sanctum) <br>
- [Publisher profile](https://clawhub.ai/user/athola) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and checklist items.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces structural observations, file counts, directory layout notes, and hotspot summaries; no credentials are required.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
