## Description: <br>
Builds journal club or literature-report slide decks from research PDFs with a figure-first workflow that preserves paper logic, safe crops, matched supporting evidence, and render-based QA. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yufeng166977](https://clawhub.ai/user/yufeng166977) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, students, and academic teams use this skill to turn one or more research PDFs into presentation-ready journal club, lab meeting, literature review, or paper-report decks. It is especially suited to figure-heavy scientific talks where paper logic, main/support evidence pairing, readable crops, and final render inspection matter. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research PDFs and supplementary files may contain unpublished or sensitive material. <br>
Mitigation: Use the skill only with documents the user is comfortable having the agent process, and avoid unnecessary retention or sharing of source files and generated extracts. <br>
Risk: Deck generation may require package installs or document-conversion commands. <br>
Mitigation: Review proposed installs and conversion commands before execution, prefer a local virtual environment, and inspect generated files before relying on them. <br>
Risk: Generated slides can misrepresent a paper if figure crops, support figures, or rendered output are not checked. <br>
Mitigation: Verify figure identity, crop boundaries, support-evidence pairing, readability, and final rendered slides before presenting. <br>


## Reference(s): <br>
- [MetaEdit journal-club mapping and crop notes](references/metaedit-jcslides-mapping-and-crop-notes.md) <br>
- [Multi-paper plasmid copy-number deck](references/multi-paper-plasmid-copy-number-deck.md) <br>
- [Python-pptx first-pass render QA lessons](references/python-pptx-render-qa-first-pass.md) <br>
- [Figure integrity deep-fix notes](references/figure-integrity-deep-fix-notes.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Files] <br>
**Output Format:** [Markdown guidance with optional code, shell commands, PPTX files, PDF exports, and rendered slide images] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include slide logic, figure mappings, crop notes, PPTX generation scripts, presentation files, and render QA outputs.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata; artifact frontmatter lists 2.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
