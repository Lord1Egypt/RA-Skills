## Description:

This ClawHub plug bundle combines search, news sentiment scanning, English-Chinese translation, and DOCX document handling skills for knowledge workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers use this bundle to search public information, scan news sentiment, translate English and Chinese text, and prepare document outputs in a combined knowledge workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad read, command execution, search, and write capabilities can process unintended data or modify files.

Mitigation: Use the bundle only on intended data, scope file access, and review planned commands and write targets before execution.

Risk: API keys or access tokens may be exposed if pasted into prompts or code.

Mitigation: Store credentials in environment variables and avoid hard-coding or sharing secrets.

Risk: Generated search, sentiment, translation, or document outputs may be incomplete or inaccurate.

Mitigation: Review outputs before using them in decisions or writing final documents.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/plug-bundle-google-search)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline command examples and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include file-writing or batch-processing steps when the agent uses write-capable member skills.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
