## Description:

Routes users who are unsure which Buddhist master or teaching mode to use to the appropriate destination without answering doctrinal or practice questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xr843](https://clawhub.ai/user/xr843)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this meta-skill when a user needs help choosing the appropriate Buddhist master skill, comparison mode, debate mode, or curriculum route before asking a substantive question.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Accidental invocation on a substantive doctrinal or practice question could route the user instead of allowing the matching master skill to answer directly.

Mitigation: Review trigger wording before deployment and preserve the documented boundary that this skill only helps users choose a destination.

Risk: Routing guidance may be incomplete if local routing metadata or the optional recommendation command is unavailable.

Mitigation: Keep routing metadata available with the skill collection and fall back to the documented routing order when the command cannot run.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xr843/skills/master-help)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Three lines or fewer; names destination skills and gives a short reason without doctrinal explanation.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter reports 0.11.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
