## Description: <br>
Automatically adds relevant academic references to research papers by reading Overleaf-style TeX projects, searching Google Scholar, adding BibTeX entries, inserting citation markers, and generating a report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oldglycine](https://clawhub.ai/user/oldglycine) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers and technical writers use this skill to add missing citations to LaTeX research papers, especially Introduction, Related Work, and Method sections. It is intended for projects with TeX files and a BibTeX bibliography. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads the target paper project and sends search terms derived from the paper to Google Scholar through scholarly. <br>
Mitigation: Use it only on paper projects whose content may be used for external literature search, and avoid sensitive unpublished material unless that disclosure is acceptable. <br>
Risk: The skill modifies bibliography, manuscript, and report files, which can introduce incorrect citations or unwanted edits. <br>
Mitigation: Run it on a copy or version-controlled project and review diffs before relying on the added citations. <br>
Risk: Google Scholar access through scholarly may trigger service rate limits or automated-access controls. <br>
Mitigation: Use conservative request volumes and stop if Google Scholar blocks or challenges automated access. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oldglycine/oldglycine-paper-add-citations) <br>
- [Publisher profile](https://clawhub.ai/user/oldglycine) <br>
- [Paper Reference Adder Tool](reference/TOOL.MD) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with parameter descriptions, shell commands, generated BibTeX entries, TeX citation markers, and an ADD.MD report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads TeX and BibTeX project files, queries Google Scholar through scholarly, appends references to the bibliography, and writes a citation report.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
