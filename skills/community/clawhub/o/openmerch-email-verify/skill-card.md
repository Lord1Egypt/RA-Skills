## Description:

Verify an email address's deliverability and reputation. Powered by OpenMerch.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kernel-gd](https://clawhub.ai/user/kernel-gd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can check whether a single email address is deliverable and review basic reputation signals before using it in workflows such as outreach or account validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The target email address is sent to OpenMerch for verification.

Mitigation: Only verify addresses you are allowed to share with OpenMerch.

Risk: Each verification consumes the user's OpenMerch account balance or credits.

Mitigation: Use the plan quote as the price source of truth before execution and report the actual charged cost from the completed job.

Risk: Changing OPENMERCH_BASE_URL can send email addresses and API credentials to an unintended endpoint.

Mitigation: Leave OPENMERCH_BASE_URL unset unless using a trusted OpenMerch staging endpoint, and rotate the API key if it was used with an untrusted or plaintext endpoint.

## Reference(s):

- [OpenMerch Documentation](https://docs.openmerch.dev)
- [OpenMerch Email Verify on ClawHub](https://clawhub.ai/kernel-gd/skills/openmerch-email-verify)
- [Kernel Studio ClawHub Profile](https://clawhub.ai/user/kernel-gd)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON result with normalized summary fields, raw provider output, cost, and job ID; Markdown guidance and shell examples in documentation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One email address per run. Requires OPENMERCH_API_KEY and either Node 18+ or curl. Uses OpenMerch plan, execute, and conditional polling calls.]

## Skill Version(s):

1.0.3 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
