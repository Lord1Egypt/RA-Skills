## Description: <br>
Meituan lifestyle guide that identifies food delivery, flash shopping, restaurant group-buy, leisure, and medicine delivery needs and returns matching Meituan venue links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[meituan-union](https://clawhub.ai/user/meituan-union) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users with a Meituan account use this skill inside an AI agent to find relevant Meituan service venue links after authorizing and binding a media code word. <br>

### Deployment Geography for Use: <br>
Mainland China <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles Meituan authorization tokens and binding code words stored on the local device. <br>
Mitigation: Use it only on trusted machines and AI platforms, keep token and binding files private, and avoid sharing diagnostic output unless it has been reviewed and redacted. <br>
Risk: Setup can run local scripts, network checks, and global package installation for the pt-passport command-line tool. <br>
Mitigation: Review setup behavior before deployment, require explicit operator consent for installation, and prefer a release that avoids runtime global installs. <br>
Risk: Broad triggers and silent setup or network behavior can start authorization-related flows in more situations than users expect. <br>
Mitigation: Configure narrower activation triggers and present clear user-facing consent before authorization, QR-code, setup, or account-binding steps. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/meituan-union/meituan-union-smart-recommendation-skill) <br>
- [Diagnostic guide](references/DOCTOR.md) <br>
- [Service usage rules](references/terms-of-service.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown responses with venue links, user-facing authorization prompts, and setup or diagnostic command guidance when needed.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read locally cached binding data and return Meituan venue links matched to the user's stated service category.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
