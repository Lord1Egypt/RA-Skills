## Description:

Help users use Jingyi Module with E-language by searching command names, fetching official documentation, and generating directly runnable code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[junqianglu3-netizen](https://clawhub.ai/user/junqianglu3-netizen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to look up Jingyi Module commands, retrieve official command details, and produce copyable E-language examples based on documented signatures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs local Python utilities and fetches command details from the official Jingyi documentation site.

Mitigation: Review the Python scripts before installation, confirm the requests dependency is available, and allow outbound access only to expected Jingyi documentation endpoints.

Risk: Generated E-language code may be incorrect if command index data is missing, stale, or rebuilt from incomplete source data.

Mitigation: Confirm the command index is included or rebuilt successfully, and prefer fetched official command documentation before generating code.

## Reference(s):

- [Jingyi Module official documentation](https://ec.ijingyi.com/sub.htm)
- [Jingyi Module documentation endpoint](https://ec.ijingyi.com/plugin.php?id=plugin1&)
- [ClawHub skill page](https://clawhub.ai/junqianglu3-netizen/skills/jingyi-module)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown with text explanations, command examples, and E-language code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated code is expected to use .版本 2 when code is requested.]

## Skill Version(s):

0.1.0 (source: server release metadata and manifest.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
