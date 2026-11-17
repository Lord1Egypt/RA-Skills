## Description:

Audit local HTML labels, alt text, duplicate IDs and heading order, and calculate explicit colour-pair contrast.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hznetnewpower](https://clawhub.ai/user/hznetnewpower)

### License/Terms of Use:

MIT No Attribution

## Use Case:

Developers and UI teams use this skill to check selected local HTML for common labeling, image alternative, duplicate ID, and heading-order issues, and to calculate contrast for explicit foreground and background colour pairs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Static checks cannot assess keyboard navigation, focus, dynamic states, screen-reader behavior, responsive layout, or rendered contrast.

Mitigation: Follow the audit with browser-based checks of those behaviors and assistive-technology testing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hznetnewpower/skills/mochi-ui-accessibility)
- [MochiLab homepage](https://mochilab.bz)
- [input.md](references/input.md)

## Skill Output:

**Output Type(s):** [Analysis, Files]

**Output Format:** [JSON audit data and an HTML report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports are saved under exports/ in the active workspace. Checks cover static HTML and explicitly supplied opaque colour pairs.]

## Skill Version(s):

1.0.1 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
