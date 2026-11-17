## Description:

Discover and download static PDF files from Investor Relations (IR) sites, including annual reports and quarterly results, by finding PDF URLs, probing common IR paths, querying Wayback, or downloading known static PDFs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangwllu](https://clawhub.ai/user/wangwllu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to locate and download public IR PDFs such as annual reports or quarterly result documents. It is intended for document discovery and retrieval, not structured SEC/XBRL financial analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent broad outbound download ability and local PDF write behavior without enough network safeguards.

Mitigation: Use known public IR or SEC URLs, avoid untrusted URL lists, and prefer a network-restricted environment until URL validation, redirect validation, private-address blocking, and download size limits are added.

## Reference(s):

- [Issuer hints](references/issuers.json)
- [Wayback Machine CDX API endpoint](https://web.archive.org/cdx/search/cdx)

## Skill Output:

**Output Type(s):** [text, shell commands, files, guidance]

**Output Format:** [Markdown guidance with inline bash commands and local PDF file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Makes outbound web requests and writes downloaded PDFs locally.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
