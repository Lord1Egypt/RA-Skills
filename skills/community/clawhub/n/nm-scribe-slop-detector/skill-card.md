## Description: <br>
Detects AI-generated writing patterns in prose. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, documentation maintainers, and reviewers use this skill to audit prose, documentation, and repository text for AI-writing markers, identity leaks, hallucinated references, weak claims, stubs, and cleanup risks before publication or release. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad writing-related triggers may cause the skill to run during many documentation and repository-review workflows. <br>
Mitigation: Review or narrow triggers before installation so the skill runs only in intended audit contexts. <br>
Risk: Repository review and remediation behavior can affect more than passive prose detection. <br>
Mitigation: Keep remediation and prevention-mode behavior disabled unless explicitly requested, and review proposed changes before applying them. <br>
Risk: Style and demographic heuristics can overstate confidence or produce false positives. <br>
Mitigation: Treat heuristic findings as advisory and require human review, especially for low-confidence findings. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-scribe-slop-detector) <br>
- [Publisher profile](https://clawhub.ai/user/athola) <br>
- [Homepage from ClawHub metadata](https://github.com/athola/claude-night-market/tree/master/plugins/scribe) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with structured findings and optional inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings may include file, line, category, severity, confidence, evidence, rationale, and suggested fix.] <br>

## Skill Version(s): <br>
1.9.13 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
