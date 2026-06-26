## Description: <br>
Turn pet photos into cinematic character posters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shuminliu026](https://clawhub.ai/user/shuminliu026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and creators use this skill to transform pet photos into cinematic character posters through a two-stage mew.design workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a mew.design API key and asks the agent to make external API calls. <br>
Mitigation: Ask for the key only when needed, do not persist it, and stop using it if authentication fails. <br>
Risk: Local images or chat attachments may need upload to an external file host before downstream APIs can use them. <br>
Mitigation: Prefer public image URLs and obtain explicit user consent before any temporary third-party upload. <br>
Risk: Generated posters can alter pet identity or place text over important parts of the image. <br>
Mitigation: Run the documented identity and readability checks before returning the final poster, retrying when preservation or layout fails. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shuminliu026/pet-movie-poster) <br>
- [Mew account and API key setup](https://mew.design/login) <br>
- [Mew image-process API endpoint](https://api.mew.design/open/api/image/process) <br>
- [Mew design-generate API endpoint](https://api.mew.design/open/api/design/generate) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, API calls, Guidance] <br>
**Output Format:** [Markdown image syntax with an original-image link and a short theme summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-provided mew.design API key and a public pet image URL, or explicit consent before temporary third-party upload.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
