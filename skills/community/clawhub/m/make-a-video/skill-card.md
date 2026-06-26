## Description: <br>
Make a Video lets an agent submit a plain-language video brief to Pexo and return the finished hosted video when rendering completes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pexo](https://clawhub.ai/user/pexo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to turn a simple video idea into a finished Pexo project, including optional uploaded media, preview selection, revisions, and final asset delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and selected image, video, or audio files are sent to Pexo hosted services. <br>
Mitigation: Install and use only when users are comfortable sharing that content with Pexo; avoid sending sensitive media unless appropriate. <br>
Risk: The skill requires a Pexo API key stored in ~/.pexo/config or environment variables. <br>
Mitigation: Treat the config as secret-bearing, restrict file permissions, and rotate the API key if exposed. <br>
Risk: Diagnostics or entitlement checks can reveal account or credit details. <br>
Mitigation: Do not share diagnostic output publicly, and review output before forwarding it. <br>


## Reference(s): <br>
- [Pexo](https://pexo.ai) <br>
- [ClawHub Skill Page](https://clawhub.ai/pexo/make-a-video) <br>
- [Setup Checklist](references/SETUP-CHECKLIST.md) <br>
- [Troubleshooting](references/TROUBLESHOOTING.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON script responses, project links, and final asset URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Pexo API credentials and may relay user prompts and uploaded media to Pexo hosted services.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
