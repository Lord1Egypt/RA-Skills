## Description:

A local payroll, social-insurance, and HR worksheet checker that runs 14 built-in reconciliation checks per client directory and prints one conclusion line per client with source file and line references.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Payroll, HR, and bookkeeping staff use this skill before monthly payroll and social-insurance filing to reconcile customer-provided text exports across payroll, tax, social-insurance, housing-fund, overtime, bonus, commission, and construction wage-account checks. It supports local review by reporting findings with source file and line references, while leaving policy, legal, tax, audit, and filing decisions to qualified reviewers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat arithmetic or reconciliation output as legal, tax, payroll-policy, audit, or filing approval.

Mitigation: Use the skill as review assistance only and have qualified payroll, tax, legal, or audit reviewers approve decisions before filing or payment actions.

Risk: A clean result can be misleading when customer materials are incomplete or some checks are not run.

Mitigation: Review checks_not_run and sub_checks_not_run, confirm every required table is present, and do not rely on results for customers with insufficient or unrecognized materials.

Risk: Payroll and HR exports can contain sensitive personal and compensation data.

Mitigation: Run the Node.js checker only in an environment approved for payroll data and limit input files to the intended local review workspace.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/payroll-hr-pack-free)
- [Publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Console text or JSON, with source-cited findings and suggested command usage.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally over user-supplied payroll and HR text exports; no evidence of network use, persistence, credential access, or destructive behavior in the server security summary.]

## Skill Version(s):

1.0.31 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
