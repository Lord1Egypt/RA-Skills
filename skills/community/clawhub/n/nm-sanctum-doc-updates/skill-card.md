## Description: <br>
Updates documentation after code changes with quality gates, slop detection, and accuracy checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and documentation maintainers use this skill after code changes to update READMEs, plans, wikis, ADRs, and docstrings while checking style, consolidation opportunities, capability registration drift, and factual accuracy. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can edit, merge, split, delete, or stage documentation files, which can remove useful content if applied without review. <br>
Mitigation: Review consolidation suggestions before approving deletes, merges, splits, or staging; use skip or dry-run options for routine documentation edits. <br>
Risk: Documentation updates can introduce incorrect or stale claims about versions, counts, paths, or public APIs. <br>
Mitigation: Run the built-in accuracy checks and preview diffs before accepting changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-sanctum-doc-updates) <br>
- [Metadata homepage](https://github.com/athola/claude-night-market/tree/master/plugins/sanctum) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and plain text with inline shell commands, checklists, file edits, and diffs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can propose documentation edits, consolidation actions, capability sync changes, accuracy warnings, and git staging steps for user review.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
