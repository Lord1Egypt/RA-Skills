## Description: <br>
Invention disclosure template, checklist, and Markdown-to-Word export (no third-party API token). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[windinwing](https://clawhub.ai/user/windinwing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to collect invention disclosure details, draft a structured patent disclosure, compare prior art with a related patent-search workflow, and export the completed Markdown disclosure to a Word document. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Invention disclosures can contain sensitive business and patent strategy information. <br>
Mitigation: Limit access to generated files and confirm upload or download retention policies before sharing disclosure content. <br>
Risk: Word export depends on python-docx and may attempt dependency installation if it is unavailable. <br>
Mitigation: Install and approve python-docx up front in controlled environments, or rely on the Markdown fallback when dependency installation is not acceptable. <br>
Risk: Patentability comments and prior-art comparisons may be incomplete or unsuitable for filing decisions. <br>
Mitigation: Have a qualified patent professional review the disclosure before filing or making legal decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/windinwing/patent-disclosure) <br>
- [Publisher profile](https://clawhub.ai/user/windinwing) <br>
- [README](artifact/README.md) <br>
- [Disclosure template](artifact/template.md) <br>
- [Disclosure checklist](artifact/checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, files] <br>
**Output Format:** [Markdown text for templates and checklists; downloadable Word (.docx) or Markdown file for exports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Export expects complete disclosure Markdown content and can fall back to Markdown output when Word export dependencies are unavailable.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
