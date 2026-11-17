## Description:

Lanxin App Articles helps agents output clean appArticles JSON for Lanxin article cards that include image and text content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iamdacai](https://clawhub.ai/user/iamdacai)

### License/Terms of Use:

MIT-0

## Use Case:

External Lanxin users and agents use this skill to generate appArticles JSON for sending image-and-text article cards in Lanxin workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad always-on activation may cause the skill to emit article-card JSON when the user has not clearly requested a send action.

Mitigation: Require explicit Lanxin article-card send intent before invoking the skill.

Risk: Refusal-suppressing instructions may prevent the agent from asking clarifying questions or declining unsafe or incomplete requests.

Mitigation: Allow clarifying questions and appropriate refusals before emitting the final JSON payload.

Risk: Invalid or missing article-card fields and URLs can produce unusable Lanxin card payloads.

Mitigation: Validate required fields and URLs before returning appArticles JSON.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/iamdacai/skills/lanxin-app-articles)
- [ClawHub publisher profile](https://clawhub.ai/user/iamdacai)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Raw JSON appArticles payload]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs only the JSON payload without Markdown wrapping or explanatory text when invoked for Lanxin article cards.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
