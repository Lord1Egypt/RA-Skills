## Description: <br>
Converts local PDF files into Markdown with OCR, layout, tables, formulas, and extracted images preserved by running MinerU on a Modal L4 GPU. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[speech2srt](https://clawhub.ai/user/speech2srt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and document-processing users use this skill to OCR selected PDFs and retrieve Markdown outputs with associated images and auxiliary parsing files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected PDFs are uploaded to Modal-managed remote infrastructure and may remain in Modal volumes after processing. <br>
Mitigation: Use a unique slug for each job, avoid highly sensitive documents unless Modal storage is acceptable, and delete uploaded inputs and outputs from the Modal volume after processing. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown files with extracted image folders and auxiliary JSON/PDF outputs; agent guidance may include shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are organized under a slug-specific Modal volume path and downloaded as a preserved directory tree.] <br>

## Skill Version(s): <br>
v1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
