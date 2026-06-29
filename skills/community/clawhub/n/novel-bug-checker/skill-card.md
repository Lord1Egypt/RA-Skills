## Description: <br>
Novel Bug Checker audits Chinese novels for logic flaws, character inconsistencies, pacing issues, and narrative bugs, then produces graded reports with repair suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bbroot](https://clawhub.ai/user/bbroot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Writers, editors, and writing-focused agents use this skill to review Chinese novel chapters or manuscripts for narrative logic, character continuity, pacing, and foreshadowing issues. The skill returns prioritized findings and repair guidance without directly rewriting the source text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bundled templates and examples may steer the agent beyond novel review into software troubleshooting, diagnostics, or publishing actions. <br>
Mitigation: Restrict use to local novel text analysis and require separate explicit approval before publishing revisions, contacting readers, running diagnostics, or making operational changes. <br>
Risk: Generated reports or log files may persist novel content or local details. <br>
Mitigation: Review output locations, avoid providing real system logs or environment diagnostics, and handle generated files as potentially sensitive manuscript material. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bbroot/skills/novel-bug-checker) <br>
- [Bug pattern classification](references/bug-patterns.md) <br>
- [Character consistency guide](references/character-consistency.md) <br>
- [Narrative theory foundation](references/narrative-theory.md) <br>
- [Repair strategy library](references/repair-strategies.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown reports with text findings, prioritized repair suggestions, and optional Python command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports may include severity levels, issue locations, root-cause analysis, at least three repair options per bug, and validation notes for revised text.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
