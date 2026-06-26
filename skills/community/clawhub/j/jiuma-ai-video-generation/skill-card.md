## Description: <br>
Jiuma AI Video Generation (Free) helps agents authenticate with Jiuma, upload media, submit AI media-generation tasks, and retrieve generated media results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[github-gamma](https://clawhub.ai/user/github-gamma) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users can use this skill to run Jiuma media-generation workflows, including authorization, media upload, task submission, and result lookup for generated video, image, audio, action-imitation, and character-replacement outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores a Jiuma authorization token in the local keyring. <br>
Mitigation: Use a fresh authorization flow, keep the account scoped to the intended workflow, and remove the jiuma_ai authorized_token keyring entry when finished. <br>
Risk: The upload helper sends local files to Jiuma. <br>
Mitigation: Verify every file path before upload and avoid sensitive or private media unless the user intends to share it with Jiuma. <br>
Risk: Authorization-code handling in the instructions can be risky if reused from examples or prior sessions. <br>
Mitigation: Do not reuse sample identification codes; request or generate a current authorization code for the active user session. <br>


## Reference(s): <br>
- [Jiuma official website](https://www.jiuma.com) <br>
- [ClawHub skill page](https://clawhub.ai/github-gamma/jiuma-ai-video-generation) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands; helper scripts return JSON from Jiuma APIs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local keyring token for Jiuma API calls and can upload user-selected media files to Jiuma.] <br>

## Skill Version(s): <br>
1.0.8 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
