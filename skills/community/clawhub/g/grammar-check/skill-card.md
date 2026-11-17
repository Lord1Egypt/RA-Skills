## Description:

Grammar Check helps agents review and correct English grammar, explain grammar rules, estimate CEFR difficulty, generate practice exercises, and compare English and Chinese grammar.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyetianya](https://clawhub.ai/user/xueyetianya)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask an agent for English grammar checking, correction, explanation, CEFR difficulty grading, practice exercise generation, and Chinese-English comparison.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release includes an extra local utility script that can silently store user-provided text locally.

Mitigation: Avoid passing private drafts, business text, credentials, or sensitive search terms to grammar-check commands unless the publisher clarifies or removes the local data/history storage behavior.

Risk: Security evidence marks this release as suspicious.

Mitigation: Review and scan the skill before deployment, with particular attention to local data and history storage behavior.

## Reference(s):

- [Grammar Check on ClawHub](https://clawhub.ai/xueyetianya/skills/grammar-check)
- [xueyetianya Publisher Profile](https://clawhub.ai/user/xueyetianya)
- [BytesAgain Homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with command-line help text and structured prompt templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are single-stream agent guidance; no structured machine-readable payload is specified.]

## Skill Version(s):

2.3.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
