## Description: <br>
AI-powered meme generation, meme editing, meme video generation for your projects, powered by memelord.com's trending memetic data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iamjasonlevin](https://clawhub.ai/user/iamjasonlevin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to create and edit image or video memes through the Memelord API, save JSON/media outputs locally, and validate webhook callbacks for asynchronous renders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends prompts, captions, template data, optional audio URLs, webhook URLs, webhook secrets, and the Memelord API key to Memelord. <br>
Mitigation: Use it only with content and callback URLs appropriate for Memelord processing, avoid confidential prompts or internal URLs, and keep the API key out of shared logs and repositories. <br>
Risk: Local .env loading can expose credentials if the file is committed or shared. <br>
Mitigation: Store MEMELORD_API_KEY in a trusted local .env or shell environment and exclude credential files from shared artifacts. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/iamjasonlevin/memelord) <br>
- [Memelord Documentation](https://www.memelord.com/docs) <br>
- [Memelord Homepage](https://memelord.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON, files, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; helper scripts produce JSON responses and local image or video files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MEMELORD_API_KEY and the node, curl, and realpath binaries; optional webhook URLs, webhook secrets, audio URLs, output paths, counts, categories, and NSFW inclusion flags may be supplied.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
