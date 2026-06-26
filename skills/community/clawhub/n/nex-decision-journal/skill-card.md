## Description: <br>
Nex Decision Journal is a local CLI skill for logging decisions, predictions, confidence, follow-up reviews, outcomes, and reflection statistics in a SQLite-backed personal decision journal. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nexaiguy](https://clawhub.ai/user/nexaiguy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, founders, managers, freelancers, consultants, and other decision makers use this skill to record important choices before acting, revisit outcomes later, and identify patterns such as overconfidence, underconfidence, and category-specific judgment accuracy. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores sensitive personal or business decisions persistently in a local SQLite database under ~/.nex-decision-journal. <br>
Mitigation: Require explicit user confirmation before logging, editing, reviewing, abandoning, or exporting decisions, and treat the database and exported files as confidential. <br>
Risk: The export option can write or overwrite files outside the intended export folder when users provide unsafe output paths. <br>
Mitigation: Avoid absolute paths and ../ path segments in --output values, and review export destinations before running export commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nexaiguy/nex-decision-journal) <br>
- [Nex AI homepage](https://nex-ai.be) <br>
- [README](artifact/README.md) <br>
- [Skill documentation](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text and Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [CLI output includes decision IDs, ISO dates, confidence scores, accuracy markers, statistics, search results, and export paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
