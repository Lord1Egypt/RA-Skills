## Description:

Medical QA helps users understand symptoms, interpret test results, learn medication basics, and decide when to seek medical care.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yishuihan132](https://clawhub.ai/user/yishuihan132)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to ask medical knowledge questions, including symptom interpretation, test-report explanation, medication basics, and when to seek care. It returns informational answers and should not be treated as a substitute for professional diagnosis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Potentially sensitive health questions may be sent to an external Yunzhisheng service without clear consent or privacy controls.

Mitigation: Warn users before use, ask for consent, advise users not to include identifying information, and document privacy and retention handling.

Risk: Medical answers may be mistaken for diagnosis, prescription guidance, or emergency-care advice.

Mitigation: State that answers are informational, do not replace professional medical diagnosis, avoid prescription or dosage advice, and direct users to seek timely care for serious symptoms.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yishuihan132/skills/medical-qa)
- [Yunzhisheng medical QA service endpoint](https://shangbao.yunzhisheng.cn/skills/medical-qa/unisound_zhiyi_service)

## Skill Output:

**Output Type(s):** [Text, Code, Guidance]

**Output Format:** [Plain text answer returned by a Python function, with Markdown documentation and Python usage example]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return null after three failed service requests; each request uses a 600-second timeout.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
