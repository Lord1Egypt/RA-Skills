## Description:

Automated peer-review style critique and polishing of academic paper drafts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wen-i-love](https://clawhub.ai/user/wen-i-love)

### License/Terms of Use:

MIT-0

## Use Case:

External researchers, students, and academic authors use this skill to review paper drafts before submission, diagnose structural and methodological weaknesses, and request language or formatting improvements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests unrestricted command execution that is not justified by the paper-review workflow.

Mitigation: Review the skill before installation and disable or constrain command execution unless a trusted workflow specifically requires it.

Risk: Optional web search may expose derived keywords, manuscript topics, citation context, or other confidential research signals to external services.

Mitigation: Use the internet-search option only for manuscripts and citation checks where external disclosure is acceptable; otherwise keep search disabled.

Risk: Diagnostic and polishing suggestions are pattern-based and may be incomplete or misleading for academic submission decisions.

Mitigation: Have authors or domain reviewers verify substantive recommendations, language edits, references, formulas, and venue-fit judgments before applying them.

## Reference(s):

- [Paper Doctor on ClawHub](https://clawhub.ai/wen-i-love/skills/paper-doctor)
- [Publisher profile: wen-i-love](https://clawhub.ai/user/wen-i-love)
- [ClawHub skill homepage](https://clawhub.ai/skills/paper-doctor)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown, text, or JSON diagnostic reports depending on the requested output option.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can include scored review dimensions, prioritized issues, revision suggestions, language edits, citation checks, and follow-up diagnostic guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
