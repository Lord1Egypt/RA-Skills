## Description:

Diagnose and fix model routing conflicts. Ensure primary model uses correct provider endpoint without duplicate overrides.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dalomeve](https://clawhub.ai/user/dalomeve)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to audit OpenClaw model routing, correct Bailian provider endpoint mismatches, remove conflicting agent overrides, and verify model calls after a gateway restart.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repair steps can overwrite global OpenClaw routing configuration.

Mitigation: Review the exact target files and back up openclaw.json before applying fixes.

Risk: The workflow can delete an agent-specific models.json override and restart the gateway.

Mitigation: Confirm the override is unwanted, preserve a copy when needed, and run restart steps only after configuration review.

Risk: Secret scans may surface plaintext credentials if run in directories containing sensitive files.

Mitigation: Run scans only where appropriate and redact credential values in any shared output.

## Reference(s):

- [Privacy Checklist](references/privacy-checklist.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline PowerShell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes audit, repair, restart, verification, and privacy checklist steps for OpenClaw routing configuration.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
