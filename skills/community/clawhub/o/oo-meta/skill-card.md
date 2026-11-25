## Description:

Operate Meta (Facebook) through an OOMOL-connected account to read advertising and Page data, manage insights reports, and create, update, or delete Page posts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using an OOMOL-connected Meta account can retrieve advertising and Facebook Page data, generate insights reports, and manage Page posts. The skill provides the documented actions and setup guidance for using the oo CLI with Meta.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The fallback setup runs a remote installer with local user privileges, and the scanner did not inspect that installer's contents.

Mitigation: Review the installer's source and contents before running it; follow the documented setup steps only when the command's origin and effects are understood.

Risk: The security scan had partial coverage because two local path-like references could not be resolved.

Mitigation: Review the unresolved references and the full skill before installation.

## Reference(s):

- [Meta business homepage](https://business.meta.com/)
- [Meta developer documentation](https://developers.facebook.com/docs/)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-meta)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [JSON action responses with concise task results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Response content depends on the selected Meta action and the connected account's permissions.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
