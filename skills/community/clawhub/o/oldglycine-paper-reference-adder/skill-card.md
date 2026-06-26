## Description: <br>
Adds academic citation support for Overleaf-style LaTeX papers by analyzing project files, selecting references, inserting citation markers in key sections, and producing an ADD.MD report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oldglycine](https://clawhub.ai/user/oldglycine) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, authors, and developers working on Overleaf-style LaTeX projects use this skill to add relevant paper references, insert citation markers into introduction or related-work sections, and review the resulting ADD.MD citation report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can directly edit manuscript files and overwrite the configured report without a dry run or confirmation step. <br>
Mitigation: Run it only on a copied project or after a separate backup, inspect target .tex files and output_report before execution, and review diffs before keeping changes. <br>
Risk: Scholar searches may expose manuscript-derived keywords or paper content context outside the local project. <br>
Mitigation: Avoid use with confidential manuscripts unless the user approves any Google Scholar queries derived from the paper content. <br>


## Reference(s): <br>
- [Code Reference](reference/CODE.MD) <br>
- [Backup Guidance](reference/BACKUP.MD) <br>
- [Reference Addition Guidance](reference/REFERENCES.MD) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance, Python code, LaTeX citation edits, and ADD.MD report content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May modify .tex files and write or overwrite the configured ADD.MD report in the target project.] <br>

## Skill Version(s): <br>
1.1.0 (source: server evidence and skill frontmatter metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
