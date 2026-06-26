## Description: <br>
Records agent learning events, detects errors, promotes recurring lessons into knowledge files, and reports learning statistics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alsoforever](https://clawhub.ai/user/alsoforever) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to capture conversation learnings, error observations, feature requests, and recurring patterns so an agent can maintain local improvement records. It is suited for workflows that intentionally keep persistent learning notes and periodically promote reviewed lessons into agent knowledge files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persistently records conversation and error context. <br>
Mitigation: Use it only for intentional local learning workflows, avoid private or regulated data, and add opt-in, redaction, and retention controls before broader deployment. <br>
Risk: The promotion workflow can modify long-lived agent knowledge files such as AGENTS.md, SOUL.md, TOOLS.md, and MEMORY.md. <br>
Mitigation: Require manual review before promotion and limit or remove the generic promote command in automated agent workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alsoforever/gungun-12-clo) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown records and command-line text reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates local learning, error, feature request, statistics, and promoted knowledge Markdown files.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
