## Description:

Time awareness for sovereign entities — manage availability, book meetings, negotiate schedules over Nostr relays.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vveerrgg](https://clawhub.ai/user/vveerrgg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to give agents Nostr-based scheduling capabilities, including publishing availability, checking free slots, booking meetings, and negotiating meeting times over relays.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Nostr private key that can sign events for the entity.

Mitigation: Use a dedicated key, keep unrelated secrets out of the same runtime, and store NOSTR_NSEC only in an approved secret store or environment.

Risk: Installed code can publish availability, booking requests, and meeting negotiations to Nostr relays.

Mitigation: Require explicit operator approval before an agent publishes, books, accepts, declines, cancels, or negotiates meetings.

Risk: The install path can fetch unpinned package versions.

Mitigation: Pin and review package versions before deployment, including the nostrcalendar package and its nostrkey dependency.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vveerrgg/skills/nostrcalendar)
- [Project homepage from ClawHub metadata](https://github.com/HumanjavaEnterprises/nostrcalendar.app.OC-python.src)
- [PyPI package](https://pypi.org/project/nostrcalendar/)
- [Nostr NIP-52 calendar events](https://github.com/nostr-protocol/nips/blob/master/52.md)
- [NostrKey prerequisite skill](https://clawhub.ai/vveerrgg/nostrkey)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with Python examples, install commands, environment variables, and usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Nostr private key in NOSTR_NSEC and can publish signed scheduling events to the configured relay.]

## Skill Version(s):

0.2.3 (source: frontmatter, artifact metadata, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
