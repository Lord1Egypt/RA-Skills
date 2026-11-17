## Description:

Guides agents using the Kleos CLI to create, review, schedule, and measure TikTok and Instagram posts, upload media, and connect accounts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rhuancruz](https://clawhub.ai/user/rhuancruz)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and their operators use this skill to manage Kleos social content for apps, including drafting and reviewing posts, uploading media, scheduling approved posts, connecting accounts, and reporting performance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running an unpinned CLI can introduce unreviewed changes.

Mitigation: Use a pinned, reviewed Kleos CLI version or a preinstalled binary.

Risk: Broad API keys and generic tool calls can grant access beyond the intended content task.

Mitigation: Use least-privilege keys and avoid unattended runs with broad account scopes.

Risk: Publishing, scheduling, spending, account connections, or team changes can affect live accounts.

Mitigation: Require explicit user approval before these actions and generic `kleos call` operations.

## Reference(s):

- [Kleos CLI skill release](https://clawhub.ai/rhuancruz/skills/kleos-cli)
- [Kleos tool documentation](https://ugc.zurc.app/llms-full.txt)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Text]

**Output Format:** [Markdown with shell commands and result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include post URLs, media IDs, and metrics returned by Kleos.]

## Skill Version(s):

0.2.0 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
