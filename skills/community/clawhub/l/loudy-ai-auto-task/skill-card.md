## Description:

Helps agents query Loudy.ai earning pools, submit user-provided task links, and track review and payment status through Loudy.ai API calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sfsf332](https://clawhub.ai/user/sfsf332)

### License/Terms of Use:

MIT

## Use Case:

External users and agent operators use this skill to manage Loudy.ai task workflows: list active earning pools, submit manually created X/Twitter task links, and check audit or payment status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Loudy.ai API key and sends task links plus status requests to Loudy.ai.

Mitigation: Use a scoped key where possible, provide it through LOUDY_API_KEY, and install only when this data sharing is acceptable.

Risk: The provided installer fetches mutable remote code and may target root or system-wide install paths.

Mitigation: Avoid curl-to-bash and root or system-wide installation; prefer an immutable reviewed package or pinned artifact.

Risk: The optional cron job repeatedly runs task checks and writes local task status files.

Mitigation: Enable cron only with least-privilege filesystem access, cleanup, locking, and reviewed workspace paths.

Risk: The skill steers users toward a separate Binance/X posting skill.

Mitigation: Review that separate component independently before installing or using it.

## Reference(s):

- [Loudy.ai API Reference](references/api.md)
- [ClawHub Skill Page](https://clawhub.ai/sfsf332/skills/loudy-ai-auto-task)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command examples and JSON/API response summaries from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires LOUDY_API_KEY; optional cron behavior writes Loudy.ai task status files in the configured workspace.]

## Skill Version(s):

1.1.0 (source: server release metadata; artifact/package.json reports 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
