## Description: <br>
A pure-python CLI application for manipulating PDF files, including compression, merging, splitting, rotation, signing, text and image extraction, metadata inspection, and file conversion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[overdue-lin](https://clawhub.ai/user/overdue-lin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to select and apply pdfly CLI commands for common PDF manipulation workflows, including combining documents, extracting content, rotating pages, managing metadata, and signing or verifying PDFs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PDF signing examples can expose certificate passwords or encourage unsafe private-key export if copied directly into commands or chat. <br>
Mitigation: Prefer new output files, keep backups, avoid placing real certificate passwords in commands or chats, and do not use unencrypted private-key export unless the storage location is controlled. <br>


## Reference(s): <br>
- [pdfly-cli ClawHub page](https://clawhub.ai/overdue-lin/pdfly-cli) <br>
- [Cat Command Reference](references/cat.md) <br>
- [Page Range Syntax Reference](references/page-ranges.md) <br>
- [Rotate Command Reference](references/rotate.md) <br>
- [PDF Signing Reference](references/sign.md) <br>
- [pypdf documentation](https://pypdf.readthedocs.io/) <br>
- [fpdf2 documentation](https://pyfpdf.github.io/fpdf2/) <br>
- [endesive documentation](https://endesive.readthedocs.io/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance may include pdfly command syntax, page range notation, output file options, and certificate handling notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
