## Description:

Find, verify, and reserve parking worldwide with provider selection, live-signal triage, and local memory for favorite places and cities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to find nearby parking, compare reservation and payment providers, pre-book airport or event parking, and preserve approved local parking preferences for recurring trips. Developers and operators can also use it for parking platform and API research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may save local parking notes such as favorite garages, home-city patterns, and vehicle constraints.

Mitigation: Use one-off mode or decline memory creation when you do not want local parking notes saved.

Risk: Live provider handoff can disclose destination, time window, route context, plate, or vehicle details to parking, map, or city-data services.

Mitigation: Approve live provider handoff only for services you trust and only when the requested data is needed for the parking task.

Risk: Static listings, payment apps, and discovery surfaces can be mistaken for guaranteed parking inventory.

Mitigation: Treat availability as guaranteed only when a provider exposes reservation inventory or confirmed booking status.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/skills/parking)
- [Provider Registry](artifact/provider-registry.md)
- [City Patterns](artifact/city-patterns.md)
- [Execution Playbook](artifact/execution-playbook.md)
- [API Notes](artifact/api-notes.md)
- [Source Ledger](artifact/source-ledger.md)
- [Parkopedia](https://www.parkopedia.com)
- [SpotHero](https://spothero.com)
- [ParkWhiz API](https://api.parkwhiz.com)
- [Hong Kong Parking Vacancy API](https://api.data.gov.hk)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown guidance with provider links, comparison notes, verification status, and optional local memory instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include provider handoff recommendations and concise local note updates when the user approves memory]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
