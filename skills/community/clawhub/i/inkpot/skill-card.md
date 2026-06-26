## Description: <br>
InkPot is a knowledge-management skill that monitors learning conversations, records knowledge points and study behavior, updates a local user profile, and provides review, search, recommendation, statistics, and export commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fslong520](https://clawhub.ai/user/fslong520) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Learners, coaches, and developers can use InkPot to build a local study knowledge base from conversations and retrieve or review recorded concepts with /墨池 commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests always-on monitoring of ordinary conversations and automatic loading across sessions. <br>
Mitigation: Enable it only for intentional study sessions or explicit /墨池 commands, and provide a clear pause or disable control before use. <br>
Risk: The skill stores learning activity and profile-like data from conversations. <br>
Mitigation: Avoid sensitive conversations, review stored knowledge/profile records regularly, and provide delete and export controls for the stored data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fslong520/inkpot) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [TEST_REPORT.md](artifact/TEST_REPORT.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown and plain text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can create or update local knowledge, profile, and learning-log files during recording workflows.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
