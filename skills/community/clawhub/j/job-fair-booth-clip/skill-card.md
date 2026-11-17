## Description:

Turn authorized stills and already-written job-fair role notes into one booth talking clip per still.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Recruiting teams and their agents use this skill to turn authorized still images and already-written job-fair role notes into short booth talking clips. It plans each clip before paid work, then can run Beatra speech, optional voice clone, and image-to-video tasks to produce separate 2 to 15 second clips.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package receives broad Beatra account authority, including spending and task-control permissions.

Mitigation: Review the Beatra approval screen before connecting, consider using a dedicated account or budget limit, and monitor wallet and ledger activity.

Risk: Billable clone, speech, and video tasks can spend credits if approved and submitted.

Mitigation: Use the skill's six-field approval cards, live model pricing checks, unique client request IDs, and task polling before starting paid stages.

Risk: Automatic package updates are enabled by default and can change package code without a separate confirmation.

Mitigation: Disable automatic updates with `python3 scripts/mcp_client.py update --auto off` when package changes should require a manual step.

Risk: The workflow can use faces or cloned voices and therefore depends on valid likeness and voice rights.

Mitigation: Provide only authorized stills and voice samples, and require explicit approval before cloning a voice or animating a person.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/beatra-ai/skills/job-fair-booth-clip)
- [Beatra skill homepage](https://beatra.ai/skills/job-fair-booth-clip)
- [Job-fair booth talking workflow](references/workflow.md)
- [Installation and authentication](references/installation-and-auth.md)
- [Installation registration](references/installation-registration.md)
- [Tasks and results](references/tasks-and-results.md)
- [Billing, errors, and recovery](references/billing-errors-and-recovery.md)
- [MCP connection](references/mcp-connection.md)
- [Automatic updates and safety](references/automatic-updates-and-safety.md)
- [Uninstall and disconnect](references/uninstall-and-disconnect.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON payload examples and shell commands; generated media is delivered as separate Beatra task artifacts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill first produces a free labeled clip plan, then can produce separate short booth talking clip files after user-approved paid tasks.]

## Skill Version(s):

0.1.2 (source: server release metadata and manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
