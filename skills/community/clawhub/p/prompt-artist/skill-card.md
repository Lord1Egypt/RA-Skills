## Description: <br>
Optimize and generate text-to-image prompts for Midjourney, Nano Banana, Dreamina, and Qwen, including platform-specific variations, style modifiers, aspect ratios, and negative prompts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[elevo11](https://clawhub.ai/user/elevo11) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, creators, and developers use this skill to turn short image ideas into platform-ready text-to-image prompts and to browse or apply reusable art styles. It also supports prompt history, favorites, and SkillPay billing flows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The billing command can charge the configured SkillPay account by default. <br>
Mitigation: Require explicit user approval before each charge and verify the user ID, amount, and SkillPay account tied to SKILLPAY_API_KEY. <br>
Risk: Prompt history and favorites are stored locally and may include sensitive prompt text. <br>
Mitigation: Avoid entering sensitive prompt text unless local retention is acceptable, and review or clear stored history when needed. <br>
Risk: The skill depends on a SkillPay API key for billing operations. <br>
Mitigation: Store SKILLPAY_API_KEY securely, restrict access to the runtime environment, and rotate the key if exposure is suspected. <br>


## Reference(s): <br>
- [Platform Specifications](references/platform-specs.md) <br>
- [Prompt Artist ClawHub Listing](https://clawhub.ai/elevo11/prompt-artist) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or JSON prompt-optimization results with command-line usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include optimized prompts, negative prompts, platform tips, style listings, history records, billing status, and payment-link responses.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
