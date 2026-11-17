## Description:

Processes links shared in a Discord findings channel by validating and fetching public URLs, summarizing them into Discord threads, and saving synthesized notes to a local knowledge base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zerone0x](https://clawhub.ai/user/zerone0x)

### License/Terms of Use:


## Use Case:

Developers and knowledge workers use Link Digest to monitor a configured Discord channel for shared URLs, produce short source-linked summaries, and preserve distilled notes in a local knowledge base.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fetching URLs from Discord can expose the agent to SSRF attempts or redirected internal destinations.

Mitigation: Use URL validation and network policy controls that block private, link-local, metadata, non-HTTP, and redirected internal destinations before fetching.

Risk: Fetched page content may contain prompt-injection instructions or unsafe commands.

Mitigation: Treat fetched content as untrusted input, ignore embedded instructions, and write only agent-authored summaries to Discord and the knowledge base.

Risk: Knowledge-base updates and commits could affect files outside the intended note directory.

Mitigation: Keep KB_DIR narrowly scoped and commit only files under that configured directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zerone0x/skills/link-digest)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries, Discord thread messages, knowledge-base entries, and git commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Discord summaries are intended to stay under 500 characters; knowledge-base writes should contain synthesized notes only.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
