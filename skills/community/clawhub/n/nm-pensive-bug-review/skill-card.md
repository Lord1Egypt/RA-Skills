## Description: <br>
Hunts bugs with evidence trails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to guide systematic bug review, defect documentation, fix preparation, and verification planning across common programming ecosystems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad activation triggers may cause the bug-review workflow to run more often than intended. <br>
Mitigation: Invoke it for explicit debugging, defect review, release readiness, security audit, or production-issue investigation tasks. <br>
Risk: Generated findings, patches, or verification commands may be incomplete or incorrect. <br>
Mitigation: Review proposed changes and run the relevant tests, linters, or reproduction commands before accepting fixes. <br>
Risk: The artifact mentions an optional separate Claude Code plugin for the full experience. <br>
Mitigation: Review the separate plugin and its installation behavior before installing it. <br>


## Reference(s): <br>
- [Pensive plugin homepage](https://github.com/athola/claude-night-market/tree/master/plugins/pensive) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with file references, defect summaries, proposed fixes, test updates, evidence notes, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose code changes and verification commands for user review; no API keys or credential environment variables were detected.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release metadata; artifact frontmatter reports 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
