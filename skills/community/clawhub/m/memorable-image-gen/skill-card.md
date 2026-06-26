## Description: <br>
Science-backed image generation agent that uses Gemini image generation and ResMem memorability scoring to iterate toward images that meet a target memorability threshold. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[kiwi-phantomworks](https://clawhub.ai/user/kiwi-phantomworks) <br>

### License/Terms of Use: <br>
MIT-0; ResMem Non-commercial License applies to ResMem use <br>


## Use Case: <br>
Developers, marketers, and content creators use this skill to generate blog hero images, marketing visuals, social media graphics, and product thumbnails when memorability is an explicit goal. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends prompts and generated-image requests to the configured Gemini-compatible API endpoint. <br>
Mitigation: Avoid submitting sensitive prompts or input images, and use a scoped API key where possible. <br>
Risk: Generated images are written to a local output path. <br>
Mitigation: Set the output path to an expected directory and review generated files before reuse. <br>
Risk: ResMem is documented as non-commercial in the skill evidence. <br>
Mitigation: Confirm intended use is compatible with the ResMem license before commercial deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kiwi-phantomworks/memorable-image-gen) <br>
- [Source Homepage](https://github.com/PhantomWorksIO/clawhub-skills/tree/main/memorable-image-gen) <br>
- [ResMem](https://github.com/Brain-Bridge-Lab/resmem) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [Generated image file with command-line status output and memorability scores] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Gemini API key; accepts a prompt, output path, memorability threshold, maximum attempts, and verbose mode.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
