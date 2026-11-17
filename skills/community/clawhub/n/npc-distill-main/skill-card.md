## Description:

Npc Distill Main helps agents build local, anonymized digital personas from a person's communications so users can rehearse reports, pressure-test plans, draft audience-fit materials, and anticipate decision concerns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bangbangmao666666](https://clawhub.ai/user/bangbangmao666666)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers can use this skill to organize local evidence about a workplace stakeholder, rehearse likely reactions, pressure-test plans, and draft materials tuned to that stakeholder's documented preferences. The skill is intended for private preparation and does not replace real communication or consent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive interpersonal and workplace material in local plaintext files.

Mitigation: Use a dedicated private directory, avoid shared drives and repositories, and enable disk or container encryption when device access is shared.

Risk: URL ingestion can expose internal or private web content to the host agent's fetching tools.

Mitigation: Do not fetch internal or private URLs through the skill; paste only content that is appropriate for the active agent environment.

Risk: Helper commands and dependencies may be unsafe if run with untrusted aliases, IDs, or unpinned packages.

Mitigation: Install dependencies in an isolated environment, pin dependencies where possible, and review commands before execution.

Risk: Retention behavior may leave sensitive records available longer than expected.

Mitigation: Treat deletion as archive/comment-out unless the user explicitly performs secure removal, and periodically clean up obsolete memory files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bangbangmao666666/skills/npc-distill-main)
- [Project homepage](https://github.com/clawhub/npc-distill)
- [Agent skills compatibility](references/agentskills-compat.md)
- [Memory file format](references/memory-format.md)
- [agentskills.io standard](https://agentskills.io)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with optional Python helper commands, diffs, and local memory-file updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local plaintext memory files using anonymized IDs such as L001/L002 and asks users to review diffs before writes.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
