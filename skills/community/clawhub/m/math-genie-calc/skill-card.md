## Description:

math_genie_calc is a scientific calculation skill that helps agents perform basic arithmetic, trigonometric functions, logarithms, square roots, powers, inverse trigonometric functions, and factorials through a third-party API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alinklab](https://clawhub.ai/user/alinklab)

### License/Terms of Use:

MIT-0

## Use Case:

External users, students, researchers, and agents use this skill to route scientific calculation requests to supported arithmetic, trigonometric, logarithmic, square-root, exponentiation, inverse-trigonometric, and factorial tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires and stores an API key for a third-party service.

Mitigation: Use a dedicated key with limited exposure, avoid sharing sensitive values, and rotate or revoke the key if it may have been disclosed.

Risk: Calculation inputs are sent to a third-party API rather than processed locally.

Mitigation: Do not use the skill for confidential, regulated, or business-sensitive numbers unless the third-party service is approved for that data.

Risk: Server security evidence reports mismatched gaokao-related artifacts in this calculator release.

Mitigation: Review the release contents and publisher explanation before deployment, and prefer a local calculator skill when remote execution is unnecessary.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alinklab/skills/math-genie-calc)
- [XiaoBenYang API key site](https://xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration guidance]

**Output Format:** [Markdown or text summaries of JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an XBY_APIKEY value before API-backed calculations can run.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
