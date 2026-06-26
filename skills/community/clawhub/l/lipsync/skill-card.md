## Description: <br>
Routes lip-sync requests through the RunComfy CLI across Sync Labs, OmniHuman, Kling, Creatify, and related video endpoints based on whether the user provides source video, a portrait, audio, or a script. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kalvinrv](https://clawhub.ai/user/kalvinrv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and workflow operators use this skill to select and invoke a RunComfy lip-sync workflow for video dubbing, talking-head avatar generation, or script-driven synced speech. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Lip-sync generation can be misused to pair a real person's face or voice with speech they did not consent to. <br>
Mitigation: Use only media and voices the operator has permission to process, and refuse requests involving non-consensual public-figure, defamatory, or sexual synthetic media. <br>
Risk: The skill depends on the external RunComfy CLI and an API token. <br>
Mitigation: Install only from the verified @runcomfy/cli package, trust RunComfy before use, and keep RUNCOMFY_TOKEN or ~/.config/runcomfy credentials private. <br>
Risk: User-provided media URLs may produce unexpected or misleading generated video output. <br>
Mitigation: Use only URLs explicitly provided for the current lip-sync task and review generated results before publication or downstream use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kalvinrv/lipsync) <br>
- [RunComfy](https://www.runcomfy.com) <br>
- [RunComfy CLI Docs](https://docs.runcomfy.com/cli/introduction?utm_source=clawhub&utm_medium=skill&utm_campaign=lipsync) <br>
- [Sync Labs Lip-sync v2](https://www.runcomfy.com/models/sync/sync/lipsync/v2?utm_source=clawhub&utm_medium=skill&utm_campaign=lipsync) <br>
- [Sync Labs Lip-sync v2 Pro](https://www.runcomfy.com/models/sync/sync/lipsync/v2/pro?utm_source=clawhub&utm_medium=skill&utm_campaign=lipsync) <br>
- [OmniHuman Model](https://www.runcomfy.com/models/bytedance/omnihuman/api?utm_source=clawhub&utm_medium=skill&utm_campaign=lipsync) <br>
- [Kling Lip-sync Audio-to-Video](https://www.runcomfy.com/models/kling/lipsync/audio-to-video?utm_source=clawhub&utm_medium=skill&utm_campaign=lipsync) <br>
- [Kling Lip-sync Text-to-Video](https://www.runcomfy.com/models/kling/lipsync/text-to-video?utm_source=clawhub&utm_medium=skill&utm_campaign=lipsync) <br>
- [Creatify Lip-sync](https://www.runcomfy.com/models/creatify/lipsync?utm_source=clawhub&utm_medium=skill&utm_campaign=lipsync) <br>
- [RunComfy Lip-sync Catalog](https://www.runcomfy.com/models/feature/lip-sync?utm_source=clawhub&utm_medium=skill&utm_campaign=lipsync) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with bash and JSON CLI examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the runcomfy CLI, RUNCOMFY_TOKEN or RunComfy login, and user-provided media URLs; generated videos are written by the CLI to the selected output directory.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
