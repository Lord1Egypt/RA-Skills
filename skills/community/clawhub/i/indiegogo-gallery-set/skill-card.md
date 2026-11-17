## Description:

Turn a written campaign and reward-tier plan into one gallery still per named slot.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and campaign teams use this skill to plan crowdfunding gallery stills from already-approved campaign and reward-tier text, then generate one Beatra image per named slot after confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package uses a shared, broad Beatra device token.

Mitigation: Review the Beatra authorization page and scopes before approval, keep the token only in the documented local credential file, and revoke the device in the Beatra Console when access is no longer trusted.

Risk: Executable package files can silently self-update by default.

Mitigation: Disable automatic updates with the documented `python3 scripts/mcp_client.py update --auto off` command when review-before-update is required, and use `update --check` to inspect available updates.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/beatra-ai/skills/indiegogo-gallery-set)
- [Beatra skill homepage](https://beatra.ai/skills/indiegogo-gallery-set)
- [Crowdfunding gallery workflow](references/workflow.md)
- [Installation and authentication](references/installation-and-auth.md)
- [Billing, errors, and recovery](references/billing-errors-and-recovery.md)
- [Tasks and results](references/tasks-and-results.md)
- [Automatic updates and safety](references/automatic-updates-and-safety.md)
- [Uninstall and disconnect](references/uninstall-and-disconnect.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Image artifacts]

**Output Format:** [Markdown guidance with JSON payloads, shell commands, task metadata, and generated image artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a labeled gallery plan before paid generation; billable image output is one still per named slot.]

## Skill Version(s):

0.1.2 (source: server release evidence and manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
