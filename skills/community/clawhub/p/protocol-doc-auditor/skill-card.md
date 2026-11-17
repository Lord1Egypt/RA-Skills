## Description:

Helps detect hidden attacks in API and protocol documentation by scanning integration guides for dangerous instructions like curl|bash, credential harvesting, and irrevocable identity bindings disguised as setup steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andyxinweiminicloud](https://clawhub.ai/user/andyxinweiminicloud)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to audit API documentation, protocol specifications, and integration guides before following setup instructions. It produces risk assessments and safer alternatives for instructions that could expose credentials, execute unverified code, leak data, bind identities irrevocably, or escalate privileges.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may mistake risky commands shown in analyzed documentation or examples for approved commands to run.

Mitigation: Treat the skill as a text-auditing aid only, review its reports before acting, and do not copy-run commands from analyzed documentation just because they appear in the audit examples.

Risk: The auditor checks known risky instruction patterns and may miss novel attack vectors or source-trust problems.

Mitigation: For high-stakes integrations, combine the generated audit report with manual expert review of the full setup flow before executing instructions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/andyxinweiminicloud/skills/protocol-doc-auditor)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown audit report with instruction lists, risk ratings, and safer alternatives]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Overall document risk rating: SAFE, CAUTION, or DANGEROUS]

## Skill Version(s):

1.0.0 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
