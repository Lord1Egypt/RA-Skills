## Description: <br>
OpenLens Skill provides GUI, CLI, and callable-agent access for generating images, videos, prompt refinements, and text through configurable OpenAI-compatible APIs while saving generated media locally. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openclawrr](https://clawhub.ai/user/openclawrr) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and creators use this skill to submit text-to-image, text-to-video, image-to-video, video-to-video, and prompt-enhancement tasks to a configured API provider, then retrieve local output files or generated text. It is suited for agent workflows that need media-generation calls plus local artifact paths. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, uploaded media, local file contents, and bearer API keys may be sent to the configured API provider. <br>
Mitigation: Use only trusted HTTPS API endpoints, avoid sensitive prompts or files, and review provider terms before installation. <br>
Risk: A bundled API key appears in configuration evidence and may be real. <br>
Mitigation: Rotate the bundled key before use and replace it with a user-managed secret stored outside shared release artifacts. <br>
Risk: Generated outputs are saved locally and may contain sensitive or policy-relevant media. <br>
Mitigation: Review and restrict the configured output directory, and remove generated files that should not persist. <br>
Risk: The Streamlit interface could expose credential and generation controls if made reachable on a network. <br>
Mitigation: Run the UI locally or behind access controls, and add URL validation and clearer credential handling before network exposure. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/openclawrr/openlens-skill) <br>
- [OpenLens Skill README](artifact/README.md) <br>
- [OpenLens Skill Instructions](artifact/SKILL.md) <br>
- [Release Notes v1.0.7](artifact/RELEASE-v1.0.7.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON-compatible task results, local file paths, downloaded media files, Streamlit UI output, and CLI text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated media is saved under a configured local outputs directory; API calls send prompts, uploaded media, and bearer tokens to the configured provider.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release evidence, manifest.json, CHANGELOG.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
