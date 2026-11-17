## Description:

mubu-integration helps agents import Mubu outlines into Obsidian, sync Markdown back to Mubu, and query or export Mubu notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuboacean](https://clawhub.ai/user/liuboacean)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent read, export, create, and update Mubu outlines as Markdown for Obsidian or local knowledge workflows. It is intended for users who are comfortable granting an agent access to their own Mubu account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use saved account credentials to read and modify real Mubu notes.

Mitigation: Install only when agent access to the account is acceptable, protect MUBU_PHONE, MUBU_PASSWORD, MUBU_MEMBER_ID, and ~/.mubu_token, and require human confirmation before create, save, move, rename, export-tree, or purge actions.

Risk: A misconfigured MUBU_BASE_URL could send authenticated requests to an unintended endpoint.

Mitigation: Do not set MUBU_BASE_URL unless it is an HTTPS Mubu URL.

Risk: The security scan requires review because safety claims are broader than the code enforces.

Mitigation: Review the skill before deployment and enforce approval around commands that alter or export account content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liuboacean/skills/mubu-integration)
- [Mubu API base endpoint](https://api2.mubu.com/v3/api)
- [README](artifact/README.md)
- [Skill usage guide](artifact/SKILL.md)
- [Changelog](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON, OPML or FreeMind XML, and CLI text depending on the command]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May perform authenticated Mubu API calls and write local Markdown exports when explicitly commanded.]

## Skill Version(s):

1.3.16 (source: server release evidence and CHANGELOG, released 2026-09-02)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
