## Description:

Detect text originality and AI-generated content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and content reviewers use this skill to screen text or local files for originality, AI-generation probability, paragraph-level risk, and rewriting recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Originality and AI-generation results are heuristic and may be inaccurate.

Mitigation: Use results as screening guidance only, and require human review before making academic, legal, or disciplinary decisions.

Risk: The skill reads user-provided local files.

Mitigation: Provide only files intended for analysis and avoid submitting sensitive or unrelated content.

Risk: Some documented options and detection methods may be inaccurate or not implemented.

Mitigation: Confirm supported command-line options before use and disclose any unsupported workflow steps to the user.

## Reference(s):

- [Detection Guide](references/detection-guide.md)
- [Detection Report Template](references/report-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with terminal report text and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Originality score, AI-generation probability, paragraph-level flags, and recommendations are heuristic and should be reviewed by a person.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
