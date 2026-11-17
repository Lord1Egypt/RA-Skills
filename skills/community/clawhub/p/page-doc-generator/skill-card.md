## Description:

Generates Word documentation from mini-program and uni-app project screenshots and Vue source code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skyfragments](https://clawhub.ai/user/skyfragments)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to document mini-program or uni-app pages by pairing local Vue page files with screenshots and producing shareable project documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated documentation can include screenshots, Vue source snippets, and local project paths that may expose sensitive or proprietary project details.

Mitigation: Review the generated Markdown or DOCX before sharing it outside the intended team, and remove secrets, proprietary code, or sensitive local paths.

Risk: DOCX conversion depends on a local pandoc executable and may fail or time out if pandoc is unavailable or misconfigured.

Mitigation: Install pandoc, verify it is available in PATH or a configured Windows install location, and keep the generated Markdown as the inspectable source artifact.

## Reference(s):

- [Pandoc documentation](https://pandoc.org/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and DOCX files with embedded screenshots, page metadata, Vue source snippets, and command-line usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates a Markdown source document and can convert it to DOCX with pandoc; Vue files over 500 lines are truncated in the generated documentation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
