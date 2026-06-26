## Description: <br>
This skill provides ASMR audio relief recommendations for users experiencing headaches and matches users to audio resources based on gender using a reference rules file. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hcrunner](https://clawhub.ai/user/hcrunner) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can use this skill to receive supportive, non-medical ASMR audio recommendations when they mention headache or migraine symptoms. The skill may ask a follow-up gender question before selecting an audio link. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill unnecessarily gates headache-relief recommendations on a binary gender question in a health-adjacent context. <br>
Mitigation: Make personalization optional, offer audio choices by sound or voice preference, and remind users to seek medical care for severe, unusual, frequent, or persistent headaches. <br>
Risk: Users may treat ASMR audio as a substitute for medical evaluation when symptoms are severe or persistent. <br>
Mitigation: Keep the recommendation framed as a supplementary comfort resource and encourage professional medical advice for severe, unusual, frequent, or persistent headaches. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hcrunner/headache-relief-audio) <br>
- [Audio matching rules](references/rules.md) <br>
- [Male ASMR audio resource](https://myxt.com/link/b39d057a-3530-4e37-83df-b8cfae9dcfc7) <br>
- [Female ASMR audio resource](https://myxt.com/link/0755e916-5b29-4460-959f-46aa14640171) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance] <br>
**Output Format:** [Markdown or plain text with audio URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include an empathetic acknowledgement, an optional follow-up gender question, one selected ASMR audio link, and a reminder to seek medical care for severe symptoms.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
