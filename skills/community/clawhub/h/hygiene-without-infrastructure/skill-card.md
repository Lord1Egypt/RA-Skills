## Description:

Maintaining hygiene and sanitation when normal infrastructure fails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[howtousehumans](https://clawhub.ai/user/howtousehumans)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to provide practical hygiene, water treatment, sanitation, food safety, and field-cleanliness guidance during water outages, sewer backups, power outages, camping, or other situations where normal plumbing is unavailable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence flags the install metadata as suspicious because it uses an unpinned npx installer whose executed code can change after review.

Mitigation: Review or replace the install command before installation; prefer a pinned and verified ClawHub CLI version or a trusted local installer, and install with minimal privileges and no unrelated secrets in the environment.

Risk: The skill gives emergency sanitation, water treatment, food safety, and wound-hygiene guidance that may need local adaptation.

Mitigation: Ask for the user's location and situation when relevant, prefer authoritative local emergency instructions, and advise checking local rules for human waste disposal, greywater use, and declared-emergency sanitation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/howtousehumans/skills/hygiene-without-infrastructure)
- [CDC Emergency Water Disinfection](https://www.cdc.gov/healthywater/drinking/travel/emergency_disinfection.html)
- [WHO Water, Sanitation and Health](https://www.who.int/teams/environment-climate-change-and-health/water-sanitation-and-health)
- [EPA Emergency Disinfection of Drinking Water](https://www.epa.gov/ground-water-and-drinking-water/emergency-disinfection-drinking-water)
- [Ready.gov Water](https://www.ready.gov/water)
- [American Red Cross](https://www.redcross.org/)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration]

**Output Format:** [Markdown prose with checklists, step-by-step instructions, and structured state guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May adapt recommendations by region for bleach concentration, water quality standards, waste disposal rules, product availability, and emergency contact numbers.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
