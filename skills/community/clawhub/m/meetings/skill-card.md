## Description:

Designs, runs, records, and closes out meetings: agendas, facilitation, decisions, minutes, and follow-up.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, managers, facilitators, and external-facing teams use this skill to prepare agendas, run meetings, capture decisions and action items, write recaps or minutes, and reduce unnecessary recurring meetings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may maintain long-lived meeting, contact, and project notes, including behavioral context about people.

Mitigation: Require explicit confirmation before writes or deletions in workplace use, avoid subjective comments about people, and keep sensitive HR, legal, health, and compensation content out of local notes.

Risk: Meeting transcripts and invites can contain credentials such as passcodes, dial-in PINs, meeting passwords, or secret calendar URLs.

Mitigation: Strip credentials before saving meeting records and store only a pointer such as a keychain or password-manager reference.

Risk: Local meeting memory and follow-up ledgers can become operationally important and may be edited or retired by the skill.

Mitigation: Back up the local data stores and review named writes, deletions, and follow-up closures before relying on them as records.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/meetings)
- [Clawic Meetings homepage](https://clawic.com/skills/meetings)
- [Skill definition](artifact/SKILL.md)
- [Working file templates](artifact/memory-template.md)
- [Remote and hybrid meeting guidance](artifact/remote.md)
- [Recaps and minutes guidance](artifact/recaps-and-minutes.md)
- [Follow-through guidance](artifact/follow-through.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance, files]

**Output Format:** [Markdown guidance, meeting artifacts, and local note updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May maintain local meeting memory, contact rows, project references, meeting records, decisions, and follow-up ledgers under configured local paths.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
