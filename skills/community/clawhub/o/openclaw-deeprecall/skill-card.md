## Description:

Openclaw Deeprecall provides persistent two-tier memory for AI agents, combining structured fact search with raw content retrieval and cleanup of temporary session files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hallllllll](https://clawhub.ai/user/hallllllll)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to let OpenClaw agents search prior session facts, retrieve source memory content, summarize memory files, and manage temporary memory files across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Raw session memory may be stored permanently and later returned verbatim.

Mitigation: Use no_store_raw or set store_raw_content false where possible, and keep secrets, credentials, private keys, regulated data, and other sensitive content out of memory files.

Risk: Memory content may be sent to a configured LLM provider during summarization.

Mitigation: Use an explicit trusted provider or local-only extraction, and test provider settings before processing real memory content.

Risk: Automatic cleanup can delete Markdown files from the detected memory directory.

Mitigation: Run cleanup in dry-run mode first, verify the detected memory directory, and avoid scheduling automatic jobs until retention and size settings are understood.

Risk: Under-scoped paths can read or process more local data than expected.

Mitigation: Process only trusted, explicit memory directories or files, and do not pass arbitrary file paths to the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hallllllll/skills/openclaw-deeprecall)
- [Configuration Guide](artifact/CONFIG_GUIDE.md)
- [Skill README](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with command examples and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return compact fact-search results or raw memory content; summarization can persist extracted facts and optional raw content for later retrieval.]

## Skill Version(s):

0.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
