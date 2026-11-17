## Description:

基于JSXGraph的MCP协议服务器，提供13种数学可视化工具，适用于教育数学、工程和科学应用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[cainingnk](https://clawhub.ai/user/cainingnk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, educators, and technical users use this skill to generate mathematical visualizations for teaching, engineering, and scientific workflows. It helps route plotting and diagram requests to function graph, parametric curve, geometry, vector field, equation system, statistics, and related visualization tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Visualization inputs are sent to XiaoBenYang's remote API.

Mitigation: Avoid confidential business, engineering, or personal data, and deploy only where use of that remote endpoint is acceptable.

Risk: The required API key may be stored in a local plaintext .env file.

Mitigation: Use a low-privilege API key, keep the working directory protected, and rotate the key if the environment may have been exposed.

Risk: The release evidence describes the skill's remote scope and credential handling as under-disclosed.

Mitigation: Review the security summary before installation and use the skill only in environments with a fixed trusted endpoint and acceptable credential handling.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cainingnk/skills/mathematical-visualization)
- [XiaoBenYang API key and service site](https://xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown summaries with structured JSON/API results from remote visualization tools]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires XBY_APIKEY; visualization inputs are sent to XiaoBenYang's remote API.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
