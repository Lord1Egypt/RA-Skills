## Description:

Complete local PDF toolkit for OCR, merge, split, compress, watermark, conversion, and other Stirling-PDF operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wudi488](https://clawhub.ai/user/wudi488)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document-processing users can use this skill to deploy and operate a private Stirling-PDF workflow for local PDF OCR, conversion, merging, compression, watermarking, and security operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive PDFs, API keys, document passwords, or signing material may be sent to an untrusted or unintended Stirling-PDF endpoint.

Mitigation: Use only a local or trusted private Stirling-PDF instance, prefer HTTPS for any non-local endpoint, and confirm the configured base URL before processing sensitive documents.

Risk: One helper script defaults to an undocumented private network address and uses a different base-url variable than the main instructions.

Mitigation: Avoid sensitive PDFs until the hardcoded default and environment-variable mismatch are removed or explicitly reviewed.

Risk: Merge helper behavior can expose users to command injection when filenames are untrusted.

Mitigation: Do not run merge helpers on untrusted filenames; review or replace the helper with argument-safe command construction before deployment.

Risk: The Docker deployment example uses a floating image tag.

Mitigation: Pin the Stirling-PDF image to a reviewed version or digest before production use.

Risk: Document passwords passed as command-line arguments may be exposed through shell history or process listings.

Mitigation: Use safer secret handling for passwords and avoid passing sensitive document secrets directly on the command line.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wudi488/skills/local-pdf-suite)
- [Stirling-PDF project](https://github.com/Stirling-Tools/Stirling-PDF)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces commands and configuration guidance for a user-controlled Stirling-PDF instance; generated files are created by the invoked Stirling-PDF API.]

## Skill Version(s):

1.0.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
