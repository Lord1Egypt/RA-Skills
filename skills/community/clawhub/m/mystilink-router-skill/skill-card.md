## Description:

Chooses which Mystilink metaphysics skill to use (BaZi, Zi Wei, tarot, Liu Yao, western horoscope) when the user has not named a system, asks which method fits, or mixes several traditions in one request.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mystilink-ai](https://clawhub.ai/user/mystilink-ai)

### License/Terms of Use:

MIT

## Use Case:

External users and agent operators use this skill to route ambiguous or mixed metaphysics requests to one Mystilink target skill before continuing with that target skill. It helps select a method; it does not compute charts or draw cards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The router may hand off to separate Mystilink target skills whose behavior is outside this package.

Mitigation: Install and review only trusted target skills before allowing handoff.

Risk: The skill chooses a method but does not compute charts or draw cards, so an ambiguous request may still need clarification.

Mitigation: Have the agent state why the selected system fits and ask for preference when multiple systems remain plausible.

Risk: Optional wiki lookup can involve network access and may fall back to another locale when a translation is missing.

Mitigation: Disable the wiki lookup where network access is not approved, or review wiki-derived routing context before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mystilink-ai/skills/mystilink-router-skill)
- [Server-resolved GitHub source](https://github.com/mystilink-ai/mystilink-router-skill)
- [Router reference overview](references/overview.md)
- [Routing cases](examples/routing-cases.md)
- [Mystilink choosing-a-system wiki endpoint](https://wiki.mystilink.com/api/v1/pages/shared.concept.choosing-a-system?locale=en)

## Skill Output:

**Output Type(s):** [Guidance, Text, Markdown]

**Output Format:** [Markdown or plain text guidance naming one selected target skill and a brief rationale]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use an optional wiki lookup to inform routing; otherwise produces a single primary system choice.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
