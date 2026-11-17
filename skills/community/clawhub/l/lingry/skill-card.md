## Description:

Discover Lingry words, generate immutable candidates, and coin only the currently selected candidate after explicit user publication intent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[svetlyoh](https://clawhub.ai/user/svetlyoh)

### License/Terms of Use:

MIT-0

## Use Case:

People using an agent can discover public Lingry words, generate candidates from concepts, and explicitly publish a selected candidate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Word prompts are sent to Lingry's server.

Mitigation: Share only concepts you are comfortable sending to the service; never provide wallet secrets.

Risk: Coining permanently publishes the selected candidate.

Mitigation: Coin only after the user explicitly requests publication of the currently selected candidate.

## Reference(s):

- [Lingry project homepage](https://github.com/svetlyoh/web-wallet/tree/master/skills/lingry)
- [Lingry service](https://lingry.net)
- [ClawHub Lingry release](https://clawhub.ai/svetlyoh/skills/lingry)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Markdown with word and candidate details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [A published candidate returns a transaction ID; generating a candidate does not publish it.]

## Skill Version(s):

2.0.9 (source: ClawHub release metadata; bundled files declare 2.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
