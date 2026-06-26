## Description: <br>
Updates documentation after code changes with quality gates, slop detection, and accuracy checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and documentation maintainers use this skill to update README files, plans, wikis, docstrings, ADRs, and plugin capability documentation after code changes. It emphasizes grounded edits, consolidation review, style checks, slop detection, and accuracy verification before previewing changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Documentation updates, plugin.json fixes, file deletions, merges, or git staging changes could introduce incorrect or unwanted repository changes. <br>
Mitigation: Review proposed actions before accepting them, especially plugin-sync, consolidation, deletion, merge, and staging steps. <br>
Risk: Consolidation behavior can merge, split, or remove documentation when stale or redundant files are detected. <br>
Mitigation: Use the documented skip, selection, or dry-run controls when only documentation edits are desired or when consolidation needs separate review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-sanctum-doc-updates) <br>
- [OpenClaw homepage](https://github.com/athola/claude-night-market/tree/master/plugins/sanctum) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and documentation edits] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose file edits, plugin registration updates, consolidation actions, and git staging changes for user review.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
