## Description: <br>
PPT/PPTX batch formatting repair skill that normalizes small font sizes, enables wrapping, fixes shapes that exceed slide bounds, and detects or removes common page-number formats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liuwenqi123123](https://clawhub.ai/user/liuwenqi123123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to batch process PPT/PPTX files with local python-pptx scripts that adjust undersized text, keep shapes within slide bounds, detect page numbers, and remove page-number elements after review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automated page-number removal and boundary fixes can unintentionally change slide layout or remove text that resembles a page number. <br>
Mitigation: Write changes to a separate output PPTX, inspect the result in PowerPoint or WPS, and replace originals only after confirming the layout and removed elements are correct. <br>
Risk: Font-size normalization may cause text reflow or clipping in some shapes after PowerPoint recalculates layout. <br>
Mitigation: Review slides after processing and manually adjust any text boxes that remain clipped or visually crowded. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/liuwenqi123123/pptx-batch-fix) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, code, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and script-generated console summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces corrected PPTX output files through local scripts; users should review generated files before replacing originals.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
