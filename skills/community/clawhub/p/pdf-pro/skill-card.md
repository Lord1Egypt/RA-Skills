## Description: <br>
Pdf Pro helps agents inspect and modify PDF documents through local utilities for merging, splitting, extracting pages, rotating, compressing, converting images, encrypting, decrypting, and reading PDF metadata. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SxLiuYu](https://clawhub.ai/user/SxLiuYu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and document-processing agents use this skill to perform common PDF maintenance tasks on local files, including combining documents, extracting or rotating pages, converting between PDFs and images, and applying or removing PDF passwords when authorized. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can decrypt PDFs and handle password-protected documents. <br>
Mitigation: Use it only on documents the operator is authorized to access, and keep passwords private. <br>
Risk: PDF editing commands write output files and could overwrite or expose sensitive document contents if paths are chosen carelessly. <br>
Mitigation: Choose explicit output paths, avoid overwriting originals, and handle generated files according to the document's sensitivity. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/SxLiuYu/pdf-pro) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files, guidance] <br>
**Output Format:** [Markdown guidance with command examples and local file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include modified PDF files, image files converted from PDF pages, and text metadata from inspected PDFs.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
