## Description:

Runs a personal journaling practice for capturing entries, prompting blank pages, reviewing weeks or years, and identifying recurring patterns while preserving user read-scope and privacy limits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to keep a local Markdown journal, receive situation-aware prompts, restart or maintain the practice, perform reviews, and analyze recurring themes only within declared read-scope limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates and maintains a plaintext local journal corpus that may include sensitive entries and metadata.

Mitigation: Install only after reviewing the disclosed config paths, read-scope settings, no-go file, backup/sync choices, and shared health/finance/contact paths.

Risk: Journal content typed or dictated into a hosted assistant may reach that assistant provider before it is saved locally.

Mitigation: For material that must never leave the device, write directly in the local entry file offline and exclude it from future agent reads.

Risk: Secrets copied into journal material could be persisted in local plaintext files or synced backups.

Mitigation: Strip credentials, PINs, keys, tokens, recovery phrases, and full account numbers before writing, preserving only safe pointers to where secrets are stored.

Risk: The skill can move neutral records such as mood ratings, contact names, project summaries, or finance figures into shared local folders.

Mitigation: Confirm the shared folder paths and keep journal entry content inside the journal folder unless the user explicitly requests a shareable excerpt.

## Reference(s):

- [ClawHub Journal skill page](https://clawhub.ai/ivangdavila/skills/journal)
- [Publisher profile](https://clawhub.ai/user/ivangdavila)
- [Clawic Journal homepage](https://clawic.com/skills/journal)
- [Privacy evidence](artifact/privacy.md)
- [Storage evidence](artifact/storage.md)
- [Difficult entries evidence](artifact/difficult-entries.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Configuration, Guidance]

**Output Format:** [Markdown text and local Markdown/YAML journal files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Maintains local journal state and related neutral shared records under disclosed configuration paths.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
