## Description:

Before publishing to ClawHub, validate a skill-shaped folder with required file, frontmatter, size, authentication, slug availability, and dry-run publish checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT

## Use Case:

Developers and skill publishers use this skill to run a repeatable preflight check before publishing a ClawHub skill package. It helps catch missing metadata, oversized files, unavailable slugs, authentication issues, and dry-run publish failures before the real release.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The preflight script invokes an authenticated ClawHub CLI and may submit the selected skill package to ClawHub during dry-run validation.

Mitigation: Run it only against the intended skill folder while authenticated to the correct ClawHub account, and review dry-run output before publishing.

## Reference(s):

- [ingest-preflight resource description](references/DESCRIPTION.md)

## Skill Output:

**Output Type(s):** [Shell commands, Analysis, Guidance]

**Output Format:** [Markdown with shell commands and preflight result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports pass, warning, and failure status; exits 0 when ready to publish, 1 for fixable failures, and 2 for argument errors.]

## Skill Version(s):

1.0.0 (source: SKILL.md metadata and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
