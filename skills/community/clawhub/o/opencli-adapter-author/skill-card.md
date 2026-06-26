## Description: <br>
Guides agents through writing or updating OpenCLI adapters, from site reconnaissance and field decoding through adapter coding and verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liberalchang](https://clawhub.ai/user/liberalchang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to author or update OpenCLI browser adapters for sites whose target data can be inspected in a live browser and validated through OpenCLI verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can lead agents to inspect live browser sessions, cookies, tokens, signed requests, account identifiers, private watchlists, or other user-specific data. <br>
Mitigation: Run it only for sites intentionally being adapted, review generated adapters and local site-memory changes before sharing, and remove raw cookies, Bearer tokens, account IDs, private watchlists, and unsanitized dumps. <br>
Risk: An adapter can appear to verify while returning incorrect data because of stale endpoints, field mapping errors, unit mistakes, or overly weak fixtures. <br>
Mitigation: Compare representative output fields against the live page, tighten fixture patterns, notEmpty checks, and row counts, and revisit field decoding when values do not match. <br>
Risk: Debug captures and fixtures may persist sensitive or stale endpoint data in the wrong location. <br>
Mitigation: Store sanitized fixtures only in the intended local OpenCLI site-memory paths or temporary directories, keep verified_at metadata current, and avoid committing raw HTML, JSON, cookie, or token dumps. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/liberalchang/opencli-adapter-author) <br>
- [Coverage Matrix](artifact/references/coverage-matrix.md) <br>
- [Site Recon](artifact/references/site-recon.md) <br>
- [API Discovery](artifact/references/api-discovery.md) <br>
- [Field Conventions](artifact/references/field-conventions.md) <br>
- [Field Decode Playbook](artifact/references/field-decode-playbook.md) <br>
- [Output Design](artifact/references/output-design.md) <br>
- [Adapter Template](artifact/references/adapter-template.md) <br>
- [Site Memory](artifact/references/site-memory.md) <br>
- [Success Rate Pitfalls](artifact/references/success-rate-pitfalls.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and JavaScript code/configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides changes to OpenCLI adapter files, verification fixtures, and local site-memory records.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
