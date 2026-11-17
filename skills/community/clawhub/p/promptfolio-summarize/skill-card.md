## Description:

Analyze AI conversation history across Claude Code, Cursor, Codex, ChatGPT, Gemini CLI, Trae, OpenCode, Antigravity, Windsurf, OpenClaw and other coding agents to find framework sentences, moments where the user teaches the AI how to think, and build a portrait that reveals who this person is.

This skill is ready for commercial/non-commercial use.

## Publisher:

[billc8128](https://clawhub.ai/user/billc8128)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to analyze local AI coding-agent conversations, extract framework sentences and activity patterns, generate profile JSON, review the portrait, and sync a draft to Promptfolio after confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill inspects private AI chat histories and creates a public-profile draft from behavioral and conversation-derived data.

Mitigation: Review the detected sources, generated portrait, and complete payload before approving sync; remove confidential projects, company names, or unwanted sessions before upload.

Risk: The skill runs an external updater and can send structured results to a configured API host.

Mitigation: Verify the updater, authentication script, API URL, and upload destination before running the workflow, especially when PROMPTFOLIO_API_URL or local config changes are present.

Risk: The workflow stores local profile artifacts and an API token under user-writable locations.

Mitigation: Protect or delete generated _pf_parts files and promptfolio_payload.json after use, and rotate the Promptfolio token if local files may have been exposed.

Risk: Broad session discovery can include conversation history beyond the user's intended sources.

Mitigation: Restrict PF_SOURCES, inspect SESSION_LIST, and exclude unwanted exported files before computing statistics or generating the portrait.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown review text, JSON profile artifacts, and shell command workflows]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local _pf_parts JSON files, a promptfolio_payload.json sync payload, and a reviewed profile draft.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
