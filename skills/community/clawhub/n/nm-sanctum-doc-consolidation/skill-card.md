## Description: <br>
Merges ephemeral report and analysis artifacts into permanent documentation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and documentation maintainers use this skill to identify valuable content in temporary Markdown reports, route it into permanent documentation, and clean up source artifacts after review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can rewrite documentation and delete source report files during consolidation. <br>
Mitigation: Run it only in a version-controlled workspace with a clean git status, review the consolidation plan before execution, and keep source artifacts until the merged documentation is manually verified. <br>
Risk: The generated routing or merge plan may place content in the wrong destination or preserve low-value material. <br>
Mitigation: Review the proposed destinations, merge strategies, and skipped content before approving changes. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/athola/nm-sanctum-doc-consolidation) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/athola) <br>
- [Source Homepage](https://github.com/athola/claude-night-market/tree/master/plugins/sanctum) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, shell commands, guidance] <br>
**Output Format:** [Markdown plans, Markdown documentation files, and concise execution summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update documentation files and delete consolidated source artifacts after approval.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release metadata; artifact frontmatter says 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
