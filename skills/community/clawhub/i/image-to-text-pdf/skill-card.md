## Description: <br>
Convert a finished raster image, especially a generated poster or visual resume, into an image-based PDF with an additional selectable, copyable, searchable text layer. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zjsxply](https://clawhub.ai/user/zjsxply) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content creators use this skill to preserve a finished image as the visual PDF layer while adding selectable, copyable, and searchable text. It is suited for posters, visual resumes, and similar raster layouts where rebuilding the layout in another format would be fragile. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Images or source text may be sent to an external OCR or vision service if the user chooses one outside the local scripts. <br>
Mitigation: Use trusted OCR providers or local OCR for sensitive files, and review provider data-handling terms before submitting private content. <br>
Risk: OCR boxes or corrected text may be misaligned or inaccurate, making copied PDF text differ from the visual image. <br>
Mitigation: Inspect the generated debug PDF and correct the layout JSON before delivering the final invisible-text PDF. <br>
Risk: Non-Latin or CJK text may not extract correctly if the default PDF font lacks required glyphs. <br>
Mitigation: Provide an appropriate Unicode font with the script's font-file option for non-Latin content. <br>


## Reference(s): <br>
- [Layout JSON](references/layout-json.md) <br>
- [OCR and Source-Text Alignment](references/ocr-alignment.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON layout examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces guidance for generating a final invisible-text PDF and a visible inspection PDF; scripts may also produce layout JSON and PDF files.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
