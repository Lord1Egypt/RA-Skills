## Description:

Use this skill to read, create, and update Docparser data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to inspect parsers, retrieve parsed document results and status, and submit supported document uploads or processing requests through a connected Docparser account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Document imports send a URL to a destination parser and process its contents through the connected OOMOL account.

Mitigation: Confirm every import, including its URL and destination parser, and review which documents the connected account may access.

Risk: CLI setup can run downloaded installation scripts, and the security review notes automatic skill installation may occur without separate confirmation.

Mitigation: Use a reviewed CLI release and confirm local installation behavior before running setup scripts.

## Reference(s):

- [Docparser API documentation](https://docparser.com/api/)
- [Docparser](https://docparser.com)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [JSON API responses and concise text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
