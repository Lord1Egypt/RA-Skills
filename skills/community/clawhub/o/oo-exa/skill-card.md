## Description:

Operate Exa search, content retrieval, similar-page, and citation-backed answer actions through the oo CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other users use this skill to search the web, find similar pages, retrieve page contents, and generate citation-backed answers through Exa.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fallback setup runs downloaded installer code without a separate approval step.

Mitigation: Preinstall a trusted, verified CLI version and require approval before allowing fallback installation.

Risk: OOMOL mediates Exa requests and credentials, and the CLI may automatically sync skills.

Mitigation: Review the CLI's automatic skill-sync settings and understand the OOMOL connection before use.

## Reference(s):

- [Exa](https://exa.ai)
- [Exa API documentation](https://docs.exa.ai/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Text]

**Output Format:** [JSON connector responses and citation-backed text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the user's connected Exa account through OOMOL; the answer action can write data.]

## Skill Version(s):

1.0.6 (source: artifact frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
