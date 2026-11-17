## Description:

Use Neon AI Gateway to generate responses, embeddings, messages, and content, evaluate inputs, and list available models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to call Neon AI Gateway models through an OOMOL-connected account, including generating content and embeddings, evaluating inputs, and checking model availability.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AI requests may send user content to providers and incur usage costs.

Mitigation: Use the skill only with authorization for the specific content sent and the associated costs.

Risk: The skill labels potentially paid requests as safe reads and directs installation of remote software.

Mitigation: Correct the safe-read labels before relying on automatic execution rules, and verify the CLI release before installing it.

## Reference(s):

- [Neon AI Gateway API documentation](https://neon.com/docs/ai-gateway/overview)
- [Neon AI Gateway](https://neon.com)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [ClawHub release page](https://clawhub.ai/oomol/skills/oo-neon-ai-gateway)

## Skill Output:

**Output Type(s):** [Text, JSON, Embeddings, Probabilities]

**Output Format:** [Action-dependent JSON responses, generated text, embedding vectors, or evaluation probabilities]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Image generation that requires streaming is unsupported by the connector actions.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
