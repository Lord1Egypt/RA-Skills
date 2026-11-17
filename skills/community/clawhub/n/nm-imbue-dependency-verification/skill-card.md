## Description:

Verifies a package exists before install, defending against hallucination and slopsquatting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to check proposed dependencies in their package registries and identify nonexistent or typo-like names before installing or recommending them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reported medium confidence because some local references were unresolved, despite finding no issues in the reviewed skill content.

Mitigation: Review the source and any unresolved local references before relying on the skill.

Risk: A registry lookup can be unavailable, leaving a package unverified.

Mitigation: Keep the result marked unverified and retry the check when the registry is reachable before installing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-imbue-dependency-verification)
- [Project homepage](https://github.com/athola/claude-night-market/tree/master/plugins/imbue)

## Skill Output:

**Output Type(s):** [Guidance, Analysis, Shell commands]

**Output Format:** [Markdown guidance with registry check results and evidence]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May report a package as unverified when its registry cannot be reached.]

## Skill Version(s):

1.10.3 (source: frontmatter, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
