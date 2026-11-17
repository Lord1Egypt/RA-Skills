## Description:

Generates Chinese and English name ideas for babies, brands, pen names, usernames, and related naming use cases with short meaning notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to produce candidate baby, English, brand, pen, and username ideas, then refine them based on meaning, style, pronunciation, and availability considerations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package includes an under-disclosed generic utility that persistently stores and logs user-provided text on disk.

Mitigation: Avoid passing private names, business plans, or sensitive text to scripts/script.sh; prefer scripts/name.sh for the advertised naming functions and review the package before installing.

Risk: Generated names and meanings may be incomplete, culturally inappropriate, or unavailable for trademark, domain, or social media use.

Mitigation: Review generated names for pronunciation, meaning, negative associations, trademark conflicts, domain availability, and cross-platform availability before adoption.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ckchzh/skills/name-generator)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Terminal text or Markdown containing generated name lists, meaning notes, and naming guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Name suggestions can vary between runs; some utility commands may write user-provided text to local plaintext logs.]

## Skill Version(s):

2.0.0 (source: server release and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
