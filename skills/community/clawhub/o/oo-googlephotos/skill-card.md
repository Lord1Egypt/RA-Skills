## Description:

Use this skill to read and manage Google Photos albums and media through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to find and manage Google Photos albums and media, including items selected through Google Photos Picker. It can also upload media, update albums or descriptions, and manage picker sessions through the connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup uses an unverified remote installer and may install additional agent skills automatically.

Mitigation: Review the installer and oo CLI behavior before installation; check whether synchronization controls can disable automatic skill installs.

Risk: The connected account can expose Google Photos data and allow changes.

Mitigation: Review OOMOL's account permissions and confirm each proposed write or destructive action.

## Reference(s):

- [Google Photos](https://www.google.com/photos/about/)
- [Google Photos API overview](https://developers.google.com/photos/overview/about)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance]

**Output Format:** [Markdown guidance with oo CLI command examples and JSON payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include results returned by Google Photos actions.]

## Skill Version(s):

1.0.5 (source: frontmatter; release metadata agrees)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
