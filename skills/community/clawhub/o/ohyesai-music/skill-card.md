## Description: <br>
Generate custom music tracks (vocal or instrumental) via OhYesAI asynchronously. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bajie-git](https://clawhub.ai/user/bajie-git) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to collect music requirements, submit asynchronous OhYesAI generation jobs, poll for completion, and download generated MP3 tracks for delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends the API key and user-provided prompts, styles, and song details to OhYesAI. <br>
Mitigation: Install only if you trust OhYesAI with those inputs, store the API key in the OHEYSAI_API_KEY environment variable, and avoid sensitive prompts. <br>
Risk: Generation uses outbound API calls and polling that may consume account quota or trigger billing. <br>
Mitigation: Confirm account limits before use, monitor generated requests, and stop polling when the service reports a missing or failed task. <br>
Risk: The workflow downloads generated MP3 files into the local working directory. <br>
Mitigation: Review downloaded audio files before sharing them and only deliver the intended local file links to the user. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bajie-git/ohyesai-music) <br>
- [OhYesAI developer homepage](https://dev.ohyesai.com) <br>
- [OhYesAI API key setup](https://ohyesai.com?from=https://clawhub.ai) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, markdown, files, guidance] <br>
**Output Format:** [Markdown with bash commands and local MP3 file links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OHEYSAI_API_KEY and the curl, grep, and sleep command-line tools.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
