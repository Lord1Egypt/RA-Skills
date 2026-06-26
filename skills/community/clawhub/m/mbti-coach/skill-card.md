## Description: <br>
MBTI Personality Coach helps users understand their current MBTI type, set a target type, and grow deliberately through schedule management and expert coaching. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leilei926524-tech](https://clawhub.ai/user/leilei926524-tech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to assess MBTI-related cognitive function patterns, choose development goals, receive daily coaching exercises, schedule practice, and visualize progress. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Calendar integration and profile storage can handle sensitive personal data and credentials. <br>
Mitigation: Review the Feishu calendar script before use, keep data/profile.json private, and use least-privilege Feishu or Lark credentials. <br>
Risk: Calendar writes may send personal development schedule details outside the local machine. <br>
Mitigation: Confirm each calendar write and avoid scheduling sensitive details unless external calendar storage is acceptable. <br>
Risk: The script can print a Feishu tenant access token for debugging. <br>
Mitigation: Avoid the token command and do not share terminal output or logs that may contain credentials. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/leilei926524-tech/mbti-coach) <br>
- [Feishu Open APIs](https://open.feishu.cn/open-apis) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, files] <br>
**Output Format:** [Markdown coaching guidance with optional shell commands and generated local profile or chart files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local profile data, calendar events, and radar chart images when the user enables those workflows.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
