## Description:

Converts PPTX presentations into structured content, slide thumbnails, and a polished Markdown speech draft written by the agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qigaiai](https://clawhub.ai/user/qigaiai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn a provided .pptx deck into a readable Markdown speech or presentation script with supporting slide thumbnails.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence says the skill performs broad automatic dependency setup, including unverified executable downloads.

Mitigation: Use only in a disposable or locked-down environment, preinstall LibreOffice and Poppler, and avoid allowing automatic downloads in production.

Risk: The security evidence says Linux dependency setup may use privileged package-manager installation and create global symlinks.

Mitigation: Do not run the skill with sudo or administrator rights; review and remove privileged installation behavior before deployment.

Risk: The artifact workflow can overwrite generated Markdown output.

Mitigation: Run the skill on copies of input files and preserve existing outputs before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qigaiai/skills/ppt-to-speech)
- [Sample speech output](artifact/examples/sample_speech.md)
- [Poppler Windows binary release used by the artifact](https://github.com/oschwartz10612/poppler-windows/releases/download/v25.12.0-0/Release-25.12.0-0.zip)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown speech draft with generated PNG slide thumbnails and inline shell commands for extraction.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports .pptx input only; outputs are written near the input presentation.]

## Skill Version(s):

1.0.3 (source: ClawHub release metadata; artifact frontmatter reports 3.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
