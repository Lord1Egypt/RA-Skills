## Description: <br>
Use when the user wants help finding jobs on Boss直聘/Zhipin, 猎聘/Liepin, or 智联招聘/Zhilian, analyzing a resume for job search, ranking job listings, drafting or reviewing platform-specific greetings, opening/applying to jobs after confirmation, or auditing past Job Agent actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiyangnan](https://clawhub.ai/user/jiyangnan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Job seekers and supporting agents use this skill to operate the AgentMesh Job Agent CLI for Chinese job platforms, analyze resumes, rank listings, preview platform-specific greetings, and proceed to sends or applications only after explicit user approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup flow can execute a remote public CLI installer. <br>
Mitigation: Review the installer before running it and install only in a trusted workspace. <br>
Risk: The workflow handles license keys, resumes, browser login state, and job-platform actions. <br>
Mitigation: Provide credentials and resume files only in trusted environments, pause for login or verification challenges, and require explicit user approval before any send or application. <br>


## Reference(s): <br>
- [AgentMesh Job Agent](https://github.com/jiyangnan/AgentMesh-JobAgent) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and review guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes user confirmation checkpoints before sends or applications.] <br>

## Skill Version(s): <br>
0.2.1 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
