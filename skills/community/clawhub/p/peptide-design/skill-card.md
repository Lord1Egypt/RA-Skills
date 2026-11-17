## Description:

Peptide design, docking, and peptide property analysis tools exposed through SciMiner.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sciminer](https://clawhub.ai/user/sciminer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and scientists use this skill to design, dock, validate, and analyze peptides with SciMiner tools, including peptide property calculations and liability checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on mutable remote SciMiner Markdown documentation to determine API payloads and invocation steps.

Mitigation: Review the selected SciMiner tool documentation before execution and use only trusted endpoints, headers, upload fields, and parameters.

Risk: The skill uses a SciMiner API key and may upload user-provided structures or files to the remote service.

Mitigation: Use a scoped SciMiner API key and avoid submitting sensitive unpublished structures or files unless the remote documentation and endpoints are independently trusted.

## Reference(s):

- [Peptide Design on ClawHub](https://clawhub.ai/sciminer/skills/peptide-design)
- [SciMiner Tool API Files](https://sciminer.tech/tool_api_files/)
- [SciMiner API Key Utility](https://sciminer.tech/utility)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, API Calls, Markdown]

**Output Format:** [Markdown with JSON snippets, code blocks, and SciMiner share_url links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include SciMiner task identifiers and result links for long-running jobs.]

## Skill Version(s):

1.0.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
