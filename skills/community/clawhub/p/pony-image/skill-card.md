## Description: <br>
Generates business images from prompts, reference styles, or product suite plans through a Supabase-hosted image API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lirule007](https://clawhub.ai/user/lirule007) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to create product or marketing images, replicate a reference image style, and generate cohesive image sets. It guides the agent through prompt collection, API calls, and response handling for generated image outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and uploaded product or reference images are sent to the Pony Supabase-hosted service. <br>
Mitigation: Avoid submitting confidential, regulated, personal, or unreleased assets unless the service operator and retention practices are acceptable. <br>
Risk: The required Supabase anon key can consume quota or billing on the connected service. <br>
Mitigation: Use a dedicated limited key where possible and monitor usage. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lirule007/pony-image) <br>
- [Skill source](artifact/SKILL.md) <br>
- [Pony Supabase API endpoint](https://vecarpahagopuqbwxbjh.supabase.co/functions/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, Images] <br>
**Output Format:** [Markdown guidance with curl examples and JSON API responses containing generated image data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PONY_SUPABASE_ANON_KEY and sends prompts, product images, or reference images to the Pony Supabase-hosted service.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
