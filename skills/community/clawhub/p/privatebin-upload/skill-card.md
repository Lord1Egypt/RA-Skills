## Description:

Upload content to a PrivateBin instance and return a shareable link.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kafcoppelia](https://clawhub.ai/user/kafcoppelia)

### License/Terms of Use:

MIT

## Use Case:

Developers, engineers, and other agent users use this skill to upload selected text, code, reports, or files to a configured PrivateBin instance and receive an expiry-controlled share link.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can upload selected content to an external PrivateBin instance and return a link that grants access.

Mitigation: Require explicit confirmation of the target instance and sharing settings before upload, and avoid uploading secrets or proprietary files.

Risk: The security guidance flags unsafe shell-command examples around invoking the PrivateBin CLI.

Mitigation: Invoke the CLI without shell interpolation and pass user-controlled values as arguments or stdin through safe process APIs.

Risk: Unreviewed PrivateBin CLI dependency versions or untrusted instances can increase sharing and operational risk.

Mitigation: Pin reviewed dependency versions and prefer a trusted self-hosted PrivateBin instance.

## Reference(s):

- [PrivateBin](https://privatebin.info/)
- [privatebin CLI](https://github.com/gearnode/privatebin)
- [privatebin CLI Releases](https://github.com/gearnode/privatebin/releases/latest)
- [ClawHub Skill Page](https://clawhub.ai/kafcoppelia/skills/privatebin-upload)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and paste-link details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns the paste URL, expiry setting, and password details when a password is explicitly requested.]

## Skill Version(s):

1.0.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
