## Description:

Creates, edits, simulates, and shares isometric city maps for PowPow City / IsoCity, including maps based on OpenStreetMap data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[durenzidu](https://clawhub.ai/user/durenzidu)

### License/Terms of Use:

MIT-0

## Use Case:

Players and developers use this skill to build or edit playable city maps, generate maps from real-world locations, preview or simulate cities, and share results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: City editing commands change files in the working directory.

Mitigation: Review the target path before editing and retain the generated .bak backups for recovery.

Risk: Short-link sharing uploads a city snapshot; gallery sharing publicly lists it.

Mitigation: Review the snapshot before sharing and use --gallery only when public listing is intended.

Risk: Optional screenshot and simulation setup can vary with the installed Playwright version.

Mitigation: Pin Playwright when reproducible setup is important.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/durenzidu/skills/powpowcity-map-editor)
- [PowPow City browser game](https://powpowcity.powpow.online/)

## Skill Output:

**Output Type(s):** [Text, JSON files, PNG screenshots, Share links]

**Output Format:** [CLI text, .isocity.json city files, optional PNG images and browser URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Screenshots and simulations require access to the game and optional Playwright setup.]

## Skill Version(s):

1.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
