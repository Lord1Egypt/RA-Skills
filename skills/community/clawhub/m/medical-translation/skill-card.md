## Description:

Use medical translation for academic writing workflows that need structured execution, explicit assumptions, and clear output boundaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to produce bounded medical terminology translations for academic writing workflows, with explicit assumptions, source and target languages, and review notes. It is best suited to narrow term-level Chinese-English lookup and should not be treated as professional medical translation without manual review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented scope may read broader than the implemented local terminology lookup.

Mitigation: Use the skill for narrow medical term translation only, and manually review outputs before using them in academic, clinical, or publication contexts.

Risk: Unsupported language pairs or terms outside the small built-in dictionary may produce fallback text instead of a verified translation.

Mitigation: Confirm source and target languages up front, check any manual-confirmation notes, and route unsupported terms to a qualified reviewer.

Risk: Some audit inputs reached only partial status due to execution gaps or weak boundary handling.

Mitigation: Run the documented smoke test and require complete positional inputs before relying on the executable path.

## Reference(s):

- [Audit Reference](artifact/references/audit-reference.md)
- [ClawHub Skill Page](https://clawhub.ai/aipoch-ai/skills/medical-translation)
- [Publisher Profile](https://clawhub.ai/user/aipoch-ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown or plain text with optional shell commands and structured translation fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should include assumptions, limits, missing inputs, and manual review notes for unsupported or uncertain terms.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
