## Description: <br>
Image Compressor helps agents compress, resize, convert, and optionally upload images with rv-image-optimize while returning JSON-friendly summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ziji1224054593](https://clawhub.ai/user/ziji1224054593) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, designers, and content operators use this skill to reduce image size, convert batches to WebP or AVIF, resize image sets, and prepare optimized files for upload from an agent or CLI workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Upload workflows can send files or credentials to an unintended endpoint if the URL, HTTPS trust, selected files, Authorization value, or Cookie value is wrong. <br>
Mitigation: Review upload configuration before execution, prefer explicit config files, and use preview-only behavior when checking FormData fields. <br>
Risk: Destructive flags can delete or replace source images. <br>
Mitigation: Use output-directory compression by default and only use --delete-original or --replace-original after explicit user confirmation. <br>
Risk: The skill depends on the third-party rv-image-optimize npm package. <br>
Mitigation: Install and execute it only when the package source and current package version are trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ziji1224054593/image-compressor) <br>
- [Image Compressor Reference](reference.md) <br>
- [rv-image-optimize homepage](https://github.com/ziji1224054593/Rv-image-optimize) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON/configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Recommends --json output summaries for processed counts, failures, output paths, and upload status when applicable.] <br>

## Skill Version(s): <br>
3.0.30 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
