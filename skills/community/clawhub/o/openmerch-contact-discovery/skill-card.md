## Description: <br>
Find a professional's work email from their name and company domain using OpenMerch; this is contact discovery, not email verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kernel-gd](https://clawhub.ai/user/kernel-gd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users with a legitimate business contact-discovery purpose use this skill to look up one professional work email from a first name, last name, and company domain. It returns a normalized lookup result with confidence, optional profile fields, cost, and job ID. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Lookups send names and company domains to the external OpenMerch service and may involve personal data. <br>
Mitigation: Use the skill only for legitimate business purposes, follow applicable privacy and retention rules, and avoid submitting sensitive or non-consensual personal data. <br>
Risk: Each successful lookup can spend OpenMerch account credits. <br>
Mitigation: Review the planned price before execution, use the quoted max_cost, and reuse the same idempotency key when retrying the same lookup. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kernel-gd/openmerch-contact-discovery) <br>
- [OpenMerch documentation](https://docs.openmerch.dev) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [JSON result or concise text summary with optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [One lookup per run; result may include email, confidence score, optional profile fields, raw provider output, cost_usd, and job_id.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
