## Description:

Creates KSVC-validated Twitter/X content from analyst research PDFs, including long threads, quick takes, breaking-news reactions, personal commentary, victory laps, and other market commentary formats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lukerspace](https://clawhub.ai/user/lukerspace)

### License/Terms of Use:


## Use Case:

Developers and content operators use this skill to turn research PDFs into source-checked market commentary drafts with holdings checks, audit steps, voice stylization, and publish-ready thread packaging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports unsafe pickle loading from auto-discovered local RLM state files.

Mitigation: Run the cache builder only on fully trusted state.pkl files and prefer an explicit approved-file import flow for state inputs.

Risk: The security scan reports a deliberate symlink workaround around subagent file-access limits.

Mitigation: Remove or replace the symlink workaround with an approved file-access process before deployment.

Risk: Financial content, holdings claims, and investment-position language can be incorrect or misleading if drafts are published without review.

Mitigation: Manually review final content, holdings references, audit outputs, and investment-position language before copying drafts to shared thread folders.

## Reference(s):

- [Kirk Voice Guide](references/kirk-voice.md)
- [Serenity Style](references/serenity-style.md)
- [Citrini7 Style](references/citrini7-style.md)
- [Jukan Patterns](references/jukan05-patterns.md)
- [Zephyr Patterns](references/zephyr-patterns.md)
- [RLM Extraction Cache System](scripts/README-extraction-cache.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown drafts, JSON extraction caches, audit reports, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are intended for manual review before publishing; final thread packages may include clean post text, internal metadata, audit notes, and chart assets.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
