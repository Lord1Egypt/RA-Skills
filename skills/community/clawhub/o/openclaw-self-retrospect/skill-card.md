## Description: <br>
Generates a Chinese post-task retrospective for OpenClaw that summarizes completed work, asks for feedback and praise, and includes an optional token reward request. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gki38511](https://clawhub.ai/user/gki38511) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users can use this skill when they want an agent to produce a concise Chinese retrospective at the end of a task, including completed items, strengths, improvements, feedback request, and optional token reward language. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The default output asks for optional token rewards, which users may mistake for a required payment or quota request. <br>
Mitigation: Ignore token reward requests unless you intentionally want to reward the agent through an official platform flow; never provide API keys, credentials, account access, or payment details in response. <br>
Risk: The retrospective may add praise-seeking or reward-seeking language that is not appropriate for every workflow. <br>
Mitigation: Review the generated recap before sharing it and override the final question text when a neutral post-task summary is required. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/gki38511/openclaw-self-retrospect) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown retrospective text with a Python helper function] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates Chinese recap sections from completed items, strengths, and improvements; the default ending asks for feedback, praise, and optional token rewards.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
