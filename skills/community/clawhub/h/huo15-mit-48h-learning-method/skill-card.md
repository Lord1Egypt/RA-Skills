## Description: <br>
Guides an agent through a NotebookLM-based 48-hour learning workflow using three prompts for mental models, expert disagreements, and probing questions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jobzhao15](https://clawhub.ai/user/jobzhao15) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Learners, researchers, and agents use this skill to create a NotebookLM notebook, add learning sources, ask a structured three-question learning framework, and generate audio or video overviews. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill performs authenticated NotebookLM and Google account actions and may open a login flow automatically. <br>
Mitigation: Install only if the publisher is trusted, use an appropriate NotebookLM profile, and review commands before allowing account-linked actions. <br>
Risk: Selected local files and links can be uploaded to NotebookLM as learning sources. <br>
Mitigation: Use only sources that are approved for cloud processing and avoid sensitive local files unless the account and data handling are acceptable. <br>
Risk: The security scan warns that crafted file:// inputs can be unsafe. <br>
Mitigation: Do not pass untrusted file:// URLs; review or patch file URL handling before using that input mode. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jobzhao15/huo15-mit-48h-learning-method) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and NotebookLM CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or reuse NotebookLM notebooks, upload selected sources, generate audio or video overviews, and store the active notebook ID in the user's home directory.] <br>

## Skill Version(s): <br>
2.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
