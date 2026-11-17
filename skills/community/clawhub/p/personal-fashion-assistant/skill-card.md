## Description:

A personal fashion assistant that builds style profiles, manages a digital wardrobe, checks clothing conflicts, analyzes wardrobe health, and recommends daily outfits.

This skill is for research and development only.

## Publisher:

[yunaiikim](https://clawhub.ai/user/yunaiikim)

### License/Terms of Use:

PolyForm Noncommercial License 1.0.0

## Use Case:

External users use this skill to maintain a personal style profile and digital wardrobe, archive clothing photos, check for similar or conflicting items, generate wardrobe analysis dashboards, and receive weather-aware outfit recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill collects and stores sensitive body, appearance, photo, and routine data.

Mitigation: Use only non-sensitive data and photos, obtain explicit consent before uploads or persistent profile writes, and remove stored data when it is no longer needed.

Risk: The skill may send appearance data and photos to an external model service.

Mitigation: Disclose the external model use before submission, send only data needed for the requested analysis, and avoid uploading sensitive images.

Risk: The skill saves model-generated HTML that should be treated as untrusted.

Mitigation: Inspect and sanitize generated dashboard files before opening or sharing them.

Risk: The skill writes model-derived profile, wardrobe, and statistics updates to local files.

Mitigation: Review generated updates before accepting them and keep backups of profile and inventory files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yunaiikim/skills/personal-fashion-assistant)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown responses plus local Markdown, image, and HTML files for profile, wardrobe, recommendation, and dashboard workflows]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update USER.md and inventory.md, archive wardrobe photos, and save model-generated HTML dashboard files.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
