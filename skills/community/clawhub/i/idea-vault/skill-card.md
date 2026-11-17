## Description:

Save and organize links, notes, and timestamps into a searchable Idea Vault for later retrieval by source, channel, date, or keyword.

This skill is ready for commercial/non-commercial use.

## Publisher:

[loughness](https://clawhub.ai/user/loughness)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to capture YouTube links, web links, note-only ideas, timestamps, and attachments from chat into a persistent local markdown vault, then query or annotate saved entries later.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read recent chat content and write a persistent local vault.

Mitigation: Use it only with content appropriate for local persistence, configure IDEA_VAULT_DIR deliberately, and review saved entries before broad use.

Risk: The skill can make outbound requests to YouTube, TranscriptAPI, and source or asset URLs included in captured messages.

Mitigation: Install only if those network calls are acceptable, keep API keys in environment variables, and restrict or allowlist external origins before broad deployment.

Risk: Security evidence flags unsafe attachment handling, including attachment filename, host, and response-size concerns.

Mitigation: Sanitize attachment filenames, restrict allowed attachment URL hosts, and enforce response-size limits before relying on attachment downloads.

Risk: Security evidence flags under-disclosed channel-monitor behavior.

Mitigation: Document the channel-monitor command and its network behavior clearly, or remove it before broad use.

Risk: The dependency declaration is not pinned to an exact version.

Mitigation: Pin dependencies and review updates before deployment.

## Reference(s):

- [Idea Vault ClawHub release](https://clawhub.ai/loughness/skills/idea-vault)
- [TranscriptAPI endpoint used by the skill](https://transcriptapi.com/api/v2)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown entries, JSON command outputs, and concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes persistent vault files, transcripts, optional downloaded assets, and index.json under the configured vault directory.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
