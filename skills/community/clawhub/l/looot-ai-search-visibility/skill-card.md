## Description:

Check AI search visibility. Use when the user says things like "does ChatGPT mention our brand for this prompt", "what sources does the AI cite for best project management tools" or "check how AI answers rank us against competitors". Runs through looot, billed per call.

This skill is ready for commercial/non-commercial use.

## Publisher:

[walidboulanouar](https://clawhub.ai/user/walidboulanouar)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can compare how AI search services answer buyer-style prompts, which brands they mention, and which sources they cite for a selected country.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid provider runs incur a per-call charge.

Mitigation: Inspect the endpoint price, tell the user the cost, and get approval before running; report the total after a batch.

Risk: AI search answers vary, so one result may not represent what buyers consistently see.

Mitigation: Identify the prompt, country, and provider, describe each run as a sample, and repeat prompts when a comparison needs more evidence.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/walidboulanouar/skills/looot-ai-search-visibility)
- [Looot skill setup guide](https://looot.ai/skill.md)
- [AI Search Visibility skill page](https://looot.ai/agent-skills/ai-search-visibility)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown]

**Output Format:** [Markdown summary of brand mentions, answer order, and cited sources]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [A run is one sample; answers can vary by prompt, provider, country, and time.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
