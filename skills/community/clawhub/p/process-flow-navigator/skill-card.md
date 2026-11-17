## Description:

Business process flow navigation assistant that helps agents navigate complex multi-branch flows, plan paths, query skill codes, and inspect A-to-K process branches.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jopyin](https://clawhub.ai/user/jopyin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and workflow operators use this skill to answer process-navigation questions, identify next steps, retrieve process skill codes, and visualize branches in a documented A-to-K business flow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The authoritative security summary reports that CLI argument handling can execute injected Python from a crafted node argument.

Mitigation: Review and fix CLI argument handling before installation, and do not allow untrusted users or agents to supply node names until that issue is resolved.

Risk: The bundled path-planning command is described by the security guidance as incomplete.

Mitigation: Treat path-planning output as advisory and verify routes against the flow rules or a human-reviewed process source before using it operationally.

Risk: Documentation and command output are primarily in Chinese.

Mitigation: Confirm language suitability for intended users or add localization notes before deployment.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown or terminal text with process paths, node codes, next-step guidance, and branch summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language documentation and CLI output are expected.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata and artifact changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
