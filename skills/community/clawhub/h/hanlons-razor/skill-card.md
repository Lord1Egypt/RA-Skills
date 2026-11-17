## Description:

Helps users test a non-malice explanation before attributing harmful or hostile behavior to intent, while treating that explanation as a revisable prior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deciqai](https://clawhub.ai/user/deciqai)

### License/Terms of Use:

MIT-0

## Use Case:

Individuals and teams use this reasoning guide to examine perceived harmful actions, compare mistake-based explanations with evidence of intent, and choose a proportionate first response. It is not intended for situations with concrete evidence of malice or catastrophic costs of wrongly assuming non-malice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A mistake-first lens could minimize harm or delay protection in abusive, safety-critical, or strongly asymmetric situations.

Mitigation: Apply the skill's fit check; prioritize safety and protective action in high-stakes contexts, and update the attribution when evidence changes.

Risk: Reusable incident examples could expose identifiable details.

Mitigation: Avoid recording identifiable incident details in reusable examples.

## Reference(s):

- [Sources](references/sources.md)
- [Hanlon's Razor skill overview](https://www.deciqai.com/c/hanlons-razor)
- [Machine-readable skill metadata](https://www.deciqai.com/s/hanlons-razor.json)
- [Quote Investigator: Hanlon's Razor](https://quoteinvestigator.com/2016/12/30/not-malice/)
- [Google: Gemini image generation got it wrong. We'll do better.](https://blog.google/products/gemini/gemini-image-generation-issue/)
- [ClawHub release page](https://clawhub.ai/deciqai/skills/hanlons-razor)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Markdown]

**Output Format:** [Markdown with a structured incident analysis and stepwise coaching prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Interactive coaching pauses for user input between steps; includes a revisable prior and override signals.]

## Skill Version(s):

1.0.6 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
