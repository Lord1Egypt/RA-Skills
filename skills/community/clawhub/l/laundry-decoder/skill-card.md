## Description:

Decode laundry care symbols from text descriptions (tub, triangle, iron, circle, square shapes with dots/bars), build a safe wash plan for a mixed load (color bleeding risk, temperature ceilings, fabric conflicts), and give evidence-based stain removal protocols by stain type. Use when the user asks what a care label means, whether clothes can be washed together, what temperature is safe, or how to remove a specific stain without ruining the fabric.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

External users and agents use this skill to interpret laundry care labels from text descriptions, plan safe mixed laundry loads, and produce stain-removal guidance for common fabrics and stains.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Laundry, stain, and fabric guidance can be wrong for specialty materials, leather, suede, structured garments, or professional dry-cleaning chemical handling.

Mitigation: Treat outputs as household guidance, verify garment labels and hidden areas before treatment, and use professional cleaners for specialty materials or chemical dry-cleaning decisions.

Risk: User-supplied garment descriptions may omit constraints such as trims, dyes, finishes, or fabric blends that affect safe washing and stain treatment.

Mitigation: Ask for missing care-label details and choose the least aggressive treatment first, especially for delicates, wool, silk, and new or dark garments.

## Reference(s):

- [Laundry Science & Practice Reference](references/care-and-stains.md)
- [ClawHub skill page](https://clawhub.ai/voronindenis5/skills/laundry-decoder)
- [Publisher profile](https://clawhub.ai/user/voronindenis5)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, JSON, Guidance]

**Output Format:** [Markdown or plain text guidance, with optional JSON from the load planner]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Offline stdlib-only Python tool; no credentials or network access required.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
