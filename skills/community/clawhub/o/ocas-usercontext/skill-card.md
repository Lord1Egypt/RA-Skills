## Description:

Maintains a compact Daily Context block in the owner's USER.md with evidence-grounded mood, location, week theme, and yesterday/today/tomorrow bullets from available calendar, session, email, messaging, and memory signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[indigokarasu](https://clawhub.ai/user/indigokarasu)

### License/Terms of Use:

MIT

## Use Case:

External users or operators of a Hermes-style agent profile use this skill to refresh a daily personal context snapshot in USER.md. It is intended for status snapshots and scheduled recovery of the Daily Context block, not weather, advice, long-term planning, or unrestricted personal data collection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read reachable private communications, calendars, session history, email, and memory sources.

Mitigation: Install only in a private, controlled profile and configure an explicit source allowlist before enabling scheduled runs.

Risk: The skill writes a recurring Daily Context summary into USER.md, which future sessions load as persistent context.

Mitigation: Back up USER.md before installation and validate that each run replaces only the Daily Context block.

Risk: The artifact includes account-specific calendar fallback details, hardcoded account paths, and a plaintext sample schedule.

Mitigation: Remove the packaged new_context.md sample and replace all hardcoded accounts, calendars, paths, and fallback details with deployment-specific values.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/indigokarasu/skills/ocas-usercontext)
- [Data Sources](references/data-sources.md)
- [Installation & Instantiation](references/install.md)
- [Cron-Mode Calendar Access](references/cron-calendar-access.md)
- [Mood Inference](references/mood-inference.md)
- [Validation Checklist](references/validation.md)
- [Constraints and Design Rationale](references/constraints.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown block written into USER.md, with supporting shell commands or configuration guidance when installing or recovering the scheduled job]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Daily Context block should remain under the configured USER.md size cap, target under 300 words, and avoid quoting private messages or email text.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter metadata.version is 3.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
