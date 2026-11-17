## Description:

Drive Herdr terminal multiplexer panes from Telegram: spawn a dedicated tab, send prompts to any CLI agent, wait for done/blocked, and relay transcripts back.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mentholmike](https://clawhub.ai/user/mentholmike)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to drive persistent CLI-agent sessions in Herdr from Telegram, including spawning panes, submitting prompts, relaying progress, handling blocked states, and returning transcript tails.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Terminal content can be exposed externally through the Telegram chat.

Mitigation: Avoid sending secrets through this workflow, review pane output before forwarding it, and relay only panes intentionally controlled by the skill.

Risk: Untrusted Telegram text can become unsafe command input if implementations interpolate chat text into shell command strings.

Mitigation: Implement command execution with shell-free argv/stdin handling and treat Telegram messages as untrusted input.

Risk: The workflow can disrupt unrelated terminal sessions if it targets panes, tabs, or workspaces it did not create.

Mitigation: Drive only panes and tabs spawned by the skill unless the user explicitly names a pane ID, parse opaque IDs from JSON responses, and do not close unrelated Herdr resources.

## Reference(s):

- [Herdr](https://github.com/mentholmike/herdr)
- [ClawHub skill page](https://clawhub.ai/mentholmike/skills/herder-telegram)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline bash command examples and fenced terminal transcript excerpts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Telegram relay output should be chunked for 4096-character message limits; terminal output is relayed as text in fenced code blocks.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
