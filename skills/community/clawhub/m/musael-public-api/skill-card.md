## Description:

Integrates Musael's public seeded name-generator endpoint. Use when a task needs repeatable names for a supported generator kind.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lucernel](https://clawhub.ai/user/lucernel)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents can generate bounded lists of names for supported fantasy, place, character, and science-fiction categories. The kind and seed are retained so a list can be reproduced for the same generator release.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review was partial because a referenced local path could not be matched to the supplied artifact, so the behavior of that reference remains unverified.

Mitigation: Review the referenced path and its behavior before execution; the benign verdict does not resolve the missing evidence.

## Reference(s):

- [Musael endpoint reference](references/musael.md)
- [Musael public names API](https://musael.com/api/public/v1/names)
- [Musael fantasy name generator](https://musael.com/tools/fantasy-name-generator)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [A list of generated names with generator kind, seed, and source metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Count is limited to 1–20; results are reproducible for a given generator release and are suggestions, not claims of name availability.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
