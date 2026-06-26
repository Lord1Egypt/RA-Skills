## Description: <br>
A powerful document conversion tool supporting Html, Markdown, Docx, PDF, and LaTeX formats. Provides bidirectional conversion between these formats using a WebAssembly-based engine similar to Pandoc. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guyoung](https://clawhub.ai/user/guyoung) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and document authors use this skill to prepare OpenClaw WASM sandbox commands for converting, validating, or inspecting Markdown, HTML, LaTeX, Docx, and PDF-related documents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill instructs users to download and run an unpinned remote WASM converter. <br>
Mitigation: Install only from a trusted source, prefer a pinned release or commit with a published checksum, and verify the component before execution. <br>
Risk: The WASM converter requires filesystem access through --work-dir. <br>
Mitigation: Run it with --work-dir set to a small temporary folder containing only the documents intended for conversion. <br>


## Reference(s): <br>
- [Pandoc Rs Usage Guide](references/USAGE.md) <br>
- [Pandoc Rs ClawHub listing](https://clawhub.ai/guyoung/pandoc-rs) <br>
- [Pandoc WASM component download](https://raw.githubusercontent.com/guyoung/wasm-sandbox-openclaw-skills/main/pandoc-rs/files/pandoc-component.wasm) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown with inline shell commands and file-oriented instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Conversion commands can write output files inside the selected --work-dir; stats and validation commands return text.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
