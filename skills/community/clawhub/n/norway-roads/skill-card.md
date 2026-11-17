## Description:

Query real-time road conditions, closures, and traffic issues in Norway.

This skill is ready for commercial/non-commercial use.

## Publisher:

[geoffreycasaubon](https://clawhub.ai/user/geoffreycasaubon)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to check Norway road closures, barriers, and route-relevant road condition information from public Statens Vegvesen NVDB data.

### Deployment Geography for Use:

Norway

## Known Risks and Mitigations:

Risk: The skill makes live HTTPS requests to Statens Vegvesen's NVDB API, so availability, latency, and returned road data can vary at runtime.

Mitigation: Confirm time-sensitive travel decisions against official Vegvesen channels when road safety or schedule impact is significant.

Risk: The skill reports registered NVDB closures and barriers and may not include every recent traffic incident.

Mitigation: Use the output as a planning aid and check live traffic sources for urgent or safety-critical trips.

## Reference(s):

- [Norway Roads API Reference](references/api-docs.md)
- [Statens Vegvesen NVDB API](https://nvdbapiles-v3.atlas.vegvesen.no)
- [Norway Roads on ClawHub](https://clawhub.ai/geoffreycasaubon/skills/norway-roads)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, JSON, guidance]

**Output Format:** [Markdown or JSON road condition summaries with optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include live closure counts, locations, counties, municipalities, closure periods, causes, and timestamps from the public NVDB API.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
