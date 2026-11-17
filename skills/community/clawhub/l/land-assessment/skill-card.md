## Description:

Evaluating and purchasing rural or semi-rural property. Use when someone is considering buying land, wants to homestead, is evaluating a property for food production potential, or needs to understand what to look for in rural real estate.

This skill is ready for commercial/non-commercial use.

## Publisher:

[howtousehumans](https://clawhub.ai/user/howtousehumans)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to evaluate rural or semi-rural property before purchase, with emphasis on water, soil and septic feasibility, access, zoning, flood risk, utilities, and full ownership costs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests filesystem access even though the available behavior is advisory guidance.

Mitigation: Remove the filesystem requirement unless a specific file feature is added, and avoid granting broad local file access during installation or use.

Risk: The install path uses an unpinned npx command, which can change across installations.

Mitigation: Pin or integrity-protect the install target and review the package before installing, especially in commercial environments.

## Reference(s):

- [USDA Web Soil Survey](https://websoilsurvey.nrcs.usda.gov/)
- [FEMA Flood Maps](https://msc.fema.gov/)
- [EPA Brownfields Program](https://www.epa.gov/brownfields)
- [USDA Plant Hardiness Zone Map](https://planthardiness.ars.usda.gov/)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Text]

**Output Format:** [Markdown checklists and advisory guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include jurisdiction-specific prompts and due diligence checklists.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
