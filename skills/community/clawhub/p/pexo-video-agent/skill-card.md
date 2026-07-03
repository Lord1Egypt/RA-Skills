## Description: <br>
Pexo Video Agent helps an agent create hosted, multi-shot videos from text, images, scripts, or page URLs by creating a Pexo project, uploading assets, relaying the user's prompt, polling progress, and returning the finished video URL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pexo](https://clawhub.ai/user/pexo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask an agent to create or revise short videos through Pexo, including ads, social clips, explainers, product videos, and brand films. The skill guides project setup, media upload, polling, preview selection, revisions, and final delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, referenced page content, and uploaded media are sent to Pexo for hosted video generation. <br>
Mitigation: Use the skill only when that data sharing is acceptable, and avoid sending sensitive media or confidential source material unless the user has approved it. <br>
Risk: The local Pexo API key is loaded from ~/.pexo/config or $PEXO_CONFIG, and the security evidence flags that config handling for review. <br>
Mitigation: Store the config with owner-only permissions, avoid untrusted content in config files, and rotate the API key if the file may have been exposed. <br>


## Reference(s): <br>
- [Pexo homepage](https://pexo.ai) <br>
- [ClawHub listing](https://clawhub.ai/pexo/pexo-video-agent) <br>
- [Setup Checklist](references/SETUP-CHECKLIST.md) <br>
- [Troubleshooting](references/TROUBLESHOOTING.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON script responses, project links, and final asset URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PEXO_API_KEY and PEXO_BASE_URL; video projects are asynchronous and should be polled without duplicate chat calls while WAIT is active.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
