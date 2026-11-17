## Description:

Create evidence-backed Chinese or English flashcards from supplied local text, verify exact source quotes, and export safe Markdown, Anki TSV and a manual review checklist. Use for Study Cards with Source References or note-to-question practice; not inventing knowledge, scheduling or syncing an external learning account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hznetnewpower](https://clawhub.ai/user/hznetnewpower)

### License/Terms of Use:

MIT-0

## Use Case:

Learners use this skill to turn supplied English or Simplified Chinese notes into source-backed flashcards, check answers against exact quotes, and export cards for manual review or Anki import.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Supplied notes may contain information the user has not approved for processing by the connected model, and source snapshots and drafts remain locally until removed.

Mitigation: Use only notes permitted for the configured model, and remove local snapshots and drafts when they are no longer needed.

Risk: A generated answer may be inaccurate even when its quote appears in the source, and an Anki TSV import may be mapped or displayed incorrectly.

Mitigation: Review answer accuracy and preview the TSV with HTML disabled before manually importing it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hznetnewpower/skills/mochi-learning-cards)
- [MochiLab](https://mochilab.bz)
- [Anki text file import guide](https://docs.ankiweb.net/manual/importing/text-files)

## Skill Output:

**Output Type(s):** [Markdown, TSV, JSON]

**Output Format:** [Markdown, UTF-8 tab-separated text, and JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a Markdown card set, Anki TSV, and manual review checklist; card count is configurable from 1 to 20 (default 8). Source input is limited to 64 KiB and 1–80 paragraphs.]

## Skill Version(s):

1.0.1 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
