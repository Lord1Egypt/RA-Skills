## Description:

Search, summon, and possess your agent with SOUL.md personality files from the OpenSOUL.md registry

This skill is ready for commercial/non-commercial use.

## Publisher:

[danielliuzy](https://clawhub.ai/user/danielliuzy)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to search the OpenSOUL.md registry, download SOUL.md personality files, activate them for future agent conversations, and restore the original personality state when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs mutable remote code through the OpenSOUL.md installer or npm package source.

Mitigation: Install only if the OpenSOUL.md installer, registry, and npm package source are trusted; prefer a pinned and verified install path.

Risk: The skill can bypass confirmation while changing persistent agent personality state.

Mitigation: Preview or dry-run any soul before activation, and avoid confirmation-bypass behavior unless the exact soul and source are clear.

Risk: Possession changes can affect future conversations, while banish removes local cached files.

Mitigation: Use status checks before changes, keep the original restoration path available, and use exorcise to restore the original personality when needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/danielliuzy/skills/opensoulmd)
- [OpenSOUL.md installer](https://opensoul.md/install.sh)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the soul command-line tool; search commands should use non-interactive mode.]

## Skill Version(s):

1.0.1 (source: server release metadata; package.json declares 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
