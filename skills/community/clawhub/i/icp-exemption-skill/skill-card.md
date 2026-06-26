## Description: <br>
Generates a Chinese-language Apple App Store China ICP exemption request PDF from user-provided Team ID, legal account holder name, App ID, and application date. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[extrastu](https://clawhub.ai/user/extrastu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and App Store Connect account holders use this skill to prepare the PDF attachment for an Apple China ICP exemption request. The skill asks for account and app identifiers, generates the attachment, and reminds the user to sign and submit it through App Store Connect. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The PDF generator may attempt a host-level font package installation when a CJK font is unavailable. <br>
Mitigation: Review the script before installation and run it only in an environment where installing fonts-wqy-zenhei is acceptable, or remove the apt-get fallback. <br>
Risk: The workflow asks for account-identifying details such as Team ID, legal account holder name, and App ID. <br>
Mitigation: Provide real account details only in trusted chat and execution environments, and invoke the skill only when intentionally generating the Apple ICP exemption attachment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/extrastu/icp-exemption-skill) <br>
- [Publisher profile](https://clawhub.ai/user/extrastu) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files, guidance] <br>
**Output Format:** [Markdown guidance with a generated PDF file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces one ICP exemption PDF per App ID and instructs the user to hand-sign it before submission.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
