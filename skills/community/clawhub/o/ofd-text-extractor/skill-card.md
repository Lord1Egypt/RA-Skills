## Description:

Extracts text from OFD files and preserves page, template, boundary, coordinate, and optional character-level position data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuwei19820201](https://clawhub.ai/user/liuwei19820201)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document-processing teams use this skill to inspect OFD files, extract page and template text, and capture coordinates for invoices or other fixed-layout documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted or very large OFD files can create avoidable local parsing and resource-exhaustion risk.

Mitigation: Run the extractor only on trusted or size-checked OFD files, and apply resource limits before automated bulk processing.

Risk: The optional JSON output path can overwrite an existing file if chosen carelessly.

Mitigation: Choose an explicit output location and check whether the target file already exists before running extraction.

## Reference(s):

- [OFD Structure Reference](references/ofd-structure.md)
- [OFD Specification Namespace](http://www.ofdspec.org/2016)
- [OFD Specification Site](http://www.ofdspec.org/)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Markdown guidance with shell commands and optional JSON extraction output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The Python script can print extracted text to stdout or write structured JSON to a chosen output path; character-level positions are included only when requested.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
