## Description:

Infinite organized memory that complements an agent's built-in memory with unlimited categorized storage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardyjcool](https://clawhub.ai/user/edwardyjcool)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create and maintain a local ~/memory/ folder for structured long-term notes, project history, contacts, decisions, knowledge, and collections.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local memory files can retain personal or sensitive information over time.

Mitigation: Avoid storing credentials, government IDs, health or financial details, and sensitive business information unless local protections are in place; periodically review ~/memory/ for deletion or redaction.

Risk: Optional sync from built-in memory can copy more information into persistent local storage than intended.

Mitigation: Use sync narrowly, keep it one-way into ~/memory/, and review synced entries before relying on or retaining them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/edwardyjcool/skills/my-custom-skill)
- [Publisher profile](https://clawhub.ai/user/edwardyjcool)
- [Skill homepage](https://clawic.com/skills/memory)
- [Setup guide](artifact/setup.md)
- [Memory templates](artifact/memory-template.md)
- [Organization patterns](artifact/patterns.md)
- [Troubleshooting](artifact/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and local file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates local files under ~/memory/ when used; no network services are required.]

## Skill Version(s):

1.0.0 (source: server release metadata, released 2026-05-17)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
