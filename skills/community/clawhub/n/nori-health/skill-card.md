## Description: <br>
Query personal health data from wearables and nutrition logs and get AI coaching on sleep, workouts, heart rate, recovery, and health insights. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danmurphy1217](https://clawhub.ai/user/danmurphy1217) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to relay health, fitness, sleep, nutrition, and recovery questions to Nori for coaching based on their connected health account data. It is not for medical diagnosis, prescriptions, or emergency health situations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Health-related prompts and connected account data are sent to Nori for processing. <br>
Mitigation: Use the skill only when the user intends Nori to receive the prompt and process connected health account data, and review Nori's privacy and retention practices before use. <br>
Risk: The Nori API key grants access to the user's Nori integration. <br>
Mitigation: Keep the NORI_API_KEY value private, store it only in the intended local configuration, and regenerate it if exposure is suspected. <br>
Risk: The skill is not intended for diagnosis, prescriptions, or emergency health situations. <br>
Mitigation: Direct medical, prescription, or emergency requests to qualified medical professionals or emergency services instead of using this skill. <br>


## Reference(s): <br>
- [Nori Health](https://nori.health) <br>
- [Nori Health on ClawHub](https://clawhub.ai/danmurphy1217/nori-health) <br>
- [Publisher profile: danmurphy1217](https://clawhub.ai/user/danmurphy1217) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text responses with setup guidance and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Relays the user's prompt to Nori and returns Nori's reply without reformatting when the API call succeeds.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
