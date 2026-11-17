## Description:

OpenLens Skill helps agents generate images, videos, and text through OpenAI-compatible APIs, with CLI, Streamlit GUI, prompt refinement, and local file saving.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openclawrr](https://clawhub.ai/user/openclawrr)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent builders use OpenLens Skill to route media-generation tasks to their chosen OpenAI-compatible provider, refine prompts, and save generated images or videos locally.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package includes a real-looking API key in config.json.

Mitigation: Revoke or replace the bundled key before use and provide credentials only through a trusted local configuration.

Risk: Prompts, uploaded media, generated media, and credentials are forwarded to the configured API provider.

Mitigation: Use only trusted HTTPS API endpoints and avoid submitting sensitive prompts, images, or videos.

Risk: Generated and uploaded media may be saved or temporarily retained on local or shared Streamlit hosts.

Mitigation: Run the skill in a trusted environment and clean output and temporary directories after use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/openclawrr/skills/openlens-skill)
- [SKILL.md](artifact/SKILL.md)
- [README.md](artifact/README.md)
- [Tool Definition](artifact/tool_definition.json)
- [Release Notes v1.0.7](artifact/RELEASE-v1.0.7.md)

## Skill Output:

**Output Type(s):** [Text, Files, Shell commands, Configuration]

**Output Format:** [JSON-style task results with generated text or local file paths; CLI and GUI usage commands in documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated images and videos may be saved under the configured local outputs directory.]

## Skill Version(s):

1.0.7 (source: server release metadata, manifest.json, CHANGELOG.md, RELEASE-v1.0.7.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
