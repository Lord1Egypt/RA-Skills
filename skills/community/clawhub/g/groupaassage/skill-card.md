## Description:

Generates a Chinese daily-report HTML template specification with dark-theme defaults, a three-column masonry layout, light/dark theme switching, and content-splitting guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jfzerozhuo](https://clawhub.ai/user/jfzerozhuo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content teams use this skill to generate consistent Chinese daily-report HTML with theme support, masonry section layout, and practical rules for splitting long report sections.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports may include theme-sync postMessage code that accepts messages from embedded or cross-origin pages.

Mitigation: When embedding reports with untrusted pages or serving across origins, check message origin and source and allow only light or dark theme values.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jfzerozhuo/skills/groupaassage)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Configuration]

**Output Format:** [Markdown guidance with HTML, CSS, and JavaScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces template requirements for generated daily-report HTML, including theme variables, layout rules, and content-splitting thresholds.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
