## Description: <br>
Generates brand-quality product photos and campaign visuals through the Higgsfield CLI with guided mode selection and short pre-generation questions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[higgsfield](https://clawhub.ai/user/higgsfield) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, marketers, ecommerce teams, and agents use this skill to choose a product-visual mode, collect a few missing creative details, run the Higgsfield product photoshoot command, and return generated image URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install and run a third-party CLI through Bash. <br>
Mitigation: Review the displayed commands before execution and authenticate only with an account appropriate for the requested image-generation task. <br>
Risk: Generated product imagery may not match the intended product, brand constraints, or advertising requirements. <br>
Mitigation: Use the skill's pre-generation questions to provide product references, usage channel, count, style, and brand constraints, then review generated images before publication. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/higgsfield/higgsfield-product-photoshoot) <br>
- [Higgsfield CLI install script](https://raw.githubusercontent.com/higgsfield-ai/cli/main/install.sh) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Text, Image URLs] <br>
**Output Format:** [Short Markdown list of generated image URLs, with brief failure status only when a job fails] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Asks at most four short pre-generation questions, runs polling silently, and avoids returning JSON, IDs, internal model names, or enhanced prompt text.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
