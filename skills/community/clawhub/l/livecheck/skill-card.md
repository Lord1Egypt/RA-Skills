## Description:

Checks specific job and product URLs for current availability, with optional condition checks, watchers, and post-submission confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moyecj-snap](https://clawhub.ai/user/moyecj-snap)

### License/Terms of Use:

MIT-0

## Use Case:

Job seekers, shopping assistants, and developers use this skill to check whether specific job postings or product listings are still available before applying, contacting someone, or recommending a purchase. Optional checks monitor changes or confirm a completed form or order.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Checking a link sends its URL to an external service.

Mitigation: Share only URLs the user approves sending to livecheck.fly.dev.

Risk: Paid checks and watchers can consume wallet funds, particularly across large batches.

Mitigation: Confirm expected charges before batches or watchers and limit requests to the needed URLs.

Risk: Blocked or JavaScript-only pages may not yield a reliable availability result.

Mitigation: Report unknown results as uncertain; do not treat them as confirmed live or closed.

## Reference(s):

- [Livecheck release on ClawHub](https://clawhub.ai/moyecj-snap/skills/livecheck)
- [Getting started](artifact/rules/getting-started.md)

## Skill Output:

**Output Type(s):** [Text, Guidance, Shell commands]

**Output Format:** [Markdown status summaries and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Availability is reported as live, closed, or unknown, with page title and supporting signals where available.]

## Skill Version(s):

4.1.1 (source: server-resolved release and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
