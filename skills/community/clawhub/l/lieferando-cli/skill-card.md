## Description:

Read-only German food-delivery discovery for Lieferando and Uber Eats: search restaurants near an address, inspect menus, item option groups, prices, delivery fees, ETA, and opening state, with JSON envelope output and no login, ordering, or payment support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[karimqpn](https://clawhub.ai/user/karimqpn)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to compare food-delivery options in Germany, inspect restaurant menus, resolve item options, and estimate local cart totals before the user orders through the provider's own app or website.

### Deployment Geography for Use:

Germany

## Known Risks and Mitigations:

Risk: Searched addresses and coordinates may be sent to OSM for geocoding and retained in a plaintext local cache.

Mitigation: Prefer postcodes or coordinates instead of full home or work addresses when possible, and remove the local cache if location history should not be retained.

Risk: Some provider endpoints may rate-limit or block requests, especially Uber Eats item-detail lookups.

Mitigation: Back off on rate-limit or block errors, avoid repeated retries, and continue only with lower-risk commands such as search, restaurant, or menu when appropriate.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/karimqpn/skills/lieferando-cli)
- [Skill homepage](https://clawhub.ai/skills/lieferando-cli)
- [OpenStreetMap Nominatim search endpoint](https://nominatim.openstreetmap.org/search)
- [Just Eat discovery API base](https://i18n.api.just-eat.io)
- [Just Eat menu CDN base](https://globalmenucdn.eu-central-1.production.jet-external.com)
- [Uber Eats API base](https://www.ubereats.com/api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with shell commands that return JSON envelopes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Command output uses a JSON envelope with meta, data, warnings, and optional error fields; prices are integer euro cents.]

## Skill Version(s):

0.2.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
