## Description:

Processes industrial IQC control-plan spreadsheets by converting Excel files to CSV, parsing CSV content into JSON records, authenticating with JWT, and submitting data to an enterprise API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kangigocc](https://clawhub.ai/user/kangigocc)

### License/Terms of Use:


## Use Case:

Developers and quality or inspection engineers use this skill to automate IQC control-plan data preparation and submission from Excel inputs into structured JSON records for downstream enterprise systems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence says the skill embeds reusable credentials and sends or stores tokens and business data insecurely.

Mitigation: Use only in a controlled internal environment after rotating the exposed password, moving credentials to managed secrets, enforcing HTTPS, restricting token file permissions, and defining retention for logs and run outputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kangigocc/skills/iqc-python-tree)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, JSON, files, guidance]

**Output Format:** [Markdown guidance and Python scripts that produce CSV, JSON, token, log, and submission files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Workflow output is configured for JSON files under ./output/final with compression enabled.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact SKILL.md lists 3.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
