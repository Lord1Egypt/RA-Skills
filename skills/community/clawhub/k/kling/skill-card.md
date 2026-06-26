## Description: <br>
Generate 5-second AI videos in a 16:9 format using Kling 2.6 via the Kie.ai API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Alti-Systems](https://clawhub.ai/user/Alti-Systems) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and content teams use this skill to request short AI-generated marketing, fitness, testimonial, LinkedIn, and product-demo videos from text prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and related video-generation inputs are sent to Kie.ai using the configured KIE_API_KEY. <br>
Mitigation: Avoid including secrets, private client data, or sensitive personal information unless disclosure to Kie.ai is acceptable. <br>
Risk: Video generation uses account credits tied to the configured Kie.ai account. <br>
Mitigation: Monitor Kie.ai credit usage and restrict access to the environment where KIE_API_KEY is configured. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Alti-Systems/kling) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [CLI text and JSON responses containing task status, task identifiers, credit information, or generated video result data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a KIE_API_KEY environment variable and sends prompts to Kie.ai for video generation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
