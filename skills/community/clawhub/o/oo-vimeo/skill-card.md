## Description:

Operate Vimeo videos, folders, showcases, and tags through the user's OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People and agents use this skill to inspect and manage Vimeo videos, folders, showcases, and tags, and to upload or download video files through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup immediately executes a remote CLI installer; the installer and hosted connector have not been verified.

Mitigation: Review and verify the CLI installer before setup, including whether it installs other agent skills.

Risk: Video transfers may bypass confirmation safeguards, and downloaded files are stored in connector transit storage.

Mitigation: Confirm OOMOL access and video-storage retention terms, explicitly authorize transfers, and retain the skill's confirmations for Vimeo changes and deletions.

## Reference(s):

- [Vimeo API reference](https://developer.vimeo.com/api/reference)
- [Vimeo](https://vimeo.com)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [JSON connector responses with concise user-facing text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses depend on the selected Vimeo action and the connected account.]

## Skill Version(s):

1.0.5 (source: skill frontmatter and server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
