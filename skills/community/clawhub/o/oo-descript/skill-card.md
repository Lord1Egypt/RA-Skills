## Description:

Use this skill to read, create, update, and delete Descript data through the user's OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Descript users use this skill to inspect projects and jobs, import media, create or edit projects, publish compositions, and manage asynchronous actions through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup runs an installer from a changeable remote URL, and the remote installer and connector implementations were not included in the artifact inspection.

Mitigation: Review and approve CLI installation separately before setup, including any bundled skill installation or updates; consider OOMOL's account permissions and data handling.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Descript](https://www.descript.com/)
- [Descript API documentation](https://docs.descriptapi.com/)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON request examples; connector action results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions may run asynchronously and return job identifiers and results.]

## Skill Version(s):

1.0.3 (source: frontmatter, server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
