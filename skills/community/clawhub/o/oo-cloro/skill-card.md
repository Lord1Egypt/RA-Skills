## Description:

Use this skill to read, create, update, and delete Cloro data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use Cloro to run search and AI monitoring actions, check task status and credits, and manage queued work through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The required oo CLI may change other assistants’ installed skills, a behavior this skill does not explain.

Mitigation: Use a reviewed CLI release and check its documented effects; set OO_SKILLS_SYNC_DISABLED=1 before invoking the CLI if cross-assistant skill syncing is unwanted.

Risk: The exact remote installer is unverified, and Cloro actions can incur costs or delete queued tasks.

Mitigation: Review the CLI before installation, confirm the connected Cloro organization and expected costs, and verify the deletion target before running clear_queue.

Risk: Write and destructive actions can change or remove Cloro data.

Mitigation: Review the exact payload and effect, then obtain user confirmation before running write or destructive actions.

## Reference(s):

- [Cloro homepage](https://cloro.dev)
- [Cloro API documentation](https://cloro.dev/docs)
- [oo CLI command documentation](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [Cloro release page](https://clawhub.ai/oomol/skills/oo-cloro)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [oo CLI commands with JSON payloads and JSON action results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action schemas are checked before requests; writes and destructive actions require user confirmation.]

## Skill Version(s):

1.0.2 (source: frontmatter metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
