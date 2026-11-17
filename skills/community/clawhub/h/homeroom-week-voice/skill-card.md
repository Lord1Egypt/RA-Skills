## Description:

Turn a written homeroom week plan into one homeroom week voice clip per labeled cue, delivering 8 to 20 forwardable class notice audio files from the teacher's supplied plan.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External educators and teachers use this skill to convert an already-written homeroom week plan into labeled, forwardable voice clips. The agent plans the clip slots, confirms any paid clone or speech steps, and delivers audio artifacts without inventing schedule content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan marked the release suspicious because it uses broad shared account access and automatic updates for executable package code.

Mitigation: Install only if the user trusts Beatra, keep the device credential private under ~/.beatra, and consider disabling automatic updates with `python3 scripts/mcp_client.py update --auto off` before routine use.

Risk: Paid clone and speech requests can create charges or duplicate work if retried with changed inputs.

Mitigation: Use one opaque `client_request_id` per paid request, retry only byte-identical uncertain submissions with the same request identity, and read the terminal billing fields before reporting charges.

Risk: Teacher voice cloning can misuse a likeness when file access is treated as consent.

Mitigation: Require explicit likeness and voice rights before cloning, inspect only authorized samples, and skip cloning unless the teacher confirms the sample is allowed.

## Reference(s):

- [Homeroom week voice workflow](references/workflow.md)
- [Installation and authentication](references/installation-and-auth.md)
- [Installation registration](references/installation-registration.md)
- [Tasks and results](references/tasks-and-results.md)
- [Billing, errors, and recovery](references/billing-errors-and-recovery.md)
- [MCP connection](references/mcp-connection.md)
- [Automatic updates and safety](references/automatic-updates-and-safety.md)
- [Uninstall and disconnect](references/uninstall-and-disconnect.md)
- [ClawHub skill page](https://clawhub.ai/beatra-ai/skills/homeroom-week-voice)
- [Beatra skill homepage](https://beatra.ai/skills/homeroom-week-voice)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Files, Guidance]

**Output Format:** [Markdown guidance with JSON payloads and Beatra task outputs; final artifacts are MP3 audio files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces 8 to 20 labeled homeroom clips; optionally creates a cloned voice when the teacher confirms voice rights.]

## Skill Version(s):

0.1.2 (source: server release metadata and package manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
