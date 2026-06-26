## Description: <br>
Generate research-backed Ideal Customer Profiles (ICPs) for mortgage and real estate products, including buyer personas, Meta and Google ad targeting parameters, trigger phrases, content tone, and platform routing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[drivenautoplex1](https://clawhub.ai/user/drivenautoplex1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing, mortgage, real estate, and financial-services practitioners use this skill to generate ICP profiles, ad-targeting guidance, trigger phrases, and ICP-specific content direction for campaign planning. The optional content-generation mode can draft ICP-tuned marketing copy when an Anthropic API key and LLM backend are configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional generated content can send prompts to a third-party AI/API service and may incur API costs. <br>
Mitigation: Use offline profile and JSON modes when API transmission is not acceptable; enable --generate-content only with an approved Anthropic API key and expected cost controls. <br>
Risk: Ad targeting recommendations for housing, mortgage, credit, or veteran audiences may have platform or legal compliance constraints. <br>
Mitigation: Review output against applicable ad-platform policies and legal requirements before using recommendations in live campaigns. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/drivenautoplex1/icp-modeler) <br>
- [Project homepage](https://github.com/drivenautoplex1/openclaw-skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [Plain text or structured JSON, with optional generated marketing copy in text form] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Offline profile modes do not require an API key; --generate-content uses a third-party AI/API feature and may transmit prompts or incur API costs.] <br>

## Skill Version(s): <br>
1.0.2 (source: SKILL.md frontmatter, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
