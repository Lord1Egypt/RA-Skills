## Description: <br>
Slices long images/screenshots into overlapping segments, adds sequence numbers, and arranges them into a paginated PDF with configurable gaps, grids, and page numbers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wux818738-alt](https://clawhub.ai/user/wux818738-alt) <br>

### License/Terms of Use: <br>
GPL-3.0 <br>


## Use Case: <br>
External users and legal-document workflows use this skill to convert long screenshots or multiple evidence images into a paginated, printable PDF with sequence markers for easier review and citation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer downloads and replaces local skill files before installing Python dependencies. <br>
Mitigation: Review the installer before running it and prefer a pinned or checksum-verified release. <br>
Risk: The runtime guidance can lead an agent to open generated PDFs automatically. <br>
Mitigation: Open generated PDFs only when explicitly requested after confirming the output path. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wux818738-alt/image-paginator) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/wux818738-alt) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, guidance, files] <br>
**Output Format:** [Markdown guidance with inline shell commands; runtime execution produces PDF files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The command-line tool accepts one or more source image paths plus pagination, grid, overlap, margin, numbering, and cleanup options.] <br>

## Skill Version(s): <br>
2.4.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
