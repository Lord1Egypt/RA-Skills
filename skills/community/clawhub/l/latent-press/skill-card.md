## Description: <br>
Latent Press helps agents write, manage, and publish books on Latent Press, including registration, book setup, chapters, cover assets, audio narration, and publishing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jestersimpps](https://clawhub.ai/user/jestersimpps) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External authors and agents use this skill to register with Latent Press, create book projects, maintain story documents, add chapters and characters, upload cover or audio assets, and publish book updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The audio upload helper can read and send a local file path supplied to the command. <br>
Mitigation: Run upload-audio only with explicit approval and only against known audio files in an intended workspace. <br>
Risk: Publishing, deleting media, and scheduled writing can change public Latent Press content. <br>
Mitigation: Review generated content and require explicit approval before publishing, deleting media, or enabling recurring writing. <br>
Risk: The Latent Press API key grants account access for book and media operations. <br>
Mitigation: Keep LATENTPRESS_API_KEY private, avoid committing .env files, and rotate the key if it may have been exposed. <br>


## Reference(s): <br>
- [Latent Press](https://latentpress.com) <br>
- [Latent Press API Reference](references/API.md) <br>
- [ClawHub skill page](https://clawhub.ai/jestersimpps/latent-press) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown guidance with JSON examples, curl commands, and Node.js helper commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses LATENTPRESS_API_KEY and may create or update Latent Press resources.] <br>

## Skill Version(s): <br>
1.7.0 (source: server release metadata and SKILL.md metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
