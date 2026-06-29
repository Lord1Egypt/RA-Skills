## Description: <br>
Use when a user provides an authorized 18+ face, selfie, or portrait photo and asks for an official MogScore, mog rating, AI face rating, face score, or free Mog Rating preview through the existing MogScore website. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[roooo-798](https://clawhub.ai/user/roooo-798) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to submit an authorized adult selfie or portrait through the MogScore web flow and return the free preview JSON. It is intended for consented uploads only and not for identity, medical, surveillance, impersonation, or paid-report workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow uploads the selected face photo to MogScore for processing, which may expose sensitive personal data. <br>
Mitigation: Use only photos the user has the right to submit, avoid sensitive or non-consensual images, and proceed only when the user accepts the privacy implications. <br>
Risk: Changing the base URL can send the selected image to a destination other than MogScore. <br>
Mitigation: Leave MOGSCORE_BASE_URL unset unless the user intentionally wants to use a different trusted endpoint. <br>


## Reference(s): <br>
- [MogScore Mog Rating Preview](https://mogscore.ai/mog-rating) <br>
- [MogScore Upload Flow](https://mogscore.ai/mog-rating?mode=upload) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON success or failure payload, with optional Markdown shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node 20+, playwright-core, a local Chrome-compatible browser, and a user-supplied image path; the browser must run headed and the skill does not install or download Chromium.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
