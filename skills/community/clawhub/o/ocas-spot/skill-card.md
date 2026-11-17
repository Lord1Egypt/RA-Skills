## Description:

Spot helps agents check appointment and reservation availability, book services, monitor openings, and discover venues across supported salon, spa, and restaurant platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[indigokarasu](https://clawhub.ai/user/indigokarasu)

### License/Terms of Use:

MIT

## Use Case:

External users and agents use Spot to find available appointment or reservation slots, complete supported booking flows, and monitor venues for newly opened times. It is aimed at service venues such as salons, spas, and restaurants across the booking platforms documented by the skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can store account/session data and booking contact details.

Mitigation: Prefer manual OAuth or login flows over sharing raw passwords, restrict data directory access, and review stored session and contact files before deployment.

Risk: The skill can run scheduled monitoring and modify local booking, venue, watchlist, audit, and journal files.

Mitigation: Run it in a contained workspace, review cron or scheduled sweep configuration, and monitor generated JSONL and journal records for unexpected changes.

Risk: The skill includes browser automation, CDP/VNC-style host controls, and VPN routing for bot-blocked platforms.

Mitigation: Keep CDP and VNC endpoints bound to localhost, run VPN and browser components in an isolated environment, and verify that automation complies with venue and platform terms.

Risk: The skill includes a self-update command that can pull and replace package files.

Mitigation: Disable or avoid spot.update unless updates are reviewed, pinned, and scanned before installation.

## Reference(s):

- [Spot ClawHub skill page](https://clawhub.ai/indigokarasu/skills/ocas-spot)
- [Booking workflow](references/booking-workflow.md)
- [Platform decision tree](references/platforms/README.md)
- [Platform access matrix](references/platform-access-matrix.md)
- [Storage layout](references/storage-layout.md)
- [Journal schema](references/journal-schema.md)
- [VPN integration](references/vpn-integration.md)
- [Self-update procedure](references/self-update.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command invocations and JSONL record outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write booking, venue, watchlist, audit, journal, and session records under the agent data directories described by the skill.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter and changelog report 2.7.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
