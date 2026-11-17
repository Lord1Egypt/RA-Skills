## Description:

Expert guidance on validating, optimizing, and ensuring quality of Mapbox styles through validation, accessibility checks, and optimization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mapbox](https://clawhub.ai/user/mapbox)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and map engineers use this skill to prepare Mapbox styles for production by validating GeoJSON and expressions, checking accessibility, comparing style versions, and reviewing optimization steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optimization guidance can remove unused sources, duplicate layers, or empty layers when users choose to run those tools.

Mitigation: Review the optimization report and test the optimized style before deploying it.

## Reference(s):

- [Optimization Best Practices](references/optimization.md)
- [Style Comparison Workflow](references/comparison.md)
- [Integration with Development Workflow](references/ci-integration.md)
- [Mapbox Style Specification](https://docs.mapbox.com/mapbox-gl-js/style-spec/)
- [Mapbox Expression Reference](https://docs.mapbox.com/mapbox-gl-js/style-spec/expressions/)
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [GeoJSON Specification (RFC 7946)](https://tools.ietf.org/html/rfc7946)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with code snippets, shell commands, checklists, and tool recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend validation, comparison, and optimization tool calls; users should review optimization results before deployment.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
