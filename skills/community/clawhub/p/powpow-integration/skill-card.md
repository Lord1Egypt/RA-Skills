## Description:

Helps PowPow users draft and publish travel posts and create digital humans pinned to the public map.

This skill is ready for commercial/non-commercial use.

## Publisher:

[durenzidu](https://clawhub.ai/user/durenzidu)

### License/Terms of Use:

MIT-0

## Use Case:

PowPow users can turn photos or notes into travel posts, publish them to their account, and create map-pinned digital humans. Platform maintainers can also inspect their digital-human collection using their own credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may receive a PowPow password in chat and retain a short-lived session token locally.

Mitigation: Use a dedicated account or remove local session state on shared machines; avoid sharing credentials beyond what is necessary.

Risk: A stored session can publish or delete posts and create public digital humans without code-enforced confirmation.

Mitigation: Review the account, content, images, location, and badge cost, and personally confirm each publish, delete, or creation action.

Risk: Maintainer inspection uses a high-privilege Supabase credential.

Mitigation: Only the platform maintainer should use that credential, on a trusted machine.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/durenzidu/skills/powpow-integration)
- [PowPow homepage](https://global.powpow.online)
- [Security architecture and platform API](references/security.md)
- [File structure](references/file-structure.md)
- [Product screenshots](references/screenshots.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, HTML, Shell commands, Guidance]

**Output Format:** [Conversational guidance, HTML post drafts, and published links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can publish posts and digital humans to a public map after user approval.]

## Skill Version(s):

2.2.0 (source: ClawHub release, SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
