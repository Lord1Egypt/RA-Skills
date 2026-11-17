## Description:

Product Image Archiver archives original images for a manually supplied product link and product ID, preserving files, organizing folders, checking integrity, and marking potential image-risk indicators.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guowaa223](https://clawhub.ai/user/guowaa223)

### License/Terms of Use:

MIT-0

## Use Case:

E-commerce operators and agents use this skill to archive one product's source images into a fixed folder structure and create a manifest for review before listing or reuse.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill fetches network content and writes local files without enough scoping for untrusted product URLs.

Mitigation: Review before installing and run only in a restricted, non-admin environment with a dedicated archive directory and limited outbound network access.

Risk: Untrusted product URLs may expose the operator to unsafe redirects, unexpected hosts, oversized downloads, or unsafe product ID paths.

Mitigation: Do not process untrusted product URLs until hostname allowlisting, redirect validation, image URL validation, size quotas, and product ID path sanitization are added.

Risk: Advertised risk-detection and completeness checks are incomplete.

Mitigation: Treat risk and integrity results as advisory and require human review before relying on archived images for publication or reuse.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guowaa223/skills/product-image-archiver)
- [ClawHub publisher profile](https://clawhub.ai/user/guowaa223)
- [Baidu AI Console](https://console.bce.baidu.com/ai/)
- [1688](https://www.1688.com)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [Structured archive folders with original image files, an Excel manifest, and terminal status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3 and writes archives to a local archive directory; declared dependencies include requests, pandas, openpyxl, and Pillow.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
