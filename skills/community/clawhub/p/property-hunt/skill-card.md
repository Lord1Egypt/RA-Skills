## Description:

Track houses for sale on a private map by saving listing details, user notes, ratings, status, photos, and map pins in the user's local Plow properties folder.

This skill is ready for commercial/non-commercial use.

## Publisher:

[srosro](https://clawhub.ai/user/srosro)

### License/Terms of Use:

MIT-0

## Use Case:

External users house hunting with Plow use this skill to add, refresh, review, annotate, and remove saved property listings. It produces a private local property map and a local store of saved listing facts, photos, ratings, notes, and statuses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can open user-supplied listing URLs in Plow Browser, and the security evidence flags missing local and private-network destination blocking for browser navigation.

Mitigation: Use trusted public listing URLs, avoid unknown or shortened links, and review browser navigation behavior before deployment.

Risk: The skill writes a local property map and saved property data under the user's Plow properties folder.

Mitigation: Review generated local files before sharing or syncing the folder, especially because notes, ratings, listing details, and photos may reveal house-hunting preferences.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/srosro/skills/property-hunt)
- [Plow private preview](https://plow.co/private-preview)
- [Leaflet](https://leafletjs.com)
- [Nominatim](https://nominatim.org)
- [OpenStreetMap copyright and license](https://www.openstreetmap.org/copyright)
- [Frontend map template](references/frontend/index.html)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Plain text guidance with shell commands; local JSON-backed data.js, HTML map, and image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local property data, photos, and a browser-openable map under the user's Plow properties folder.]

## Skill Version(s):

0.1.3 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
