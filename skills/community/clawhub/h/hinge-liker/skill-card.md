## Description: <br>
Automates Hinge profile review on an Android emulator with Gemini vision AI, sending selected likes or comments, skipping other profiles, and producing a detailed session report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MattttMan](https://clawhub.ai/user/MattttMan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to configure and run an Android-emulator workflow that operates their logged-in Hinge account, evaluates profiles with Gemini vision, sends likes or comments, and reports session outcomes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can take live actions on a dating account by sending likes and comments. <br>
Mitigation: Run only with explicit user intent, keep like limits low, and review session reports for unintended actions. <br>
Risk: Profile screenshots may be uploaded to Gemini and stored locally with detailed logs or recordings. <br>
Mitigation: Use protected secret storage for API keys, restrict the work directory, and regularly delete screenshots, recordings, and logs. <br>
Risk: Unattended scheduling can repeatedly operate the account and expose secrets if API keys are embedded in cron payloads. <br>
Mitigation: Avoid unattended daily runs unless explicitly desired and provide secrets through protected environment or secret-management mechanisms. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/MattttMan/hinge-liker) <br>
- [Gemini Generative Language API endpoint used by the skill](https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON logs, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands, stdout session reports, and JSON log files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local screenshots, optional screen recordings, and detailed session logs when run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
