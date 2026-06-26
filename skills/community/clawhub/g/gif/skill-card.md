## Description: <br>
Find, search, and create GIFs with proper optimization and accessibility. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, designers, and content teams use this skill to find GIF sources, generate optimized GIFs from video, and apply accessibility guidance for animated media. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated media commands could target unintended files if run without review. <br>
Mitigation: Review generated commands before running them and verify input and output paths point only to intended media files. <br>
Risk: Giphy or Tenor API keys may be exposed in prompts, logs, shell history, or shared files. <br>
Mitigation: Keep API keys in environment variables or a secure secret store and avoid pasting them into shared prompts, logs, or files. <br>


## Reference(s): <br>
- [ClawHub GIF skill page](https://clawhub.ai/ivangdavila/gif) <br>
- [Giphy Search API example](https://api.giphy.com/v1/gifs/search?api_key=$GIPHY_API_KEY&q=thumbs+up&limit=10) <br>
- [Tenor Search API example](https://tenor.googleapis.com/v2/search?key=$TENOR_API_KEY&q=thumbs+up&limit=10) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash, HTML, and API request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ffmpeg for GIF creation; gifsicle and GIF search API keys are optional.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
