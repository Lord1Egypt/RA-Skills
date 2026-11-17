## Description:

Publishes a local folder as an unauthenticated LAN web knowledge share for browsing and searching Markdown, spreadsheets, HTML reports, images, and video without database setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vesentanger](https://clawhub.ai/user/vesentanger)

### License/Terms of Use:

MIT

## Use Case:

Developers, employees, and knowledge workers use this skill to share a tightly scoped local documentation or file folder with trusted colleagues on the same LAN. It is suited for internal knowledge sharing where users understand the unauthenticated exposure model.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The LAN HTTP service has no authentication, so any reachable device on the same network can browse the selected shared folder.

Mitigation: Share only a narrow folder containing files intended for LAN access, use trusted private networks, and do not forward the LAN address to public or untrusted networks.

Risk: Symlinks can expose files outside the selected folder.

Mitigation: Remove or avoid symlinks in shared folders until symlink containment is fixed, and never share home directories, repositories, credential folders, internal reports, or personal data.

Risk: Shared Markdown or HTML content is rendered with weak isolation.

Mitigation: Preview Markdown and HTML files only from trusted contributors until preview sandboxing is fixed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vesentanger/skills/lan-folder-share)
- [SkillHub listing template](artifact/references/skillhub-listing.md)
- [Bundled third-party library provenance and checksums](artifact/assets/runtime/assets/vendor/THIRD-PARTY.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell commands and LAN URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompts the user to confirm folder scope and unauthenticated LAN exposure before starting the server.]

## Skill Version(s):

1.0.12 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
