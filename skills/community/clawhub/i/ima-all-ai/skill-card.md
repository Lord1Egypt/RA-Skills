## Description: <br>
Creates AI-generated images, videos, music, and speech through IMA Studio models, with runtime model discovery and optional workflow guidance for multimodal creative tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[allenfancy-gan](https://clawhub.ai/user/allenfancy-gan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and creative teams use this skill to generate or transform images, video, music, and speech from prompts or source media through IMA Studio's API-backed models. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, uploaded source media, and the IMA API key are sent to IMA Studio provider endpoints during generation workflows. <br>
Mitigation: Install only if you trust IMA Studio with this data, use a dedicated or test API key where possible, and monitor key usage. <br>
Risk: Local preference and generation-history data may remain under ~/.openclaw after use. <br>
Mitigation: Delete ~/.openclaw/memory/ima_prefs.json or ~/.openclaw/logs/ima_skills/ when local preference or generation history retention is not desired. <br>


## Reference(s): <br>
- [IMA Studio skill page](https://clawhub.ai/allenfancy-gan/ima-all-ai) <br>
- [IMA Studio API key page](https://www.imaclaw.ai/imaclaw/apikey) <br>
- [IMA Studio dashboard](https://imastudio.com/dashboard) <br>
- [SECURITY.md](artifact/SECURITY.md) <br>
- [clawhub.json](artifact/clawhub.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API Calls, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated media is returned as provider-hosted URLs; local preferences and generation logs may be written under ~/.openclaw.] <br>

## Skill Version(s): <br>
1.0.10 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
