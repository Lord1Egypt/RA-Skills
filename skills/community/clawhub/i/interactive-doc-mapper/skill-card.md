## Description: <br>
Create JSON-driven single-page interactive HTML documentation for app workflows between packages, services, and components. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zack-dev-cm](https://clawhub.ai/user/zack-dev-cm) <br>

### License/Terms of Use: <br>
MIT No Attribution <br>


## Use Case: <br>
Developers and engineers use this skill to map app workflows across packages, services, components, queues, databases, build systems, and external adapters. It helps produce validated JSON flow definitions and self-contained interactive HTML diagrams for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated diagrams may expose internal architecture details, private URLs, or sensitive workflow notes if those details are included in the input flow JSON. <br>
Mitigation: Review the generated HTML before sharing it and omit credentials, raw tokens, cookies, customer data, private URLs, and secret environment values from the source JSON. <br>
Risk: The skill writes generated JSON, validation reports, and HTML documentation files into the workspace. <br>
Mitigation: Run it only in repositories where generated documentation artifacts are expected, and review output paths before keeping or publishing the files. <br>


## Reference(s): <br>
- [Flow JSON Schema](references/flow-schema.md) <br>
- [ClawHub skill page](https://clawhub.ai/zack-dev-cm/interactive-doc-mapper) <br>
- [Publisher profile](https://clawhub.ai/user/zack-dev-cm) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON flow definitions, validation commands, and generated HTML documentation files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated HTML is self-contained and intended to work from file:// without a build step or external CDN.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
