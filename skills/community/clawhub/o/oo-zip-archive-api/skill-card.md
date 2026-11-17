## Description:

Use the oo CLI to compress publicly accessible files and extract public archives through Zip Archive API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to compress publicly accessible files into ZIP archives or extract public archives through their connected Zip Archive API account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fallback setup executes downloaded installer code whose contents have not been verified.

Mitigation: Install a reviewed oo CLI release separately and check its automatic skill synchronization settings.

Risk: The skill's safety guidance misclassifies remote archive creation as read-only.

Mitigation: Before processing files, approve the input URLs, potential charges, and transit-storage handling.

## Reference(s):

- [Zip Archive API documentation](https://archiveapi.com/rest-api/)
- [Zip Archive API homepage](https://archiveapi.com)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON request and response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions return archive download URLs or extracted files through transit storage.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
