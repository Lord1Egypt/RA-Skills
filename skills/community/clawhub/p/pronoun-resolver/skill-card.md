## Description:

Detects ambiguous pronouns, vague referents, and bare imperatives in user messages and flags them for resolution using conversation context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaicianflone](https://clawhub.ai/user/kaicianflone)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding-agent users use this skill to make ambiguous prompts visible before an agent guesses the wrong referent. It guides the agent to resolve high-confidence references from conversation context, state assumptions for moderate confidence, or ask before acting when context is weak.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The hook runs on every submitted prompt and scans prompt text locally.

Mitigation: Install only where this behavior is acceptable, and use the documented project disable sentinel when prompt scanning should be inactive.

Risk: The skill keeps local analytics and a resolution ledger under the skill directory.

Mitigation: Review the stored fields and delete the ledger or analytics files when retained metadata is no longer wanted.

Risk: Stored free-text resolution metadata may still contain novel secret formats or plain-language personal data despite pattern-based redaction.

Mitigation: Avoid logging sensitive referents, review retained metadata periodically, and clear the local files for sensitive projects.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kaicianflone/skills/pronoun-resolver)
- [Publisher profile](https://clawhub.ai/user/kaicianflone)
- [README](artifact/README.md)
- [Changelog](artifact/CHANGELOG.md)
- [Evaluation results](artifact/evals/results.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and local hook output flags]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally as a user-prompt-submit hook; stores local analytics and resolution metadata when the agent records a resolution.]

## Skill Version(s):

0.11.0 (source: SKILL.md frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
