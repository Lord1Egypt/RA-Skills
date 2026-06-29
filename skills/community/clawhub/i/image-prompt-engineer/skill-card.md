## Description: <br>
Image Prompt Engineer helps agents generate, refine, critique, and package production-ready prompts for Midjourney and other image models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clarezoe](https://clawhub.ai/user/clarezoe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and creators use this skill to turn image concepts into paste-ready prompts, prompt variants, and refinements for Midjourney or another named image model. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may default to Midjourney when the user did not specify a model, which can produce model-specific parameters that do not fit another generator. <br>
Mitigation: Confirm the target image model for model-specific work and omit Midjourney-only parameters when another model is named. <br>
Risk: Midjourney model defaults and parameter compatibility can change over time. <br>
Mitigation: Verify current official model and parameter details before relying on version-specific or time-sensitive prompt guidance. <br>


## Reference(s): <br>
- [Midjourney Prompt Guide](references/midjourney-prompt-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown containing paste-ready image prompts, compact variants, and short rationale or change notes when useful.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to Midjourney when no model is specified; Midjourney parameters are placed at the end of the prompt.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
