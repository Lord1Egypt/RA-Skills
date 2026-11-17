## Description:

Manage Threads accounts, OAuth connect URLs, drafts, and publishing through the local threadsctl CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dladislav201](https://clawhub.ai/user/dladislav201)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to manage Threads accounts, create OAuth connection URLs, prepare or approve drafts, inspect stats, and publish text, image, carousel, or spoiler media posts through threadsctl.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An agent could publish content immediately to a public Threads account when the user intended review first.

Mitigation: Use draft-first workflows unless the user clearly asks to post now, and verify the account and content before using --confirmed.

Risk: OAuth connection URLs and configured Threads service credentials can affect account access.

Mitigation: Install only for environments that should manage Threads accounts, keep THREADS_SERVICE_API_KEY protected, and share connection URLs only with the intended account owner.

Risk: Media posts can use the wrong source type or spoiler behavior.

Mitigation: Use local files only with --file or --files, public URLs only with --media-url or --media-urls, and apply --spoiler only when the user asks for media to be hidden.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dladislav201/skills/openclaw-threadsctl)
- [ClawHub source listing](https://clawhub.ai/dladislav201/openclaw-threadsctl)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and concise status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include account labels, draft IDs, publish results, OAuth connect URLs, and error summaries when relevant.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
