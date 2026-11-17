## Description:

Tracks menstrual cycles, symptoms, fertility signals, contraception-related bleeding, pain, and mood patterns from local user logs, producing predictions and red-flag guidance without diagnosing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to privately log menstrual cycle events, symptoms, fertility signals, contraception-related bleeding, pain, and mood patterns, then receive cycle predictions and safety-oriented prompts based on their own logged baseline.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores highly sensitive reproductive-health records as local plaintext files.

Mitigation: Confirm the storage path before use, keep the directory out of cloud sync, and rely on system-level protections such as disk encryption, account isolation, and backups chosen by the user.

Risk: First-use migration can move legacy period-tracking data into the active skill directory.

Mitigation: Review whether legacy directories should be migrated before first use and verify the resulting files in ~/Clawic/data/period/.

Risk: The skill can export or delete cycle, symptom, fertility, contraception, mood, and configuration records.

Mitigation: Require explicit user requests for export or deletion, confirm the requested scope, and verify the directory contents after deletion.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/period)
- [Clawic skill homepage](https://clawic.com/skills/period)
- [Skill definition](artifact/SKILL.md)
- [Privacy, storage, export, and deletion](artifact/privacy.md)
- [Data formats](artifact/log-template.md)
- [First-use setup](artifact/setup.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Plain text or Markdown responses with local Markdown and YAML file updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create, read, migrate, export, or delete local plaintext records under ~/Clawic/data/period/ when the user requests tracking, export, deletion, or first-use setup.]

## Skill Version(s):

1.0.3 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
