## Description: <br>
统一进化系统，自动化技能发现、评估、安装、进化。当用户需要技能管理、系统进化、能力评估、技能搜索安装时使用此技能。支持ClawHub技能搜索、VFM评估、自动安装、每日进化流程。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[skillforge-jojo](https://clawhub.ai/user/skillforge-jojo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to discover, evaluate, install, and record improvements to agent skills through a recurring evolution workflow. It is aimed at skill management, VFM evaluation, automatic installation, and reflection logging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary says the skill asks the agent to automatically find, install, or create other skills on a recurring schedule without clear approval controls. <br>
Mitigation: Use the skill as a manual discovery assistant unless approval is required before each install or skill creation, versions are pinned, and source and publisher are inspected. <br>
Risk: The daily evolution workflow could introduce unreviewed third-party skills or changes into an agent environment. <br>
Mitigation: Disable recurring execution by default and require human review, source scanning, and publisher verification before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/skillforge-jojo/maske-evolution) <br>
- [Publisher profile](https://clawhub.ai/user/skillforge-jojo) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with Python and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce skill recommendations, VFM scoring guidance, installation commands, evolution logs, and reflection notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
