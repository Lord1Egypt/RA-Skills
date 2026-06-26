## Description: <br>
Validates Markdown files for broken local links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wanng-ide](https://clawhub.ai/user/wanng-ide) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and documentation maintainers use this skill to scan Markdown files or directories for broken relative links before publishing or sharing documentation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The JSON report can expose local file paths, link text, and broken-link URLs from scanned documentation. <br>
Mitigation: Run the skill only on intended files or folders and review the report before sharing it outside the trusted workspace. <br>
Risk: The checker ignores external HTTP/HTTPS URLs and same-file anchors, so a clean report is not a complete Markdown quality audit. <br>
Mitigation: Use it as a local relative-link check and pair it with other documentation review steps when external links or anchors matter. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wanng-ide/markdown-validator) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/wanng-ide) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [JSON report with file validity, broken-link details, link text, URLs, and line numbers.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [External HTTP/HTTPS URLs and same-file anchors are ignored.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
