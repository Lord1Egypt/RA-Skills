## Description: <br>
Use when the user needs to convert documents between formats with Pandoc, including Markdown, DOCX, PDF, HTML, EPUB, LaTeX, Typst, RST, AsciiDoc, Org, ODT, RTF, ipynb, single-file conversion, batch document conversion, citations, templates, table of contents, Pandoc installation help, or PDF engine troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liuwei1125](https://clawhub.ai/user/liuwei1125) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and document authors use this skill to convert individual files or batches of documents with Pandoc while validating inputs, selecting formats, handling citations and templates, and troubleshooting PDF engine requirements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Document conversions operate on user-supplied files and directories and may overwrite output files. <br>
Mitigation: Review batch inputs and output directories before running conversions, choose explicit output paths, and use --skip-existing when preserving existing files matters. <br>
Risk: The optional installer can execute a package-manager command when --yes is approved. <br>
Mitigation: Run the installer in dry-run mode first and approve --yes only after reviewing the printed command. <br>


## Reference(s): <br>
- [Pandoc Format Reference](references/formats.md) <br>
- [Pandoc Conversion Workflows](references/workflows.md) <br>
- [Pandoc Troubleshooting](references/troubleshooting.md) <br>
- [Pandoc Installing Documentation](https://pandoc.org/installing.html) <br>
- [ClawHub Skill Page](https://clawhub.ai/liuwei1125/pandoc-convert-pro) <br>
- [Publisher Profile](https://clawhub.ai/user/liuwei1125) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and generated document files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce converted files, batch reports, validation messages, and Pandoc installation guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
