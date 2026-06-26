## Description: <br>
A local PDF toolkit for merging, splitting, compressing, converting, and extracting text from PDF files without network access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[newaiguy](https://clawhub.ai/user/newaiguy) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and document-processing users can use this skill to run local PDF merge, split, compression, conversion, and text-extraction workflows while keeping files offline. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crafted filenames, paths, or page-range inputs could trigger unintended local command execution. <br>
Mitigation: Use trusted documents and simple trusted filenames, review commands before execution, and run the skill in a sandbox when handling untrusted files. <br>
Risk: Relaxing ImageMagick PDF policy can broaden system-wide PDF processing exposure. <br>
Mitigation: Avoid globally changing ImageMagick PDF policy unless the operational risk is understood and accepted. <br>
Risk: PDF passwords supplied on the command line can be exposed through shell history or process listings. <br>
Mitigation: Avoid placing sensitive PDF passwords directly on the command line; prefer safer secret-handling workflows where available. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and local file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local PDF utilities such as poppler-utils, Ghostscript, and ImageMagick.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
