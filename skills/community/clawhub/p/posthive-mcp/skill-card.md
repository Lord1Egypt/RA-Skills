## Description:

Schedule social media posts to 13 platforms through the Posthive CLI for creating, scheduling, listing, updating, deleting, and managing a posting queue.

This skill is ready for commercial/non-commercial use.

## Publisher:

[astablackclove](https://clawhub.ai/user/astablackclove)

### License/Terms of Use:

MIT-0

## Use Case:

External users and social media operators use this skill to manage Posthive posting workflows through CLI commands, including drafts, scheduling, updates, deletion, templates, media upload, and queue inspection across connected accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Runtime package fetching or unpinned CLI installation can expose users to dependency supply-chain changes.

Mitigation: Prefer a trusted, pinned, or locked Posthive CLI version before installation or execution.

Risk: The skill uses Posthive credentials and connected social accounts, so incorrect commands could create, schedule, update, or delete social posts.

Mitigation: Keep the draft-first workflow, confirm account IDs and user intent before scheduling or deletion, and use direct scheduling only when explicitly requested.

Risk: Scheduled timestamps may publish at an unintended time if the user's timezone is assumed incorrectly.

Mitigation: Confirm the user's timezone and use ISO 8601 UTC timestamps for scheduling commands.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/AstaBlackClove/posthive/tree/main/apps/cli/skills/posthive)
- [ClawHub skill page](https://clawhub.ai/astablackclove/skills/posthive-mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and structured JSON command-output expectations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Posthive CLI commands are expected to emit structured JSON, and error cases emit a JSON object on stdout.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
