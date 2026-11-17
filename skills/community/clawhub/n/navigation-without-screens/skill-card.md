## Description:

Provides physical navigation guidance for map reading, compass use, natural navigation, and navigating when technology fails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[howtousehumans](https://clawhub.ai/user/howtousehumans)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to learn screen-free navigation, including reading physical maps, orienting with a compass, using terrain and landmarks, and responding when lost. It is especially relevant for hiking, travel, education, and backup planning when digital navigation is unavailable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence flags an unpinned npx installer that could execute changing upstream code.

Mitigation: Review the install command before use, prefer a pinned or trusted installer path, and avoid elevated privileges.

Risk: The release evidence says the skill asks for unnecessary filesystem access.

Mitigation: Grant filesystem access only when needed and limit it to a narrow workspace when the platform supports scoped permissions.

Risk: Navigation and emergency guidance can be consequential if a user is lost or in danger.

Mitigation: Do not rely on the skill as a substitute for local emergency services, official maps, practical training, or search-and-rescue guidance.

## Reference(s):

- [Navigation Without Screens on ClawHub](https://clawhub.ai/howtousehumans/skills/navigation-without-screens)
- [USGS Topographic Maps](https://www.usgs.gov/programs/national-geospatial-program/topographic-maps)
- [Ordnance Survey Map Reading](https://www.ordnancesurvey.co.uk/map-reading)
- [NOAA Magnetic Declination Calculator](https://www.ngdc.noaa.gov/geomag/calculators/magcalc.shtml)
- [National Outdoor Leadership School](https://www.nols.edu/)
- [Wilderness Education Association](https://www.weainfo.org/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown guidance with structured steps and code-fenced examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May ask for the user's location to localize magnetic declination, map systems, emergency numbers, and hemisphere-specific natural navigation guidance.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
